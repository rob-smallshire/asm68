from util import typename


class U8:
    
    def __init__(self, value):
        if not (0 <= value < 2**8):
            raise ValueError("{} value {!r} out of range".format(typename(self), value))
        self._value = value
        
    @property
    def value(self):
        return self._value


class U16:
    
    def __init__(self, value):
        if not (0 <= value < 2**16):
            raise ValueError("{} value {!r} out of range".format(typename(self), value))
        self._value = value
        
    @property
    def value(self):
        return self._value


class U32:
    
    def __init__(self, value):
        if not (0 <= value < 2**32):
            raise ValueError("{} value {!r} out of range".format(typename(self), value))
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    
class I8:
    
    def __init__(self, value):
        if not (-128 <= value < 127):
            raise ValueError("{} value {!r} out of range".format(typename(self), value))
        self._value = value
        
    @property
    def value(self):
        return self._value


class I16:
    
    def __init__(self, value):
        if not (-32768 <= value < 32767):
            raise ValueError("{} value {!r} out of range".format(typename(self), value))
        self._value = value
        
    @property
    def value(self):
        return self._value


class I32:
    
    def __init__(self, value):
        if not (-2147483648 <= value < 2147483647):
            raise ValueError("{} value {!r} out of range".format(typename(self), value))
        self._value = value
        
    @property
    def value(self):
        return self._value