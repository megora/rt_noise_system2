#!/usr/bin/python
from data_acquisition2.vxi_11 import vxi_11_connection


class mult_34460(vxi_11_connection):
    def __init__(self,ipaddr='129.59.93.32',gpib=22):
        vxi_11_connection.__init__(self,host=ipaddr, device="gpib0,%s" % str(gpib), raise_on_err=0, timeout=5000, device_name="Voltage_supply")

    def read_voltage(self):
        self.write("MEAS:VOLT:DC?") 
        volt=float(self.read()[2])
        return volt

    def sendCmd(self,command):
        self.write(command)

if __name__=='__main__':
    mlt=mult_34460('129.59.93.192',23)
    volt=mlt.read_voltage()
    print volt

