import sys
input_n = "" if len(sys.argv) == 1 else sys.argv[1]

data = [x.strip() for x in open(f"input{input_n}.txt")]