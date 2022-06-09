#!/bin/python3
def overlap(argZero, argOne):
	for itemZero in argZero:
		for itemOne in argOne:
			if itemZero == itemOne:
				return True
	return False

if __name__ == "__main__":
	print(overlap(["a", "n"], ["d", "p"]), "== False")
	print(overlap(["a", "d"], ["b", "c"]), "== False")
	print(overlap(["a", "n"], ["b", "n"]), "== True")
	print(overlap(["x", "x"], ["y", "y"]), "== False")
	print(overlap(["x", "x"], ["x", "y"]), "== True")
