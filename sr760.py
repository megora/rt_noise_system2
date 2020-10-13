#!/usr/bin/python

from data_acquisition2.vxi_11 import vxi_11_connection
import time

class sr760(vxi_11_connection):
    def __init__(self,ipaddr='127.0.0.1', gpib=12,enable_selector=True):
        vxi_11_connection.__init__(self,host=ipaddr, device="gpib0,%s" % str(gpib), raise_on_err=1, timeout=1500, device_name="SR760")

    def setup(self,numAvg=1000,freqSpan=11,startFreq=0.0):
        self.write("*RST\n")
        self.write("STOP\n")

        self.write('SPAN %s\n' % freqSpan)
        self.write("STRF %s\n" % startFreq)
    
        self.write("ACTG 0\n") #;//active trace 0    
        self.write("MEAS 0,1\n") #;//measure PSD
        self.write("DISP 0,0\n") #;//LogMag
        self.write("UNIT 0,1\n") #;//units Vrms
        self.write("WNDO 0,2\n") #;//hanning window

        self.write("ISRC 0\n") #;//SET INPUT TO A 
#        self.write("IRNG 34\n") #;//SET INPUT range to 34 dbV 
        self.write("IGND 0\n") #;//SET INPUT GROUNDING TO FLOAT 
        self.write("AUTS 0\n") #;//SET AUTOSCALE
        
        self.write("AOFM 0\n") #;//turn off calibration edit by chundong liang
        self.write("AOFF 0\n") #;//SET AUTOOFFSET edit by chundong liang
        

        self.write("NAVG %s\n" % numAvg)
        self.write("AVGO1\n") #;   //turn averaging on
        self.write("AVGT0\n") #;   //set averaging type to RMS

    def start(self):
        self.write("STRT\n")# ;    //start average  

    def wait(self):
        while True:
            time.sleep(1)
            err,status=self.read_status_byte()
            #print (status & 1), (status & 2)
            if  ((status & 1) and (status & 2)):
                return

    def read_spectrum(self):
        f_spectrum=[]
        d_spectrum=[]
        for i in range(400):
            self.write("BVAL?0, %s\n" % i)
            trace=self.recv(count=30).strip()
            f_spectrum.append(float(trace))
            self.write("SPEC?0, %s\n" % i)
            trace=self.recv(count=30).strip()
            d_spectrum.append(float(trace))
        return f_spectrum, d_spectrum

    def abort(self):
        pass

    def send(self,string):
        self.write(string)

    def recv(self,timeout=None,count=None):
        return self.read(timeout=timeout,count=count)[2]

if __name__=='__main__':
    SA=sr760('169.254.58.10',10)
    SA.setup()
    SA.start()
    SA.wait()
    print "wait is over"
    SA.read_spectrum()
