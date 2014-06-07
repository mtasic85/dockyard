# -*- coding: utf-8 -*-
__all__ = ['DebugPrint', 'enable_debug_print', 'disable_debug_print']

import os
import sys
import inspect

_orig_sys_stdout = sys.stdout
_prev_sys_stdout = sys.stdout

class DebugPrint(object):
    def __init__(self, f):
        self.f = f
        self.buffer = []
    
    def write(self, text):
        if text == os.linesep:
            frame = inspect.currentframe()
            filename = frame.f_back.f_code.co_filename.rsplit(os.sep, 1)[-1]
            lineno = frame.f_back.f_lineno
            prefix = "[%s:%s] " % (filename, lineno)
            
            self.buffer.append(text)
            text = ''.join(self.buffer)
            del self.buffer[:]
            self.f.write(prefix + text)
        else:
            self.buffer.append(text)

def enable_debug_print():
    global _prev_sys_stdout
    
    if not isinstance(sys.stdout, DebugPrint):
        _prev_sys_stdout = sys.stdout
        sys.stdout = DebugPrint(sys.stdout)

def disable_debug_print():
    sys.stdout = _prev_sys_stdout
    _prev_sys_stdout = _orig_sys_stdout
