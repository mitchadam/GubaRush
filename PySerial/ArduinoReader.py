import serial


class ArduinoReader:
    def __init__(self):
        #TODO: don't hard code port
        self.ser = serial.Serial('/dev/ttyACM1')
        self.current_position = 0
        self.x = self.y = self.z = 0


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
        else:
            pass


def main():
    arduinoReader = ArduinoReader()

    while 1:
        arduinoReader.read()
        print('{}, {}, {}'.format(arduinoReader.x, arduinoReader.y, arduinoReader.z))



if __name__== '__main__':
    main()
