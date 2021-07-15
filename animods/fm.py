import ffmpeg
import json
from animods.misc import c

def fm_sanity():
    return True


def get_probe(path):
    probe = ffmpeg.probe(path)
    return probe

def save_probe_to_json(path):
    probe = ffmpeg.probe(path)
    file = open(f'{path}.json','w')
    json.dump(probe,file)
    file.close()


def get_num_streams_from_filepath (fpath):
    fp = ffmpeg.probe(fpath)
    return fp["format"]["nb_streams"]

def get_streams_from_filepath (fpath):
    fp = ffmpeg.probe(fpath)
    return fp["streams"]

def get_video_qual_from_filepath (fpath):
    print(f'{c.purple}Probing {fpath}{c.o}')
    fp = None
    vstreams = []
    try:
        fp = ffmpeg.probe(fpath)
        for stream in fp["streams"]:
            if stream['codec_type'] == "video":
                vstreams.append(stream['height'])
        return vstreams
    except ffmpeg.Error as e:
        print(f'{c.red}{e.stderr}{c.o}')
        return 'Probe_error'
def get_video_streams_from_filepath (fpath):
    print(f'{c.purple}Probing {fpath}{c.o}')
    fp = None
    vstreams = []
    try:
        fp = ffmpeg.probe(fpath)
        for stream in fp["streams"]:
            if stream['codec_type'] == "video":
                vstreams.append(stream)
        return vstreams
    except ffmpeg.Error as e:
        print(f'{c.red}{e.stderr}{c.o}')
        return 'Probe_error'

def get_audio_streams_from_filepath (fpath):
    print(f'{c.purple}Probing {fpath}{c.o}')
    fp = None
    astreams = []
    try:
        fp = ffmpeg.probe(fpath)
        for stream in fp["streams"]:
            if stream['codec_type'] == "audio":
                astreams.append(stream)
        return astreams
    except ffmpeg.Error as e:
        print(f'{c.red}{e.stderr}{c.o}')
        return 'Probe_error'

def get_subtitle_streams_from_filepath (fpath):
    print(f'{c.purple}Probing {fpath}{c.o}')
    fp = None
    sstreams = []
    try:
        fp = ffmpeg.probe(fpath)
        for stream in fp["streams"]:
            if stream['codec_type'] == "subtitle":
                sstreams.append(stream)
        return sstreams
    except ffmpeg.Error as e:
        print(f'{c.red}{e.stderr}{c.o}')
        return 'Probe_error'

def get_attachment_streams_from_filepath (fpath):
    print(f'{c.purple}Probing {fpath}{c.o}')
    fp = None
    astreams = []
    try:
        fp = ffmpeg.probe(fpath)
        for stream in fp["streams"]:
            if stream['codec_type'] == "attachment":
                astreams.append(stream)
        return astreams
    except ffmpeg.Error as e:
        print(f'{c.red}{e.stderr}{c.o}')
        return 'Probe_error'
