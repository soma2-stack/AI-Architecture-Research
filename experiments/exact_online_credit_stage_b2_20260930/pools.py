"""Inspect actual loaded OpenBLAS thread counts without initializing CUDA."""
import ctypes

def thread_pools(process):
    result=[]
    for mapping in process.memory_maps():
        if 'openblas' not in mapping.path.lower():continue
        dll=ctypes.CDLL(mapping.path)
        for symbol in ('scipy_openblas_get_num_threads64_','scipy_openblas_get_num_threads','openblas_get_num_threads','openblas_get_num_threads64_'):
            try:fn=getattr(dll,symbol)
            except AttributeError:continue
            fn.restype=ctypes.c_int;result.append({'dll':mapping.path,'symbol':symbol,'threads':fn()});break
    return result
