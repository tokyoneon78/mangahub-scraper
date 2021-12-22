import cloudscraper
import json
import os
import requests
import time

#endpoint to scrape
api = "https://api.mghubcdn.com/graphql"

#Headers for scraper
headers = {
  'Content-Type': 'application/json'
}

#Scraper module configuration
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)


#Slug to input e.g "reincarnation-of-the-suicidal-battle-god"
slug = input("Enter slug:- ")

def manga_info(slug, headers):
  #converts payload to query endpoint with to json
  payload = json.dumps({
    "query": "{manga(x:m01,slug:\""+ slug +"\"){id,rank,title,slug,status,image,latestChapter,author,artist,genres,description,alternativeTitle,mainSlug,isYaoi,isPorn,isSoftPorn,unauthFile,noCoverAd,isLicensed,createdDate,updatedDate,chapters{id,number,title,slug,date}}}"
  })


  #Query sent to the server works like requests
  response = scraper.request("POST", api, headers=headers, data=payload).text
  #print(len(json.loads(response)["data"]["manga"]["chapters"]))
  return response


def manga_download(slug, headers):
  #Converted output to JSON
  base_data = json.loads(manga_info(slug, headers))

  #printing out base info about the manga
  print(base_data)

  #Gets a list of the chapters using JSON manipulation
  chapter_number = (base_data["data"]["manga"]["chapters"])
  l = 0

  #print(chapter_number)

  #Creates directory for the slug and switches into it

  
  os.mkdir(slug)
  os.chdir(slug)
  parent_dir = os.getcwd()

  print("There are {} chapters.".format(len(chapter_number)))
  start_of_chapters = int(input('Enter the first chapter to download: ')) - 1
  end_of_chapters = int(input('Enter the last chapter to download: ')) 
  range_download = chapter_number[start_of_chapters:end_of_chapters]
  print(range_download)
  
  #Looping through each chapter received
  for chapter in range_download:
    #Sleep statement to avoid bot flagging by cloudflare
    time.sleep(1.0)
    #Scrape indiviual chapters
    rurl = "{\"query\":\"{chapter(x:m01,slug:\\\"" + base_data["data"]["manga"]["slug"] + "\\\",number:" + str(chapter_number[start_of_chapters]["number"]) + "){pages}}\"}"
    
    chaps_indi = scraper.request("POST", api, headers=headers, data=rurl)
    proc_chap = chaps_indi.json()
    t = (json.loads(proc_chap["data"]["chapter"]["pages"]))
    r = json.dumps(t)
    o = json.loads(r)
    directory = chapter_number[start_of_chapters]["title"]
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    print('Created Path: ', path)
    page_count = 1
    for attributes, values in o.items():
      current_image = 'https://img.mghubcdn.com/file/imghub/' + values
      print(current_image)
      with open("test.json", "a") as write_file:
        json.dump(current_image, write_file, indent=4)
        write_file.write(", \n")
        download_image = scraper.get(current_image).content
        with open(f"{path}/{page_count}.jpg", "wb+") as f:
          f.write(download_image)
        page_count += 1   
    start_of_chapters +=1

  
  
manga_info(slug, headers)


def manga_popular(headers):
  payload = json.dumps({
  "query": "{latestPopular(x:m01){id,title,slug,image,latestChapter,unauthFile}}"
  })
  popular = scraper.request("POST", api, headers=headers, data=payload).text
  for item in json.loads(popular)['data']['latestPopular']:
    print (item['title'], item['latestChapter'])


manga_download(slug, headers)

  
  



