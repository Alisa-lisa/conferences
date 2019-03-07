build:
	cargo build --release
	cp -a target/release/libpyladies_wordcount.so pyladies_wordcount.so

.PHONY: naive
naive:
	hyperfine -r 3 "python main.py lol1.txt naive"

.PHONY: simple
simple:
	hyperfine -r 3 "python main.py lol1.txt smart"

.PHONY: magic
magic:
	hyperfine -r 3 "python main.py lol1.txt seq"

.PHONY: black-magic
black-magic:
	hyperfine -r 3 "python main.py lol1.txt rayon"

.PHONY: grepgrep
grepgrep:
	hyperfine -r 3 "grep -o -i Alice lol1.txt | wc -l"

.PHONY: darkest-magic
darkest-magic:
	hyperfine -w 1 -r 3 "rg -c -i Alice lol1.txt"

.PHONY: test1
test1:
	python main.py lol1.txt smart

.PHONY: test2
test2:
	python main.py lol1.txt rayon

.PHONY: heap-py
heap-py:
	heaptrack --analyze heaps/simple.zst

.PHONY: heap-rs
heap-rs:
	heaptrack --analyze heaps/rayon.zst

prepare-lol:
	for i in {1..100}; do cat alice_in_wonderland.txt >> lol.txt; done
