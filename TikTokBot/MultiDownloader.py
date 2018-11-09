import os
from typing import Optional, Callable, Any, Iterable, Mapping
from urllib.request import Request, urlopen
import time
from queue import Queue
from threading import Thread

class MultiProcess(Thread):
    def __init__(self,threadname, url, filename, ranges=0):
        pass