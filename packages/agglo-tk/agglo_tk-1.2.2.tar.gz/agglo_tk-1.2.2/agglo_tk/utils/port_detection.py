# @file 
# @brief 
# @copyright Copyright PA.COTTE 2020

import platform
import itertools

if platform.system() == "Windows":
    import winreg
else:
    import serial.tools.list_ports
    import serial.tools.list_ports_linux

__all__ = ["detect_ports"]


COM_PORT_PATH = "HARDWARE\\DEVICEMAP\\SERIALCOMM"
COM_PORT_FULL_NAME_PATH = "SYSTEM\\ControlSet001\\Control\\COM Name Arbiter\\Devices"

def detect_ports(vendor_id: str=None, product_id: str=None):
    if vendor_id is None:
        raise Exception("You shall provide a vendor_id to search for")

    com_port_list = []

    if platform.system() == "Windows":
        all_com_ports = []

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, COM_PORT_PATH)
            full_name_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, COM_PORT_FULL_NAME_PATH)

            # First list currently attached com ports
            for i in itertools.count():
                try:
                    value = winreg.EnumValue(key, i)
                    all_com_ports.append(str(value[1]))
                except EnvironmentError:
                    break
            
            # Refine list with only board com ports
            for i in itertools.count():
                try:
                    port, full_name = winreg.EnumValue(full_name_key, i)[:2]

                    if (port in all_com_ports) and (vendor_id.lower() in full_name):
                        com_port_list.append(port)
                except EnvironmentError:
                    break

        except WindowsError:
            pass

    else:
        # ports = glob.glob('/dev/ttyACM[0-9]*')
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if vendor_id in hwid and product_id in hwid:
                com_port_list.append(port)
                # print("{}: {} [{}]".format(port, desc, hwid))    
            
    return sorted(com_port_list)
