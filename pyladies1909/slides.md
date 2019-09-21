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

-> we do not consider APM (application performance monitoring)


---
-> Pre-requirements
====================
* how much time does the program actually take?
-> `hyperfine 'python profile_example.py'`
* how much memory does the program uses/allocates?
-> `heaptrack python profile_example.py`
-> `heaptrack --analyze file_name`
* more specific for python
-> `python -m memory_profiler profile_example.py`
---------------------

---
-> In-code profilers
====================
* [Official docs](https://docs.python.org/3/library/debug.html)
