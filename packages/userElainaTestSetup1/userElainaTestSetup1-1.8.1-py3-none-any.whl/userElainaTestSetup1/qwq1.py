import os
def f():
	pth=os.path.abspath(os.path.dirname(__file__))+'/1.txt'
	print(open(pth,'r').read())


