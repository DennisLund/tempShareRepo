#!/usr/bin/env python3
# encoding: utf-8

import time
import os
import traceback
import importlib


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


if __name__ == '__main__':
  path='/opt/scripts/memcacheScripts/'
  run_indefinitely = True
  while run_indefinitely:
    currentfile='not set'
    try:
      for entry in os.listdir(path):
        currentfile=path+entry
        execfile(currentfile)
        with open('/var/log/misppullLog.txt','a') as logfile:
          logfile.write('{0} - Executing {1} \n'.format(time.asctime(), entry))

    except Exception as e:
      with open('/var/log/misppullLog.txt','a') as file:
        file.write('{0} - {1} failed with error: {2} \n'.format(str(time.asctime()), currentfile, str(traceback.format_exc())))
    time.sleep(60)
