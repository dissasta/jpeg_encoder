from random import randint
import math

def main():
    #print(0.25*(1/math.sqrt(2))*(1/math.sqrt(2))*-55*math.cos((((2*7)+1)*8*math.pi)/16)*math.cos((((2*0)+1)*8*math.pi)/16))
    sum = 0.0
    for x in range(8):
        for y in range(8):
            sum += -34*math.cos(((2*x+1)*7*math.pi)/16)*math.cos(((2*y+1)*7*math.pi)/16)

    print(0.25*1.0/math.sqrt(2)*1.0/math.sqrt(2)*sum)

if __name__ == "__main__":
    main()