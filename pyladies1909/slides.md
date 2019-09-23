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
* is my algorithm at fault?
-> `timeit_babe`

---
-> Performance profiling
=========================
the simplest profile
-------------
* [cProfile](https://docs.python.org/3/library/debug.html)
-> [snakeviz](https://jiffyclub.github.io/snakeviz/)
-> `snakeviz profile_output.prof`

---
-> Performance profiling
=========================
the fanciest
-------------
* [heartrate](https://github.com/alexmojaki/heartrate)
-> `enable in the code` + `python profile_example.py`

---
-> Performance profiling
=========================
the established one
-------------------
* [py-spy](https://github.com/benfred/py-spy)
-> `py-spy record -o profile.svg -- python profile_example.py`

---
-> Performance profiling
=========================
the ugly bu the real one
------------------------
* [pyCallgraph](http://pycallgraph.slowchop.com/en/master/)
-> `pycallgraph graphviz profile_example.py`

---
-> Performance profiling
=========================
the hardcore one
----------------
* [valgrind](http://valgrind.org/)
-> [kcachgrind](http://kcachegrind.sourceforge.net/html/Home.html)


---
-> Memory profiling
====================
* how much memory does the program uses/allocates?
-> `heaptrack python profile_example.py`
-> `heaptrack --analyze file_name`
* more specific for python
-> `python -m memory_profiler profile_example.py`

