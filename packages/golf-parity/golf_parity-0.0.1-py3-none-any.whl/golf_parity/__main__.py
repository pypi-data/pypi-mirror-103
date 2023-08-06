import sys
from adicity.__main__ import main
def _main():
	main(['parity'] + sys.argv[1:])
if __name__ == '__main__':
	_main()