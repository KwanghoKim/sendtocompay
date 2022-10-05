#!/home/seralee/.virtualenvs/myenv/bin/python
import os 
import argparse
import time
import datetime
from datetime import date
from datetime import datetime

log_dir = ""
version = "5"

# key :link, value : time
#@@filters = {"hair" : 60, "mask" : 180, "rabbit" : 300, "glasses" : 600, "none" : 60} 
#@@filters = {"hair" : 60, "mask" : 180, "rabbit" : 300, "hair" : 180, "mask" : 300, "rabbit" : 60} 
#@@filters = {"hair" : 300, "mask" : 60, "rabbit" : 180} 
#@@filters = {"hair" : 600, "mask" : 600, "rabbit" : 600} 
##@@filters = {"glasses" : 60, "glasses" : 180, "glasses" : 300, "glasses" : 600} 
#@@filters = {"glasses" : 60, "glasses" : 180} 
#@@filters = {"glasses" : 60} 
#@@filters = {"hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"hair" : 30, "mask" : 30, "rabbit" : 30, "glasses" : 30} 
#@@filters = {"hair" : 120, "mask" : 120, "rabbit" : 120, "glasses" : 120} 
#@@filters = {"hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 
#@@filters = {"hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"hair" : 600, "mask" : 600, "rabbit" : 600, "glasses" : 600} 
#@@filters = {"hair" : 180, "mask" : 180, "rabbit" : 180, "glasses" : 180} 
#@@filters = {"hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 
#@@filters = {"hair" : 120, "mask" : 120, "rabbit" : 120, "glasses" : 120} 
#@@filters = {"hair" : 30, "mask" : 30, "rabbit" : 30, "glasses" : 30} 

#@@filters = {"hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 
#@@filters = {"hair" : 180, "mask" : 180, "rabbit" : 180, "glasses" : 180} 
#@@filters = {"hair" : 120, "mask" : 120, "rabbit" : 120, "glasses" : 120} 
#@@filters = {"none" : 180, "hair" : 180, "mask" : 180, "rabbit" : 180, "glasses" : 180} 
#@@filters = {"glasses" : 180} 
#@@filters = {"none" : 600, "hair" : 600, "mask" : 600, "rabbit" : 600, "glasses" : 600} 
#@@filters = {"none" : 300, "hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"none" : 120, "hair" : 120, "mask" : 120, "rabbit" : 120, "glasses" : 120} 
#@@filters = {"none" : 60, "hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 
#@@filters = {"none" : 30, "hair" : 30, "mask" : 30, "rabbit" : 30, "glasses" : 30} 
#@@filters = {"none" : 600, "hair" : 600, "mask" : 600, "rabbit" : 600, "glasses" : 600} 
#@@filters = {"none" : 300, "hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"none" : 60, "hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 
#@@filters = {"none" : 180, "hair" : 180, "mask" : 180, "rabbit" : 180, "glasses" : 180} 

#@@filters = {"none" : 30, "hair" : 30, "mask" : 30, "rabbit" : 30, "glasses" : 30} 
#@@filters = {"none" : 300, "hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"none" : 600, "hair" : 600, "mask" : 600, "rabbit" : 600, "glasses" : 600} 


#@@filters = {"hair" : 600, "mask" : 600, "rabbit" : 600, "glasses" : 600} 
#@@filters = {"hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"hair" : 180, "mask" : 180, "rabbit" : 180, "glasses" : 180} 
#@@filters = {"hair" : 120, "mask" : 120, "rabbit" : 120, "glasses" : 120} 
#@@filters = {"hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 

filters = {"hair" : 300, "mask" : 300, "rabbit" : 300, "glasses" : 300} 
#@@filters = {"hair" : 600, "mask" : 600, "rabbit" : 600, "glasses" : 600} 
#@@filters = {"hair" : 60, "mask" : 60, "rabbit" : 60, "glasses" : 60} 
#@@filters = {"hair" : 180, "mask" : 180, "rabbit" : 180, "glasses" : 180} 
#@@filters = {"hair" : 120, "mask" : 120, "rabbit" : 120, "glasses" : 120} 

def exec_cmd(cmd):
  print(cmd)
  os.system(cmd)

def measure_perf(package, duration, i, device_id):
  duration = duration
  log_perf_path = f"{perf_log_dir}/{i}/perf.data"
  exec_cmd(f"python simpleperf/app_profiler.py -d {device_id} -p {package} -o {log_perf_path} -r '-e instructions -f 1000 --duration {duration} --call-graph fp'")
  log_output_path = f"{perf_log_dir}/{i}/perf_output"
  exec_cmd(f"python simpleperf/report.py -i {perf_log_dir}/{i}/perf.data> {log_output_path}")

