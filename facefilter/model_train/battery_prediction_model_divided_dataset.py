import tensorflow as tf
from keras.datasets import boston_housing
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras import optimizers
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer


import numpy as np
import json
import os
import re

#data load

keys = []

target_log_dir = "logs/logs_0B131JEC200794"

class Model:
  def __init__(self):
    np.set_printoptions(suppress=True)
    """
    self.target_categories = ["screen_usagePowerMah", \
        "wifiPowerMah", "cpuPowerMah",\
        "audioPowerMah", "videoPowerMah", "totalPowerMah",\
        "screen_usageTimeMs", "audioTimeMs", "cpuTimeMs",\
        "wifiRunningTimeMs", "videoTimeMs","wifiRxPackets",\
        "wifiTxPackets", "wifiRxBytes",
        "wifiTxBytes"]
    """
    """
    self.target_categories = ["screen_usagePowerMah", \
        "wifiPowerMah", "cpuPowerMah",\
        "audioPowerMah", "videoPowerMah", "totalPowerMah"]
    self.target_categories = ["screen_usageTimeMs", "audioTimeMs", "cpuTimeMs",\
        "wifiRunningTimeMs", "videoTimeMs"]
    """
    self.target_categories = ["wifiRxPackets","wifiTxPackets",\
        "wifiRxBytes", "wifiTxBytes"]


    self.target_parameters = ["time"]


    self.target_categories = ["screen_usagePowerMah", \
        "wifiPowerMah", "cpuPowerMah",\
        "audioPowerMah", "videoPowerMah", "totalPowerMah"]

    self.target_categories = ["screen_usagePowerMah", \
        "wifiPowerMah", "cpuPowerMah",\
        "audioPowerMah", "videoPowerMah", "totalPowerMah"]

    self.target_categories = ["screen_usagePowerMah", \
        "wifiPowerMah", "cpuPowerMah",\
        "audioPowerMah", "videoPowerMah", "totalPowerMah"]


    self.target_categories = ["screen_usagePowerMah", \
        "wifiPowerMah", "cpuPowerMah",\
        "audioPowerMah", "videoPowerMah", "totalPowerMah"]

    #self.target_categories = ["audioTimeMs", "cpuTimeMs", "videoTimeMs", "screen_usageTimeMs", "wifiIdleTimeMs", "wifiRxTimeMs", "wifiTxTimeMs", "wifiRunningTimeMs"]
    self.target_categories = ["audioTimeMs", "cpuTimeMs", "videoTimeMs", "screen_usageTimeMs",  "wifiRunningTimeMs"]
    
  def data_preprocessing(self, data_set):
    total_x_data = [] 
    total_y_data = []
    i = 0
    t_param = 0
    t_cate = 0

    for data in data_set:
      i += 1
      x_data = []
      y_data = []
#@@      print("#!#!#!#!@@@@@@@@@ i=", i)
#@@      print("#!#!#!#!@@@@@@@@@ i=", i, "data=", data)
#@@      print("#!#!#!#!@@@@@@@@@")
      try:
        for target_param in self.target_parameters:
          t_param += 1
#@@          print("#!#!#!#!#!@@@@@@@@@@@@ t_param=", t_param)
          x_data.append(int(data[target_param]))
#@@          print("#!#!#!#!#!@@@@@@@@@@@@ x_data=", x_data)
        for target_category in self.target_categories:
          t_cate += 1
#@@          print("#!#!#!#!#!@@@@@@@@@@@@ t_cate=", t_cate)
#@@          print("#!#!#!#!#!@@@@@@@@@@@ target_category=", target_category)
          if("Ms" in target_category):
            data[target_category] /= 1.0
          elif("Bytes" in target_category):
            data[target_category] /= 1000.0 
          y_data.append(data[target_category])
#@@          print("#!#!#!#!#!@@@@@@@@@@@@ y_data=", y_data)
        total_x_data.append(x_data)
        total_y_data.append(y_data)
