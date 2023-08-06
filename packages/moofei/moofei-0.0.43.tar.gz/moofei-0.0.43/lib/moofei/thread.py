#!/usr/bin/python
# -*- coding: utf-8 -*-
# editor: mufei(ypdh@qq.com tel:+086 15712150708)
'''
Mufei _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''
__all__ = ['Thread', 'is_threading_patch']

import time
import threading
import traceback
import os
import signal
import ctypes
from threading import Thread as _Thread
from time import sleep

try:
    from gevent import monkey, Greenlet, sleep
    is_threading_patch = monkey.is_module_patched('threading')    
except:
    monkey = Greenlet = None
    is_threading_patch = False
        
class Thread(_Thread):
    fncall = None #回调函数
    is_end = 0
    
    def __init__(self, fncall=None, thread_id=None, *args, **awgs):
        self.is_end = 0
        _Thread.__init__(self)
        self.args = args
        self.awgs = awgs
        self.daemon = True
        if fncall: self.fncall=fncall
        self.thread_id = thread_id
        self._pid = os.getpid()
        
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: return id
        return self.ident
        
    def kill(self):
        #os.kill(self._pid, signal.SIGKILL)  # kill子进程
        thread_id = self.get_id() 
        #精髓就是这句话，给线程发过去一个exceptions，线程就那边响应完就停了
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            
    def run(self):
        try:
            self.fncall(self.thread_id, *self.args, **self.awgs)
        finally:
            self.is_end = 1
    
    
    @classmethod    
    def main(cls, num, fncall, *args,  **awgs):
        """
        >>> rs = []            
        >>> def fncall(thread_id,L):
        >>>     while 1:
        >>>         time.sleep(0.5)
        >>>         if not L: break
        >>>         rs.append([thread_id,L.pop()])
        >>> Thread.main(10, fncall, range(10,100)) 
        >>> for e in rs: print(e)
        """
        threads = []
        for i in range(1,num+1):
            t = cls(fncall, i, *args,  **awgs)
            threads.append(t)

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()


            
        


    
            
