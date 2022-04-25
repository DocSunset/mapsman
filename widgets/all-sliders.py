from PySide6 import QtCore, QtWidgets
import libmapper as mpr

class AllSliders(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    self.dev = mpr.Device("AllSliders")
    self.dev.graph().add_callback(types=mpr.Type.DEVICE
        , func=lambda t, dev, evt: self.device_callback(dev, evt)
        )
    self.dev.graph().add_callback(types=mpr.Type.SIGNAL
        , func=lambda t, sig, evt: self.graph_signal_callback(sig, evt)
        )
    self.dev.graph().add_callback(types=mpr.Type.MAP
        , func=lambda t, mp, evt: self.map_callback(mp, evt)
        )
    self.dev.graph().subscribe(None, mpr.Type.OBJECT, -1)
    self.libmapper_timer = QtCore.QTimer()
    self.libmapper_timer.timeout.connect(self.libmapper_poll)
    self.libmapper_timer.start(10)
    self.slider_labels = dict()
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
    copy = self.dev.add_signal(name = name
        , dir = mpr.Direction.OUTGOING
        , length = 1#sig['length']
        , datatype = mpr.Type.INT32
        , min = 0
        , max = 1000
        , callback = self.signal_callback
        )
    copy['is_local_copy'] = 1

    label_cell = QtWidgets.QTableWidgetItem(name)
    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(1000)
    self.sliders[name] = label_cell
    row = self.table.rowCount()
    self.table.insertRow(row)
    self.table.setItem(row, 0, label_cell)
    self.table.setCellWidget(row, 1, slider)

    slider.sliderMoved.connect(lambda v: copy.set_value(v))
    mpr.Map(copy, sig)
    #mpr.Map(sig, copy)

  def modify_signal(self, sig):
    pass

  def remove_signal(self, sig):
    # get the matching local copy
    # delete it
    # 
    pass

  def graph_signal_callback(self, sig, evt):
    #print("signal callback: {}, {}".format(sig, evt))
    #print("    ", [sig.get_property(i) for i in range(sig.get_num_properties())])
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