#@@        print("#!#!#!#!@@@@@@@@@@@@@ total_x_data=", total_x_data, "total_y_data=", total_y_data)
      except Exception as e:
        #print(e)
        pass

#@@    print("#!#!#!#!@@@@@@@@@@@@@ len(total_x_data)=", len(total_x_data), "len(total_y_data)=", len(total_y_data))
    return np.array(total_x_data).astype(np.float32), np.array(total_y_data).astype(np.float32)




  def set_training_data(self, data_set):
    #pre_processing
    self.x_train, self.y_train = self.data_preprocessing(data_set)
    print("len(self.x_train)=", len(self.x_train), "len(self.y_train)=", len(self.y_train))

  def set_testing_data(self, data_set):
    np.set_printoptions(suppress=True)
    #pre_processing
    self.x_test, self.y_test = self.data_preprocessing(data_set)
    print("len(self.x_test)=", len(self.x_test), "len(self.y_test)=", len(self.y_test))

  def load_training_data(self, target_log_dir):
    self.x_train, self.y_train = self.parse_data_from_dir(target_log_dir)

  def load_testing_data(self,target_log_dir):
    self.x_test, self.y_test = self.parse_data_from_dir(target_log_dir)

  def set_target_result_categories(self, categories, parameters):
    # e.g. totalPowerMah, resolution, time 
    self.categories = categories
    self.target_parameters = parameters
  
  def divide_train_and_test_set(self):
    pass

  def parse_data_from_dir(self, target_log_dir):
    """
    return json data
    """

    total_data = []

    x_data = []
    y_data = []
    #find the log file recursively
    for _dir in os.listdir(target_log_dir):
      for path, directories, files in os.walk(os.path.join(target_log_dir,_dir)):
        #get setting parameter first,
        parameter = []
        data = {}
        log = "log"

        print("#!#!#!#!#! @@@@@@@@ path=", path, "dir=", directories, "files=", files)
        metadata_file = "" 
        #if("99" not in path and "9A" not in path and "9B" not in path ):
        #  continue
        if (os.path.isfile(os.path.join(path,"setting"))):
          metadata_file = "setting"
          setting = open(os.path.join(path, metadata_file)).read()
          log = "log"
          
          for para in list(map(lambda x: x.strip().split("="),setting[10:-1].split(","))):
            data[para[0]] = para[-1]
        elif (os.path.isfile(os.path.join(path,"youtube_info"))):
          metadata_file = "youtube_info"
          setting = open(os.path.join(path, metadata_file)).read()
          splited = setting.strip().split("__")
          data["time"] = splited[0] 
          log = "battery_stats"
        else:
          continue

        """
        **consider when more parameters are needed

        if(os.path.isfile(os.path.join(path,"setting_detail"))):
          detail = open(os.path.join(path,"setting_detail")).read()
          if(detail):
            parameters.pop(-1) # remove previous volume
            setting_detail = re.findall(r'volume_music_speaker=\d+', detail)[0]
                
            volume = float(setting_detail.split("=")[1])
            parameters.append(volume)
        """
        

        for _file in files:
          if(_file.startswith(log)):
            #only consider log files, not setting files
            lines = open(os.path.join(path, _file)).read()
            if(lines[0] != "{"):
              lines = lines[1:]
            for line in lines.split("\n"):
              try:
                json_data = json.loads(str(line).strip("'<>() ").replace('\'', '\"'))

                self.keys = json_data.keys()

                #some data don't have target app power data:(
                if("com.gsrathoreniks.facefilter" in json_data.values()):
                  data = {**data, **json_data}
                if("Screen" in json_data.values()):
                  data["screen_usagePowerMah"] = json_data["usagePowerMah"]
                  data["screen_usageTimeMs"] = json_data["usageTimeMs"]
                if("android.uid.system:1000" in json_data.values()):
                  #system power usage
                  data["system_cpuTimeMs"] = json_data["cpuTimeMs"]
