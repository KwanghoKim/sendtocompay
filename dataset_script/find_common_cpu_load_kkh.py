import os
import numpy as np
import glob
import argparse
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import pandas as pd
import re
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

pd.set_option('display.width', 550)
"""
parse log path

"""
target_packages_from_dir = {"cake_50s": "me.mycake","cake_95s": "me.mycake", "cake_150s" : "me.mycake", "cake" : "me.mycake",\
    "youtube_str_120s": "com.google.android.youtube", "youtube_str_60s": "com.google.android.youtube", "youtube_vod_200s" : "com.google.android.youtube", "youtube" : "com.google.android.youtube", "twitch_str_60s": "tv.twitch.android.app", "twitch_str_120s" : "tv.twitch.android.app", "twitch_kk" : "tv.twitch.android.app" , "ulike_60s":"com.gorgeous.liteinternational", "zoom" : "us.zoom.videomeetings"}


def parse_batterystats(path, target_package, logged_data, target_device_model):
  data = open(path).read()
  if(data[0] != "{"):
    data = data[1:]

  for line in data.split("\n"):
    try:
      json_data = json.loads(line)
      keys = json_data.keys()
      target_category = ["cpuPowerMah","cpuTimeMs"]


      for target_package_name, app_name in [[target_package, "ar"]]:
        if(target_package_name in json_data.values()):
          keys = json_data.keys()
          for key in keys:
            if(key == "cpuusagejson"):
              cpuusagejson = json.loads(json_data[key])
              total_time = 0
              for cluster in cpuusagejson:
                for key in cluster.keys():
                  total_time += cluster[key]

              total_cycle , cycles_per_cluster, estimated_power, time_per_cluster = calculate_inst_number(cpuusagejson, target_device_model)
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
      #print(e)
      pass

def parse_perf(path, parsed_value, target_device_model, device_id, iter_num):
      f = open(f"{path}/perf_output")

      parsable = False
      inst = 0

      #set filter

      #denied_list = [".cfi", "try_to_wake", "el0_svc_naked","art_jni_trampoline", "__memcpy","split_config.arm64_v8a.apk"] zoom
      denied_list = ["com.google.android.apps.meetings", ".cfi","__wake_up_common_lock","try_to_wake"] 
      denied_list = [] 

      for line in f.readlines():
        if("Event count" in line):
          total_inst = int(line.strip().split()[-1])
          print("#!#!#!#!#!")
          print(total_inst)
        if("Shared Object" in line):
          parsable = True
          continue

        if(parsable):
          overhead = float(line[0:10].strip().replace("%",""))
          comm = line[10:27].strip().replace(" ","-")
          shared_object = line[41:134].strip()
          symbol = line[133:-1].strip().replace(" ","-")
          symbol = re.sub(r'\[\+[0-9a-f]{4,10}\]'," ", symbol)
          device_model = target_device_model

          flag_overhead = float(overhead) > 0.1
          flag_overhead = True

          flag = True
          for d in denied_list:
            flag = flag and (d not in symbol)

          denied_comm  = []
          for d in denied_comm:
            flag = flag and (d not in comm)

          if(flag and flag_overhead):
            parsed_value["overhead"].append(overhead)
            parsed_value["iter"].append(iter_num)
            parsed_value["comm"].append(f"{comm}")
            #parsed_value["comm"].append(f"{comm}-{iter_num}")
            parsed_value["shared_object"].append(shared_object)
            parsed_value["symbol"].append(symbol)
            parsed_value["device_model"].append(device_model)
            parsed_value["total_inst"].append(int(total_inst*float(overhead)/100))
            parsed_value["target_app"].append(target_app)
            parsed_value["device_id"].append(device_id)


def find_common_cpu_load(parsed_data):
  """
    GOAL: find common CPU load

    def of common CPU load : the set of functions running on multiple devices in a scenario

  """

  hashmap_cnts = defaultdict(list)

  cnt_per_comm_each_device = defaultdict(lambda: defaultdict(int))

  total_cnt = len(parsed_data[list(parsed_data.keys())[0]])

  comms = parsed_data["comm"]
  symbols = parsed_data["symbol"]
  inst_nums = parsed_data["total_inst"]
  device_ids = parsed_data["device_id"]
  iters = parsed_data["iter"]
  shared_objs = parsed_data["shared_object"]

  models = parsed_data["device_model"]
  

  for i in range(total_cnt):
    comm = comms[i]
    symbol = symbols[i]
    num_inst = inst_nums[i]
    model = models[i].split("_")[-1]
    device_id = device_ids[i][:3]
    shared_obj = shared_objs[i].split("/")[-1]
    partition_data = partition_total_data[models[i]]
    iter = iters[i]

    key = f"{comm}||{symbol}-{shared_obj}"
    if(num_inst == 0):
      continue

    if( key not in hashmap_cnts):
      hashmap_cnts[key] = [num_inst, 1, [f"{device_id}-{iter}[{model}]"]]
    else:
      hashmap_cnts[key][0] += num_inst
      hashmap_cnts[key][1] += 1
      hashmap_cnts[key][2].append(f"{device_id}-{iter}[{model}]")



  for key in hashmap_cnts.keys():
    comm, sym = key.split("||")

    total_inst_num, cnt, model = hashmap_cnts[key]

    prev = partition_data[comm][cnt][sym]
    if(prev == 0):
      prev = ""

    partition_data[comm][cnt][sym] = ", ".join(model) 
    partition_data[comm][cnt]["total_inst_num"] += total_inst_num
    



