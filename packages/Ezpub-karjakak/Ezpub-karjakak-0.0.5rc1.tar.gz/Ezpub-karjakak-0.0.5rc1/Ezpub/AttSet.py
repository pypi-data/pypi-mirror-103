# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import stat
import ctypes
import os

class AttSet:
    """
    Class attribute only hidden and system for TVG.
    """
    FILE_ATTRIBUTE_HIDDEN = stat.FILE_ATTRIBUTE_HIDDEN
    FILE_ATTRIBUTE_SYSTEM = stat.FILE_ATTRIBUTE_SYSTEM
    
    def __init__(self, filename: str, state: bool = False):
        self.filename = filename
        self.state = state
    
    def curstat(self):
        # Attributes states.
        
        current = os.stat(self.filename).st_file_attributes
        ck = ((stat.FILE_ATTRIBUTE_HIDDEN, 'Hidden'), 
              (stat.FILE_ATTRIBUTE_SYSTEM, 'System'),
             )
        ckr = {}
        for i, j in ck:
            ckr[j] = current & i == i
        ckr = {self.filename: ckr}
        return ckr

    """
    Code from:
    https://stackoverflow.com/questions/40367961/how-to-read-or-write-the-a-s-h-r-i-file-attributes-on-windows-using-python-and-c 
    """
    def set_file_attrib(self, attr: int):
        # Set tvg file attributes.
        
        if attr in [AttSet.FILE_ATTRIBUTE_HIDDEN, AttSet.FILE_ATTRIBUTE_SYSTEM]:
            current = os.stat(self.filename).st_file_attributes
            if self.state:
                changed = current | attr
            else:
                changed = current & ~attr
            if current != changed:
                if not ctypes.windll.kernel32.SetFileAttributesW(self.filename, changed):
                    raise ctypes.WinError(ctypes.get_last_error())