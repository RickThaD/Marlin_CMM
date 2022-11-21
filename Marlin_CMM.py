import serial
import time
import struct
import csv

z_safeheight = 0
resolution = 0
width = 0
height = 0
resolution = 0
port = 'COM8'
baud = 115200
connection = True
ser = serial.Serial(port, baud, timeout=0)
answer = ""
answerz = "0"
bit = 1
rows = []
nextstring=''

print("Connected to " + port + " at baud rate " + str(baud))
z_safeheight = input("What is the Z safe height?")
sres = input("What is the resolution to scan (mm between points)?")
resolution = float(sres)
initstring='G1 Z'+str(z_safeheight)+'\n'
swidth = input("How many points to measure? (X)?")
width = int(swidth)
sheight = input("How many points to measure? (Y)?")
height = int(sheight)
ser.write(bytes(b'M155 S0'+b'\n'))
time.sleep(0.5)
ser.write(bytes(b'G28 Z'+b'\n'))
time.sleep(0.5)
ser.write(bytes(initstring,'ascii'))
time.sleep(0.5)
ser.write(bytes(b'M18'+b'\n'))
time.sleep(0.5)
input("Please move head to zero position (bottom left) and press enter.")
ser.write(bytes(b'M17'+b'\n'))
time.sleep(0.5)
ser.write(bytes(b'G90'+b'\n'))
time.sleep(0.5)
ser.write(bytes(b'G92 X0 Y0'+b'\n'))
time.sleep(0.5)
ser.readlines()
ser.write(bytes(b'G90'+b'\n'))
time.sleep(0.5)
ser.write(bytes(nextstring,'ascii'))
answer = b''

for x in range(width):
    for y in range(height):
        nextstring = 'G1 X'+str(x*resolution)+' Y'+str(y*resolution)+' Z'+str(z_safeheight)+'\n'
        ser.write(bytes(initstring,'ascii'))
        time.sleep(0.5)
        ser.write(bytes(nextstring,'ascii'))
        print(nextstring)
        time.sleep(0.5)
        ser.readlines()
        ser.write(bytes(b'G30'+b'\n'))
        time.sleep(0.5)
        while answer == b'ok\n' or answer == b'' or answer == b'Error:!! STOP called because of BLTouch error - restart with M999\n':
            time.sleep(0.5)
            answer = ser.readline()
            if answer == b'Error:!! STOP called because of BLTouch error - restart with M999\n':
                ser.write(bytes(b'M999'+b'\n'))
                time.sleep(0.5)
                ser.write(bytes(nextstring,'ascii'))
                time.sleep(0.5)
                ser.write(bytes(b'M119'+b'\n'))
                time.sleep(0.5)
                ser.write(bytes(b'M280 P0 S10'+b'\n'))
                time.sleep(0.5)
                ser.write(bytes(b'M119'+b'\n'))
                time.sleep(0.5)
                ser.write(bytes(b'M280 P0 S60'+b'\n'))
                time.sleep(0.5)
                input("Stow probe and press enter")
                ser.write(bytes(b'M119'+b'\n'))
                time.sleep(0.5)
                ser.write(bytes(b'M280 P0 S160'+b'\n'))
                time.sleep(0.5)
                ser.write(bytes(b'M999'+b'\n'))
                time.sleep(0.5)
                y = y-1 
                ser.write(bytes(nextstring,'ascii'))
                time.sleep(2)
                ser.readlines()
                ser.write(bytes(b'G30'+b'\n'))
                time.sleep(0.5)
        answerss = bytes.decode(answer)
        print(answerss)
        answer2 = [x*resolution,y*resolution,answerss]
        answer = b''
        rows.append(answer2)
        
        
        
filename = "output.csv"
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)