def print_partition_data(partition_data):

  for comm in partition_data.keys():
    #print(f"[*] Command: {comm}")
    for c in range(2,10):
      #print(f"cnt {c}")
      for sym in partition_data[comm][c].keys():
        sym_ = sym
        if(len(sym) >= 30):
          sym_ = sym[:30]
        #print(f"{sym_}[{partition_data[comm][c][sym]}]")
      #print("\n")
    for i in range(10):
      i += 1
      total_cnt_per_comm_cnt[comm][i] += partition_data[comm][i]["total_inst_num"]
      total_cnt_per_comm_cnt[comm]["total"] += partition_data[comm][i]["total_inst_num"]
      #print(f'cnt {i}: {partition_data[comm][i]["total_inst_num"]}')


def parse_log_path(path):
  splited_path = path.split("/")

  target_app = splited_path[2]
  iter_num = splited_path[-1]
  device_id , device_model = None, None


  for dir_name in splited_path:
    if("Pixel" in dir_name):
      device_model = dir_name
    elif("logs_" in dir_name):
      device_id = dir_name.replace("logs_", "")

  return device_model, target_app, device_id, iter_num

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Parse the perf and batterystats data')

  #TODO: muti_data
  parser.add_argument('--log_dir', type=str, help="target log directory, e.g. twitch_10m")

  args = parser.parse_args()
  target_log_dir = args.log_dir

  parsed_battery_data = defaultdict(list)
  parsed_perf_data = defaultdict(list)

  partition_total_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

  for path, dirs, files in os.walk(target_log_dir):
    if("batterystats" in files):
      device_model, target_app, device_id, iter_num = parse_log_path(path)
      target_package =  target_packages_from_dir[target_app]

      parse_batterystats(f"{path}/batterystats", target_package, parsed_battery_data, device_model)
      parsed_battery_data["device_model"].append(device_model)
      parsed_battery_data["device_id"].append(device_id)
      parsed_battery_data["target_app"].append(target_app)


    if("perf_output" in files):
      f = open(f"{path}/perf_output")

      device_model, target_app, device_id, iter_num = parse_log_path(path)
      parse_perf(path, parsed_perf_data, device_model, device_id, iter_num)

      pass

  find_common_cpu_load(parsed_perf_data)
  total_cnt_per_comm_cnt = defaultdict(lambda: defaultdict(int))
  total_cnt_per_comm = defaultdict(int)
  

  total = 0

  for device_model in partition_total_data.keys():
    print_partition_data(partition_total_data[device_model])

  for comm in total_cnt_per_comm_cnt.keys():
    print(f"[*] Command {comm}")
    total_cnt = total_cnt_per_comm_cnt[comm]["total"]
    for i in range(1,11):
      cnt = total_cnt_per_comm_cnt[comm][i]
      total += cnt
      total_cnt_per_comm[i] += cnt

      if(total_cnt):
        print(f"[*] cnt {i}: {round(cnt / total_cnt * 100,1)} %")


  print("[*] total cnt")
  for i in range(1,11):
    cnt = total_cnt_per_comm[i]
    print(f"[*] cnt {i}: {round(cnt / total * 100,1)} %")
    

  pv = pd.DataFrame(parsed_battery_data)
  grouped_pv = pv.groupby(["target_app","device_model","device_id"]).agg(['mean','std']).sort_values(by=["target_app","device_model",("cpuPowerMah","mean")], ascending=False)
  print(grouped_pv)
  print("=============================================================================================================")


  pv = pd.DataFrame(parsed_perf_data)
  grouped_pv = pv.groupby(["target_app","device_model","device_id","comm"])['overhead','total_inst'].agg(['sum','std']).sort_values(by=["target_app", ("total_inst","sum"),"comm","device_model","comm"], ascending=False)
  print(grouped_pv)
  for key, grouped in grouped_pv:
    print(key)
  exit()



