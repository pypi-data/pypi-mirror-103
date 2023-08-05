#!/usr/bin/env python
# coding: utf-8

# In[4]:


import time
class smartPID:
    def __init__(self,P=0.2,I=0.0,D=0.0):
        self.P=P
        self.I=I
        self.D=D
        self.vPID=0.03
        self.vP=0.1
        self.vI=0.1
        self.vD=0.1
        self.wkp_last=0.1
        self.wki_last=0.1
        self.wkd_last=0.1
        self.sampletime=0.01
        self.outputlast=0.0
        self.timelabel=time.time()
        self.timelabel_last=self.timelabel
        self.reset()
    def reset(self):
        self.set_point=0.0
        self.Pgain=0.0
        self.Igain=0.0
        self.Dgain=0.0
        self.devia_realtime=0.0
        self.devia_lasttime=0.0
        self.devia_last2time=0.0
        self.output=0.0
    def position(self,input_signal):
        self.timelabel=time.time()
        self.input_signal=input_signal
        self.devia_realtime=self.set_point-self.input_signal
        self.timerange=self.timelabel-self.timelabel_last
        self.deviarange=self.devia_realtime-self.devia_lasttime
        if  self.timerange>self.sampletime:
            self.Pgain=self.P*self.devia_realtime
            self.Igain+=self.devia_realtime*self.timerange
            if self.devia_lasttime==0:
                self.Igain==0
            self.Dgain=0
            if self.timerange>0:
                self.Dgain=self.deviarange/self.timerange
            self.timelable_last=self.timelabel
            self.devia_lasttime=self.devia_realtime
            self.output=self.Pgain+self.I*self.Igain+self.D*self.Dgain
    def incremental(self,input_signal):
        self.timelabel=time.time()
        self.input_signal=input_signal
        self.input_signal_last=0.0
        self.devia_realtime=self.set_point-self.input_signal
        self.timerange=self.timelabel-self.timelabel_last
        self.deviarange=self.devia_realtime-self.devia_lasttime
        if  self.timerange>self.sampletime:
            self.Pgain=self.P*(self.devia_realtime-self.devia_lasttime)
            self.Igain=self.devia_realtime
            self.Dgain=0
            if self.timerange>0:
                self.Dgain=self.devia_realtime-2*self.devia_lasttime+self.devia_last2time
            self.timelable_last=self.timelabel
            self.devia_last2time=self.devia_lasttime
            self.devia_lasttime=self.devia_realtime
            self.input_signal_last=self.output
            self.gain_ouput=self.Pgain+self.I*self.Igain+self.D*self.Dgain
            self.output=self.input_signal_last+self.gain_ouput
    def SNPID(self,input_signal):
        self.timelabel=time.time()
        self.input_signal=input_signal
        self.devia_realtime=self.set_point-self.input_signal
        self.timerange=self.timelabel-self.timelabel_last
        self.deviarange=self.devia_realtime-self.devia_lasttime
        if  self.timerange>self.sampletime:
            x1=self.devia_realtime-self.devia_lasttime
            x2=self.devia_realtime
            x3=self.devia_realtime-2*self.devia_lasttime+self.devia_last2time
            wkp=self.wkp_last+self.vP*self.devia_realtime*self.outputlast*x1
            wki=self.wki_last+self.vI*self.devia_realtime*self.outputlast*x2
            wkd=self.wkd_last+self.vD*self.devia_realtime*self.outputlast*x3
            wtotal=abs(wkp)+abs(wki)+abs(wkd)
            self.P=wkp/wtotal
            self.I=wki/wtotal
            self.D=wkd/wtotal
            self.output=self.outputlast+self.vPID*((x1*wkp)+(x2*wki)+(x3*wkd))
            self.devia_last2time=self.devia_lasttime
            self.devia_lasttime=self.devia_realtime
            self.outputlast=self.output
            self.wkp_last=wkp
            self.wki_last=wki
            self.wkd_last=wkd
    def set_PID(self, P_value,I_value,D_value):
        self.P = P_value
        self.I = I_value
        self.D = D_value
    def set_set_point(self,set_point):
        self.set_point=set_point
    def set_sampletime(self, sample_time):
        self.sampletime = sample_time
    def set_SNPID_LR(self,vPID,vP,vI,vD):
        self.vPID=vPID
        self.vP=vP
        self.vI=vI
        self.vD=vD
    def set_SNPID_IW(self,wkp_IW,wki_IW,wkd_IW):
        self.wkp_last=wkp_IW
        self.wki_last=wki_IW
        self.wkd_last=wkd_IW
    def display_PIDvalue(self):
        print(f'The P value is:{self.P}\nThe I value is:{self.I}\nThe D value is:{self.D}\nThe sampletime is:{self.sampletime}\nThe setpoint is:{self.set_point}')
    def display_SNPIDvalue(self):
        print(f'The P value learning rate is:{self.vP}\nThe I value learning rate is:{self.vI}\nThe D value learning rate is:{self.vD}\nThe initial value of P is:{self.wkp_last}\nThe initial value of I is:{self.wki_last}\nThe initial value of D is:{self.wkd_last}\nThe final value of P is:{self.P:.2f}\nThe final value of I is:{self.I:.2f}\nThe final value of D is:{self.D:.2f}')

