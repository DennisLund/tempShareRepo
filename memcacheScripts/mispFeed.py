#!/usr/bin/env python3
# encoding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
import json
import time

class mispToMemcache():

  def stringHelper(inputVar):
    testVar=list(inputVar.split(','))
    outVar=[]
    for i in testVar:
      outVar.append(i.translate({ord(k): None for k in "'[]{} "}))

    return outVar


  def run(self):

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    client = Client(('127.0.0.1', 11211))
    mispKey='<MISP-API-KEY>'
    dataTypes={'domain', 'ip-%'}
    mispAddress='192.168.0.13'

    for dt in dataTypes:
      mispvalue='misp-'
      if(dt=='domain'):
        mispvalue=mispvalue + 'domain'
      if(dt=='ip-%'):
        mispvalue=mispvalue + 'ip'

      headers={'Authorization':mispKey,'Accept':'application/json','Content-type':'application/json'}
      data=json.dumps({"returnFormat":"json","type":dt,"tags":"Feed-%","to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})

      try:
        response = requests.post('https://{0}/attributes/restSearch'.format(mispAddress),headers=headers,data=data,verify=False)
        data=response.json()
        if(data):
          responseArr=[]
          for item in data["response"]["Attribute"]:
            responseArr.append(item['value'])

          valueCheck=client.get_many(responseArr)
          for k in responseArr:
            valueArr=[]
            tempArr=[]
            tempArr.append(mispvalue)
            if k in valueCheck:
              val=valueCheck[k].decode()
              valueArr=mispToMemcache.stringHelper(val)
              for item in valueArr:
                if item not in tempArr:
                  tempArr.append(item)
            client.set(k,tempArr, 300)

      except Exception as e:
        with open('/var/log/misppullLog.txt','a') as file:
          file.write('{0} - mispFeed-script failed with error: {1} \n'.format(str(time.asctime()), str(e)))


if __name__=='__main__':
  mispToMemcache().run()

