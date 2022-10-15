import os, sys, time, math
from random import *

period = [60,50,40,30,20,10]

def generate_temperature() -> float:
    value = uniform(30,35)
    return value

def update_error(currTemp, prevTemp) -> float:
    return abs(prevTemp-currTemp)    

def get_error_range_normal(MaxError, numPeriod) -> list:
    diff = (MaxError/numPeriod)
    error = []
    for i in range(0,numPeriod+1):
        error.append(diff*i)
    return error

def period_from_error(error, curr_error) -> int:
    index=0
    for i in range(0,len(error)):
        if(curr_error<error[i]):
            index = i
            break
    
    return index

def main():
    seed(time.time())
    error_range = get_error_range_normal(3,len(period))
    prev = 33.00
    a = time.time()
    for i in range(0,10):
        curr = generate_temperature()
        err = update_error(curr, prev)
        index = period_from_error(error_range, err)
        print("CurrTemp: {:.2f}\t PrevTemp: {:.2f}\t Error: {:.2f}\t Period: {:.2f}".format(curr, prev, err, period[index-1]))
        prev=curr
        time.sleep(period[index-1]/100)
    b = time.time()
    print("Static period:")
    for i in range(0,10):
        curr = generate_temperature()
        err = update_error(curr, prev)
        index = period_from_error(error_range, err)
        print("CurrTemp: {:.2f}\t PrevTemp: {:.2f}\t Error: {:.2f}\t Period: {:.2f}".format(curr, prev, err, 20))
        prev=curr
        time.sleep(20/100)
    c = time.time()

    print("Time [Value Aware: {}]\nTime [Normal: {}]".format(b-a,c-b))


if __name__ == '__main__':
    main()
