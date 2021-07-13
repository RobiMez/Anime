import time 
import PIL
import os
import re
import json
from pprint import pprint 
import pathlib
from pathlib import Path
import collections
# -------------------------------------------------
from animods.misc import *
from animods.fm import *
from animods.fs import *
from animods.api import *
from animods.img import *

def cls_in(delay=0,keep='') :
    time.sleep(delay)
    os.system('cls')
    print(keep)

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def _startup_check() : 
    print(f'\n{c.green}Startup checks ...{c.o}\n')
    print(f'{c.green}\tFilesystem module : {c.o}{fs_sanity()}')
    print(f'{c.green}\tFFempeg module : {c.o}{fm_sanity()}')
    print(f'{c.green}\tApi module : {c.o}{api_sanity()}')
    print(f'{c.green}\tImage module : {c.o}{img_sanity()}')
    print(f'{c.green}\tMisc module: {c.o}{misc_sanity()}\n\n')

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def prompt_verification_from_lock(path):

    lock_file = open(Path.joinpath(path,'ani.lock'), 'r',encoding='utf-8')
    lock_file_data = lock_file.read()
    lock_file.close()
    # wrap the file data in an eval()
    #  to make it pythonable 
    lock_file_data = eval(lock_file_data)
    # logic after lock data is available
    predictions = lock_file_data['predictions']
    
    print(f'\n{c.b_black} -------------------------------- {c.o}')
    print(f'{c.b_purple} Prompt : Choose the correct prediction for the current folder {c.o}\n')
    print(f'{c.b_black} -------- [ Folder data ] -------- {c.o}')
    print(f'{c.blue} {lock_file_data["folder_name"]} {c.o}')
    print(f'{c.b_black} -------- [ Predictions ] -------- {c.o}\n')
    print(f'\n{c.purple} [0] : Skip{c.o}\n')
    i = 1
    for prediction in predictions:
        print(f'{c.green} [{i}] : {prediction[0]} {c.o}')
        print(f'{c.b_black} {prediction[2]} {c.o}')
        i = i + 1
    
    print(f'\n{c.b_black} -------------------------------- {c.o}\n')
    choice = input('Choice :')

    if choice.isnumeric():
        if int(choice) <= 5 and int(choice) >= 0:
            # we have verification 
            # set is verified to true 
            lock_file_data['is_verified'] = True
            correct_prediction = None
            # get the correct predicion 
            # unless skipped 
            if int(choice) == 0 : 
                pass
            else:
                correct_prediction = predictions[int(choice)-1] 
            # Get the correct predicion data
            lock_file_data['correct_prediction'] = correct_prediction
            # remove the predicions as now we are sure
            lock_file_data.pop('predictions')
            generate_lock_file(path,lock_file_data)
    else: 
        print(f'Please choose from [ 0 - 5 ]')

def generate_predictions_and_folder_data_to_lock(path):
    # lock data starts empty as this is the first step
    lock_data = {}
    
    lock_data['folder_name'] = path.name
    
    lock_data['folder_size_MB'] = round((get_size(path)/1024)/1024,2)
    lock_data['folder_size_GB'] = round(((get_size(path)/1024)/1024)/1024,2)
    # count up the files and their types
    # bundle it up into a dict and add it to the lock data
    file_enumeration = count_filetypes(path)
    folder_contents = {}
    
    for filetype in file_enumeration:
        folder_contents[filetype] = file_enumeration[filetype]

    lock_data['folder_contents'] = folder_contents
    # get the predictions from the api and add that to the lock data 
    predictions = get_predictions_for_folder_name(path.name)
    lock_data['predictions'] = predictions
    # set some of these for further down the line 
    lock_data['is_verified'] = False
    lock_data['is_ignored'] = False
    lock_data['api_fetched'] = False
    lock_data['episode_names'] = False
    lock_data['local_ep_data'] = False
    lock_data['ffmpeg_fetched'] = False
    generate_lock_file(Path.joinpath(Path.cwd(),path),lock_data)
    pass

def generate_api_data_from_lock(path):
    lock_file = open(Path.joinpath(path,'ani.lock'), 'r',encoding='utf-8')
    lock_file_data = lock_file.read()
    lock_file.close()
    # wrap the file data in an eval()
    #  to make it pythonable 
    lock_file_data = eval(lock_file_data)
    # logic after lock data is available
    mal_id = lock_file_data['correct_prediction'][1]
    print(f'{c.purple} - Fetching detailed data for {mal_id}{c.o}')
    api_data = get_data_for_id(mal_id)
    ep_data = get_episode_names_for_anime(mal_id)
    
    print(f'\n{c.green} Fetched Data :{c.o}\n')

    print(f'\n{c.green}{api_data}{c.o}\n')
    print(f'\n{c.blue}{ep_data}{c.o}\n')
    
    # add the detailed data
    lf_api_data = Merge(lock_file_data,api_data)

    lf_api_data['episode_names'] = ep_data
    lf_api_data['api_fetched'] = True
    
    
    print(f'\n{c.yellow}{lf_api_data}{c.o}\n')
    
    generate_lock_file(path,lf_api_data)