#@@data["system_cpuTimeMs"] = json_data["audioTimeMs"]
                  data["system_audioTimeMs"] = json_data["audioTimeMs"]
                if("WIFI-Estimator" in json_data.values()):
                  data["wifiRunningTimeMs"] = json_data["wifiRunningTimeMs"]




                  """
                  ** selected data later
                  selected_power_data = [float(json_data[key]) for key in json_data.keys() if key not in ["id","package_name"]]

                  x_data.append(parameters)
                  y_data.append(selected_power_data)
                  """
              except Exception as e:
                pass
          total_data.append(data)
    return total_data
    #return np.array(x_data).astype(np.float64), np.array(y_data).astype(np.float64)

  def build_model(self):
    # checkpoint setting
    checkpoint_path = "model_logs/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path, 
        verbose=1, 
        save_weights_only=True,
        period=5)

    self.model = Sequential()
    size_x, size_y = len(self.x_train[0]), len(self.y_train[0])

    # Keras model with two hidden layer with 10 neurons each 
    self.model.add(tf.keras.Input(shape=(size_x)))
    self.model.add(Activation('relu'))
    self.model.add(Dense(32))                         # Hidden layer => only output dimension should be designated
    self.model.add(Activation('relu'))
    self.model.add(Dense(32))                         # Hidden layer => only output dimension should be designated
    self.model.add(Dense(size_y))                          # Output layer => output dimension = 1 since it is regression problem
    self.model.summary()

    
    sgd = tf.keras.optimizers.SGD(lr = 0.01)    # stochastic gradient descent optimizer
    
    checkpoint_dir = "model_logs"
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    #self.model.load_weights(latest)

    self.model.compile(optimizer='adam', loss = 'mse', metrics=['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'cosine_proximity'])
    self.model.save_weights(checkpoint_path.format(epoch=1000))
    self.model.fit(self.x_train, self.y_train, batch_size = 50, epochs = 1000, verbose = 1,callbacks=[cp_callback])


    converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
    tflite_model = converter.convert()
    with open('model.tflite_v1.0', 'wb') as f:
        f.write(tflite_model)



  def apply_data_regularization(self):
    """
    mean = self.y_train.mean(axis= 0)
    self.y_train -= mean
    std = self.y_train.std(axis=0)
    self.y_train/=std
    #self.x_validate -= mean
    #self.x_validate /= std
    self.y_test -= mean
    self.y_test /=std

    """

    mean = self.x_train.mean(axis= 0)
    self.x_train -= mean
    std = self.x_train.std(axis=0)
    self.x_train/=std
    #self.x_validate -= mean
    #self.x_validate /= std
    self.x_test -= mean
    self.x_test /=std

  def eval_model(self):
    results = self.model.evaluate(self.x_test, self.y_test)
    print('loss: ', results[0])
    print('mse: ', results[1])
    pass
  
  def predict_power_per_time(self):
    #predict model
    y_pred = self.model.predict(self.x_test)
    pred_diff = np.abs(y_pred - self.y_test)

    pred_diff_mean = pred_diff.mean(axis=0)
    y_pred_mean = y_pred.mean(axis=0)
    y_test_mean = self.y_test.mean(axis=0)

    print("len(self.x_train)=", len(self.x_train), "len(self.x_test)=", len(self.x_test))
    print("len(self.y_train)=", len(self.y_train), "len(self.y_test)=", len(self.y_test))

    for i in range(len(self.target_categories)):
      diff_per = 0
      diff = abs(y_pred_mean[i] - y_test_mean[i])
      if(y_test_mean[i] != 0):
        diff_per =  diff/ y_test_mean[i] * 100
      print("%s : pred : %0.3f, val : %0.3f, diff : %0.6f(%0.4f %%)" %
          (self.target_categories[i], y_pred_mean[i], y_test_mean[i], diff, diff_per))

  def predict_model(self):
    #predict model
    y_pred = self.model.predict(self.x_test)
    pred_diff = np.abs(y_pred - self.y_test)

    pred_diff_mean = pred_diff.mean(axis=0)
    y_pred_mean = y_pred.mean(axis=0)
    y_test_mean = self.y_test.mean(axis=0)

    print("len(self.x_train)=", len(self.x_train), "len(self.x_test)=", len(self.x_test))
    exit()

    for i in range(len(self.target_categories)):
      diff_per = 0
      diff = abs(y_pred_mean[i] - y_test_mean[i])
      if(y_test_mean[i] != 0):
        diff_per =  diff/ y_test_mean[i] * 100
      print("%s : pred : %0.3f, val : %0.3f, diff : %0.6f(%0.4f %%)" %
          (self.target_categories[i], y_pred_mean[i], y_test_mean[i], diff, diff_per))

  def print_self(self):
    print("len(self.x_train)=", len(self.x_train), "len(self.y_train)=", len(self.y_train))
    print("len(self.x_test)=", len(self.x_test), "len(self.y_test)=", len(self.y_test))

model = Model()
total_data = []
#target_dirs = ["manual_battery_log_newpipe/newpipe_various_videos"]
#target_dirs = ["/home/seralee/Research/Battery/Scripts/logs/manual_battery_log_newpipe/"]
#target_dirs = ["logs_prev/logs_9","logs_prev/logs_99101FFBA006XF", "logs_prev/logs_9A221FFBA0002G", "logs_prev/logs_9B061FFBA000ST"]
#target_dirs = ["logs_9B061FFBA000ST","logs_9A221FFBA0002G", "logs_9", "logs_99101FFBA006XF"]
#@@target_dirs =["logs_9","logs_99101FFBA006XF", "logs_9A221FFBA0002G", "logs_9B061FFBA000ST"]
'''
#@@target_dirs =["logs_0B131JEC200794"]


for target_dir in target_dirs:
  total_data.extend(model.parse_data_from_dir(os.path.join("logs",target_dir)))

"""
train = ["ZqzPGtwKowY'","mjwljR_Bc-A'"]
test = ["1Ux3tQ_pGQM'"]
#train = ["mjwljR_Bc-A'"]
#test = ["1Ux3tQ_pGQM'"]
pair = []

for _data in total_data:
  if(_data["video_link"] in train):
    train_data.append(_data)
  else:
    p = [_data["resolution"], _data["time"]]
    if(p not in pair):
      test_data.append(_data)
      pair.append(p)
"""
train_data = []
test_data = []
print("len(total_data)=", len(total_data))

for idx in range(len(total_data)):
  _data = total_data[idx]
  time = int(total_data[idx]['time'])
  print("time=", time)

  if(idx % 10 == 0):
    test_data.append(total_data[idx])
  else:
    train_data.append(total_data[idx])
'''
###
### new code for dividing dataset ##
###
train_data = []
test_data = []

#@@train_target_dirs =["train_dataset/iu", "train_dataset/kookyohwan", "train_dataset/onebeen"]
#@@train_target_dirs =["train_dataset/onebeen", "train_dataset/iu"]
#@@test_target_dirs =["test_dataset/leejeongjae"]
#@@test_target_dirs =["test_dataset/leejeongjae"]
#@@test_target_dirs =["test_dataset/yunakim"]

#@@train_target_dirs =["train_dataset/iu", "train_dataset/kookyohwan"]
#@@train_target_dirs =["train_dataset/iu", "train_dataset/kookyohwan"]
#@@test_target_dirs =["test_dataset/parkjunghun", "test_dataset/yunakim"]
#@@test_target_dirs =["test_dataset/yunakim"]

#@@train_target_dirs =["train_dataset/yunakim"]
#@@test_target_dirs =["test_dataset/yunakim"]

train_target_dirs =["train_dataset/iu", "train_dataset/kookyohwan"]
test_target_dirs =["test_dataset/parkjunghun"]
#@@test_target_dirs =["test_dataset/onebeen"]
#@@test_target_dirs =["test_dataset/parkjunghum_max_freq/60s", "test_dataset/parkjunghum_max_freq/120s", "test_dataset/parkjunghum_max_freq/180s", "test_dataset/parkjunghum_max_freq/300s", "test_dataset/parkjunghum_max_freq/600s"]
#@@test_target_dirs =["test_dataset/parkjunghun_minfreq/60s", "test_dataset/parkjunghun_minfreq/120s", "test_dataset/parkjunghun_minfreq/180s", "test_dataset/parkjunghun_minfreq/300s", "test_dataset/parkjunghun_minfreq/600s"]

for train_target_dir in train_target_dirs:
  train_data.extend(model.parse_data_from_dir(os.path.join("logs/logs_0B131JEC200794", train_target_dir)))


for test_target_dir in test_target_dirs:
  test_data.extend(model.parse_data_from_dir(os.path.join("logs/logs_0B131JEC200794", test_target_dir)))

print("len(train_data)=", len(train_data), "len(test_data)=", len(test_data))
model.set_training_data(train_data)
model.set_testing_data(test_data)

#model.load_training_data("logs_99101FFBA006XF")
#model.load_testing_data("logs_9A221FFBA0002G")
model.apply_data_regularization()




model.build_model()
#model.eval_model()
model.predict_power_per_time()
model.print_self()
exit()

"""
#for test set
target_log_dir = "test_logs"

for _dir in os.listdir(target_log_dir):
  for path, directories, files in os.walk(os.path.join(target_log_dir,_dir)):
    #get setting parameter first,
    parameter = []
    setting = open(os.path.join(path, "setting")).read()

    parameters = re.findall(r"\d+", setting )

    if(len(parameters) == 8):
      #by the typo
      parameters.pop(0) # remove typo
      parameters.pop(1) # remove repeating
      parameters.pop(3) # remove video link
    elif(len(parameters) == 7):
      parameters.pop(1)
      parameters.pop(3)

    if(os.path.isfile(os.path.join(path,"setting_detail"))):
      parameters.pop(-1) # remove previous volume
      setting_detail = re.findall(r'volume_music_speaker=\d+',open(os.path.join(path,"setting_detail")).read())[0]
          
      volume = int(setting_detail.split("=")[1])
      parameters.append(volume)

    for _file in files:
      if(_file.startswith("log")):
        #only consider log files, not setting files
        data = open(os.path.join(path, _file)).read()[1:]
        for line in data.split("\n"):
          try:
            json_data = json.loads(line)
            keys = json_data.keys()

            #some data don't have target app power data:(
            if("org.schabi.newpipe.debug" in json_data.values()):
              selected_power_data = [json_data[key] for key in json_data.keys() if key not in ["id","package_name"]]

              x_test.append(parameters)
              y_test.append(selected_power_data)
          except Exception as e:
           pass

#divding train/validate/test set

size =  int(len(x_data) * 4 / 5)
x_train = np.array(x_data[:size]).astype(np.float64)
x_validate = np.array(x_data[size+1:]).astype(np.float64)

y_train = np.array(y_data[:size]).astype(np.float64)
y_validate = np.array(y_data[size+1:]).astype(np.float64)

x_test = np.array(x_test).astype(np.float64)
y_test = np.array(y_test).astype(np.float64)

#build model
size_x = len(x_data[0])
size_y = len(y_data[0])


#regularization
mean = x_train.mean(axis= 0)
x_train -= mean
std = x_train.std(axis=0)
x_train/=std
x_validate -= mean
x_validate /= std
x_test -= mean
x_test /=std
"""







