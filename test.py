import os, sys, time
from csvreader import read_csv_file
from battery_changing_period import *

period = [10,20,30,40,50,60]

def main():
    desired_voltage = float(sys.argv[1])

    if((int(sys.argv[2]) == 1)):
        print("PRINTING LARGER PERIOD VERSION:")
        start,stop,stride,error = calculate_stride_start_stop_larger_period(desired_voltage, len(period))
        print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
        for i in error:
            print("{:.2f}".format(4.00-i))
        
    elif((int(sys.argv[2]) == 2)):
        print("PRINTING SMALLER PERIOD VERSION:")
        # start,stop,stride,error = calculate_stride_start_stop_smaller_period(4.00)
        # print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
        # for i in error:
        #     print("{:.2f}".format(i))

    else:
        print("PRINTING NORMAL PERIOD VERSION:")
        start,stop,stride,error = calculate_stride_start_stop_normal_period(desired_voltage, len(period))
        print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
        for i in error:
            print("{:.2f}".format(4.00-i))

    current_values = read_csv_file('/home/dev/Downloads/Battery Voltage-data-2022-10-12 15 37 15.csv', 100)
    a = [0]*6
    for i in current_values:
        if(i <= 3.3):
            break
        error_val = calculate_error(desired_voltage, i)
        for ii in range(0,len(error)):
            if(error[ii]>error_val):
                actual_error = error[ii]
                # print("Error: {}\t Index: {}")
                p = period[ii-1]
                a[ii-1]+=1
                break
        # print("Current Value: {}\t Error: {}\t Period: {}".format(i,actual_error, p))
        time.sleep(p/1000)
        
    total=0
    for i in a:
        total += i
    print(a,total) 
    
    # change_period(error)




if __name__ == "__main__":
    main()