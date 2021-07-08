import time 
import PIL
import os

import json
from pprint import pprint 

import pathlib
from pathlib import Path
import collections

from animods.misc import *
from animods.fm import *
from animods.fs import *
from animods.api import *
from animods.img import *


root = Path('./devy')

''' for all folders in the root 

gen lock file 
get data on files 
get data on folder 

generate icon ( with size if possible )
rename with size 






'''





















# class anicons:
#     def __init__ (self) : 
#         os.system('cls')
#         print('-------------------------------------#')
#         self.cwd = Path.cwd()
#         self.home = Path.home()
#         print('CWD:',self.cwd)
#         print('HOME:',self.home)

#     def gen_struct(self):
#         for p in Path(self.cwd).rglob('*'):
#             if p.is_dir() :
#                 print(f"[D] {p}")
#                 # time.sleep(0.1)
#             elif p.is_file():
#                 # print(f"[F]{p.suffix}]\t{p.parent}\{p.name}")
#                 # print(f"[F][{p}")
#                 # time.sleep(0.1)
#                 if p.suffix == '.mkv' or p.suffix == '.mp4':
#                     try: 
#                         probe_data = get_probe(str(p))
#                         # save_probe(str(p))
#                         # pprint(probe_data['streams'])
#                         os.system('cls')
#                     # 
#                         print(f'\n{c.green}-------  File Data  ----------------------------{c.o}')
#                     # 
#                         print(f"{c.b_black}Name : {c.o}",p.name)
#                         print(f'{c.purple}Duration :{c.o}',round(float(probe_data['format']['duration'])/60,2),'Minute(s)')
#                         print(f"{c.purple}Filesize :{c.o}",round(float(probe_data['format']['size'])/1024/1024,2),"Mb")
#                         print(f"{c.purple}Creation time :{c.o}",probe_data['format']['tags']['creation_time'].split('T')[0])

#                     # 
#                         print(f'\n{c.green}-------  Streams ( {probe_data["format"]["nb_streams"]} ) --------------{c.o}')
#                     # 
                        
#                         for stream in probe_data['streams']:
                            
#                             codec_type = stream['codec_type'].capitalize()
#                             # codec_name = stream['codec_name']
#                             codec_long_name = stream['codec_long_name']
#                             print(f'{c.b_purple}{codec_type} | {c.blue}{codec_long_name}{c.o}')
#                             # 
#                             if codec_type == 'Video':
#                                 print(f"{c.green} Quality :{c.o}",stream['height'],'P')
#                                 print(f"{c.b_black} Aspect Ratio :{c.o}",stream['display_aspect_ratio'])
#                                 print(f"{c.b_black} Dimensions :{c.o}",stream['width'],'x',stream['height'])
#                             if codec_type == 'Audio':
                                
#                                 print(f"{c.green} Language :{c.o}",stream['tags']['language'].capitalize())
#                                 print(f"{c.b_black} Channels :{c.o}",stream['channels'])
#                                 print(f"{c.b_black} Layout :{c.o}",stream['channel_layout'])

#                             if codec_type == 'Subtitle':

#                                 print(f"{c.green} Language :{c.o}",stream['tags']['language'].capitalize(),stream['tags']['title'])
#                                 print(f"{c.b_black} Size :{c.o}",round(float(stream['tags']['NUMBER_OF_BYTES'])/1024),'Kbs')

                                
#                     except KeyError as e :
#                         print(f"{c.red} {e} {c.o}")
#                         if e != 'title':
#                             pass
#                         elif e != 'NUMBER_OF_BYTES':
#                             pass
#                         else : 
#                             print(f"{c.b_black} {stream} {c.o}")
#                             time.sleep(20)
#                     time.sleep(0.03)

# ani = anicons()
# for node in get_structure('./'):
#     print(f'{c.green}{check_if_path_is_dir(node)}{c.o}')
#     print(f'{c.blue}{check_if_path_is_file(node)}{c.o}')
#     print(f'{c.b_black}{node}{c.o}')

