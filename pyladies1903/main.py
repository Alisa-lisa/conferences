import sys
from count_words import fast_count, simple_count, magic_count

if __name__ == '__main__':
    command = sys.argv[2]
    file = sys.argv[1]
    if command == "smart":
        print(fast_count(file))
    elif command == "seq":
        print(magic_count(file, True))
    elif command == "rayon":
        print(magic_count(file, False))
    else:
        print(simple_count(file))
