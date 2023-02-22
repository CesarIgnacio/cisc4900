
# render the page
from operator import index
from posixpath import split
from numpy import record
from requests_html import HTMLSession
import requests
import os
import pandas as pd
import json



url='https://ebird.org/media/catalog?taxonCode=monpar&mediaType=p'
s= HTMLSession()



r= s.get(url)

r.html.render(scrolldown=1, sleep=1,keep_page=True)

bird_list=[]

url = "https://ebird.org/media/catalog.json"
for x in range(1,2):
    querystring = {"searchField":"species","q":"","taxonCode":"monpar","hotspotCode":"","regionCode":"","customRegionCode":"","watershedCode":"","userId":"","_mediaType":"on","mediaType":"p","species":"","region":"","hotspot":"","customRegion":"","mr":"M1TO12","bmo":"1","emo":"12","yr":"YALL","by":"1900","ey":"2022","user":"","view":"Gallery","sort":"upload_date_desc","_req":"on","cap":"no","subId":"","catId":"","_spec":"on","specId":"","collection":"","collectionCatalogId":"","dsu":"-1","initialCursorMark":"MjAyMi0wMy0wNlQwNjo1MzoxMi4zOTU3MDJfXzQyMjU2NDEyMQ","count":"10","_":"1647120557635"}

    payload = {'limit': '9999'}
    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": "^\^",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    data=response.json()
    for item in data['results']['content']:
        bird_json={
            'ml_ID': item['assetId'],
            'image': item['previewUrl'],
            'mediaUrl':item['mediaUrl'],
            'mediaType':item['mediaType'],
            'longitude': item['longitude'],
            'latitude': item['latitude'],
            'commonName': item['commonName'],
            'commonName': item['commonName'],
            'sciName': item['sciName'],
            'link_bird': item['specimenUrl'],
            'location':item['location'],
            'locationLine2':item['locationLine2'],
            'Contributor': item['userDisplayName'] ,
            'City': '',
            'State': '',
            'Country': '' ,
            'Date(YYYY-MM-DD)': '',
            'Time': '',
            'Nest(0,1)':'0',
            'Audio(0,1)':'0',
            'Image(0,1)':'0',
            'Tempeture(F)':'',
            'observations':item['obsComments'],
            'mediaName':''
           
        }
        r=s.get(bird_json['link_bird'])
    
        #item['Contributor']=r.html.find('div.DefinitionList-group,dd',first=True).text.split('\n')[1]
        
        date_time=str(r.html.find('time[datetime]',first=True)).split("'")
        location=item['location']
        location2=item['locationLine2'].split(',')
        bird_json['City']=location2[0]
        bird_json['State']=location2[1]
        try:
            bird_json['Country']=location2[2]
        except:
            bird_json['Country']=location2[1]
        bird_json['Date(YYYY-MM-DD)']=date_time[5].split('T')[0]
        bird_json['Time']=date_time[5].split('T')[1]
        
        if (bird_json['mediaType']== 'Photo'):  
            print(bird_json['image']) 
            name=os.getcwd()+'/Images/'+bird_json['commonName']+'_' +bird_json['ml_ID']+ '.jpg'
            with open(name ,'wb') as f:
                res =s.get(bird_json['image'])
                f.write(res.content)
                print('Downloading Image')
                bird_json['Image(0,1)']='1'
                bird_json['mediaName']=name
        if (bird_json['mediaType']== 'Audio'): 
            name= os.getcwd()+'/Audio/'+bird_json['commonName']+'_' +bird_json['ml_ID']+'.mp3'
            with open(name,'wb') as f:
                res = s.get(bird_json['mediaUrl'])
                f.write(res.content)
                print('Downloading Audio')
                bird_json['Image(0,1)']='1'
                bird_json['mediaName']=name
        bird_list.append(bird_json)
       

print(r.status_code)

        
# for item in bird_list:
#     r=s.get(item['link_bird'])
    
#     item['Contributor']=r.html.find('div.DefinitionList-group,dd',first=True).text.split('\n')[1]
    
#     date_time=str(r.html.find('time[datetime]',first=True)).split("'")
#     location=item['location']
#     location2=item['location2'].split(',')
#     city=location2[0]
#     state=location2[1]
#     try:
#         country=location2[2]
#     except:
#         country=location2[1]
#     date=date_time[5].split('T')[0]
#     time=date_time[5].split('T')[1]
    
    

    
    

    


# def output():
df=pd.DataFrame(data=bird_list)

df.to_csv('Monkparakees2.csv')
df.to_json('Json_File.json',orient="records")
print('Saved to Csv')
