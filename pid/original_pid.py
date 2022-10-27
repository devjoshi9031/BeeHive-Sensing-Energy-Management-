import matplotlib 
# matplotlib.use('Agg') 
 
import PID 
import time 
import matplotlib.pyplot as plt 
import numpy as np 
import math 
# from scipy.interpolate import spline 


def convert_error_to_time_exp(error):
    mul = 2.851
    e = 4.3523
    return (mul*math.e**(e*error))

def convert_error_to_time_lin(error):
    mul = 54.091
    ad = 22.136
    return (mul*error+ad)

def convert_curr_consumption_to_voltage_drop(time) :
    Iactive = 3.3
    Isleep = .00235
    v = (Iactive+time*Isleep)/500
    return v
P = 1
I = 0.0001 
D = 0.0001 
pid = PID.PID(P, I, D) 
 
pid.SetPoint = 4
pid.setSampleTime(0.1) 
 
total_sampling = 200 
current_voltage = 4.4
 
def convert_error_to_time_const(error):
    return (20)


def simulate_pid(time_function, current_voltage, pid):
    feedback_list = [] 
    time_list = [] 
    setpoint_list = [] 
    error_list = []
    period_list = []
    print("simulating....") 
    for i in range(1, total_sampling): 
        pid.update(current_voltage) 
        output = pid.output 
        period = time_function(output)
        vd = convert_curr_consumption_to_voltage_drop(period)
        print("Vd: ",vd,"Output: ",output, "Feedback: ", current_voltage, "Feedback + Output: ", current_voltage+output, "Period: ", period)
        if(current_voltage<3.3):
            break
        current_voltage-=vd

    
        time.sleep(0.2) 
        feedback_list.append(current_voltage) 
        setpoint_list.append(pid.SetPoint) 
        time_list.append(i) 
        error_list.append(output)
        period_list.append(period)

    return feedback_list, setpoint_list, time_list, error_list, period_list


feedback_const_list, setpoint_list, time_const_list, error_const_list, period_const_list = simulate_pid(convert_error_to_time_const, 4.4,pid)   
feedback_exp_list, setpoint_list, time_exp_list, error_exp_list, period_exp_list = simulate_pid(convert_error_to_time_exp, 4.4,pid)   
feedback_lin_list, setpoint_list, time_lin_list, error_lin_list, period_lin_list =simulate_pid(convert_error_to_time_lin, 4.4,pid)   


time_sm = np.array(time_exp_list) 
time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300) 
# feedback_smooth = spline(time_list, feedback_list, time_smooth) 
 
fig1 = plt.gcf() 
fig1.subplots_adjust(bottom=0.15) 
 
plt.plot(time_exp_list, feedback_exp_list[:len(time_exp_list)], color='red') 
plt.plot(time_lin_list, feedback_lin_list[:len(time_lin_list)], color='blue') 
plt.plot(time_const_list, feedback_const_list[:len(time_const_list)], color='blue') 
# plt.plot(time_exp_list, setpoint_list[:len(time_exp_list)], color='blue') 
# plt.plot(time_list, error_list, color='black') 
plt.xlim((0, total_sampling)) 
# plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5)) 
plt.xlabel('time (s)') 
plt.ylabel('PID (PV)') 
plt.title('TEST PID') 
 
plt.grid(True) 
print("saving...") 
fig1.savefig('result.png', dpi=100) 

np.save("./lin_period", period_lin_list)
np.save("./exp_period", period_exp_list)

