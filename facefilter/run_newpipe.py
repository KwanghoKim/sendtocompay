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
"""
videos = {"https://www.youtube.com/watch?v=oYnfsg-l0KM" : 60, "https://www.youtube.com/watch?v=o26k0TteJRs" : 180, \
    "https://www.youtube.com/watch?v=NXPsKHqkuEM" : 300, "https://www.youtube.com/watch?v=X_hNZSYz4qE" : 600, \
    "https://www.youtube.com/watch?v=Auw-3xY1waI" : 1200}
videos = {"https://www.youtube.com/watch?v=Auw-3xY1waI" : 1200, "https://www.youtube.com/watch?v=X_hNZSYz4qE" : 600, "https://www.youtube.com/watch?v=NXPsKHqkuEM" : 300}
"""
videos = {"https://www.youtube.com/watch?v=oYnfsg-l0KM" : 60, "https://www.youtube.com/watch?v=o26k0TteJRs" : 180, \
    "https://www.youtube.com/watch?v=NXPsKHqkuEM" : 300, "https://www.youtube.com/watch?v=X_hNZSYz4qE" : 600, \
    "https://www.youtube.com/watch?v=Auw-3xY1waI" : 1200}

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

def set_video(target, value):
  global version
  if(version == "5"):
    if(target == "resolution"):
      if(value == 1080):
        print("hi")
        exec("sleep 0.5 && input tap 770 465 && sleep 0.5 && input tap 730 210 && sleep 0.1 && input tap 750 325")
      if(value == 720):
        exec("sleep 0.5 && input tap 770 465 && sleep 0.5 && input tap 730 210 && sleep 0.1 && input tap 750 460")
      elif(value == 480):
        exec("sleep 0.5 && input tap 770 465 && sleep 0.5 && input tap 730 210 && sleep 0.1 && input tap 750 580")
      elif(value == 360):
        exec("sleep 0.5 && input tap 770 465 && sleep 0.5 && input tap 730 210 && sleep 0.1 && input tap 750 710")
  else:
    if(target == "resolution"):
      if(value == 1080):
        exec("sleep 0.5 && input tap 747 579 && sleep 0.5 && input tap 1017 193 && sleep 0.1 && input tap 1000 326")
      if(value == 720):
        exec("sleep 0.5 && input tap 747 579 && sleep 0.5 && input tap 1017 193 && sleep 0.1 && input tap 1000 466")
      elif(value == 480):
        exec("sleep 0.5 && input tap 747 579 && sleep 0.5 && input tap 1017 193 && sleep 0.1 && input tap 1000 664")
      elif(value == 360):
        exec("sleep 0.5 && input tap 747 579 && sleep 0.5 && input tap 1017 193 && sleep 0.1 && input tap 1000 866")

def launch_newpipe_with_link(link):
  exec("am start -a android.intent.action.VIEW -n org.schabi.newpipe.debug/org.schabi.newpipe.RouterActivity -d  " + link)

def quit_newpipe():
  exec("am force-stop org.schabi.newpipe.debug")

def unplug():
  exec("dumpsys battery set ac 0; dumpsys battery set usb 0;");

def plug():
  exec("dumpsys battery set ac 1; dumpsys battery set usb 1;");

def wakeup():
  exec("input keyevent 26;input swipe 500 1000 300 300")

def reset():
  global target
  os.system("adb -s %s logcat -c" % (target))

def log():
  global target
  os.system("adb -s %s root && adb -s %s shell 'chmod 777 /data/local/tmp' && adb -s %s shell 'setenforce 0' && adb -s %s shell dumpsys batterystats" % (target, target, target, target))

def save(num):
  global log_dir
  global target
  os.system(f"adb -s {target} pull  /data/local/tmp/log logs_{target}/{log_dir}/log_{num}" )

def save_args(args):
  global log_dir
  global target
  now = datetime.now()
  log_dir = now.strftime("%m-%d[%H:%M]")
  os.system("mkdir -p logs_%s/%s" %(target, log_dir))
  f = open(f"logs_{target}/{log_dir}/setting","w")
  f.write(str(args))
  f.close()
  os.system(f"adb -s {target} shell settings list system > logs_{target}/{log_dir}/setting_detail")
  os.system(f"adb -s {target} shell dumpsys display | grep 'mScreenState'  >  logs_{target}/{log_dir}/setting_screen")


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Execute the experiment')
  parser.add_argument('--time', '-t', type=int, 
                          help='time to play the video', default=180)

  parser.add_argument('--video_link', '-l', type=str, 
      help='time to play the video', default="https://www.youtube.com/watch?v=1Ux3tQ_pGQM")
  #kda https://www.youtube.com/watch?v=1Ux3tQ_pGQM
  #news https://www.youtube.com/watch?v=ZqzPGtwKowY
  #classic https://www.youtube.com/watch?v=mjwljR_Bc-A
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

  args = parser.parse_args()

  target = args.target

  #for i in range(8):
  #  set_system("volume", 0)
  set_system("brightness", 100)
  args.brightness = 100 
  args.volume = 8 

  #for rand_volume in range(10):
    #set_system("volume", rand_volume)
    #for rand_brightness in range(30,150,10):
      #set_system("brightness",rand_brightness)
  for _iter in range(3): 
    for video_link, rand_time in videos.items():
      for rand_resolution in [1080, 720, 480, 360]:
        args.time = rand_time
        args.resolution = rand_resolution
        args.video_link = video_link
        save_args(args)

        for i in range(7):
          print(rand_time, rand_resolution, i, args.target)
          disable_screen_off()
          reset()
          unplug()
          quit_newpipe()
          launch_newpipe_with_link(args.video_link)
          time.sleep(2)
          set_video("resolution", args.resolution)
          time.sleep(2)
          big_screen()
          #time.sleep(args.time)
          time.sleep(rand_time)
          quit_newpipe()
          plug()
          log()
          save(i)

  """
  for rand_time in range(600, 3600, 300):
    #for video_link in ["https://www.youtube.com/watch?v=1Ux3tQ_pGQM", "https://www.youtube.com/watch?v=ZqzPGtwKowY","https://www.youtube.com/watch?v=mjwljR_Bc-A"]:
    for video_link in ["https://www.youtube.com/watch?v=mjwljR_Bc-A"]:
    #for video_link in ["https://www.youtube.com/watch?v=1Ux3tQ_pGQM", "https://www.youtube.com/watch?v=ZqzPGtwKowY"]:
      for rand_resolution in [1080,720,480,360]:
        args.time = rand_time
        args.resolution = rand_resolution
        args.video_link = video_link
        save_args(args)

        for i in range(5):
          print(rand_time, rand_resolution, i, args.target)
          disable_screen_off()
          reset()
          unplug()
          launch_newpipe_with_link(args.video_link)
          time.sleep(2)
          set_video("resolution", args.resolution)
          time.sleep(2)
          big_screen()
          #time.sleep(args.time)
          time.sleep(rand_time)
          quit_newpipe()
          plug()
          log()
          save(i)
  """



