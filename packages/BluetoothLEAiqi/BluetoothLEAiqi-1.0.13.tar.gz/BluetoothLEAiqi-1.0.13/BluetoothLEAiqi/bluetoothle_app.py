import time

import BluetoothLEAiqi

'''
蓝牙相关变量

'''
blue_watcher = None
blue_gatt = None
# 要连接的设备mac
mydev = "E8F4F3395CBD"
connectid = mydev
ble_connect_mode = None
ble_connect_mode_name = None
ble_connect_mode_mac = None
ble_value_change_handle = None
ble_connect_stats_handle = None

log_title = "bluetoothle_app:"

'''
建立连接  状态回调

'''


def Ble_connect_create_handle(sender, stats):
    if stats < BluetoothLEAiqi.Connect_result.Connect_Send_OK.value:

        if stats == BluetoothLEAiqi.Connect_result.Connect_Notify_OK.value:
            print(log_title + "connect ok")
        else:
            print(log_title + "connect err", stats)
    else:
        print(log_title + "blue send stats", stats)


def Ble_scan_handle(sender, par):
    print(par)
    if ble_connect_mode == None:
        print(log_title + "please set connect mode")
        return
    if ble_connect_mode == "name":
        if par[0] == ble_connect_mode_name:
            blue_watcher.Bluetooth_Watch_Enable(False)
            # 建立连接
            blue_gatt.bluetooth_connect_create(par[3])

    elif ble_connect_mode == "mac":
        if par[1] == ble_connect_mode_mac:
            blue_watcher.Bluetooth_Watch_Enable(False)
            print("find device")
            # 建立连接
            blue_gatt.bluetooth_connect_create(par[3])


'''

蓝牙连接状态监听

'''


def Ble_connect_stats_handle(sender, par):
    if par == BluetoothLEAiqi.Connect_Status.Connected_OK.value:
        print(log_title + "connecthandle dev connect ok")
        ble_connect_stats_handle(0)
        if ble_connect_stats_handle != None:
            ble_connect_stats_handle(0)
    else:
        print(log_title + "connecthandle dev disconnect")
        if ble_connect_stats_handle != None:
            ble_connect_stats_handle(1)


'''

蓝牙接受数据监听

'''


def Ble_value_change_handle(sender, par):
    print(log_title + "rev value len:", len(par))
    print(par[0])


'''
蓝牙初始化
Connect_stats_handle 蓝牙连接状态回调
value_change_handle 蓝牙数据接收回调

'''


def BluetoothLE_INIT(Connect_stats_handle=None, value_change_handle=None):
    global blue_watcher, blue_gatt, ble_value_change_handle, ble_connect_stats_handle

    blue_watcher = BluetoothLEAiqi.Bluetooth_Watch_Init(Ble_scan_handle)

    blue_gatt = BluetoothLEAiqi.Bluetooth_Init(Connect_stats_handle, Ble_connect_create_handle,
                                               value_change_handle)


'''
蓝牙连接
参数 name ,若使用名字作为参数，那么默认扫描到即连接
参数 mac ,扫到mac即连接
'''


def BluetoothLE_Connect(name=None, mac=None):
    global ble_connect_mode, ble_connect_mode_name, ble_connect_mode_mac
    if name != None:
        ble_connect_mode = "name"
        ble_connect_mode_name = name
        # print("mode is name")
    elif mac != None:
        ble_connect_mode = "mac"
        ble_connect_mode_mac = mac
        # print("mode is mac")
    else:
        ble_connect_mode = None
        return None

    BluetoothLEAiqi.Bluetooth_Scan_Ctrl(blue_watcher, True)

    return True

def BluetoothLE_DIsconnect():
    BluetoothLEAiqi.Bluetooth_Disconnect(blue_gatt)

'''
buff 待发送数组
蓝牙发送

'''
def BluetoothLE_Send(buff):
    BluetoothLEAiqi.Bluetooth_Send(blue_gatt, buff)

'''
mesh dev login
'''


def Ble_OneBot_Mesh_Login():
    Onebot_Mesh_Login_1 = "PoW6p99mRQ3yPOhS1dSqnA=="
    Onebot_Mesh_Login_2 = "Am49m1E9XXyNxW2/bjHZaQ=="
    Onebot_Mesh_Login_3 = "cP2qHxIa0nPrxuSildnyKw=="

    BluetoothLEAiqi.Bluetooth_Send(blue_gatt, Onebot_Mesh_Login_1)
    time.sleep(0.2)
    BluetoothLEAiqi.Bluetooth_Send(blue_gatt, Onebot_Mesh_Login_2)
    time.sleep(0.2)
    BluetoothLEAiqi.Bluetooth_Send(blue_gatt, Onebot_Mesh_Login_3)
    time.sleep(0.3)


'''
mibot login

'''


def Ble_Mibot_Login():

    Onebot_Mibot_Login = "78BByM0pzI4R9kcA5G7ra5+JQLL1MoxMMuDxhakTh4qcC86hZGr1GZEIH2+P7FYY"

    time.sleep(0.3)
    BluetoothLEAiqi.Bluetooth_Send(blue_gatt, Onebot_Mibot_Login)




