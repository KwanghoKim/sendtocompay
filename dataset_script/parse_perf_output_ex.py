"""
consideration: 10 sec and 10 interations, w/ same scenario 
  - for same scenario, set the automatic UI testing (maybe 

1. get file
2. needed info overhead(%), # of inst, thread command, shared lib, symbol, device_model
3. needed value : mean and std of portion of each symbol
4. variations of inst of funcitons in device and bw devices
"""

import os
#@@import numpy as np
import glob
import argparse
from collections import defaultdict
import json
#@@import matplotlib.pyplot as plt
#@@import pandas as pd
#@@pd.set_option('display.float_format', lambda x: '%.3f' % x)

#@@pd.set_option('display.width', 350)
#@@pd.set_option("display.max_rows", None, "display.max_columns", None)

# parse recored perf output

parsed_value = defaultdict(list)
parsed_batterystats = defaultdict(list)
target_package = "com.gsrathoreniks.facefilter"

target_category = ["cpuPowerMah", "cpuTimeMs"]

def calculate_inst_number(cpu_running_time_per_freq, target_device_model):
  freq_per_device = {"Pixel_4XL":[[300000, 403200, 499200, 576000, 672000, 768000, 844800, 940800, 1036800, 1113600, 1209600, \
      1305600, 1382400, 1478400, 1555200, 1632000, 1708800, 1785600],\
      [710400, 825600, 940800, 1056000, 1171200, 1286400, 1401600, 1497600, 1612800, 1708800, 1804800, 1920000, 2016000\
      , 2131200, 2227200, 2323200, 2419200],\
      [825600, 940800, 1056000, 1171200, 1286400, 1401600, 1497600, 1612800, 1708800, 1804800, 1920000, 2016000, 2131200, 2227200,\
      2323200, 2419200, 2534400, 2649600, 2745600, 2841600]], \
      "Pixel_4a": [[300000, 576000, 768000, 1017600, 1248000, 1324800, 1497600, 1612800, 1708800, 1804800] ,\
      [300000, 652800, 806400, 979200, 1094400, 1209600, 1324800, 1555200, 1708800, 1843200, 1939200, 2169600, 2208000]]\
      }
  power_per_device = {"Pixel_4XL": [[39.44, 41.34, 43.57, 45.48, 47.20, 49.64,\
      51.88, 53.34, 56.69, 58.78, 61.41, 65.11, 67.49, 70.61, 72.39, 75.43, 80.21, 85.05]\
      , [50.35, 55.12, 61.45, 69.92, 77.48, 85.35, 95.17, 103.26, 118.19, 132.72, 143.83, 155.91, 190.16, 213.11, 237.96, 266.97, 302.04]\
      ,[52.70, 55.90, 59.73, 63.66, 67.28, 71.66, 76.47, 80.92, 85.81, 93.19, 98.06, 119.08, 127.88, 129.85, 140.37, 151.22, 160.73, 175.5, 186.29, 223.89]],\
      "Pixel_4a" :[[34.55, 46.57, 54.84, 68.16, 80.70, 86.6, 99.13, 111.05, 119.59, 128.45],\
        [42.23, 56.92, 63.41, 73.03, 80.38, 87.17, 96.55, 125.61, 145.51, 182.94, 198.92, 238.54, 266.21]]\
      }

  freq_per_cluster = freq_per_device[target_device_model]
  power_per_cluster = power_per_device[target_device_model]
  total_cycles = 0
  total_power = 0
  cycles_per_clusters = defaultdict(int)
  time_per_clusters = defaultdict(int)
  
  for i in range(len(cpu_running_time_per_freq)):
    power = power_per_cluster[i]
    cpu_running_time = cpu_running_time_per_freq[i]
    freq_set = freq_per_cluster[i]
    for key in cpu_running_time.keys():
      total_cycles += freq_set[int(key)] * cpu_running_time[key]
      cycles_per_clusters[i] += freq_set[int(key)] * cpu_running_time[key]
      total_power += cpu_running_time[key] * power[int(key)]
      time_per_clusters[i] += cpu_running_time[key]
      
  total_power /= 3600.0
  total_power /= 1000.0
  total_power /= 1000.0
  return total_cycles, cycles_per_clusters, total_power, time_per_clusters 







  


