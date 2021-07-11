import json
import requests
from pprint import pprint
from jikanpy import Jikan
ji = Jikan()


def api_sanity():
    return True


def anime_fetch_to_json(anime, limit):
    data = ji.search(search_type='anime', query=anime,
                     parameters={'limit': limit})
    print(data)
    file = open(f'{anime}.json', 'w')
    json.dump(data, file)
    file.close()

# Download the poster from jikan


def download_poster(image_url, out_dir):
    print("[ ^>^ ] Downloading cover art :")
    buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        downloaded = 0
        filesize = int(r.headers['content-length'])
        for chunk in r.iter_content(chunk_size=1024):
            downloaded += len(chunk)
            buffer.write(chunk)
            # print(printprogressBar(downloaded))
            printProgressBar(downloaded, filesize)
            time.sleep(0.007)
            # print(downloaded/filesize)
        buffer.seek(0)
        print()
        i = Image.open(io.BytesIO(buffer.read()))
        i.save(os.path.join(out_dir, 'image.jpg'), quality=100)
    buffer.close()


def get_episode_names_for_anime(anime_name):
    mal_id = anime_name

    response_body = requests.get(
        f'https://api.jikan.moe/v3/anime/{mal_id}/episodes')
    response_body = response_body.content.decode('utf-8')
    # response_body = response_body[:-1]
    # response_body = response_body[:-1]
    pprint(type(response_body))
    pprint(response_body)
    # String manipulation 
    evald = json.loads(response_body)
    episodes = evald['episodes']
    ep_names = []
    for ep in episodes:
        ep_names.append(ep['title'])
        
    print('\n\n\n')
    pprint(ep_names)

def get_data_for_id(mal_id):

    response_body = requests.get(f'https://api.jikan.moe/v3/anime/{mal_id}')
    if response_body.status_code == 404 :
        print('404')
        return False
    else : 
        response_body = response_body.content.decode('utf-8')

        pprint(type(response_body))
        pprint(response_body)

        result = json.loads(response_body)
        print (result)
        data = {}

        print('\n\n\n')
        
        data['title'] = result['title']
        data['mal_id'] = result['mal_id']
        data['episodes'] = result['episodes']
        data['status'] = result['status']
        data['airing'] = result['airing']
        data['title_english'] = result['title_english']
        data['title_japanese'] = result['title_japanese']
        data['aired'] = result['aired']['string']
        data['rating'] = result['rating']
        data['premiered'] = result['premiered']
        data['favorites'] = result['favorites']
        data['score'] = result['score']
        data['scored_by'] = result['scored_by']
        data['type'] = result['type']
        
        genre_list = []
        for genre in result['genres']:
            genre_list.append(genre['name'])
        data['genres'] = genre_list
        
        licensors_list = []
        for licensor in result['licensors']:
            licensors_list.append(licensor['name'])
        data['licensors'] = licensors_list
            
        producers_list = []
        for producer in result['producers']:
            producers_list.append(producer['name'])
        data['producers'] = producers_list
        
        studios_list = []
        for studio in result['studios']:
            studios_list.append(studio['name'])
        data['studios'] = studios_list
        


        pprint(data)




def get_predictions_for_folder_name(folder_name):

    resp = ji.search('anime', folder_name, parameters={'limit': 5})
    results_list = []
    for result in resp['results']:
        results_list.append((result['title'],result['mal_id']))
    return results_list
    

    # response_body = requests.get(f'https://api.jikan.moe/v3/anime/{mal_id}')
    # if response_body.status_code == 404 :
    #     print('404')
    #     return False
    # else : 
    #     response_body = response_body.content.decode('utf-8')

    #     pprint(type(response_body))
    #     pprint(response_body)

    #     result = json.loads(response_body)
    #     print (result)
    #     data = {}

    #     print('\n\n\n')
        
    #     data['title'] = result['title']
    #     data['mal_id'] = result['mal_id']
    #     data['episodes'] = result['episodes']
    #     data['status'] = result['status']
    #     data['airing'] = result['airing']
    #     data['title_english'] = result['title_english']
    #     data['title_japanese'] = result['title_japanese']
    #     data['aired'] = result['aired']['string']
    #     data['rating'] = result['rating']
    #     data['premiered'] = result['premiered']
    #     data['favorites'] = result['favorites']
    #     data['score'] = result['score']
    #     data['scored_by'] = result['scored_by']
    #     data['type'] = result['type']
        
    #     genre_list = []
    #     for genre in result['genres']:
    #         genre_list.append(genre['name'])
    #     data['genres'] = genre_list
        
    #     licensors_list = []
    #     for licensor in result['licensors']:
    #         licensors_list.append(licensor['name'])
    #     data['licensors'] = licensors_list
            
    #     producers_list = []
    #     for producer in result['producers']:
    #         producers_list.append(producer['name'])
    #     data['producers'] = producers_list
        
    #     studios_list = []
    #     for studio in result['studios']:
    #         studios_list.append(studio['name'])
    #     data['studios'] = studios_list
        


    #     pprint(data)



