from scrap import ScrapBlogs
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
import io
import os
import json
import datetime
from deta import app


load_dotenv(find_dotenv())


urls = os.environ.get("URL")
api_url = os.environ.get("APIURL")
project_key = os.environ.get("PROJECTKEY")
current_date = datetime.datetime.now()
folder_date=current_date.strftime("%x")
new_folder_date=folder_date.replace("/", "_")


urls = ScrapBlogs(urls)

@app.lib.run(action="blogs")
@app.lib.cron()
def blogs_scrap(event):

    try:

        for url in urls:

            scrap_url = f"https://medium.com{url}"
            find_name=re.findall('\w+', url)
            name_list = [x for x in find_name if x.isalpha()]
            file_name="_".join(name_list)
            response = requests.get(scrap_url).text.encode('utf8').decode('ascii', 'ignore')
            soup = BeautifulSoup(response, 'html.parser')
            find_section = soup.find("section")
            title = soup.find("h1")

            data = {
                "title":title.text,
                "tags":["programming"],
                "body":str(find_section),
            }

            if find_section is None:
                continue
            else:
                response = requests.post(api_url, json=data)
                if response.status_code =="400":
                    continue
                
        return "Scrapped Successfully"


    except Exception as e:
        print(e)
