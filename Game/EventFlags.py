""" Class which provides flags if certain events have occured
    (up, down, left, right)
"""


import time

from ArduinoReader import ArduinoReader


class EventFlags:
    def __init__(self, **kwargs):
        self.arduinoReader = ArduinoReader(kwargs['port'])
        self.up_flag = self.down_flag = self.left_flag = self.right_flag = False

        self.x_threshold = kwargs['x_threshold']
        self.y_threshold = kwargs['y_threshold']
        self.z_threshold = kwargs['z_threshold']


    def calibrate(self):
        """ Reads from arduinoReader to set baseline x,y,z accelerations
        """

        #TODO: take average over 5 seconds

        # Get time as a float in seconds
        start_time = time.perf_counter()

        # Wait 5 seconds for serial data to arrive
        while ((time.perf_counter() - start_time) < 5):
            self.arduinoReader.read()

        self.initial_x = self.arduinoReader.x
        self.initial_y = self.arduinoReader.y
        self.initial_z = self.arduinoReader.z

        print('{}, {}, {}'.format(self.initial_x, self.initial_y,
                                  self.initial_z))
        

    def check(self):
        """ Checks if event thresholds have been reached
            Should be called in a loop
        """
        self.arduinoReader.read()

        if self.arduinoReader.y - self.initial_y > self.y_threshold:
            self.up_flag = True
            print('up')
        if self.arduinoReader.y - self.initial_y < -(self.y_threshold):
            self.down_flag = True
            print('down')
        if self.arduinoReader.x - self.initial_x > self.y_threshold:
            self.left_flag = True
            print('left')
        if self.arduinoReader.x - self.initial_x < -(self.y_threshold):
            self.right_flag = True
            print('right')


    def up(self):
        """ Returns True if up flag has been set, then sets up flag to False
        """
        if (self.up_flag):
            self.up_flag = False
            return True
        else:
            return False


    def down(self):
        """ Returns True if down flag has been set, then sets down flag to False
        """
        if (self.down_flag):
            self.down_flag = False
            return True
        else:
            return False


    def left(self):
        """ Returns True if left flag has been set, then sets left flag to False
        """
        if (self.left_flag):
            self.left_flag = False
            return True
        else:
            return False


    def right(self):
        """ Returns True if right flag has been set, then sets right flag to False
        """
        if (self.right_flag):
            self.right_flag = False
            return True
        else:
            return False


def main():
    eventFlags = EventFlags(port='/dev/ttyACM1',
                            x_threshold=3000,
                            y_threshold=3000,
                            z_threshold=3000)
    eventFlags.calibrate()

    while 1:
        eventFlags.check()


if __name__== '__main__':
    main()
