from requests_oauthlib import OAuth1Session
from datetime import datetime

import json, codecs
import os
import sys
import urllib

import settings

now = datetime.now()
twitter = OAuth1Session(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

params = {'count':199,'result_type' : 'recent','q': '飯テロ filter:images'}
req = twitter.get("https://api.twitter.com/1.1/search/tweets.json", params = params)

timeline = json.loads(req.text)

# タイムラインを保存
f = codecs.open("data/"+now.strftime("%Y_%m%d_%H%M%S")+".json", "w", "utf-8")
json.dump(timeline, f, ensure_ascii=False, indent=2)

# 画像の取得
for tweet in timeline["statuses"]:
	try:
		image_list = tweet["extended_entities"]["media"]
		for image_dict in image_list:
			url = image_dict["media_url"]
			url_large = url + ":large"
			image_name = "./data/img/"+os.path.basename(url)
			with open(image_name, 'wb') as f:
				img = urllib.request.urlopen(url_large, timeout=5).read()
				f.write(img)
			print("<Success> "+image_name)
	except KeyError:
		print("<Failed> KeyError")
	except:
		print("<Warning> Error")

