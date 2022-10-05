import os
import numpy as np
import glob
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.width', 350)
pd.set_option("display.max_rows", None, "display.max_columns", None)

#power
target_categories = ['screenPowerMah',\
    'wifiPowerMah', 'cpuPowerMah',\
    'audioPowerMah','videoPowerMah',\
    'gpsPowerMah', 'sensorPowerMah',\
    'mobileRadioPowerMah', 'wakeLockPowerMah',\
    'cameraPowerMah', 'flashlightPowerMah',\
    'bluetoothPowerMah',\
    'totalPowerMah']

noise_time = []


# get log dir list
#@@target_log_dir = "logs/manual_battery_logs/" 

target_log_dir = "logs/perf_vari_apps_test/youtube_kkh2/Pixel_4a/logs_0B131JEC200794/0/"


def get_power_info(path, target_package_app_name):
  data = open(path).read()
  if(data[0] != "{"):
    data = data[1:]

  power_info = defaultdict(float)
  target_package_name, target_app = target_package_app_name

  for line in data.split("\n"):
    try:
      json_data = json.loads(line)
      keys = json_data.keys()


      for target_package_name, app_name in [target_package_app_name, \
          ["Screen", "screen"], ["WIFI", "wifi"], ["android.uid.system:1000",target_app], ["android.uid.systemui:10104",target_app], ["Bluetooth", target_app]]:
        if(target_package_name in json_data.values()):
          keys = json_data.keys()
          for key in keys:
            if(key not in target_categories):
              if not (key == "totalPowerMah" and app_name == "screen"):
                continue
            key_ = f"{app_name}_{key}"
            val = json_data[key]
            if("Time" in key):
              val = int(json_data[key])
            elif("Power" in key):
              val = round(float(json_data[key]), 3)
            elif("Ms" in key):
              val = int(json_data[key])

            if(key == "totalPowerMah" and app_name == "screen"):
              power_info[f"{target_app}_screenPowerMah"] += val 
              power_info[f"{target_app}_totalPowerMah"] += val 
            else:
              power_info[key_] += val

    except Exception as e:
      pass

  return ret 



#get various apps
target_apps = os.listdir(target_log_dir)

#for dataframe
total_power_infos = []

for path, dirs, files in os.walk(target_log_dir):
  if("batterystats" in files):
    splited_path = path.split("/")
    target_app = splited_path[-4]
    splited_scenario = splited_path[-3].split("_")
    scenario = "_".join(splited_scenario[:-1]) + "\n" + splited_scenario[-1]

    power_info = get_power_info(f"{path}/batterystats", [package_name_pairs[target_app], target_app])
    power_info["target_app"] = target_app
    power_info["scenario"] = scenario

    total_power_infos.append(power_info)

df = pd.DataFrame(total_power_infos)

