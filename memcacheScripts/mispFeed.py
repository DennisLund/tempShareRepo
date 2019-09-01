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
    mispKey=''
    dataTypes={'domain', 'ip-%'}

    for dt in dataTypes:
      headers={'Authorization':mispKey,'Accept':'application/json','Content-type                                                                                      ':'application/json'}
      data=json.dumps({"returnFormat":"json","type":dt,"tags":"Feed-%","to_ids":                                                                                      "yes","includeEventTags":"yes","includeContext":"yes"})
      try:
        response = requests.post('https://192.168.0.13/attributes/restSearch',he                                                                                      aders=headers,data=data,verify=False)
        data=response.json()
        if(data):
          for item in data["response"]["Attribute"]:
            valueCheck=client.get(item['value'])
            if(valueCheck):
              valuearr=[]
              temparr=[]
              mispvalue='misp-' + item['type']
              valuearr.append(valueCheck)
              valuearr.append(mispvalue)
              for arritem in valuearr:
                if arritem not in temparr:
                  temparr.append(arritem)
              client.set(str(item['value']), temparr, 2100)
            else:
              client.set(str(item['value']), 'misp-' + item['type'], 2100)

      except Exception as e:
        with open('/var/log/misppullLog.txt','a') as file:
          file.write('{0} - mispFeed-script failed with error: {1} \n'.format(st                                                                                      r(time.asctime()), str(e)))


if __name__=='__main__':
  mispToMemcache().run()

