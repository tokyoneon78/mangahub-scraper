import cloudscraper
import json
import os
import requests
import time

api = "https://api.mghubcdn.com/graphql"
slug = input("Enter slug:- ")

payload = json.dumps({
  "query": "{manga(x:m01,slug:\""+ slug +"\"){id,rank,title,slug,status,image,latestChapter,author,artist,genres,description,alternativeTitle,mainSlug,isYaoi,isPorn,isSoftPorn,unauthFile,noCoverAd,isLicensed,createdDate,updatedDate,chapters{id,number,title,slug,date}}}"
})
headers = {
  'Content-Type': 'application/json'
}

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)


response = scraper.request("POST", api, headers=headers, data=payload).text

base_data = json.loads(response)
chapter_number = (base_data["data"]["manga"]["chapters"])
l = 0
os.mkdir(slug)
os.chdir(slug)
parent_dir = './'



for x in chapter_number:
  time.sleep(1.0)
  rurl = "{\"query\":\"{chapter(x:m01,slug:\\\"" + base_data["data"]["manga"]["slug"] + "\\\",number:" + str(chapter_number[l]["number"]) + "){pages}}\"}"
  
  chaps_indi = scraper.request("POST", api, headers=headers, data=rurl)
  proc_chap = chaps_indi.json()
  t = (json.loads(proc_chap["data"]["chapter"]["pages"]))
  r = json.dumps(t)
  o = json.loads(r)
  directory = chapter_number[l]["title"]
  path = os.path.join(parent_dir, directory)
  os.mkdir(path)
  print('Created Path: ', path)
  count = 1
  for attributes, values in o.items():
    current_image = 'https://img.mghubcdn.com/file/imghub/' + values
    print(current_image)
    with open("test.json", "a") as write_file:
      json.dump(current_image, write_file, indent=4)
      write_file.write(", \n")
      download_image = requests.get(current_image).content
      with open(f"{path}/{count}", "wb+") as f:
        f.write(download_image)
      count += 1   
  l +=1

  
  




