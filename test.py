import os, sys, time
from csvreader import read_csv_file
from battery_changing_period import *
import matplotlib.pyplot as plt

period = [10,20,30,40,50,60]

numSamples = 50
def simulate_original_condition(error,start,stop,stride, msg, desired_voltage):
    current_values = read_csv_file('/home/dev/Downloads/Battery Voltage-data-2022-10-12 15 37 15.csv', numSamples)
    a = [0]*6
    p = []
    pta = time.time()
    for i in current_values:
        error_val = calculate_error(desired_voltage, i)
        for ii in range(0,len(error)):
            if(error[ii]>=error_val):
                actual_error = error[ii]
                # print("Error: {}\t Index: {}")
                p.append(period[ii-1])
                a[ii-1]+=1
                break
        print("Current Value: {}\t Error: {}\t Period: {}".format(i,actual_error, p[-1]))
        time.sleep(p[-1]/100)
    ptb = time.time()-pta
    total=0
    for i in a:
        total += i
    print("Distribution for Version [{}]: {}\t{}".format(msg,a,total))
    print(("Time for Version [{}]: {}".format(msg, ptb)))
    return a

def main():
    desired_voltage = float(sys.argv[1])

    print("PRINTING LARGER PERIOD VERSION:")
    start,stop,stride,error = calculate_stride_start_stop_larger_period(desired_voltage, len(period))
    print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
    print(error)

    p_larger = simulate_original_condition(error,start,stop,stride,"Larger Period", desired_voltage)

    print("PRINTING SMALLER PERIOD VERSION:")
    # start,stop,stride,error = calculate_stride_start_stop_smaller_period(4.00)
    # print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
    # for i in error:
    #     print("{:.2f}".format(i))

    print("PRINTING NORMAL PERIOD VERSION:")
    start,stop,stride,error = calculate_stride_start_stop_normal_period(desired_voltage, len(period))
    print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
    print(error)
    p_normal = simulate_original_condition(error,start,stop,stride,"Smaller Period", desired_voltage)


    
    plt.bar(period, p_normal, width=.5)
    plt.xlabel("error")
    plt.ylabel("Period")
    plt.show()





if __name__ == "__main__":
    main()