from os import getcwd, path
from sys import path as sys_path
sys_path.insert(0, path.dirname(getcwd()))

from core import main
if __name__ == '__main__':
    main.main()