def parse_batterystats(path, target_package, logged_data, target_device_model):
  data = open(path).read()
  if(data[0] != "{"):
    data = data[1:]

  for line in data.split("\n"):
    try:
      json_data = json.loads(line)
      keys = json_data.keys()


      for target_package_name, app_name in [[target_package, "AR"]]:
        if(target_package_name in json_data.values()):
          keys = json_data.keys()
          for key in keys:
            if(key == "cpuUsageJSON"):
              cpuUsageJson = json.loads(json_data[key])
              total_time = 0
              for cluster in cpuUsageJson:
                for key in cluster.keys():
                  total_time += cluster[key]

              total_cycle , cycles_per_cluster, estimated_power, time_per_cluster = calculate_inst_number(cpuUsageJson, target_device_model)
              logged_data["total_cycles"].append(total_cycle)
              logged_data["cycle_on_cluster0"].append(cycles_per_cluster[0])
              logged_data["cycle_on_cluster1"].append(cycles_per_cluster[1])
              logged_data["cycle_on_cluster2"].append(cycles_per_cluster[2])
              logged_data["time_on_cluster0"].append(time_per_cluster[0])
              logged_data["time_on_cluster1"].append(time_per_cluster[1])
              logged_data["time_on_cluster2"].append(time_per_cluster[2])
              logged_data["estimated_power"].append(estimated_power)

            if(key not in target_category):
              continue

            if("Time" in key):
              val = int(json_data[key])
              if(val != 0):
                logged_data[key].append(val)
            if("Power" in key):
              val = round(float(json_data[key]), 3)
              if(val != 0):
                logged_data[key].append(val)
            elif("Bytes" in key):
              val = int(json_data[key])
              if(val != 0):
                logged_data[key].append(val)


    except Exception as e:
      print(e)
      pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Parse the experiment')
  parser.add_argument('--log_dir', type=str, help="target log directory, e.g. twitch_10m")

  args = parser.parse_args()
  target_log_dir = args.log_dir

  total_inst = defaultdict(list)

  for path, dirs, files in os.walk(target_log_dir):
    if("perf_output" in files):

      f = open(f"{path}/perf_output")

      target_app = path.split("/")[2]
      target_device_model = "Pixel_4XL"

      if("Pixel_4a" in path):
        target_device_model= "Pixel_4a"


      #parse_batterystats(f"{path}/batterystats", target_package, parsed_batterystats, target_device_model)

      parsable = False
      inst = 0

      for line in f.readlines():
        if("Event count" in line):
          total_inst = int(line.strip().split()[-1])
        if("Shared Object" in line):
          parsable = True
          continue

        if(parsable):
          values = line.split()
          overhead = float(values[0][:-1])
          comm = values[1]
          shared_object = values[4]
          symbol = values[5]
          device_model = target_device_model

          if(overhead > 0.1):
            parsed_value["overhead"].append(overhead)
            parsed_value["comm"].append(comm)
            parsed_value["shared_object"].append(shared_object)
            parsed_value["symbol"].append(symbol)
            parsed_value["device_model"].append(device_model)
            parsed_value["total_inst"].append(total_inst*float(overhead)/100)
            parsed_value["target_app"].append(target_app)

#@@pv = pd.DataFrame(parsed_value)
  #group by app and then, by device etc
#@@grouped_pv = pv.groupby(["target_app","device_model","comm"]).agg(['mean','std']).sort_values(by=["target_app","device_model","comm",("overhead","mean")], ascending=False)
#@@print(grouped_pv)






