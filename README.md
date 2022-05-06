# mapsman: A Libmapper Session Manager

This project is a very early work in progress, made public in order to foster discussion and invite collaboration.

The immediate goal of `mapsman` is to provide an alternative libmapper session manager that provides the following features:

-[] Direct manipulation of destination signals that don't have incoming maps ("free destinations").
-[] Simple and unsurprising restoration of simple cases of previous sessions, including maps and free destination states.

Eventually, I may also include additional features such as the following:

-[] GPU accelerated visualization of recent signal values
-[] Command line based plugin system for launching and restoring shell-invocable libmapper devices
-[] Simple and unsurprising handling of complex session restoration scenarios, such as dealing with offline devices, staging, and name mismatches.
-[] Support for recording and editing datasets derived from signals on the network.

### Why a new session manager?

Webmapper is the de facto standard libmapper session manager. Due to complex historical reasons, it is implemented as a web-based user interface that communicates with a Python back-end server that monitors the libmapper network. This architecture introduces an idiosyncratic duplication of much of the functionality of libmapper in JavaScript and over the WebSocket connection between the front-end and the back-end. This duplication of effort makes it non-trivial for user interface elements in the front end to directly interact with devices on the libmapper network. The Webmapper front-end also employs a bare minimum of dependencies, meaning that implementation of simple user interface widgets can be complicated. For example, creating a slider that controls the value of a free destination signal would require implementing a slider widget, a bridge over the WebSocket from the front-end to the back-end, and a bridge from the WebSocket to the libmapper network. In contrast, by directly using the libmapper python bindings, with pyside for user interface widgets, the same task in `mapsman` essentially only requires to implement a bridge from the slider to the network. Basically, many of the intended features of mapsman are hard to do in Webmapper.

Other features, such as session restoration, are already implemented in Webmapper. In this case, the present application aims to provide an alternative implementation of this kind of functionality, with an aim towards eventually extending libmapper itself to better support these features. Again, due to its architecture, features implemented in Webmapper are difficult to port to the library. Implementing the same features by directly leveraging the library API makes it much easier to envisage how they could be implemented in C. This is especially relevant for features such as support for offline devices / staging, and support for recording and editing datasets.

The biggest drawback of `mapsman`'s architecture (Python + pyside) compared to Webmapper is that it must be run on a macOS, Windows, or Linux computer running python, and it must be installed. In contrast, Webmapper's implementation permits the possibility that the front-end could be served from an embedded device (such as a sound module or gestural controller), so that the end-user of the device doesn't need to install any additional software in order to use it.

Ultimately, `mapsman` is not meant to usurp or replace Webmapper as the dominant libmapper session manager. The two can coexist and complement each other. Users are free to use one or the other, or both, as they see fit.

### License

Copyright 2022 Travis West

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
