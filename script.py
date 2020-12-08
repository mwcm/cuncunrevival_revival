import requests
from bs4 import BeautifulSoup
import os
import shutil
import time

for i in range(1362, 4499):
     time.sleep(5)
     article_url = f'https://revival1874.rssing.com/chan-53891303/article{i}.html'.format(i)
     article_req = requests.get(article_url)
     content = article_req.content
     soup = BeautifulSoup(content, 'html.parser')
     title = str(soup.title).split('|')[0].replace('<title>','')
     file_name = title.replace(' ', '_').replace('-','_').replace('___','_').replace('__','_').replace('&amp;','&')[:-1]
     file_name = file_name.replace('/', '_').replace(':','_').replace('?', '_').replace('\"','').replace("\'","")

     try:
         article_content = soup.find_all('div', {'class':'cs-single-post-content'})[0]
     except Exception as e:
         print('no cs-single-post-content')
         print(article_url)

     article_images = article_content.find_all('img')
     try:
        image_url = article_images[0]['data-src'].replace('//','')
     except Exception as e:
        print("No image for article named: {}".format(file_name))

     try:
         os.mkdir('./{0}/'.format(file_name))
     except Exception as e:
        print(e)
        pass
         
     with open('./{0}/{0}.html'.format(file_name), 'wb') as f:
         f.write(article_content.prettify().encode('utf-8'))
     for image in article_images:
         image_url = image['data-src'].replace('//', 'http://')
         imgres = requests.get(image_url, stream=True)
         with open('./{0}/{1}'.format(file_name, image_url.split('/')[-1]), 'wb') as out_file:
             shutil.copyfileobj(imgres.raw, out_file)