#!/usr/bin/env python3
# encoding: utf-8

import requests
from pymemcache.client.base import Client
import time

class ransomwareToMemcache():

  def run(self):

    client = Client(('127.0.0.1', 11211))

    dataTypes={'DOM', 'IP', 'URL'}

    for dt in dataTypes:
      url='https://ransomwaretracker.abuse.ch/downloads/RW_{0}BL.txt'.format(dt)
      rwtvalue='ransomwaretracker-'
      if(dt=='DOM'):
        rwtvalue=rwtvalue + 'domain'
      if(dt=='IP'):
        rwtvalue=rwtvalue + 'ip'
      if(dt=='URL'):
        rwtvalue=rwtvalue + 'url'

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
            tempArr.append(rwtvalue)
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
          file.write('{0} - ransomwareTrackerFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))

if __name__ == '__main__':
  ransomwareToMemcache().run()

