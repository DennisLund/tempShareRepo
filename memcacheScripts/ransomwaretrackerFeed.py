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
          for line in response.text.splitlines():
            if(line.startswith('#') == False):
              valueCheck=client.get(str(line))
              if(valueCheck):
                valuearr=[]
                temparr=[]
                valuearr.append(valueCheck)
                valuearr.append(rwtvalue)
                for item in valuearr:
                  if item not in temparr:
                    temparr.append(item)
                client.set(str(line),temparr, 2100)
              else:
                client.set(str(line),rwtvalue, 2100)

      except Exception as e:
        with open('/var/log/misppullLog.txt','a') as file:
          file.write('{0} - ransomwareTrackerFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))


if __name__ == '__main__':
  ransomwareToMemcache().run()


