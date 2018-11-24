import os

class Motion(object):
    def __init__(self):
        pass

    def detect(self, new_pos, gesture_name):
        if gesture_name == 'Palm':
            command = "xte 'keyup Left'  'keyup Right'"
            os.system(command)

        if gesture_name == 'Curve':
            command = "xte 'keyup Left' 'keydown Right' "
            os.system(command)

        if gesture_name == 'Angle':
            command = "xte 'keyup Right' 'keydown Left' "
            os.system(command)

    def clear_base(self):
        command = "xte 'keyup Left'  'keyup Right'"
        os.system(command)
        pass

    def clear_gesture(self, gesture_name):
        command = "xte 'keyup Left'  'keyup Right'"
        os.system(command)
        pass
        