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

def convert_error_to_time_exp_decreasing(error):
    mul = 13.5379
    e = -3.7221
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

def convert_error_to_time_const_60(error):
    return (60)

def simulate_pid(time_function, current_voltage, pid):
    feedback_list = [] 
    time_list = [] 
    setpoint_list = [] 
    error_list = []
    period_list = []
    print("simulating....") 
    i=0
    a = time.time()
    prev_period=0
    while(1):
        pid.update(current_voltage) 
        output = pid.output 
        period = time_function(output)
        vd = convert_curr_consumption_to_voltage_drop(period)
        print("Vd: ",vd,"Output: ",output, "Feedback: ", current_voltage, "Feedback + Output: ", current_voltage+output, "Period: ", period)
        if(current_voltage<3.3):
            break
        current_voltage-=vd
        time.sleep(period/100) 
        feedback_list.append(current_voltage) 
        setpoint_list.append(pid.SetPoint) 
        time_list.append(i) 
        error_list.append(output)
        period_list.append(prev_period+period)
        prev_period = period
        i+=1
    b = time.time()-a

    return feedback_list, setpoint_list, time_list, error_list, period_list, b


feedback_const_list, setpoint_list, time_const_list, error_const_list, period_const_list, time_ran_const = simulate_pid(convert_error_to_time_const, 4.4,pid)   
feedback_const_list_60, setpoint_list, time_const_list_60, error_const_list_60, period_const_list_60, time_ran_const_60 = simulate_pid(convert_error_to_time_const_60, 4.4,pid)   
feedback_exp_list, setpoint_list, time_exp_list, error_exp_list, period_exp_list, time_ran_exp = simulate_pid(convert_error_to_time_exp, 4.4,pid)   
# feedback_lin_list, setpoint_list, time_lin_list, error_lin_list, period_lin_list =simulate_pid(convert_error_to_time_lin, 4.4,pid)   
# feedback_exp_dec_list, setpoint_list, time_exp_dec_list, error_exp_dec_list, period_exp_dec_list =simulate_pid(convert_error_to_time_exp_decreasing, 4.4,pid)   


time_sm = np.array(time_exp_list) 
time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300) 
# feedback_smooth = spline(time_list, feedback_list, time_smooth) 
 
fig1 = plt.gcf() 
fig1.subplots_adjust(bottom=0.15) 
 
plt.plot(period_exp_list, feedback_exp_list, color='red') 
# plt.plot(time_exp_dec_list, feedback_exp_dec_list[:len(time_exp_dec_list)], color='blue') 
# plt.plot(time_lin_list, feedback_lin_list[:len(time_lin_list)], color='blue') 
plt.plot(period_const_list, feedback_const_list[:len(period_const_list)], color='black') 
plt.plot(period_const_list_60, feedback_const_list[:len(period_const_list_60)], color='blue') 
# plt.plot(time_exp_list, setpoint_list[:len(time_exp_list)], color='blue') 
# plt.plot(time_list, error_list, color='black') 
plt.xlim((0, period_exp_list)) 
# plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5)) 
plt.xlabel('time (s)') 
plt.ylabel('PID (PV)') 
plt.title('TEST PID') 
 
plt.grid(True) 
print("saving...") 
fig1.savefig('result.png', dpi=100) 

# np.save("./lin_period", period_lin_list)
np.save("./exp_period", period_exp_list)
# np.save("./exp__dec_period", period_exp_dec_list)

print(time_ran_const, time_ran_const_60, time_ran_exp)