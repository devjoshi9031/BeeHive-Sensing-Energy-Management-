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

def calculate_stride_start_stop_larger_period(expected, numPeriods) -> tuple:
    max = 4.45
    min = 3.3
    start = expected - max
    stop = expected - min
    s = (stop-start)/get_sum_of_n_numbers(numPeriods)
    error_range = []
    last=start
    for i in range(0,numPeriods+1):
        tmp = last+(i*s)
        error_range.append(tmp)
        last=tmp

    return start, stop, s, error_range

def calculate_stride_start_stop_smaller_period(expected, numPeriods) -> tuple:
    max = 4.45
    min = 3.3
    start = expected - max
    stop = expected - min
    s = (stop-start)/get_sum_of_n_numbers(numPeriods)
    error_range = []
    last=start
    for i in range(0,numPeriods+1):
        tmp = last+((numPeriods-i)*s)
        error_range.append(tmp)
        last=tmp
    return start, stop, s, error_range


def calculate_stride_start_stop_normal_period(expected, numPeriods) -> tuple:
    max = 4.45
    min = 3.3
    start = expected - max
    stop = expected - min
    s = (stop-start)/(numPeriods)
    error_range = []
    for i in range(0,numPeriods+1):
        error_range.append(start+i*s)
    return start, stop, s, error_range
