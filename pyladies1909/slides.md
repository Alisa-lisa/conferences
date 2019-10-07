%title: Code profiling: Why and How
%author: Alisa Dammer (FREE NOW)
-> How to be smart about code optimisations?
--------------------------------------------

---
-> Why?
=======
* Performance issues
* Memory leaks
* Proper analysis before refactoring

---
-> How?
========
* Python in-code profilers
* Python specific profilers
* Language agnostic profilers

1. we do not consider APM (application performance monitoring)
--------------------------------------------------------------
2. tracing is a method for profiling
------------------------------------

---
-> Pre-requirements
====================
* how much time does the program actually take?
-> `hyperfine 'python profile_example.py'`
-> repeat with increasing load to identify complexity class
-> complecity will give a hint on global scaling factor of the code

---
-> Performance profiling
=========================
the simplest profile
-------------
* [cProfile](https://docs.python.org/3/library/debug.html)
-> `python3 -m cProfile -o profile_output.prof profile_example.py`
-> [snakeviz](https://jiffyclub.github.io/snakeviz/)
-> `snakeviz profile_output.prof`
-> does not go beyound built-in python fucntions

---
-> Performance profiling
=========================
the fanciest
-------------
* [heartrate](https://github.com/alexmojaki/heartrate)
-> enable code under `# heartrate`, line: 5, 6
-> `python profile_example.py`
-> in browser follow the execution of the program

---
-> Performance profiling
=========================
the established one
-------------------
* [py-spy](https://github.com/benfred/py-spy)
-> `py-spy record -o profile.svg -- python profile_example.py`
-> svg contains a breakdown of the program execution in form of a flame graph
-> [flame graph](http://www.brendangregg.com/flamegraphs.html)

not using pyflame because it does the same thing almost
--------------------------------------------------------

---
-> Performance profiling
=========================
the ugly but the real one
------------------------
* [pyCallgraph](http://pycallgraph.slowchop.com/en/master/)
-> `pycallgraph graphviz profile_example.py`

is ugly but can be used for valgrind understanding
---------------------------------------------------

---
-> Performance profiling
=========================
the hardcore
------------
* [valgrind](http://valgrind.org/)
-> `valgrind --dsymutil=yes --tool=callgrind 'python profile_example.py'`
-> can take several minutes to create an output file
-> [kcachgrind](http://kcachegrind.sourceforge.net/html/Home.html)
-> ``


---
-> Memory profiling
====================
* how much memory does the program use/allocate?
-> `heaptrack python profile_example.py`
-> `heaptrack --analyze file_name`
* more specific for python
-> `python -m memory_profiler profile_example.py`

