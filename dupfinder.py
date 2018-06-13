'''
Normal version, no multiprocessing
'''

import argparse
from collections import defaultdict
import os
from hashlib import sha1

# Collecting command line arguments
parser = argparse.ArgumentParser('subtitles')
parser.add_argument('-d', '--dir', required = True, type = str, nargs = '+', metavar = '', help = 'Directories to search')
parser.add_argument('-R' , '--Remove', required = False, action = 'store_true', help = 'Remove duplicates')
parser.add_argument('-S' , '--Sync', required = False, action = 'store_true', help = 'Sync directories')

args = parser.parse_args()

def gethash():
    
    # Create a result dictionary, default values are lists
    resdict = defaultdict(list)
    # Check if arguments are directories
    for dirz in args.dir:
        if not os.path.isdir(dirz):
            print('\n' + dirz + ' is not a directory, please check\n')
            exit(1)
        
        # Walk through the directory structure
        for (curdir, subdirs, filenames) in os.walk(dirz) :
            for file in filenames:
                # Join filename to and path to generate full path
                filepath = os.path.join(curdir,file).encode('utf8')
                with open(filepath,'rb') as file_to_hash:
                    # Create/reset a hasher to calculate sha1 for each file
                    hasher = sha1()
                    buf = file_to_hash.read(65536)
                    hasher.update(buf)
                    resdict[hasher.hexdigest()].append(filepath)
    return resdict
                    
        
    
def main():
    
    duplicates = 0
    result = gethash()
    for i in result.keys():
        if len(result[i]) > 1 :
            duplicates += 1
            print(result[i])
    print(duplicates)
            
  
if __name__ == '__main__': main()
