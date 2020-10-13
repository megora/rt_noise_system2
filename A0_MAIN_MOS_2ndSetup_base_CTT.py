#!/usr/bin/python

#TODO:
#1. Check if possible to program amplification factor of preamp automatically

import sys
import time, os, math, numpy
import matplotlib.pyplot as plt
import datetime
from os import path
# Equipment libraries
import cryocon34
import voltage_supply
import mult_34460
import hp3562_0820
import sr760
#    Procedure of finding Vd
from setup_drain_voltage import setup_drain_voltage

# ------> NETWORK CONFIGURATION <-----
#e5810_addr='129.59.93.105'
e5810_addr='129.59.93.192'

#e5810_addr='129.59.93.32'
#setup_2_ip = '129.59.93.105'
#e5810_addr='129.59.93.166'
# e5810_addr='129.59.93.48'
#e5810_addr='169.254.58.10'
e5810_addr='10.8.129.193'

#voltsource=voltage_supply.VoltageSupply(e5810_addr,17)
voltsource=voltage_supply.VoltageSupply(e5810_addr,15)
#voltsource_2=voltage_supply.VoltageSupply(setup_2_ip,15)  #for bias on bulk
meter=mult_34460.mult_34460(e5810_addr,23)
spA=hp3562_0820.hp3562(e5810_addr,10)
#tempcon=cryocon34.cryocon34(e5810_addr,12)
#spA=sr760.sr760(e5810_addr,10)

# ---> PARAMETERS <-----
date = datetime.date.today() #today's date for naming output files
deviceName = 'TEST' #device identificator for  naming output files
deviceName = 'CTT_P1_D09_T=195' #device identificator for  naming output files

# deviceName = 'FF-SOI-D9-E30N-T8' #device identificator for  naming output files
## path = 'd:\#Research\Tools\Python\code\Noise\'
#numbAve=5000 #!5000-6000 or 8000 if noise data are not good for SR760
numbAve = 50 #50 - for HP3562A
numbAve_bg = 20 #30 - averaging for background noise for HP3562A
amplFact = 200 #!check preamplifier
spAn_array = [400] #[400]
# tstart = 300
# tend = 300
temperature = 300
Vb_array = [0]
#Vb_array = [0, -2]
Vd_array = [0.05]
# Vd_array = [0.0001]
#Vd_array = [0.03, 0.05, 0.1]
Vth_arr_0 = [0.0]
#Vth_arr_0 = [0.413, 0.400, 0.413] #!!!!!!!!!!! threshold voltages for Vb=0 for Vd=0.03, 0.05, 0.1
Vth_arr_2 = [0] #!!!!!!!!!!! threshold voltages for Vb=-2 for Vd=0.03, 0.05, 0.1
Vgt_array_ext=[0.4, 0.4]


# Vgt_array_ext=[0.00001]
# Vgt_array_ext=[0.6, 0.6]
# Vgt_array_ext=[0.1, 0.1, 0.15, 0.2, 0.25, 0.3, 0.3, 0.35, 0.45, 0.5, 0.5, 0.55, 0.6, 0.6]
# Vgt_array_ext=[]


# Vgt_array_ext=[0.45, 0.45, 0.5, 0.5, 0.55, 0.55]
# Vgt_array_ext=[0.6, 0.6]
# Vgt_array_ext=[0.3, 0.3]
# Vgt_array_red=[0.4] #6 meas
Vgt_array_red=[0]
#service variable
vd_measd = 0

###Sleep time for stabilizing the system after changing voltage
sleep_time = 20
sleep_time_bg = 20

###RTN
v = '1'
time_record_length = 30

#Vgt_array=[0.2, 0.2, 0.3, 0.3, 0.4, 0.4, 0.5, 0.5, 0.6, 0.6]
#Vgt_array=[0.3, 0.3, 0.4, 0.4, 0.5, 0.5, 0.6, 0.6]
#Vgt_array=[0.2, 0.2, 0.3, 0.4, 0.5, 0.6]
#Vgt_array=[0.4]

def convToSv(amplFact,fg_spectrum,bg_spectrum):
    noiseArr=[]
    fdataArr=[]
    bdataArr=[]
    for fgdata,bgdata in zip(fg_spectrum,bg_spectrum):
        fdata=fgdata/amplFact
        bdata=bgdata/amplFact
        noise=fdata*fdata-bdata*bdata
        noiseArr.append(noise)
        fdataArr.append(fdata*fdata)
        bdataArr.append(bdata*bdata)
    return((noiseArr,fdataArr,bdataArr))

