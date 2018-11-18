""" Class to read accelerometer data from serial port
    See main() for example usage
"""


import serial


class ArduinoReader:
    def __init__(self, port):
        self.ser = serial.Serial(port)
        self.current_position = 0
        self.x = self.y = self.z = 0
        self.gx = self.gy = self.gz = 0


    def read(self):
        """ Reads data from serial and update x,y,z
            Should be called in a loop
        """
        word = self.ser.readline()

        # strip carriage return and newline
        word = word[:-2]

        if word == b'start':
            self.current_position = 1
        elif word == b'end':
            self.current_position = 0
        elif self.current_position == 1:
            try:
                self.x = int(word)
            except:
                # Bad int
                self.ser.flush()
            self.current_position += 1
        elif self.current_position == 2:
            try:
                self.y = int(word)
            except:
                # Bad int
                self.ser.flush()
            self.current_position += 1
        elif self.current_position == 3:
            try:
                self.z = int(word)
            except:
                # Bad int
                self.ser.flush()
            self.current_position += 1
        elif self.current_position == 4:
            try:
                self.gx = int(word)
            except:
                # Bad int
                self.ser.flush()
            self.current_position += 1
        elif self.current_position == 5:
            try:
                self.gy = int(word)
            except:
                # Bad int
                self.ser.flush()
            self.current_position += 1
        elif self.current_position == 6:
            try:
                self.gz = int(word)
            except:
                # Bad int
                self.ser.flush()
            self.current_position += 1
        else:
            pass


def main():
    arduinoReader = ArduinoReader('/dev/ttyACM1')

    while 1:
        arduinoReader.read()
        print('Ax:{}, Ay:{}, Az{}, Gx:{}, Gy:{}, Gz:{}'.format(arduinoReader.x, arduinoReader.y, arduinoReader.z,
                                                               arduinoReader.gx, arduinoReader.gy, arduinoReader.gz))



if __name__== '__main__':
    main()
