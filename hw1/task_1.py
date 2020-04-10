import gc
import ctypes
import weakref

class PyObject(ctypes.Structure):
    _fields_ = [("refcnt", ctypes.c_long)]

class F():
    def __del__(self):
        print("Don't kill Kenny")

gc.disable()
kenny = F()
k_id = id(kenny)
print(PyObject.from_address(k_id).refcnt)
ref_kenny = weakref.finalize(kenny, print, 'You killed Kenny')
print(PyObject.from_address(k_id).refcnt)
del kenny
print(PyObject.from_address(k_id).refcnt)

gc.collect()
