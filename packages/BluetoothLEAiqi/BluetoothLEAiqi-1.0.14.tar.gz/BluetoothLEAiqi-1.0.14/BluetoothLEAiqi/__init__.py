
import sys
import os
import clr
import time


dll_path = os.path.split(os.path.realpath(__file__))[0]

sys.path.append(str(dll_path))


# install pythonnet
try:
    aiqi_blue = clr.AddReference('AIQI_Bluetooth_LIB')
except:

    print("please add AIQI_Bluetooth_LIB.ddl file ")
    sys.exit()


_aiqi_watcher = None
_aiqi_gatt = None

from enum import Enum
from AIQI_Bluetooth import *

class Connect_result(Enum):
    Connect_Notify_OK = 0
    Connect_Notify_ERR = 1
    Connect_Not_disconnect = 1000
    Connect_Id_null = 1001
    Connect_Unable_reset_notify = 1002
    Connect_Failed_device = 1003
    Connect_Radio_not_on = 1004
    Connect_Get_Char_err = 1005
    Connect_Get_Char_fault = 1006
    Connect_Get_Service_err = 1007

    Connect_Send_OK = 2000
    Connect_Send_Gatt_Err = 2001
    Connect_Send_device_Err = 2002
    Connect_Send_Data_Err = 2003

    Connect_Aiai_Login_OK = 3000
    Connect_Aiai_Login_ERR = 3001


class Connect_Status(Enum):
    Connected_OK = 0
    Disconnect = 1
    Connected_ERR = 0


'''
mesh dev login
'''


def Ble_OneBot_Mesh_Login():
    Onebot_Mesh_Login_1 = "PoW6p99mRQ3yPOhS1dSqnA=="
    Onebot_Mesh_Login_2 = "Am49m1E9XXyNxW2/bjHZaQ=="
    Onebot_Mesh_Login_3 = "cP2qHxIa0nPrxuSildnyKw=="

    Bluetooth_Send(_aiqi_gatt, Onebot_Mesh_Login_1)
    time.sleep(0.2)
    Bluetooth_Send(_aiqi_gatt, Onebot_Mesh_Login_2)
    time.sleep(0.2)
    Bluetooth_Send(_aiqi_gatt, Onebot_Mesh_Login_3)
    time.sleep(0.3)


'''
mibot login

'''


def Ble_Mibot_Login():

    Onebot_Mibot_Login = "78BByM0pzI4R9kcA5G7ra5+JQLL1MoxMMuDxhakTh4qcC86hZGr1GZEIH2+P7FYY"

    time.sleep(0.3)
    Bluetooth_Send(_aiqi_gatt, Onebot_Mibot_Login)


'''
蓝牙数据发送 
参数：要发送的数组

'''


def Bluetooth_Send(gatt, send_buff):
    gatt.Aiqi_Bluetooth_Send(send_buff)


'''
蓝牙扫描控制
true is  scan open
false is scan false
'''


def Bluetooth_Scan_Ctrl(watch, enable):
    watch.Bluetooth_Watch_Enable(enable)


'''
蓝牙断开
参数1 要断开的gatt 实例

'''


def Bluetooth_Disconnect(gatt):
    gatt.Bluetooth_Disconnect()


'''

蓝牙发现初始化
参数 1 蓝牙扫描回调
返回值 蓝牙watcher 实例

'''


def Bluetooth_Watch_Init(watch_handle):
    print(aiqi_blue)
    global _aiqi_watcher

    watch = Bluetooth_watcher()

    watch.Aiqi_ble_wachter_handle += watch_handle

    _aiqi_watcher = watch

    return watch


'''
蓝牙初始化
参数 1 蓝牙连接状态回调
参数 2 蓝牙建立过程回调
参数 3 蓝牙接收数据回调
返回值 gatt 实例
'''


def Bluetooth_Init(ble_stats_handle, create_stats_handle, char_ValueChanged_handle):
    print(aiqi_blue)
    global _aiqi_gatt

    gatt = Bluetooth_gatt_class()
    gatt.Aiqi_Ble_connected_stats_handle += ble_stats_handle
    gatt.Aiqi_Characteristic_ValueChanged_handle += char_ValueChanged_handle
    gatt.Aiqi_Ble_connect_build_stats_handle += create_stats_handle

    _aiqi_gatt = gatt
    return gatt
