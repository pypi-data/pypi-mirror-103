import time

import BluetoothLEAiqi


'''
蓝牙相关变量

'''
blue_watcher = None
blue_gatt = None
#要连接的设备mac
mydev = "E8F4F3395CBD"
connectid = mydev
ble_connect_mode = None
ble_connect_mode_name = None
ble_connect_mode_mac = None



'''
建立连接  状态回调

'''
def Ble_connect_create_handle(sender, stats):
    if stats < BluetoothLEAiqi.Connect_result.Connect_Send_OK.value:

        if stats == BluetoothLEAiqi.Connect_result.Connect_Notify_OK.value:
            print("connect ok")
            blue_gatt.Mibot_Login_In()

        else:
            print("connect err", stats)
    else:
        print("blue send stats", stats)


def Ble_scan_handle(sender, par):
    print(par)
    if ble_connect_mode == None:
        print("please set connect mode")
        return
    if ble_connect_mode == "name":
        if par[0] == ble_connect_mode_name :
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
        print("dev connect ok")
    else:
        print("dev disconnect")

    

'''

蓝牙接受数据监听

'''

def Ble_value_change_handle(sender, par):
    print("rev value len:",len(par))
    print(par[0])


'''
蓝牙初始化
'''
def Bluetooth_LE_INIT():
    global blue_watcher, blue_gatt

    blue_watcher = BluetoothLEAiqi.Bluetooth_Watch_Init(Ble_scan_handle)

    blue_gatt = BluetoothLEAiqi.Bluetooth_Init(Ble_connect_stats_handle, Ble_connect_create_handle,
                                               Ble_value_change_handle)


'''
蓝牙连接
参数 name ,若使用名字作为参数，那么默认扫描到即连接
参数 mac ,扫到mac即连接
'''
def Bluetooth_Connect(name=None,mac=None):
    global ble_connect_mode,ble_connect_mode_name,ble_connect_mode_mac
    if name !=None:
        ble_connect_mode ="name"
        ble_connect_mode_name=name
        print("mode is name")
    elif mac != None:
        ble_connect_mode = "mac"
        ble_connect_mode_mac =mac
        print("mode is mac")
    else:
        ble_connect_mode = None
        return None

    BluetoothLEAiqi.Bluetooth_Scan_Ctrl(blue_watcher, True)
    return True



if __name__ == '__main__':

    Bluetooth_LE_INIT()
    Bluetooth_Connect(mac=connectid)
    while True:
        time.sleep(3)