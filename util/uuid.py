# -*- coding: utf-8 -*-
__all__ = ['gen_uuid', 'gen_alphanum_uuid']
import uuid
import hashlib

def gen_uuid(items=None):
    # example:
    #   u = uuid.uuid1().get_urn()
    #   u == 'urn:uuid:f362554a-035f-11e2-b5dc-8c89a52f713b'
    if items is None:
        key = uuid.uuid1().get_urn()[9:]
        return key
    else:
        m = hashlib.sha256()
        
        for item in items:
            m.update(item)
        
        key = m.hexdigest()
        return key

def gen_alphanum_uuid():
    key = uuid.uuid1().get_urn()[9:]
    key = key.replace('-', '')
    key = key.replace('_', '')
    return key
