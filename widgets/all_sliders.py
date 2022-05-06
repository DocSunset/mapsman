#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of mapsman
#
# Copyright 2022 Travis West
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PySide6 import QtCore, QtWidgets
import libmapper as mpr

class AllSliders(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    self.dev = mpr.Device("AllSliders")
    while not self.dev.get_is_ready(): self.dev.poll(0)
    self.dev.graph().add_callback(types=mpr.Type.DEVICE
        , func=lambda t, dev, evt: self.device_callback(dev, evt)
        )
    self.dev.graph().add_callback(types=mpr.Type.SIGNAL
        , func=lambda t, sig, evt: self.graph_signal_callback(sig, evt)
        )
    self.dev.graph().add_callback(types=mpr.Type.MAP
        , func=lambda t, mp, evt: self.map_callback(mp, evt)
        )
    self.dev.graph().subscribe(None, mpr.Type.SIGNAL, -1)
    self.libmapper_timer = QtCore.QTimer()
    self.libmapper_timer.timeout.connect(self.libmapper_poll)
    self.libmapper_timer.start(10)
    self.sliders = dict()
    QtWidgets.QGridLayout(self) # accessible as self.layout()
    self.table = QtWidgets.QTableWidget(0,2)
    self.table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Signal"))
    self.table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Slider"))
    self.table.horizontalHeader().setStretchLastSection(True)
    self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    self.layout().addWidget(self.table)

  @QtCore.Slot()
  def libmapper_poll(self):
    self.dev.poll(0)

  def device_callback(self, dev, evt):
    if evt == mpr.Graph.Event.NEW:
      pass
    elif evt == mpr.Graph.Event.MODIFIED:
      pass
    elif evt == mpr.Graph.Event.REMOVED:
      pass
    elif evt == mpr.Graph.Event.EXPIRED:
      pass

  def signal_callback(sig, evt, instance, value, time):
    print("signal_callback {}".format(sig))


  def copy_signal(self, sig):
    if sig['direction'] == mpr.Direction.OUTGOING: return

    name = sig['device']['name'] + "/" + sig['name']
    length = sig['length']
    minimum = sig['min'] if sig['min'] is not None else [0 for i in range(length)]
    maximum = sig['max'] if sig['max'] is not None else None
    if maximum is None:
      if length > 1:
        maximum = [1.0 for i in range(length)] if sig['type'] is mpr.Type.FLOAT32 else [1000 for i in range(length)]
      else:
        maximum = 1.0  if sig['type'] is mpr.Type.FLOAT32 else 1000
    copy = self.dev.add_signal(name = name
        , dir = mpr.Direction.OUTGOING
        , length = sig['length']
        , datatype = sig['type']
        , min = minimum
        , max = maximum
        , callback = self.signal_callback
        )
    if type(minimum) is not list: minimum = [minimum]
    if type(maximum) is not list: maximum = [maximum]
    copy['is_local_copy'] = 1

    label_cell = QtWidgets.QTableWidgetItem(name)

    slider_parent = QtWidgets.QWidget()
    QtWidgets.QVBoxLayout(slider_parent)

    sliders = [QtWidgets.QSlider(QtCore.Qt.Horizontal) for i in range(length)]

    def slider_cb(v):
      out = [sliders[i].value()/1000.0 * (maximum[i] - minimum[i]) + minimum[i] for i in range(length)]
      copy.set_value(out)

    for slider in sliders:
      slider.setMinimum(0)
      slider.setMaximum(1000)
      slider.sliderMoved.connect(slider_cb)
      slider_parent.layout().addWidget(slider)

    self.sliders[name] = label_cell
    row = self.table.rowCount()
    self.table.insertRow(row)
    self.table.setItem(row, 0, label_cell)
    self.table.setCellWidget(row, 1, slider_parent)

    mpr.Map(copy, sig).push()

    #mpr.Map(sig, copy)


  def modify_signal(self, sig):
    pass

  def remove_signal(self, sig):
    name = sig['device']['name'] + "/" + sig['name']
    if name not in self.sliders: return
    matches = self.dev.signals().filter(mpr.Property.NAME, name)
    copy = matches[0]
    self.dev.remove_signal(copy)

    row = self.sliders[name].row()
    self.table.model().removeRow(row)
    del self.sliders[name]

  def graph_signal_callback(self, sig, evt):
    print("signal callback: {}, {}".format(sig, evt))
    print("    ", [sig.get_property(i) for i in range(sig.get_num_properties())])
    if evt == mpr.Graph.Event.NEW:
      self.copy_signal(sig)
    elif evt == mpr.Graph.Event.MODIFIED:
      self.modify_signal(sig)
    elif evt == mpr.Graph.Event.REMOVED or evt == mpr.Graph.Event.EXPIRED:
      self.remove_signal(sig)
    
  def map_callback(self, mp, evt):
    print("map callback: {}, {}".format(mp, evt))

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication([])
  widget = AllSliders()
  widget.show()
  return_code = app.exec()
  widget.dev.free()
  sys.exit(return_code)
