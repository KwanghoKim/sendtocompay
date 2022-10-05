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

"""
duration, start & end point
two mode: measure number of instructions w/ perf and cpu consumpted power using batterystats


assume that: app already launched
"""

def exec_cmd(cmd):
  print(cmd)
  os.system(cmd)

def measure_perf(package, duration, log_path, device_id):
  duration = duration
  log_perf_path = f"{log_path}/perf.data"
  exec_cmd(f"python simpleperf/app_profiler.py -d {device_id} -p {package} -o {log_perf_path} -r '-e instructions -f 1000 --duration {duration} --call-graph fp'")
  log_output_path = f"{log_path}/perf_output"
  exec_cmd(f"python simpleperf/report.py -i {log_path}/perf.data> {log_output_path}")

def exec_via_adb(cmd, target_device_id):
  os.system("adb -s " + target_device_id + " shell \"" + cmd + "\"")

def pull_via_adb(target_device_id, from_file_path, to_file_path):
  os.system("adb -s %s pull %s %s" % (target_device_id, \
      from_file_path, to_file_path))

def log_batterystat(target_device_id, log_path):
#  os.system("adb -s %s root && adb -s %s shell 'chmod 777 /data/local/tmp' && adb -s %s shell 'setenforce 0' && adb -s %s shell 'dumpsys batterystats' > {battery_log_path}" % (target_device_id, target_device_id, target_device_id, target_device_id))
  
#  print("#!#!#!#!#! battery_log_path = ???????????????")
  battery_log_path = f"{log_path}/batterystats.txt"
#  print(battery_log_path)

  os.system("adb -s %s root && adb -s %s shell 'chmod 777 /data/local/tmp' && adb -s %s shell 'setenforce 0'" % (target_device_id, target_device_id, target_device_id))
  os.system(f"adb -s %s shell 'dumpsys batterystats' > {battery_log_path}" % (target_device_id))

  to_file_path = f"{log_path}/batterystats"
  pull_via_adb(target_device_id, "/data/local/tmp/log", \
      to_file_path)

def unplug(device_id):
  exec_via_adb("dumpsys battery set ac 0; dumpsys battery set usb 0;", device_id);

def disable_screen_off(target_device_id):
  exec_via_adb("settings put system screen_off_timeout 100000000", target_device_id)
def plug(device_id):
  exec_via_adb("dumpsys battery set ac 1; dumpsys battery set usb 1;", device_id);

def measure_batterystat(duration, log_path, target_device_id):
  exec_via_adb("dumpsys batterystats --reset", target_device_id)
  unplug(target_device_id)
  time.sleep(duration)
  plug(target_device_id)
  log_path = f"{log_path}/batterystats"
  log_batterystat(target_device_id, log_path)


  

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Execute the experiment')
  parser.add_argument('--desc', type=str)
  parser.add_argument('--device_id', type=str, help="device_id")
  parser.add_argument('--device_model', type=str, help="(Pixel_4a|Pixel_4XL)")
  parser.add_argument('--duration', type=int, help="duration (sec)")
  parser.add_argument('--repeat', type=int, help="repeatation")
  parser.add_argument('--mode', type=str, help="perf|batterystats|both")
  parser.add_argument('--package_name', type=str, help="name of target pacakage")
  

  args = parser.parse_args()

  repeat = args.repeat
  desc = args.desc
  duration = args.duration
  device_id = args.device_id
  device_model = args.device_model
  target_package = args.package_name 
  mode = args.mode


  for repeat in range(repeat):
    #set log path
    log_path = f"logs/{desc}/{device_model}/logs_{device_id}/{repeat}"
    battery_log_path = f"{repeat}/batterystats.txt"
    exec_cmd(f"mkdir -p {log_path}")
    disable_screen_off(device_id)

    if(mode == "p"):
      # measure perf 
      measure_perf(target_package, duration, log_path, device_id)
    elif(mode == "b"):
      #measure batterystat
      measure_batterystat(duration, log_path, device_id)
    elif(mode == "both"):
      target_device_id = device_id
      exec_via_adb("dumpsys batterystats --reset", target_device_id)
      unplug(target_device_id)
      measure_perf(target_package, duration, log_path, device_id)
      plug(target_device_id)
#@@ log_path = f"{log_path}/batterystats"
      print("#!#!#!#!#!#! start @@@@@@@@@@@@@@@@@@@@@@@")
      log_batterystat(target_device_id, log_path)
      print("#!#!#!#!#!#! start @@@@@@@@@@@@@@@@@@@@@@@")
    time.sleep(1)

    #time.sleep(2)








