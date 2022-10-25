import matplotlib 
matplotlib.use('Agg') 
 
import PID 
import time 
import matplotlib.pyplot as plt 
import numpy as np 
# from scipy.interpolate import spline 
 
 
P = 1.4 
I = 1 
D = 0.001 
pid = PID.PID(P, I, D) 
 
pid.SetPoint = 4.4 
pid.setSampleTime(0.1) 
 
total_sampling = 100 
current_voltage = 3.3
 
feedback_list = [] 
time_list = [] 
setpoint_list = [] 
 
print("simulating....") 
for i in range(1, total_sampling): 
    pid.update(current_voltage) 
    output = pid.output 
    print("Output: ",output, "Feedback: ", current_voltage, "Feedback + Output: ", current_voltage+output)
    current_voltage+=output

 
    time.sleep(0.2) 
 
    feedback_list.append(current_voltage) 
    setpoint_list.append(pid.SetPoint) 
    time_list.append(i) 
 
time_sm = np.array(time_list) 
time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300) 
# feedback_smooth = spline(time_list, feedback_list, time_smooth) 
 
fig1 = plt.gcf() 
fig1.subplots_adjust(bottom=0.15) 
 
plt.plot(time_list, feedback_list, color='red') 
plt.plot(time_list, setpoint_list, color='blue') 
plt.xlim((0, total_sampling)) 
plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5)) 
plt.xlabel('time (s)') 
plt.ylabel('PID (PV)') 
plt.title('TEST PID') 
 
print(feedback_list)
plt.grid(True) 
print("saving...") 
fig1.savefig('result.png', dpi=100) 