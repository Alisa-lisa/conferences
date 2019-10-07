# Pyladies & Python User Group: profiling tools
-----------------------------------------------

How do I know what problems exactly my code has? Is there a memory leak, is tis function is slow or the the one?
To answer this question multiple tools exist. Some of the tools are language specific, some are rather OS specific.

warning: all tools are workign with Linux, but not all are working on Windows or Mac.
### Python specific tools:
1. [Pyflame](https://github.com/uber/pyflame) 
-> Linux only
2. [Py-spy](https://github.com/benfred/py-spy)
-> all platforms
3. [Heartrate](https://github.com/alexmojaki/heartrate)
-> python specific, all platforms
4. [Pyheat](https://github.com/csurfer/pyheat)
-> python specific, all platforms
5. [memory_profiler](https://github.com/pythonprofilers/memory_profiler)
-> python specific, all platforms
### Language agnostic tools:
1. [Heaptrack](https://github.com/KDE/heaptrack)
-> linux only
2. [Valgrind/Kachegrind](http://valgrind.org/)
-> kcachegrinf on linux, qcachegrind on mac
3. [Hyperfine](https://github.com/sharkdp/hyperfine)
-> only linux

---
In order to succesfully iprove your codes performance you should:
1. identify complexity function - if your code does not scale, small adjustments won't help
2. pin down bottlenecks by total execution time in theis function - try to narrow down to children functions you still have control over
3. make sure python is not spiking in memory usage - steady greedy allocation is normal
