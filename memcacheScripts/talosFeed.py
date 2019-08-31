#!/usr/bin/env python3
# encoding: utf-8

import requests
from pymemcache.client.base import Client
import time

class talosToMemcache():

  def run(self):

    client = Client(('127.0.0.1', 11211))
    url='https://talosintelligence.com/documents/ip-blacklist'

    try:
      response=requests.get(url)
      if(response):
        for line in response.text.splitlines():
          client.set(str('talos-ip-' + line),'talos-ip', 150)

    except Exception as e:
      with open('/var/log/misppullLog.txt','a') as file:
        file.write('{0} - talosFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))

if __name__ == '__main__':
  talosToMemcache().run()
