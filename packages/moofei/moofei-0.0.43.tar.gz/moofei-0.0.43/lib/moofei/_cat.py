#!/usr/bin/python
# coding: utf-8
# editor: mufei(ypdh@qq.com tel:15712150708)
'''
Mufei _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''

__all__ = ['_cat', ]

import sys,os,json,re,time,math
import chardet
py = list(sys.version_info)

def _cat(fname, page=None, bsize=100*1024, mode='rb', encoding=None, callback=None, **awgs):
    st_size = os.stat(fname).st_size
    if not st_size: return
    txts = []
    n = 0
    if awgs.get('show_all'):
        seek_size = 0
    elif page is None:
        seek_size = int(st_size/bsize)*bsize
    elif page<0:
        seek_size = st_size+page*bsize
    else:
        seek_size = page*bsize
    if seek_size<0: seek_size=0
    elif seek_size>st_size: 
        seek_size = int(st_size/bsize)*bsize
    
    if py[0]==2 or 'b' in mode:
        fp = open(fname,mode)
    else:
        fp = open(fname,mode, encoding=encoding or 'utf-8')
    
    if 'b' in mode :
        if  not encoding:
            d = chardet.detect(fp.read(1024*100))
            if d.get('confidence',0) > 0.7:
                encoding = d['encoding']
                if encoding.upper()=='GB2312': encoding='GBK'
            fp.seek(0)
        with fp:
            if seek_size: fp.seek(seek_size)
            txts = fp.read(bsize)
        if encoding: txts = txts.decode(encoding).split('\n')
        else: txts = [txts]
    else:            
        with fp:
            if seek_size: fp.seek(seek_size)
            for line in fp:
                n += len(line)
                txts.append(line)
                if n>=bsize: break
        
    return txts, [st_size, encoding]
    
    
def main(cmd=None):
    import argparse
    parser = argparse.ArgumentParser(description="""Cat FileName <http://www.mufei.ltd>  """,
                                     epilog="QQqun: 226895834 ",
                                     formatter_class=argparse.RawDescriptionHelpFormatter
                                     )
    if cmd:
       parser.add_argument('cmd',  help="Command line mode; generally can be ignored") 
    parser.add_argument('name')
    parser.add_argument('-bsize','--bsize', type=int, default=100*1024)
    parser.add_argument('-page','--page', type=int, default=None)
    parser.add_argument('-mode','--mode', default='rb')
    parser.add_argument('-encoding','--encoding')
    parser.add_argument('--show-all', action='store_true')
    
    args = parser.parse_args()
    if '-h' in sys.argv :
        print(args)
    else:
        rs = _cat(args.name, 
                  bsize=args.bsize,
                  mode=args.mode,
                  page=args.page,
                  encoding=args.encoding,
                  show_all=args.show_all)
        for line in rs[0]:
            print(line)  
        print('---------------end print',rs[1])            
    
if __name__ == "__main__":         
    main()