def generate_ffmpeg_data_from_lock(path):
    lock_file = open(Path.joinpath(path,'ani.lock'), 'r',encoding='utf-8')
    lock_file_data = lock_file.read()
    lock_file.close()
    # wrap the file data in an eval()
    #  to make it pythonable 
    lock_file_data = eval(lock_file_data)
    # logic after lock data is available
    print(f'\n{c.purple} Fetching Local Episode data {c.o}\n')
    # need to check stuff for every file in the dir
    folder_contents = lock_file_data['folder_contents']
    supported_media_types = ['.mp4','.mkv','.flv','.webm']
    for item in folder_contents:
        if item in supported_media_types:
            i=0
            file_data_container = []
            for item in path.rglob(f"*{item}"):
                print(f'{c.b_black}{Path.joinpath(path,item)}{c.o}')
                file_data = {}
                file_data['current_filename'] = item.name
                pep_num = re.findall(r'\b\d+\b', item.name)
                print(f'{c.red}{pep_num}{c.o}')
                file_data['predicted_ep_num'] = pep_num
                
                file_data['num_audio'] = len(get_audio_streams_from_filepath(str(Path.joinpath(Path.cwd(),item))))
                file_data['num_video'] = len(get_video_streams_from_filepath(str(Path.joinpath(Path.cwd(),item))))
                file_data['num_subtitle'] = len(get_subtitle_streams_from_filepath(str(Path.joinpath(Path.cwd(),item))))
                file_data['num_attachments'] = len(get_attachment_streams_from_filepath(str(Path.joinpath(Path.cwd(),item))))
                file_data['video_qual'] = get_video_qual_from_filepath(str(Path.joinpath(Path.cwd(),item)))

                print(f'{c.b_black}{file_data}{c.o}')

                i += 1
                file_data_container.append(file_data)
            print(f'{c.blue}{file_data_container}{c.o}')
            lock_file_data['local_ep_data'] = file_data_container
            lock_file_data['ffmpeg_fetched'] = True
            generate_lock_file(path,lock_file_data)
    pass

def splice_ep_name_predicions_with_data(path):
    lock_file = open(Path.joinpath(path,'ani.lock'), 'r',encoding='utf-8')
    lock_file_data = lock_file.read()
    lock_file.close()
    # wrap the file data in an eval()
    #  to make it pythonable 
    lock_file_data = eval(lock_file_data)
    # logic after lock data is available

    generate_lock_file(path,lf_api_data)

    pass
# def splice_ep_namepredicions_with_data(path):
#     lock_file = open(Path.joinpath(path,'ani.lock'), 'r',encoding='utf-8')
#     lock_file_data = lock_file.read()
#     lock_file.close()
#     # wrap the file data in an eval()
#     #  to make it pythonable 
#     lock_file_data = eval(lock_file_data)
#     # logic after lock data is available

#     generate_lock_file(path,new_data)

#     pass

main_path = './WATCHED'
def main():
    _startup_check()
    cls_in(2)
    for node in Path(main_path).rglob('*'):
        print(f'{c.b_black}Going through : {main_path}{c.o}')
        print(f'{c.b_black}Currently on  : {node}{c.o}')
        if node.is_dir():
            # ------------------------
            if Path.joinpath(node,'ani.lock').exists() :
                # We have a folder with a lock file 
                print(f'{c.green} Found a lockfile {c.o}')
                
                l_file = open(Path.joinpath(node,'ani.lock'), 'r',encoding='utf-8')
                data = l_file.read()
                l_file.close()
                data = eval(data)
                
                if data['is_verified'] == False:
                    prompt_verification_from_lock(node)
                # ##############################################
                if data['api_fetched'] == False:
                    generate_api_data_from_lock(node)
                else:
                    print(f'{c.green} Api data is already fetched. {c.o}\n\n')
                # ##############################################
                if data['ffmpeg_fetched'] == False:
                    generate_ffmpeg_data_from_lock(node)
                    pass
                else:
                    print(f'{c.green} file data is already fetched. {c.o}\n\n')
            else:
                generate_predictions_and_folder_data_to_lock(node)
                prompt_verification_from_lock(node)
                generate_api_data_from_lock(node)
                generate_ffmpeg_data_from_lock(node)
            # ------------------------

    print(f"\n{c.purple}Exiting ... {c.o}")
    time.sleep(1)



if __name__ == '__main__':
    main()














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