def exec(command):
  global target
  os.system("adb -s " + target + " shell \"" + command +"\"" )

def disable_screen_off():
  exec("settings put system screen_off_timeout 100000000")

def set_system(target, value):
  if(target == "brightness"):
    #0-150
    exec("settings put system screen_brightness " + str(value))
  elif(target== "volume"):
    #range 0 - 25
    exec("input keyevent 24")
    exec("settings put system volume_music_speaker " + str(value))

def big_screen():
  global version
  if(version == "5"):
    exec("input tap 1000 700")
    time.sleep(1)
    exec("input tap 1000 700")
  else:
    exec("input tap 1338 851")
    time.sleep(1)
    exec("input tap 1338 851")

def set_filter(target, value, model):
  if(target == "filter_type"):
    if(model == "pixel_4xl"):
      print("pixel_4xl")
      if(value == "hair"):
        print("hair")
        exec("sleep 0.5 && input tap 320 2766 && sleep 0.5")
      elif(value == "mask"):
        print("mask")
        exec("sleep 0.5 && input tap 507 2761 && sleep 0.5")
      elif(value == "rabbit"):
        print("rabbit")
        exec("sleep 0.5 && input tap 730 2768 && sleep 0.5")
      elif(value == "glasses"):
        print("glasses")
        exec("sleep 0.5 && input tap 924 2778 && sleep 0.5")
      elif(value == "none"):
        print("none")
        exec("sleep 0.5 && sleep 0.5")
    elif(model == "pixel_4a"):
      print("pixel_4a")
      if(value == "hair"):
        print("hair")
        exec("sleep 0.5 && input tap 248 2089 && sleep 0.5")
      elif(value == "mask"):
        print("mask")
        exec("sleep 0.5 && input tap 404 2124 && sleep 0.5")
      elif(value == "rabbit"):
        print("rabbit")
        exec("sleep 0.5 && input tap 579 2123 && sleep 0.5")
      elif(value == "glasses"):
        print("glasses")
        exec("sleep 0.5 && input tap 726 2116 && sleep 0.5")
      elif(value == "thunderglasses"):
        print("thunderglasses")
        exec("sleep 0.5 && input tap 886 2106 && sleep 0.5")
      elif(value == "sunglasses"):
        print("sunglasses")
        exec("sleep 0.5 && input tap 1054 2121 && sleep 0.5")
      elif(value == "none"):
        print("none")
        exec("sleep 0.5 && sleep 0.5")

def set_max_freq(model):
  if(model == "pixel_4xl"):
    exec("ls /sys/devices/system/cpu/cpufreq/")
    exec("echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; echo performance > /sys/devices/system/cpu/cpu4/cpufreq/scaling_governor; echo performance > /sys/devices/system/cpu/cpu7/cpufreq/scaling_governor;")
    exec("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_governor; cat /sys/devices/system/cpu/cpu7/cpufreq/scaling_governor;")
    exec("echo 1785600 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq; echo 1785600 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq; echo 2419200 > /sys/devices/system/cpu/cpu4/cpufreq/scaling_min_freq; echo 2419200 > /sys/devices/system/cpu/cpu4/cpufreq/scaling_max_freq; echo 2841600 > /sys/devices/system/cpu/cpu7/cpufreq/scaling_min_freq; echo 2841600 > /sys/devices/system/cpu/cpu7/cpufreq/scaling_max_freq;")
    exec("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_cur_freq; ")
  elif(model == "pixel_4a"):
    exec("ls /sys/devices/system/cpu/cpufreq/")
    exec("echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; echo performance > /sys/devices/system/cpu/cpu6/cpufreq/scaling_governor;")
    exec("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; cat /sys/devices/system/cpu/cpu6/cpufreq/scaling_governor;")
    exec("echo 1804800 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq; echo 1804800 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq; echo 2208000 > /sys/devices/system/cpu/cpu6/cpufreq/scaling_min_freq; echo 2208000 > /sys/devices/system/cpu/cpu6/cpufreq/scaling_max_freq;")
    exec("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_cur_freq; ")


def set_min_freq(model):
  if(model == "pixel_4xl"):
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
    print("[[[[[[[[[[[[[[[[[[[[[[[[ WARINIG ]]]]]]]]]]]]]]]]]]]]]]")
  elif(model == "pixel_4a"):
    exec("ls /sys/devices/system/cpu/cpufreq/")
    exec("echo powersave > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; echo powersave > /sys/devices/system/cpu/cpu6/cpufreq/scaling_governor;")
    exec("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; cat /sys/devices/system/cpu/cpu6/cpufreq/scaling_governor;")
    exec("echo 300000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq; echo 300000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq; echo 300000 > /sys/devices/system/cpu/cpu6/cpufreq/scaling_min_freq; echo 300000 > /sys/devices/system/cpu/cpu6/cpufreq/scaling_max_freq;")
    exec("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_cur_freq; cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_cur_freq; ")



