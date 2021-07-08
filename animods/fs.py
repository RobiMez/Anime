import os
from pathlib import Path
from animods.misc import c

def get_structure(root):
    return Path(root).rglob('*')

def check_if_path_is_dir(p):
    return Path(p).is_dir()

def check_if_path_is_file(p):
    return Path(p).is_file()

def alter_attributes(path,attribute):
    '''
    Usage :
    alter_attributes('sth.md','+R +S') # sets to read only and system
    Settings : 
        +   Sets an attribute.
        -   Clears an attribute.
    Attributes : 
        R   Read-only file attribute.
        A   Archive file attribute.
        S   System file attribute.
        H   Hidden file attribute.
        O   Offline attribute.
        I   Not content indexed file attribute.
        X   No scrub file attribute.
        V   Integrity attribute.
        P   Pinned attribute.
        U   Unpinned attribute.
        B   SMR Blob attribute.
    path : 
        path to your file 
    '''
    os.system(f'attrib {path} {attribute}')
    return 'Attributes changed'

def generate_lock_file(path,data):
    if check_if_path_is_dir(path):
        print(f'\n{c.b_black}Generating lockfile{c.o}')
        a_path = Path.absolute(path)
        a_l_path = Path.joinpath(a_path,'ani.lock')
        print(f'{c.b_black}{a_l_path}{c.o}')
        if a_l_path.exists():
            print(f'{c.blue}Info: {c.b_red}Deleting file {a_l_path}{c.o}')
            # Warning : Permanent delete powers
            os.remove(a_l_path)

        lock_file = open(a_l_path,'w')
        lock_file.write(data)
        lock_file.close()
        alter_attributes(a_l_path,'+H')
        print(f'{c.green}Generated lock file on {a_path}{c.o}')
    else:
        print(f'{c.orange}{path}{c.yellow} is not a folder.{c.o}')

# TODO:  Implement get filecount method here 






