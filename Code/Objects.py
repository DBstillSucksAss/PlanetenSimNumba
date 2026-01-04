import numpy as np
from numba import njit, float64, int64
from numba.experimental import jitclass

class ObjectContainer:
    def __init__(self, num_objects):
        self.N = num_objects
        
        # Numeric arrays (JIT)
        self.ids = np.zeros(self.N, dtype=np.int64)
        self.mass = np.zeros(self.N, dtype=np.float64)
        self.pos = np.zeros((self.N, 3), dtype=np.float64)
        self.vel = np.zeros((self.N, 3), dtype=np.float64)
        self.acc = np.zeros((self.N, 3), dtype=np.float64)
        
        # Metadata (strings, not JIT)
        self.names = np.empty(self.N, dtype=object)
        self.classes = np.empty(self.N, dtype=object)
    
    def object_view(self, idx):
        """
        Return a 'view' object for one particle at index idx.
        """
        return ObjectView(idx, self)

class ObjectView:
    def __init__(self, idx, container: ObjectContainer):
        self.idx = idx
        self.container = container
    
    @property
    def id(self):
        return self.container.ids[self.idx]
    
    @property
    def mass(self):
        return self.container.mass[self.idx]
    
    @property
    def pos(self):
        return self.container.pos[self.idx]
    
    @property
    def vel(self):
        return self.container.vel[self.idx]
    
    @property
    def acc(self):
        return self.container.acc[self.idx]



