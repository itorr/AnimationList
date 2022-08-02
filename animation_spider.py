import os
import time
import json
import copy
import requests
from bs4 import BeautifulSoup as BS

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

proxies = {
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'
}

data_list = []

template_data = {
    'title_cn': '',
    'title_jp': '',
    'year': '',
    'path': ''
}

for year in range(2006, 2023):
    for page in range(0, 20):
        r = requests.get('http://bangumi.tv/anime/browser/tv/airtime/' + str(year) + '?page=' + str(page), headers=headers, proxies=proxies)
        r.encoding = 'utf-8' 
        soup = BS(r.text, features="html.parser")
        animation_list = soup.find('ul', id='browserItemList')

        path_list = [os.getcwd(), '\\cover\\' + str(year)]
        path = os.path.join(''.join(path_list))

        if len(animation_list):
            for animation in animation_list:
                if animation.div.h3.a:
                    title_cn = animation.div.h3.a.text
                if animation.div.h3.small:
                    title_jp = animation.div.h3.small.text
                
                if animation.a.span:
                    cover_pic = animation.a.span.img.get('src')
                    if cover_pic != '/img/no_icon_subject.png':
                        cover_pic = 'https:' + cover_pic
                        large_pic = cover_pic.replace('/c/', '/l/')

                        dir_path = path + '\\' + title_cn.replace('\\', ' ').replace('/', ' ').replace(':', ' ').replace('*', ' ').replace('?', ' ').replace('\"', ' ').replace('<', ' ').replace('>', ' ').replace('|', ' ').strip()
                        mkdir(dir_path)

                        cover_path = dir_path + '\\cover.jpg'
                        with open(cover_path, 'wb') as jpg_file:
                            pic = requests.get(cover_pic, headers=headers, proxies=proxies)
                            jpg_file.write(pic.content)
                        large_path = dir_path + '\\large.jpg'
                        with open(large_path, 'wb') as jpg_file:
                            pic = requests.get(large_pic, headers=headers, proxies=proxies)
                            jpg_file.write(pic.content)
                        temp = copy.deepcopy(template_data)
                        temp['title_cn'] = title_cn
                        temp['title_jp'] = title_jp
                        temp['year'] = str(year)
                        temp['path'] = 'cover/' + dir_path.split('\\cover\\')[1].replace('\\', '/')
                        data_list.append(temp)
                time.sleep(1)
        else:
            continue
    with open('data2.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data_list, ensure_ascii=False, indent=4))