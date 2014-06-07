# -*- coding: utf-8 -*-
__all__ = ['gen_hash']
import hashlib

def gen_hash(*args):
    m = hashlib.md5()
    
    for arg in args:
        arg = str(arg)
        arg = arg.encode('utf-8')
        m.update(arg)
    
    key = m.hexdigest()
    return key