def quit_newpipe():
  exec("am force-stop org.schabi.newpipe.debug")

def launch_facefilter(model):
  exec("am start -n com.gsrathoreniks.facefilter/com.gsrathoreniks.facefilter.FaceFilterActivity")
  if(model == "pixel_4xl"):
    exec("sleep 5 && input tap 1285 2768 && sleep 1")
  elif(model == "pixel_4a"):
    exec("sleep 5 && input tap 1001 2126 && sleep 1")

def quit_facefilter():
  exec("am force-stop com.gsrathoreniks.facefilter")

def unplug():
  exec("dumpsys battery set ac 0; dumpsys battery set usb 0;");

def plug():
  exec("dumpsys battery set ac 1; dumpsys battery set usb 1;");

def wakeup():
  exec("input keyevent 26;input swipe 500 1000 300 300")

def reset():
  global target
  os.system("adb -s %s logcat -c" % (target))
  os.system("adb -s %s shell dumpsys batterystats --reset" % (target))

def log():
  global target
  os.system("adb -s %s root && adb -s %s shell 'chmod 777 /data/local/tmp' && adb -s %s shell 'setenforce 0' && adb -s %s shell dumpsys batterystats" % (target, target, target, target))

def save(num):
  global log_dir
  global target
#os.system("mkdir -p logs_{target}/{log_dir}/log_{num}")
  
  os.system(f"adb -s {target} pull  /data/local/tmp/log logs_{target}/{log_dir}/log_{num}" )
  os.system(f"adb -s {target} shell dumpsys batterystats > logs_{target}/{log_dir}/log_{num}.txt" )

def save_args(args):
  global log_dir
  global target
  global perf_log_dir

  now = datetime.now()
  log_dir = now.strftime("%m-%d[%H:%M]")
  os.system("mkdir -p logs_%s/%s" %(target, log_dir))
  f = open(f"logs_{target}/{log_dir}/setting","w")
  f.write(str(args))
  f.close()
  os.system(f"adb -s {target} shell settings list system > logs_{target}/{log_dir}/setting_detail")
  os.system(f"adb -s {target} shell dumpsys display | grep 'mScreenState'  >  logs_{target}/{log_dir}/setting_screen")

  #@@
  perf_log_dir = f"logs_{target}/{log_dir}"
  print("perf_log_dir = ", perf_log_dir)



if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Execute the experiment')
  parser.add_argument('--time', '-t', type=int, 
                          help='time to play the video', default=180)

  parser.add_argument('--brightness', '-b', type=int,
      help="brightness 0-250", default=200)

  parser.add_argument('--resolution', '-r', type=int,
      help="resolution", default=720)

  parser.add_argument('--volume', '-v', type=int,
      help="volume", default=5);

  parser.add_argument('--repeat', type=int,
      help="# of repeating", default=200)

  parser.add_argument('--target', type=str,
      help="device uniq string when you command adb devices")

  parser.add_argument('--filter_type', '-f', type=str, 
      help='filter_type', default="hair")

  parser.add_argument('--model', '-m', type=str, 
      help='device_model', default="pixel_4xl")

  args = parser.parse_args()

  target = args.target

  set_system("brightness", 100)
  args.brightness = 100 
  args.volume = 8 

#  print("#!#!#!#!#!")
  for _iter in range(1): 
    print("#!#!#!#!#! iter = ", _iter)
    for filter_type, rand_time in filters.items():
      args.time = rand_time
      args.filter_type = filter_type 
      save_args(args)

      for i in range(5):
        print("#!#!#!#!#! in 2nd for")
        print("_iter=", _iter, "i=", i, "filter_type=", filter_type, "rand_time=", rand_time)
        os.system(f"mkdir -p {perf_log_dir}/{i}")
        disable_screen_off()
        reset()
        unplug()
        quit_facefilter()
        launch_facefilter(args.model)
        time.sleep(2)
        set_filter("filter_type", args.filter_type, args.model)
        #@@ set max freq
#@@        set_max_freq(args.model)
        #@@ set min freq
        set_min_freq(args.model)

        #@@ add simpleperf
        measure_perf("com.gsrathoreniks.facefilter", rand_time, i, target)

        time.sleep(2)
#@@time.sleep(rand_time)
        quit_facefilter()
        plug()
        log()
        save(i)
