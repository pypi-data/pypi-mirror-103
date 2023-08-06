
import copy
import numpy as np
import pickle
from typing import Union

class Message:

    def __init__(self, data: list=[]):
        self._data = np.array(data, dtype=np.float64)

    def __repr__(self):
        return repr(self._data)
    
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return Slot(self._data[index], 0)

    def __setitem__(self, index: int, value: Union[int, float]):
        self._data[index] = value

    def load(self, path):
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        self.copy(tmp)
        pass

    def save(self, context, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass

    def copy(self, src):
        self._data = copy.deepcopy(src._data)

class Slot:

    def __init__(self, real: float, imag: float):
        self._real = real
        self._imag = imag

    def __repr__(self):
        return repr((self._real, self._imag))

    def real(self):
        return self._real

    def imag(self):
        return self._imag