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
        from tkinter import Tk, simpledialog, messagebox
        root = Tk()
        root.withdraw()
        root.update()
        gtt = simpledialog.askstring('', 'Token:', parent = root, show = '*')
        if gtt:
            ask = messagebox.askyesno('', 'Do you want set token to variable environment?', parent = root)
            root.destroy()            
            if ask:
                clien.cmsk(gtt, vr, vr.lower().replace('_',''))
                print('Please restart Console for var to work!')
                sys.exit()
            else:
                print('Token not set to variable environment!')
            ky = gtt
        else:
            print('No token, aborted!')
            
    if ky:
        if os.getenv(vr) != None and os.environ[vr] == ky:
            ky = clien.reading(ky, vr.lower().replace('_', ''))
            f = f'[pypi]\nusername = __token__\npassword = {ky}'
            if not '.pypirc' in os.listdir(os.environ['USERPROFILE']):
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
            print('Please set environment variable first!')

def build(path: str):
    # Build egg info, build, dist for upload to PyPI.
    # When rebuild, existing ones will be removed auto or manually by user.
    
    if os.path.isdir(path):
        os.chdir(path)
        fda = 'Archive_' + path.rpartition("\\")[2] 
        if fda not in os.listdir():
            os.mkdir(fda)
        folds = [f for i in ['build', 'dist', '.egg-info'] for f in os.listdir() if i in f]
        if folds:
            fda = os.path.join(fda, f'{str(dt.timestamp(dt.now())).replace(".", "_")}')
            os.mkdir(fda)
            try:
                for i in folds:
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
    pnam = None
    if '.pypirc' in os.listdir():
        pnam = f'py -m twine upload "{path}"'
    else:
        if os.getenv('TOKEN_PYPI') == None:
            print('Please create environment variable first for token!')
        else:
            tokfile(os.environ['TOKEN_PYPI'])
            pnam = f'py -m twine upload "{path}"'
    if pnam:
        with Popen(pnam, stdout = PIPE, bufsize = 1, universal_newlines = True, text = True) as p:
            for line in p.stdout:
                print(line, end='')
        
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