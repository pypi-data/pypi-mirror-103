#!/usr/bin/python
# coding: utf-8
# editor: mufei(ypdh@qq.com tel:15712150708)
'''
牧飞 _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''

__all__ = ['urlopen', 'urlparse', 'tldextract']

import sys, os, re
py = list(sys.version_info)


if py[0]==2:
    #url, data=None, timeout=<object>, cafile=None, capath=None, cadefault=False, context=None
    from urllib2 import urlopen
    from urlparse import urlparse
else:
    #url, data=None, timeout=<object>, *, cafile=None, capath=None, cadefault=False, context=None
    from urllib.request import urlopen
    from urllib.parse import urlparse
    
    
try:
   import tldextract
except:
   tldextract = None
   
   
try:
    import psutil
except:
    psutil = None
    
    
def split_kv(s):
    s = s.strip()
    e = s.split()
    if s.count('"')==2:
        if s[0]==s[-1]=='"':
            v = [s[1:-1]]
        else:
            o=re.match(r'\"(.+)\"\s+(.+)$', s)
            if not o:
                o=re.match(r'(.+)\s+\"(.+)\"$', s)
            if o:
                v = list(o.groups())
            else:
                v = e 
    elif s.count('"')==4:
        o=re.match(r'\"(.+)\"\s+\"(.+)\"$', s)
        if o:
            v = list(o.groups())
        else:
            v = e 
    else:
        v = e
    
    return v

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
        
    
def get_free_mem():
    if psutil:
        return psutil.virtual_memory().free
        
    if os.path.isfile('/proc/meminfo'):
        mem = {}
        f = open('/proc/meminfo')
        lines = f.readlines()
        f.close()
        for line in lines:
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            mem[name] = float(var)
        return (mem['MemFree'] + mem['Buffers'] + mem['Cached']) * 1024
                
if __name__ == "__main__":
    print(get_free_mem())        


   
  