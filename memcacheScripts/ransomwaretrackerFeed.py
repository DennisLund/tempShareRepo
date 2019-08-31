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
      try:
        response=requests.get(url)
        if(response):
          for line in response.text.splitlines():
            if(line.startswith('#') == False):
              if(dt=='DOM'):
                client.set(str('ransomwaretracker-domain-' + line),'ransomwaretracker-domain', 150)
              if(dt=='IP'):
                client.set(str('ransomwaretracker-ip-' + line),'ransomwaretracker-ip', 150)
              if(dt=='URL'):
                client.set('ransomwaretracker-url-' + str(line),'ransomwaretracker-url', 150)
      except Exception as e:
        with open('/var/log/misppullLog.txt','a') as file:
          file.write('{0} - ransomwareTrackerFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))


if __name__ == '__main__':
  ransomwareToMemcache().run()
