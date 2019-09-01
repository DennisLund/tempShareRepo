#!/usr/bin/env python3
# encoding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
import json
import time

class mispToMemcache():

  def run(self):

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    client = Client(('127.0.0.1', 11211))
    mispKey='<MISP API-KEY>'
    dataTypes={'domain', 'ip-%'}

    for dt in dataTypes:
      headers={'Authorization':mispKey,'Accept':'application/json','Content-type':'application/json'}
      data=json.dumps({"returnFormat":"json","type":dt,"tags":"Feed-%","to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})
      try:
        response = requests.post('https://192.168.0.13/attributes/restSearch',headers=headers,data=data,verify=False)
        data=response.json()
        if data:
          for item in data["response"]["Attribute"]:
            client.set(str('misp-' + item['type'] + '-' + item['value']), 'misp-' + item['type'], 150)

      except Exception as e:
        with open('/var/log/misppullLog.txt','a') as file:
          file.write('{0} - mispFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))


if __name__=='__main__':
  mispToMemcache().run()