# -----> MAIN <-----
print 'MAIN: Starting the test...'
# print 'Temperature controller: Resetting...'
# tempcon.reset()
# print 'OK'
#while temperature <= tend:
#---------> SETTING TEMPERATURE <-------
# print "Temperature controller: Current Temperature = ", round(tempcon.get_tempK(),2)
# print "Temperature controller: Setting temperature..."
# tempcon.set_tempK(temperature)
# print "Waiting..."
# tempcon.wait_tempK(temperature)
# print "Temperature controller: Goal temperature achieved: %s K \n" % round(tempcon.get_tempK(),2)
for freqspAn in spAn_array:
    for Vb in Vb_array:
        print 'MAIN: Starting the test for Vb = %s' % (Vb)
        if Vb == 0:
            Vth_array = Vth_arr_0
        else:
            Vth_array = Vth_arr_2
        for Vd, Vth in zip(Vd_array, Vth_array):
            print 'MAIN: Starting the test for Vd = %s' % (Vd)
            if Vd == 0.05:
                Vgt_array = Vgt_array_ext
            else:
                Vgt_array = Vgt_array_red
            for Vgt in Vgt_array:
                print 'MAIN: Starting the test for Vgt = %s' % (Vgt)
                voltsource.reset()
                voltsource.set_voltage_a(Vgt + Vth)  # set voltage on G

                print 'Supply: Setting drain voltage'
                setup_drain_voltage(Vd=Vd, Vd_delta=0.001, set_sup_Vd=voltsource.set_voltage_b,
                                    measure_Vd=meter.read_voltage, max_steps=5, dbg=True)
                print 'OK'

                print "Spectrum An.: Setting up for noise measurements"
                spA.reset()
                spA.setupNoise(numbAve, freqspAn)
                
                print 'Waiting for voltage to stabilize %s sec...' %sleep_time,
                time.sleep(sleep_time) 
                print "OK"

                vd_measd = meter.read_voltage()
                print 'Multimeter: Check Vd set = ', round(vd_measd, 4)
                print "Spectrum An.: Spectra measurement...",
                spA.start()
                spA.wait()
                print "OK"

                print "Spectrum An.: Downloading data...",
                time.sleep(1.5)
                f_array, fn_array = spA.getData()
                if len(f_array) == 0:
                    time.sleep(5)
                    f_array, fn_array = spA.getData()
                print "OK"


                print "Supply: Setup for background measurement: Vd = 0 V"
                voltsource.set_voltage_b(0)  # drain to zero
                print 'Waiting for gate voltage to stabilize %s sec....' %sleep_time_bg,
                time.sleep(sleep_time_bg)  # 75
                print "OK"
                print "Spectrum An: Setup for background measurement...",
                spA.reset()
                spA.setupNoise(numbAve_bg, freqspAn)

                #
                print "OK"
                print "Spectrum An.: Background measurement...",
                spA.start()
                spA.wait()
                print "OK"

                voltsource.set_voltage_a(0)  # gate to zero
                voltsource.set_voltage_b(0)  # drain to zero

                print "Spectrum An.: Downloading background data...",
                time.sleep(1.5)
                fb_array, bg_array=spA.getData()
                if len(fb_array)==0:
                    time.sleep(5)
                    fb_array, bg_array=spA.getData()
                print "OK"

                print "MAIN: Converting data...",
                noiseSv,fdata,bdata=convToSv(amplFact,fn_array,bg_array)
                print "OK"

                print "MAIN: Saving data...",
                deviceinfo='%s_%s_Vgt=%s_Vd=%s_Vb=%s' % (date,deviceName,Vgt,vd_measd, Vb)
                # while path.exists("%s.txt" % deviceinfo):
                #     deviceinfo = deviceinfo+'_v'
                ff=open('%s.txt' % deviceinfo,'w')
                #ff.write('log(f) log(Svd) log(fdata)/n')
                for c1,c2,c3,c4 in zip(fb_array,noiseSv,fdata,bdata):
                    ff.write('%s %s %s %s\n' % (c1,c2,c3,c4))
                ff.close()
                print "OK"

                print "MAIN: Plotting data...",
                plt.scatter(fb_array, noiseSv)
                plt.scatter(fb_array, bdata)
                plt.xscale('log')
                plt.yscale('log')
                plt.ylim([1e-16, 1e-7])
                plt.xlim([0.5, 10000])
                plt.xlabel('f (Hz)')
                plt.ylabel('Svd(V$^2$/Hz)')
                plt.savefig('%s.png' %deviceinfo)
                print "OK"
                print "MAIN: Test Vgt=%s is finished for Vd = %s" % (Vgt, Vd)

                # print "MAIN: Starting RTN test"
                # print "Supply: Setup for RTN... "
                # voltsource.set_voltage_a(Vgt + Vth)  # set voltage on G
                # time.sleep(3)  # 20
                # print 'Supply: Setting drain voltage...'
                # setup_drain_voltage(Vd=Vd, Vd_delta=0.005, set_sup_Vd=voltsource.set_voltage_b,
                #                     measure_Vd=meter.read_voltage, max_steps=5, dbg=True)
                # print 'OK'
                # print "Spectrum An.: Setup for RTN...",
                # spA.reset()
                # spA.setupCapture(time_record_length)
                # time.sleep(3)
                # print 'OK'
                #
                # print "Spectrum An.: RTN measurements...",
                # spA.startCapture()
                # time.sleep(time_record_length) #added a pause because of weird data without
                # spA.wait()
                # print 'OK'
                #
                # print "Spectrum An.: Downloading RTN data...",
                # time.sleep(1.5)
                # t_array, data_array = spA.getDataCapture()
                # # if len(t_array) == 0:
                # #     time.sleep(5)
                # #     t_array, data_array = spA.getDataCapture()
                # print "OK"
                #
                # voltsource.set_voltage_a(0)  # gate to zero
                # voltsource.set_voltage_b(0)  # drain to zero
                #
                # print "MAIN: Saving data...",
                # deviceinfo = '%s_RTN_%s_Vgt=%s_Vd=%s_Vb=%s_v=%s' % (date, deviceName, Vgt, Vd, Vb, v)
                # ff = open('%s.txt' % deviceinfo, 'w')
                # # ff.write('log(f) log(Svd) log(fdata)/n')
                # for c1, c2 in zip(t_array, data_array):
                #     ff.write('%s %s\n' % (c1, c2))
                # ff.close()
                # print "OK"
                # # print t_array
                # # print data_array
                #
                # print "MAIN: Plotting data...",
                # plt.plot(t_array, data_array)
                # # plt.xscale('log')
                # # plt.yscale('log')
                # # plt.ylim([1e-16, 1e-7])
                # # plt.xlim([0.5, 1000])
                # plt.xlabel('Time (sec)')
                # plt.ylabel('Drain current (A)')
                # plt.savefig('%s.png' % deviceinfo)
                # print "OK"

voltsource.reset()
# voltsource_2.reset()
