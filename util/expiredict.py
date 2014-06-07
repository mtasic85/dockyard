# -*- coding: utf-8 -*-
__all__ = ['ExpireDict']
import datetime
import threading

class ExpireDict(object):
    def __init__(self, timeout=1):
        self.lock = threading.Lock()
        self.timeout = timeout
        self.items = {}
        self._watch()
    
    def __getitem__(self, key):
        with self.lock:
            return self.items[key]
    
    def __setitem__(self, key, value):
        with self.lock:
            self.items[key] = value
    
    def __delitem__(self, key):
        with self.lock:
            del self.items[key]
    
    def __len__(self):
        with self.lock:
            return len(self.items)
    
    def __str__(self):
        with self.lock:
            return '<ExpireDict %s>' % repr(self.items)
    
    def _watch(self):
        if isinstance(self.timeout, datetime.timedelta):
            timeout = self.timeout.total_seconds()
        else:
            timeout = self.timeout
        
        t = threading.Timer(timeout, self._expire)
        t.start()
    
    def _expire(self):
        with self.lock:
            self.items.clear()
        
        self._watch()
