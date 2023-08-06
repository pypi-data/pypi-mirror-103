import time

import bluetoothle_app as le_driver


my_xl = "00312E0120AA"

'''

蓝牙连接状态监听

'''

def Ble_connect_stats_handle(sender, par):
    print("stats  ",par)
    if par == 0:
        print("connect ok")
        le_driver.Ble_OneBot_Mesh_Login()
    elif par == 2:
        print("connect err")
        le_driver.BluetoothLE_DIsconnect()
    else:
        print("disconnect")

'''

蓝牙接受数据监听

'''

def Ble_value_change_handle(sender, par):
    print("rev value len:",len(par))
    print(par[0])




if __name__ == '__main__':
    le_driver.BluetoothLE_INIT(Ble_connect_stats_handle,Ble_value_change_handle)
    le_driver.BluetoothLE_Connect(mac=my_xl)

    while True :
        time.sleep(1)
