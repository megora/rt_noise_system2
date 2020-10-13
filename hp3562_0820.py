#!/usr/bin/python

from data_acquisition2.vxi_11 import vxi_11_connection
import time, sys, math
import matplotlib.pyplot as plt

class hp3562(vxi_11_connection):
    def __init__(self,ipaddr='0.0.0.0', gpib=10):
        vxi_11_connection.__init__(self,host=ipaddr, device="gpib0,%s" % str(gpib), raise_on_err=0, timeout=5000, device_name="hp3562a")

    def reset(self):
        self.write("RST")        

    def setupNoise(self,numavg,freqrange):
        self.write("lnrs")
        self.write("clen 1000pts")
        self.write("pspc")
        self.write("ch1")
        self.write("sf 0 Hz")
        self.write("navg %s" % numavg)
        self.write("frs %s Hz" % freqrange)
        self.write("psun")
        self.write("vhz")
        self.write("wndo hann")
        self.write("stbl")
        self.write("yasc")
        self.write("ism 4")

    def setupCapture(self, t_tot):
        freqSamp = 10 * 800 / t_tot # Verified - ten records*800/time
        self.write('CPTR') #Selects the time capture measurement mode
        self.write('CH1') #Activates Channel 1 for selected measurement
        self.write('FRS %s HZ' %freqSamp) #Specifies frequency span
        self.write('SF 0HZ') #Specifies start frequency
        self.write('ITM1') #Displays the time domain signal on Channel 1

    def start(self): # for noise
        self.write("strt")

    def startCapture(self): # for capture
        self.write("stcp")

    def sendCmd(self,command):
        self.write(command)

    def query(self,command):
        self.write(command)
        data=self.read()
        return data

    # def wait(self):
    #     stat='0'
    #     while (not stat=='1'):
    #         self.write("rdy?")
    #         stat=self.read()[2].strip()

    def wait(self):
        stat='0'
        while (not stat=='1'):
            self.write("smsd")
            stat=self.read()[2].strip()
            time.sleep(1)            
    
    def getData(self):
        self.write("DDAS 1000")
        time.sleep(1)
        data=self.read()[2]
        dat=[]
        
        #header
        for line in data.split('\n'):
            if not line.find('#')==0:
                if len(line)>0 and line[1] in ['0','1','2','3','4','5','6','7','8','9']:
                    dat.append(line)
        try:
            tmp=float(dat[55])
        except IndexError:
            f_array=[]
            data_array=[]
            return f_array, data_array
        
        islog=False
        inc=float(dat[55])
        ydata=dat[66:]
        startval=float(dat[64])
        linlog=int(float(dat[40]))
        if linlog==1:
            islog=True
            xinc=math.pow(10.0,inc)
        else:
            islog=False
            xinc=inc
            
        data_array=[]
        f_array=[]
        x=startval
        for elem in ydata:
            f_array.append(x)
            data_array.append(float(elem))
            if islog:
                x=x*inc
            else:
                x=x+inc
        return f_array, data_array


    def getDataCapture(self):
        calibrationCapture=-25000; #This value need to be re-checked (retrieved by previous code and verified by manual calibration)
        self.write("DDAS") #download data in ANSII format
        time.sleep(1)
        data=self.read()[2]
        data_raw = []
        
        for line in data.split('\n'):
            if not line.find('#')==0:
                if len(line)>0 and line[1] in ['0','1','2','3','4','5','6','7','8','9']:
                    data_raw.append(line[:])

       #print data_raw
        # print data_raw[54]
        # print data_raw[55]
        # print data_raw[56]
        # print data_raw[57]
        # print data_raw[58]
        
        inc_t=float(data_raw[55])
        print 'inc_t = ', inc_t
        scale_fact=float(data_raw[56])
        print 'scale_fact = ', scale_fact
        vData=data_raw[68:]
        # print 'vData = ', vData

        t_array = []
        data_array=[]

        for i in range(len(vData)):                                                            
            t=inc_t*(i-1)
            #print t
            elem=float(vData[i])*scale_fact/calibrationCapture
            #print elem
            t_array.append(t)
            data_array.append(elem)
        # print t_array
        # print data_array
        return t_array, data_array

    # filter to usually remove 60Hz
    def filterFreq(self, f_array, data_array, ref_freq, ref_span):
        f_out=[]
        data_out=[]
        for (f_tmp, data_tmp) in zip(f_array,data_array):
            if abs(f_tmp-ref_freq)<ref_span/2.0:
                f_out.append(f_tmp)
                data_out.append(data_out)
        return f_out, data_out
      

if __name__=='__main__':
    
    ip='129.59.93.192'
    gpib=10
    amplFact=500
    avgNum=20
    freqSpan=1000
    
    spA=hp3562(ip,gpib)

    spA.reset()
#    spA.setupNoise(avgNum,freqSpan)
#    spA.start()
#    spA.wait()
#    f_array, data_array=spA.getData()
#    fg=[]
#    for i in data_array:
#        fg.append(i*i)
#    
#    plt.scatter(f_array, fg)
#    plt.xscale('log')
#    plt.yscale('log')
#    plt.ylim([1e-14, 1e-7])
#    plt.xlim([1, 2000])


####Backup:
    # def getDataCapture(self):
    #     calibrationCapture = -25000;  # This value need to be re-checked (retrieved by previous code and verified by manual calibration)
    #     self.write("DDAS")
    #     time.sleep(1)
    #     data = self.read()[2]
    #     data_raw = []
    #
    #     for line in data.split('\n'):
    #         if not line.find('#') == 0:
    #             if len(line) > 0 and line[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    #                 data_raw.append(line[:-2])
    #
    #     print data_raw
    #     print data_raw[56]
    #     print data_raw[57]
    #     print data_raw[58]
    #
    #     inc_t = float(data_raw[57])
    #     print ('inc_t = ', inc_t)
    #     scale_fact = float(data_raw[58])
    #     print ('scale_fact = ', scale_fact)
    #     vData = data_raw[68:]
    #     print ('vData = ', vData)
    #
    #     t_array = []
    #     data_array = []
    #
    #     for i in range(len(vData)):
    #         t = inc_t * (i - 1)
    #         print t
    #         vdatai = float(vData[i])
    #         elem = vdatai * scale_fact / calibrationCapture
    #         print elem
    #         t_array.append(t)
    #         data_array.append(elem)
    #
    #     return t_array, data_array