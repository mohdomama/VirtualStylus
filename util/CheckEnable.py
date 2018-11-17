import subprocess as sp
import os

class CheckEnable(object):
    """docstring for CheckEnable"""
    def __init__(self):
        self.num_frames = 0
        self.enabled = False

    def check(self, gesture):
        if gesture == 'Fist':
            self.num_frames += 1
            if self.num_frames >= 30:
                self.enabled = not self.enabled
                os.system('clear')
                header = 'Wakanda Forever'
                message = 'Gesture Enabled: ' + str(self.enabled)
                sp.call(['notify-send', header, message])
                print(message)
                self.num_frames = 0

        else:
            self.num_frames = 0

        return self.enabled