# a
# WithAIndex

# inserted automatically
import os
import marshal

import struct
import shutil

from hashlib import md5

# custom db code start
# db_custom


# custom index code start
# ind_custom


# source of classes in index.classes_code
# classes_code


# index code start

class WithAIndex(HashIndex):
    """ hache with Index Class """
    def __init__(self, *args, **kwargs):
        """init"""
        kwargs['key_format'] = '32s'
        #~ kwargs['hash_lim'] = 4 * 1024
        super(WithAIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        """make a key value from ``data`` """
        a_val = data.get("a")
        if a_val:
            if not isinstance(a_val, unicode):
                a_val = unicode(a_val)
            return md5(a_val.encode('utf8')).hexdigest(), {}
        return None

    def make_key(self, key):
        """make a ``key`` """
        if not isinstance(key, unicode):
            key = unicode(key)
        return md5(key.encode('utf8')).hexdigest()
