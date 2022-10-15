import os, sys, csv

def read_csv_file(csvfilename, NumberOfSamples) -> list:
    with open(csvfilename, 'r') as file:
        reader = csv.reader(file)
        counter=0
        rows=[]
        for row in reader:
            if(counter==0):
                counter+=1
                continue
            # if(counter==NumberOfSamples):
            #     break
            rows.append(float(row[1]))
            counter+=1
    return rows




def main():
    numbers = read_csv_file('/home/dev/Downloads/Battery Voltage-data-2022-10-12 15 37 15.csv')
    print(numbers)

if __name__ == "__main__":
    main()