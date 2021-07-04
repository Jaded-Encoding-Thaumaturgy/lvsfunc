import abc
from abc import ABC, abstractmethod
from io import BufferedReader

class Sector(ABC, metaclass=abc.ABCMeta):
    ifo: BufferedReader
    def __init__(self, ifo: BufferedReader) -> None: ...
    @abstractmethod
    def load(self): ...
