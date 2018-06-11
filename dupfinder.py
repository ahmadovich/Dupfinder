'''
Normal version, no multiprocessing
'''

import argparse
from collections import defaultdict
import os
from multiprocessing import Pool
from hashlib import sha1


parser = argparse.ArgumentParser('subtitles')
parser.add_argument('-d', '--dir', required = True, type = str, nargs = '+', metavar = '', help = 'Directories to search')
parser.add_argument('-R' , '--Remove', required = False, action = 'store_true', help = 'Remove duplicates')
parser.add_argument('-S' , '--Sync', required = False, action = 'store_true', help = 'Sync directories')

args = parser.parse_args()

def gethash(curdir,file):
    hasher = sha1()
    filepath = os.path.join(curdir,file)
    with open(filepath,'rb') as file_to_hash:
        buf = file_to_hash.read(65536)
        hasher.update(buf)
        return {hasher.hexdigest():filepath}
    
def main():
    dict1 = {}
    for i in args.dir:
        if not os.path.isdir(i):
            print('\n' + i + ' is not a directory, please check\n')
            exit(1)
        
    for (curdir, subdirs, filenames) in os.walk(args.dir[0]) :
            for file in filenames:
                dict1.update(gethash(curdir,file))
                
    print(dict1)
            
    
if __name__ == '__main__': main()
