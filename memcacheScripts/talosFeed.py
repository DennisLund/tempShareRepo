#!/usr/bin/env python3
# encoding: utf-8

import requests
from pymemcache.client.base import Client
import time

class talosToMemcache():

  def run(self):

    client = Client(('127.0.0.1', 11211))
    url='https://talosintelligence.com/documents/ip-blacklist'
    talosvalue='talos-ip'

    try:
      response=requests.get(url)
      if(response):
        responseArr=[]
        for line in response.text.splitlines():
          if(line.startswith('#') == False):
            responseArr.append(line)
        valueCheck=client.get_many(responseArr)
        for k in responseArr:
          valueArr=[]
          tempArr=[]
          tempArr.append(talosvalue)
          if k in valueCheck:
            val=valueCheck[k].decode()
            for key in val:
              valueArr.append(key)
            for item in valueArr:
              if item not in tempArr:
                tempArr.append(item)
          client.set(k,tempArr, 300)

    except Exception as e:
      with open('/var/log/misppullLog.txt','a') as file:
        file.write('{0} - talosFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))

if __name__ == '__main__':
  talosToMemcache().run()
