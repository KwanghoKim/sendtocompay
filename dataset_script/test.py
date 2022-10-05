import os 
import argparse
import time
import datetime
from datetime import date
from datetime import datetime

import sys

#from bs4 import BeautifulSoup
import heapq

def exec_cmd(cmd):
  print(cmd)
  os.system(cmd)


if __name__ == '__main__':

#  parser = argparse.ArgumentParser(description='Execute the experiment')
#  parser.add_argument('--desc', type=str)
#  parser.add_argument('--device_id', type=str, help="device_id")
#  parser.add_argument('--device_model', type=str, help="(Pixel_4a|Pixel_4XL)")
#  parser.add_argument('--duration', type=int, help="duration (sec)")
#  parser.add_argument('--repeat', type=int, help="repeatation")
#  parser.add_argument('--package_name', type=str, help="name of target pacakage")
  

#  args = parser.parse_args()

#  repeat = args.repeat
#  desc = args.desc
#  duration = args.duration
#  device_id = args.device_id
#  device_model = args.device_model
#  target_package = args.package_name 

  exec_cmd("adb devices")
#  log_path = f"logs/{desc}/{device_model}/logs_{device_id}/{repeat}"
#  exec_cmd(f"mkdir -p {log_path}")


  exec_cmd("adb root && adb shell 'chmod 777 /data/local/tmp' && adb shell 'setenforce 0' && adb shell 'dumpsys batterystats'")
  print('########################## start ')
  exec_cmd("adb shell 'dumpsys batterystats --reset' && adb shell 'dumpsys battery set ac 0' && adb shell 'dumpsys battery set usb 0';")
