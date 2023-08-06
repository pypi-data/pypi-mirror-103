#!/usr/bin/python
# -*- coding: utf-8 -*-
# editor: mufei(ypdh@qq.com tel:+086 15712150708)
'''
Mufei _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''

print('xxxxxxx222')
  
try:
    from .plugin_fix_audio import cPlugin_Fix_Audio
except:
    print(77777)
    from moofei.find.plugin_fix_audio import cPlugin_Fix_Audio
    
    
print('xxxxxxx')


class Plugin_Fix_Wav(cPlugin_Fix_Audio):
    pass