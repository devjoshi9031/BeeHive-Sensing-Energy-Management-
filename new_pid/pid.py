import time
import os
import sys
import random
import matplotlib.pyplot as plt
import numpy as np


class simulator:
    def __init__(self, vinit) -> None:
        self.v_prev = vinit

    def voltage_calculator(self,vd,vc):
        v_ch = vc
        v_next = self.v_prev + (v_ch - vd)
        self.v_prev = v_next
        return v_next
    


class ControlSystem:
    def __init__(self) -> None:
        self.Kp=1
        self.Ki=0.001
        self.Kd=0.3
        self.v_desired = 4
        self.last_time = time.time()
        self.sample_time = 2
        self.windup_guard = 10.0
        self.last_error=0
        self.PTerm=0
        self.ITerm=0
        self.DTerm=0

    def calcerror(self,v_curr):
        error = (self.v_desired-vcurr)
        self.current_time =  time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time
        
        self.last_time = self.current_time
        self.last_error = error
        return (self.PTerm + (self.Ki*self.ITerm) + (self.Kd*self.DTerm))

    def get_charging_voltage(self, time):
        if((time>5 and time<10) or (time>15 and time<20) or (time>25 and time<30) or (time>35 and time<40)):
            return 0
        else:
            rand = random.randint(1,10)
            r = random.random()
            if((int(rand)%2)==0):
                vc=0.5 + (r*0.1*0.5)
            else:
                vc=0.5 - (r*0.1*0.5)
            return vc

    def calcv_d(self,error,i):
        vc = self.get_charging_voltage(i)
        vd = vc - error
        rand = random.randint(1,10)
        r = random.random()
        # Clamping
        if(vd<=0.1):
            vd=0.1 
        elif(vd>=0.9):
            vd=0.9
        
        # if(int(rand)%2==0):
        #     vd = vd + (r*0.1*vd)
        # else:
        #     vd = vd - (r*0.1*vd)
        return vd,vc


    def calculate_vd(self,v_curr,i):
        error = self.calcerror(v_curr)
        vd = self.calcv_d(error,i)
        return vd


if __name__ == '__main__':
    vcurr = 3.3
    sim = simulator(vcurr)
    cs = ControlSystem()
    time.sleep(2)
    print("Starting PID controller with Vinit = {}, Kp = {}, range of Vd:[0.1,0.3]\n".format(vcurr,cs.Kp))

    print("Time\t Vd\t VNext\t VCharging")
    i=0
    voltages=[]
    charging_voltages=[]
    discharge_voltages=[]
    times=[]
    voltages.append(vcurr)
    times.append(i)
    while(True):
        vd,vc = cs.calculate_vd(vcurr,i)
        vcurr = sim.voltage_calculator(vd,vc)
        print("{}\t{}\t{}\t{}".format(i,vd,vcurr,vc))
        time.sleep(2)
        charging_voltages.append(vc)
        discharge_voltages.append(vd)
        voltages.append(vcurr)
        times.append(i)
        i+=1

        if(i>40):
            break

    desired_voltages = [cs.v_desired]*len(times)

    time_sm = np.array(times) 
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300) 
    plt.plot(times,desired_voltages,'red')
    plt.plot(times,voltages)

    plt.show()



