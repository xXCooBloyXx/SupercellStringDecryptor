import numpy as np
from arc4 import ARC4


def xor(key, data):
    data = np.frombuffer(data, np.uint8)
    key = np.frombuffer(key, np.uint8)
    return np.bitwise_xor(data, np.resize(key, data.size)).tobytes()

def rc4(key, data):
    return ARC4(key).encrypt(data)