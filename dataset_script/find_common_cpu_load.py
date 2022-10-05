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
target_packages_from_dir = {"cake_50s": "me.mycake","cake_95s": "me.mycake", "cake_150s" : "me.mycake", \
    "youtube_str_120s": "com.google.android.youtube", "youtube_str_60s": "com.google.android.youtube", "youtube_vod_200s" : "com.google.android.youtube", "youtube" : "com.google.android.youtube", "twitch_str_60s": "tv.twitch.android.app", "twitch_str_120s" : "tv.twitch.android.app", "ulike_60s":"com.gorgeous.liteinternational"}


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
        if("Shared Object" in line):
          parsable = True
          continue

        if(parsable):
          new_line = re.sub('\s{2,}','SERA', line).strip()
          splited_line = new_line.split("SERA")
          overhead = splited_line[0]
          comm = splited_line[1]
          shared_object = splited_line[4]
          symbol = splited_line[5]
          overhead = float(overhead.replace("%",""))
          comm = comm.strip().replace(" ","-")
          shared_object = shared_object.strip()
          symbol = symbol.strip().replace(" ","-")
          #symbol = re.sub(r'\[\+[0-9a-f]{4,10}\]'," ", symbol)
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
    symbol = symbols[i].strip()
    num_inst = inst_nums[i]
    model = models[i].split("_")[-1]
    device_id = device_ids[i][:3]
    shared_obj = shared_objs[i].split("/")[-1].strip()
    partition_data = partition_total_data[models[i]]
    iter = iters[i]

    key = f"{device_id}-{iter}"
    total_cnt_per_device_id[key] += num_inst

    if(total_used_num_per_comm[comm]):
      # not empty
      if(key not in total_used_num_per_comm[comm][2]):
        total_used_num_per_comm[comm][0] += 1
        total_used_num_per_comm[comm][2].append(key)
    else:
      total_used_num_per_comm[comm] = [1, 0, [key]]
    total_used_num_per_comm[comm][1] += num_inst




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
    if(cnt > 10):
      print(cnt, comm, sym)

    prev = partition_data[comm][cnt][sym]
    if(prev == 0):
      prev = ""

    partition_data[comm][cnt][sym] = ", ".join(model) 
    partition_data[comm][cnt]["total_inst_num"] += total_inst_num
    
    



def print_partition_data(partition_total_data):
  total_cnt_per_comm_iter = defaultdict(lambda: defaultdict(int)) # key: comm, { key: cnt, value: inst per iter}
  total_cnt_per_comm = defaultdict(int)

  

  total = 0


  for target in partition_total_data.keys():
    partition_data = partition_total_data[target]
    iter_num = iter_num_per_target[target]
    print(f"[*] max iter num {iter_num}, {target}")
    for comm in partition_data.keys():
      #print(f"[*] Command: {comm}")
      for repeated_num in range(2,iter_num):
        #print(f"cnt {repeated_num}")
        for repeated_sym in partition_data[comm][repeated_num].keys():
          sym_ = repeated_sym[:30]
          #print(f"{sym_}[{partition_data[comm][repeated_num][repeated_sym]}]")
        #print("\n")
      for i in partition_data[comm].keys():
        total_cnt_per_comm_iter[comm][i] += partition_data[comm][i]["total_inst_num"]
        total_cnt_per_comm_iter[comm]["total"] += partition_data[comm][i]["total_inst_num"]

        #print(f'cnt {i}: {partition_data[comm][i]["total_inst_num"]}')

  sorted_comm_by_num  = []

  for comm in total_cnt_per_comm_iter.keys():
    sorted_comm_by_num.append([total_cnt_per_comm_iter[comm]["total"],comm])
  
  for inst_num, comm in reversed(sorted(sorted_comm_by_num)):
    freq, inst_num, device_list = total_used_num_per_comm[comm]
    total_inst_num = 0
    for device_id in device_list:
      total_inst_num += total_cnt_per_device_id[device_id]
    portion = round(inst_num / total_inst_num * 100.0,1)
    print(f"[*] Command {comm}, freq of appearance: {freq} ({portion} %)")
    total_cnt = total_cnt_per_comm_iter[comm]["total"]
    keys = list(total_cnt_per_comm_iter[comm].keys())
    keys.remove("total")
    for i in sorted(keys):
      cnt = total_cnt_per_comm_iter[comm][i]
      total += cnt
      total_cnt_per_comm[i] += cnt

      if(total_cnt):
        print(f"[*] cnt {i}: {round(cnt / total_cnt * 100,1)} %")



  print()
  print()
  print("[*] total cnt")
  for i in range(1,iter_num+1):
    cnt = total_cnt_per_comm[i]
    print(f"[*] cnt {i}: {round(cnt / total * 100,1)} %")

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
  iter_num_per_target = defaultdict(int)


  for path, dirs, files in os.walk(target_log_dir):
    if("batterystats" in files):
      device_model, target_app, device_id, iter_num = parse_log_path(path)
      target_package =  target_packages_from_dir[target_app]

      parse_batterystats(f"{path}/batterystats", target_package, parsed_battery_data, device_model)
      parsed_battery_data["device_model"].append(device_model)
      parsed_battery_data["device_id"].append(device_id)
      parsed_battery_data["target_app"].append(target_app)

      target = device_model

      iter_num_per_target[target] += 1


    if("perf_output" in files):
      f = open(f"{path}/perf_output")

      device_model, target_app, device_id, iter_num = parse_log_path(path)
      parse_perf(path, parsed_perf_data, device_model, device_id, iter_num)

      pass

  global total_used_num_per_comm, total_cnt_per_device_id
  total_used_num_per_comm= defaultdict(list) # key: comm, value: [count, inst of comm, list of device_id inst]  for getting portion of specific comm
  total_cnt_per_device_id = defaultdict(int)

  find_common_cpu_load(parsed_perf_data)
  print_partition_data(partition_total_data)
    

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



