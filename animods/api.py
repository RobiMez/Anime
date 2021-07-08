from jikanpy import Jikan
ji = Jikan()

def anime_fetch_to_jsom(anime,limit):
    data = ji.search(search_type='anime', query=anime,parameters={'limit' :limit})
    print(data)
    file = open(f'{anime}.json','w')
    json.dump(data,file)
    file.close()

# Download the poster from jikan 
def download_poster(image_url,out_dir):
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
            printProgressBar(downloaded,filesize)
            time.sleep(0.007)
            # print(downloaded/filesize)
        buffer.seek(0)
        print()
        i = Image.open(io.BytesIO(buffer.read()))
        i.save(os.path.join(out_dir, 'image.jpg'), quality=100)
    buffer.close()