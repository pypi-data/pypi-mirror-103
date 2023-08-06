# -*- coding: utf-8 -*-
# Copyright © karjakak (K A K)

from .AttSet import AttSet
import os
import shutil
from subprocess import Popen, PIPE
import argparse
from datetime import datetime as dt
from Clien import clien
import sys

# Reference:
#stackoverflow.com/.../constantly-print-subprocess-output-while-process-is-running

def tokfile(token: str = None):
    # Create token to .pyirc for publish to PyPI.
    
    pth = os.path.join(os.environ['USERPROFILE'], '.pypirc')
    ky = None
    vr = "TOKEN_PYPI"
    if token:
        if token == 'd':
            if '.pypirc' in os.listdir(os.environ['USERPROFILE']):
                a = AttSet(pth)
                for i in [a.FILE_ATTRIBUTE_HIDDEN, 
                          a.FILE_ATTRIBUTE_SYSTEM,
                          a.FILE_ATTRIBUTE_READONLY,
                         ]:
                    a.set_file_attrib(i)
                os.remove(pth)
                print('Token Removed') 
            else:
                print('Nothing to remove, token not created yet!')
        else:
            ky = token
    else:
        print(f'IMPORTANT!')
        print(f'Please fill var: {vr}')
        gtt = clien.insdat()
        if gtt and gtt[1] == vr:
            clien.cmsk(gtt[0], gtt[1], gtt[2])
        else:
            if gtt is None:
                print('All fields need to be filled!')
            else:
                print(f'Field "var:" must be "{vr}"!')            
    if ky:
        pss = clien.pssd()
        if os.getenv(vr) and pss:
            ky = clien.reading(ky, pss)
            if ky:
                f = f'[pypi]\nusername = __token__\npassword = {ky}'
                if not os.path.isfile(pth):
                    with open(pth, 'w') as tkn:
                        tkn.write(f)
                    a = AttSet(pth, True)
                    for i in [a.FILE_ATTRIBUTE_HIDDEN, 
                              a.FILE_ATTRIBUTE_SYSTEM,
                              a.FILE_ATTRIBUTE_READONLY,
                             ]:
                        a.set_file_attrib(i)
                    print('Token created')
                else:
                    print('Nothing to create, token already created!')                    
            else:
                print('Unable to create token!')
        else:
            print('Token not created yet!')

def build(path: str):
    # Build egg info, build, dist for upload to PyPI.
    # When rebuild, existing ones will be removed auto or manually by user.
    
    if os.path.isdir(path):
        os.chdir(path)
        folds = [f for i in ['build', 'dist', '.egg-info'] for f in os.listdir() if i in f]
        if folds:
            fda = os.path.join('Archive_' + path.rpartition("\\")[2], 
                               f'{str(dt.timestamp(dt.now())).replace(".", "_")}')
            if not os.path.isdir(fda.rpartition('\\')[0]):
                os.mkdir(fda.rpartition('\\')[0])
            os.mkdir(fda)
            for i in folds:
                try:
                    shutil.move(i, fda)
                except Exception as e:
                    print(e)
                    print(f'Please remove {folds} manually!')
                    os.startfile(path)
                    sys.exit()
        pnam = f'py -m build'
        with Popen(pnam, stdout = PIPE, bufsize = 1, universal_newlines = True, text = True) as p:
            for line in p.stdout:
                print(line, end='')
                
def publish(path: str):
    # Upload to PyPI.
    
    os.chdir(os.environ['USERPROFILE'])
    if '.pypirc' in os.listdir():
        pnam = f'py -m twine upload "{path}"'
        with Popen(pnam, stdout = PIPE, bufsize = 1, universal_newlines = True, text = True) as p:
            for line in p.stdout:
                print(line, end='')
    else:
        print('Please create token first!')
        
def main():
    # This will only work in cli.
    
    parser = argparse.ArgumentParser(description = "Upload projects to PyPi")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t","--token", type = str, help = 'Token for publish.')
    group.add_argument("-b","--build", type = str, help = 'Build project, ready for publish.')
    group.add_argument("-p", "--publish", type = str, help = 'Publish to pypi.' )
    args = parser.parse_args()
    if args.token:
        if args.token == 'None':
            tokfile()
        else:
            tokfile(args.token)
    elif args.build:
        build(args.build)
    elif args.publish:
        publish(args.publish)    

if __name__ == '__main__':
    main()