import requests
from bs4 import BeautifulSoup
import os
import traceback


def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


if os.path.exists('imgs') is False:
    os.makedirs('imgs')

start = 1
end = 8000
for i in range(start, end + 1):
    url = 'http://konachan.net/post?page=%d&tags=' % i
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('span', class_="plid"):
        target_url = img.next[4:]
        tephtml = requests.get(target_url).text
        tepsoup = BeautifulSoup(tephtml, 'html.parser')
        targetimage_url = tepsoup.find('img', class_="image")['src']
        filename = os.path.join('imgs', targetimage_url.split(
            '/')[-2])+'.'+targetimage_url.split('.')[-1]
        download(targetimage_url, filename)
    print('%d / %d' % (i, end))
