""" Class which provides flags if certain events have occured
    (up, down, left, right)
"""


import time

from ArduinoReader import ArduinoReader


class EventFlags:
    def __init__(self, **kwargs):
        self.arduinoReader = ArduinoReader(kwargs['port'])
        self.up_flag = self.down_flag = self.left_flag = self.right_flag = False

        self.up_threshold = kwargs['up_threshold']
        self.down_threshold = kwargs['down_threshold']
        self.gy_threshold = kwargs['gy_threshold']

        self.ignore = False
        self.ignore_start_time = time.perf_counter()


    def calibrate(self):
        """ Reads from arduinoReader to set baseline x,y,z accelerations
        """

        #TODO: take average over 5 seconds

        # Get time as a float in seconds
        start_time = time.perf_counter()

        # Get baseline values by averaging over 5 seconds
        count = 0
        x_readings = 0
        y_readings = 0
        z_readings = 0
        gy_readings = 0
        while ((time.perf_counter() - start_time) < 5):
            self.arduinoReader.read()
            x_readings += self.arduinoReader.x
            y_readings += self.arduinoReader.y
            z_readings += self.arduinoReader.z
            gy_readings += self.arduinoReader.gy
            count += 1

        self.initial_x = x_readings / count
        self.initial_y = y_readings / count
        self.initial_z = z_readings / count
        self.initial_gy = gy_readings / count

        print('{}, {}, {}, {}'.format(self.initial_x, self.initial_y,
                                      self.initial_z, self.initial_gy))
        

    def check(self):
        """ Checks if event thresholds have been reached
            Should be called in a loop
        """
        self.arduinoReader.read()

        if self.ignore:
            # Check if enough time has passed to start accepting
            # motions again
            if (time.perf_counter() - self.ignore_start_time) > 1:
                self.ignore = False

        # If another spike happens, reset the timer but don't trigger another event
        if self.ignore:
            if self.arduinoReader.gy - self.initial_gy > self.gy_threshold:
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
            if self.arduinoReader.gy - self.initial_gy < -(self.gy_threshold):
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
            if self.arduinoReader.x - self.initial_x > self.up_threshold:
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
            if self.arduinoReader.x - self.initial_x < -(self.down_threshold):
                # Start the timer now
                self.ignore_start_time = time.perf_counter()

        if not self.ignore:
            if self.arduinoReader.gy - self.initial_gy > self.gy_threshold:
                self.right_flag = True
                self.ignore = True
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
                print('right')
            if self.arduinoReader.gy - self.initial_gy < -(self.gy_threshold):
                self.left_flag = True
                self.ignore = True
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
                print('left')
            if self.arduinoReader.x - self.initial_x > self.up_threshold:
                self.up_flag = True
                self.ignore = True
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
                print('up')
            if self.arduinoReader.x - self.initial_x < -(self.down_threshold):
                self.down_flag = True
                self.ignore = True
                # Start the timer now
                self.ignore_start_time = time.perf_counter()
                print('down')


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
                            up_threshold=10000,
                            down_threshold=10000,
                            gy_threshold=750)
    eventFlags.calibrate()

    while 1:
        eventFlags.check()


if __name__== '__main__':
    main()
