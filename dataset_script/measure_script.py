#!/home/seralee/.virtualenvs/myenv/bin/python
import os 
import argparse
import time
import datetime
from datetime import date
from datetime import datetime

import sys

from bs4 import BeautifulSoup
import heapq


def exec_cmd(cmd):
  print(cmd)
  os.system(cmd)


def exec_via_adb(cmd, target_device_id):
  os.system("adb -s " + target_device_id + " shell \"" + cmd + "\"")

def pull_via_adb(target_device_id, from_file_path, to_file_path):
  os.system("adb -s %s pull %s %s" % (target_device_id, \
      from_file_path, to_file_path))

def log_batterystat(target_device_id, to_file_path):
  os.system("adb -s %s root && adb -s %s shell 'chmod 777 /data/local/tmp' && adb -s %s shell 'setenforce 0' && adb -s %s shell dumpsys batterystats" % (target_device_id, target_device_id, target_device_id, target_device_id))

  pull_via_adb(target_device_id, "/data/local/tmp/log", \
      to_file_path)
def unplug(device_id):
  exec_via_adb("dumpsys battery set ac 0; dumpsys battery set usb 0;", device_id);

def plug(device_id):
  exec_via_adb("dumpsys battery set ac 1; dumpsys battery set usb 1;", device_id);

def measure_batterystat(duration, log_path, target_device_id):
  exec_via_adb("dumpsys batterystats --reset", target_device_id)
  unplug(target_device_id)
  #put what you measure through batterystats
  time.sleep(duration)
  plug(target_device_id)
  log_path = f"{log_path}/batterystats"
  log_batterystat(target_device_id, log_path)


  

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Execute the experiment')
  parser.add_argument('--desc', type=str)
  parser.add_argument('--device_id', type=str, help="device_id")
  parser.add_argument('--duration', type=int, help="duration (sec)")
  parser.add_argument('--repeat', type=int, help="repeatation")
  parser.add_argument('--package_name', type=str, help="name of target pacakage")
  

  args = parser.parse_args()

  repeat = args.repeat
  desc = args.desc
  duration = args.duration
  device_id = args.device_id
  target_package = args.package_name 


  for repeat in range(repeat):
    #set log path
    log_path = f"logs/{desc}/logs_{device_id}/{repeat}"
    exec_cmd(f"mkdir -p {log_path}")

    #measure batterystat
    measure_batterystat(duration, log_path, device_id)

    time.sleep(2)








