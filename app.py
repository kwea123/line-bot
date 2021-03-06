import os
from slackclient import SlackClient
from bs4 import BeautifulSoup as bs
import requests
from flask import Flask, request, make_response, Response
import json
app = Flask(__name__)


@app.route("/", methods=['POST'])
def hello():
    body = request.json
    sc = SlackClient(os.environ['slackbot'])
    e = body['event']
    if e['type'] == 'message' and 'username' not in e:
        if e['text'] == 'beauty':
            text = ""
            r = requests.get("https://www.ptt.cc/bbs/beauty/index.html")
            soup = bs(r.text,"lxml")
            page = soup.find("div", class_="btn-group-paging")
            prev = page.find_all("a")[1]['href'] # previous page
            r = requests.get("https://www.ptt.cc"+prev)
            soup = bs(r.text,"lxml")
            for div in soup.find_all("div", class_="r-ent"):
                a = div.find_all("a")
                if len(a)>0:
                    text += "https://www.ptt.cc"+a[0]['href']+'\n'
            sc.api_call("chat.postMessage",channel=e['channel'],
            text=text)
    return make_response("",200)

if __name__ == '__main__':
   app.run()

