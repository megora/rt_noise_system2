#!/usr/bin/python
# TODO:
# 1. Rewrite reset to complete reset (both channels)
from data_acquisition2.vxi_11 import vxi_11_connection


class VoltageSupply(vxi_11_connection):
    def __init__(self,ipaddr='129.59.93.105',gpib=15):
        vxi_11_connection.__init__(self,host=ipaddr, device="gpib0,%s" % str(gpib), raise_on_err=0, timeout=5000, device_name="Voltage_supply")

    def set_voltage_a(self,voltage=0.0): #FOR SYSTEM 2
        self.write("W3") #PAUSE
        self.write("A5") #DC output
        self.write("L3") #10mA limit
        self.write("PA%s;" % str(voltage)) #set voltage
        self.write("W4")#RESTART

    def set_voltage_b(self,voltage=0.0): #FOR SYSTEM 2
        self.write("W7") #reset
        self.write("RA1") #autorange
        self.write("B1") #Ch2 on in DC output
        self.write("M3") #10mA limit
        self.write("PB%s;" % str(voltage)) #set voltage
        self.write("W1")

    # def set_voltage_a(self, voltage=0.0):  # Gate voltage   #FOR SYSTEM 1
    #     self.write("W7")  # reset
    #     self.write("RA1")  # autorange
    #     self.write("A5")  # Ch1 on in DC output
    #     self.write("L3")  # 10mA limit
    #     self.write("PA%s;" % str(voltage))  # set voltage
    #     self.write("W1")
    # 
    # def set_voltage_b(self, voltage=0.0): #Drain voltage #FOR SYSTEM 1
    #     self.write("W3")  # PAUSE
    #     self.write("B1")  # DC output second channel VB
    #     self.write("M3")  # 10mA limit
    #     self.write("PB%s;" % str(voltage))  # set voltage
    #     self.write("W1")  #
    #
    # def set_voltage_b(self, voltage=0.0):  # Drain voltage
    #     self.write("W3")  # PAUSE
    #     self.write("B1")  # DC output second channel VB
    #     self.write("M3")  # 10mA limit
    #     self.write("PB%s;" % str(voltage))  # set voltage
    #     #self.write("W4")  # RESTART
    #     self.write("W1")  #

    def reset(self):
        self.write("W7")
        self.write("A5")  # Ch1 on in DC output
        self.write("B1")  # DC output second channel VB
        self.write("PA0.0;") # % str(voltage))  # set voltage
        self.write("PB0.0;") #% str(voltage))  # set voltage


if __name__=='__main__':
    ps=VoltageSupply('129.59.93.192',17)
    ps.set_voltage_a(0.0)
    ps.set_voltage_b(0.0)
    

