'''
Now the script has the results as a dictionary, with keys as hash and value as an array of files resulting in this hash
Problem now is to merge multiple dictionaries from multiple processes
Now processes overwrite dictionary values containing same keys instead of appending them

'''

import argparse
import os
import multiprocessing as mp
from hashlib import sha256
from collections import defaultdict
import sys

parser = argparse.ArgumentParser('crawler')
parser.add_argument('-d', '--dir', required = True, type = str, nargs = '+', metavar = '', help = 'Directories to search')
parser.add_argument('-p', '--proc', required = False,  type = int,default = 4, metavar = '', help = 'Number of processes to launch , default is 4')
args = parser.parse_args()

def crawldirs(dirz,inqueue):
    print(sys.getdefaultencoding())
   
    for (curdir, subdirs, filenames) in os.walk(dirz) :
        for file in filenames:
            inqueue.put(os.path.join(curdir,file).encode('utf8'))
            
              

def gethash(inqueue,resqueue): 
    print('starting')                   
    proc_result = defaultdict(list)
    
    while not inqueue.empty():
        try:
            hashfile = inqueue.get(timeout = 3)
           
            with open(hashfile,'rb') as file:
                hasher = sha256()
                hasher.update(file.read(65535))
            proc_result[hasher.hexdigest()].append(hashfile)
        except:
            break
    
    resqueue.put(proc_result)
    print('Process done')

def main():
    resultdict = {}
    dirqueue = mp.Queue(2**20)
    resultqueue = mp.Queue(2**25)
        
    for i in args.dir:
        if not os.path.isdir(i):
            print('\n' + i + ' is not a directory, please check\n')
            exit(1)
    
    for dirz in args.dir:
        crawldirs(dirz,dirqueue)
    
    processes = [mp.Process(target=gethash, args=(dirqueue,resultqueue)) for x in range(args.proc)]
    
    for p in processes:
        print('starting procs')
        p.start()
        print('Procs started')
  
    #while not resultqueue.empty():
    while True:
        running = any(p.is_alive() for p in processes)
        while not resultqueue.empty():
            resultdict.update(resultqueue.get())
        if not running:
            break

    for p in processes:
        print('closing')
        p.join()
        print('closed')

    print(resultdict)
    print(len(resultdict.keys()))
    
if __name__ == '__main__': main()
