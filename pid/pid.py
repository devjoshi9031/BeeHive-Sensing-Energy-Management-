import math, sys, time, os
import csv
import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, desired, P=1, I=0.1, D=0.001):
        self.startup(desired, P, I, D)


    def update(self,curr):
        self.error = self.set_point - curr
        self.curr_time = time.time()
        # print("curr time: {}".format(self.curr_time))
        self.time_delta = self.curr_time-self.prev_time
        P_term = self.Kp * self.error
        self.I_term += self.error * self.time_delta
        if(self.I_term < -self.windup_guard):
            self.I_term = -self.windup_guard
        elif(self.I_term > self.windup_guard):
            self.I_term = self.windup_guard
        # print("I Term: {}".format(self.I_term))
        D_term = ((self.error-self.prev_error)/self.time_delta)
        self.prev_time = self.curr_time
        self.prev_error = self.error

        return (P_term+(self.Ki*self.I_term)+(self.Kd*D_term))

    def startup(self,desired,P,I,D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.prev_error=0
        self.error=0
        self.prev_time=time.time()
        self.set_point = desired
        self.I_term = 0
        self.windup_guard = 20.0 


def generate_voltage():
#     voltages = [4.4,
# 4.41,
# 4.4,
# 4.41,
# 4.4,
# 4.4,
# 4.4,
# 4.4,
# 4.41,
# 4.41,
# 4.28,
# 4.17,
# 4.16,
# 4.17,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.15,
# 4.16,
# 4.16,
# 4.15,
# 4.15,
# 4.14,
# 4.15,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.13,
# 4.14,
# 4.14,
# 4.13,
# 4.13,
# 4.13,
# 4.13,
# 4.13,
# 4.13,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.25,
# 4.12,
# 4.12,
# 4.12,
# 4.13,
# 4.12,
# 4.12,
# 4.12,
# 4.28,
# 4.28,
# 4.28,
# 4.28,
# 4.28,
# 4.28,
# 4.27,
# 4.28,
# 4.4,
# 4.4,
# 4.41,
# 4.41,
# 4.41,
# 4.4,
# 4.4,
# 4.28,
# 4.4,
# 4.28,
# 4.17,
# 4.17,
# 4.16,
# 4.17,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.16,
# 4.15,
# 4.15,
# 4.15,
# 4.15,
# 4.15,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.14,
# 4.13,
# 4.13,
# 4.13,
# 4.13,
# 4.14,
# 4.13,
# 4.13,
# 4.13,
# 4.12,
# 4.13,
# 4.12,
# 4.13,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.12,
# 4.13,
# 4.12,
# 4.12
# ]
    min = 3.3
    max = 4.4
    curr = max
    count=0
    while(True):
        yield 4.5


def main():
    error=[]
    pid = PIDController(4.5)
    feedback=0
    count=1
    while(True):
        # if(feedback<=0):
        #     i-=feedback
        # else:
        #     i+=feedback
        # if(i<=3.3):
        #     break
        output = (pid.update(feedback))
        feedback += (output - (1/count))
        error.append(feedback)
        time.sleep(1)
        print("Feedback: ",feedback)
        count+=1

    x_axis = [x for x in range(len(error))]
    plt.plot(x_axis,error)
    plt.show()

    with open("./example_PI_1.csv","w") as file:
        writer = csv.writer(file,delimiter=',')
        writer.writerow(error)

    print("Loop ran for ",count,"times")



if __name__=='__main__':
    main()