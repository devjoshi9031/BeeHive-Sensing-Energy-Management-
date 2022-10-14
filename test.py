import os, sys, time

period = [10,20,30,40,50,60]

def calculate_error(desired, recv):
    error = desired - recv
    return error

def get_value_from_sensor():
    min = 3.3
    max = 4.4
    curr = max
    while(curr!=min):
        curr = curr-0.01
        yield curr

def get_sum_of_n_numbers(n):
    return ((n*(n+1))/2)

def calculate_stride_start_stop_larger_period(expected) -> tuple:
    max = 4.4
    min = 3.3
    start = expected - max
    stop = expected - min
    s = (stop-start)/get_sum_of_n_numbers(len(period))
    error_range = []
    last=start
    for i in range(0,len(period)+1):
        tmp = last+(i*s)
        error_range.append(tmp)
        last=tmp

    return start, stop, s, error_range

def calculate_stride_start_stop_smaller_period(expected) -> tuple:
    max = 4.4
    min = 3.3
    start = expected - max
    stop = expected - min
    s = (stop-start)/get_sum_of_n_numbers(len(period))
    error_range = []
    last=start
    for i in range(0,len(period)+1):
        tmp = last+((len(period)-i)*s)
        error_range.append(tmp)
        last=tmp
    return start, stop, s, error_range


def calculate_stride_start_stop_normal_period(expected) -> tuple:
    max = 4.4
    min = 3.3
    start = expected - max
    stop = expected - min
    s = (stop-start)/(len(period))
    error_range = []
    for i in range(0,len(period)+1):
        error_range.append(start+i*s)
    return start, stop, s, error_range




def main():
    desired_voltage = 4.23
    print("PRINTING LARGER PERIOD VERSION:")
    start,stop,stride,error = calculate_stride_start_stop_larger_period(desired_voltage)
    print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
    for i in error:
        print("{:.2f}".format(4.00-i))
    
    
    # print("PRINTING SMALLER PERIOD VERSION:")
    # start,stop,stride,error = calculate_stride_start_stop_smaller_period(4.00)
    # print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
    # for i in error:
    #     print("{:.2f}".format(i))

    print("PRINTING NORMAL PERIOD VERSION:")
    start,stop,stride,error = calculate_stride_start_stop_normal_period(desired_voltage)
    print("Stride is: {:.2f}\t{:.2f}\t{:.2f}".format(start, stop, stride))
    for i in error:
        print("{:.2f}".format(4.00-i))

    a = [0]*6
    for i in get_value_from_sensor():
        if(i <= 3.3):
            break
        error_val = calculate_error(desired_voltage, i)
        for i in range(0,len(error)):
            if(error[i]>error_val):
                actual_error = error[i]
                # print("Error: {}\t Index: {}")
                p = period[i-1]
                a[i-1]+=1
                break
        print("Error: {}\t Period: {}".format(actual_error, p))
        time.sleep(p/1000)
        
    total=0
    for i in a:
        total += i
    print(a,total) 
    
    # change_period(error)




if __name__ == "__main__":
    main()