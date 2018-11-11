import os
from util.SystemUtil import AudioUtility

audio = AudioUtility()

class Actions(object):
    clicked = False

    
    def palm_action(movement, diff):
        command = "xte 'keydown Control_L' 'keydown Alt_L' 'keydown {}' 'keyup Control_L' 'keyup Alt_L' 'keyup {}'".format(movement, movement)
        os.system(command)
    

    def fist_action(movement, diff):
        if movement == 'Right':
            audio.increaseVolume()
        elif movement == 'Left':
            audio.decreaseVolume()

        elif movement == 'Up':
            command = "xte 'keydown Control_L' 'keydown Alt_L' 'keydown T' 'keyup Control_L' 'keyup Alt_L' 'keyup T'"
            os.system(command)
            pass

        else:
            command = "xte 'keydown Super_L' 'keydown L' 'keyup Super_L' 'keyup L'"
            os.system(command)

    

    
    '''
    def palm_action(movement, diff):
        if diff > 20:
            diff = diff*4
        else:
            diff = 20
        command = "xte 'mouseup i'"
        os.system(command)


        if movement == 'Right':
            command = "xte 'mousermove {} 0'".format(diff)
            os.system(command)

        elif movement == 'Left':
            command = "xte 'mousermove -{} 0'".format(diff)
            os.system(command)

        elif movement == 'Up':
            command = "xte 'mousermove 0 -{}'".format(diff)
            os.system(command)

        elif movement == 'Down':
            command = "xte 'mousermove 0 {}'".format(diff)
            os.system(command)


    def fist_action(movement, diff):
        if diff > 20:
            diff = diff*4
        else:
            diff = 20
        command = "xte 'mousedown i'"
        os.system(command)

        if movement == 'Right':
            command = "xte 'mousermove {} 0'".format(diff)
            os.system(command)

        elif movement == 'Left':
            command = "xte 'mousermove -{} 0'".format(diff)
            os.system(command)

        elif movement == 'Up':
            command = "xte 'mousermove 0 -{}'".format(diff)
            os.system(command)

        elif movement == 'Down':
            command = "xte 'mousermove 0 {}'".format(diff)
            os.system(command)
    '''
    
        

class Motion(object):
    """docstring for """
    def __init__(self):
        self.base_pos = {}
        self.base_pos['Palm'] = None
        self.base_pos['Fist'] = None

        self.actions = {}
        self.actions['Palm'] =  Actions.palm_action
        self.actions['Fist'] = Actions.fist_action
        
        self.motion_thresh = {}
        self.motion_thresh['Palm'] = (70, 70) #Horizontal, Vertical
        self.motion_thresh['Fist'] = (50, 100) #Horizontal, Vertical


    def palm_action(self, movement):
        pass


    def fist_action(self, movement):
        pass


    def detect(self, new_pos, gesture_name):
        if self.base_pos[gesture_name] != None:
            x1, y1 = new_pos
            x0, y0 = self.base_pos[gesture_name]
            change_base = True

            if x1 - x0 > self.motion_thresh[gesture_name][0]:
                print('Right Movement of ', gesture_name)
                self.actions[gesture_name]('Right', abs(x1-x0))
            
            elif x1 - x0 < - self.motion_thresh[gesture_name][0]:
                print('Left Movement of ', gesture_name)
                self.actions[gesture_name]('Left', abs(x1-x0))
            
            elif y1 - y0 > self.motion_thresh[gesture_name][1]:
                print('Down Movement of ', gesture_name)
                self.actions[gesture_name]('Down', abs(y1-y0))

            elif y1 - y0 < - self.motion_thresh[gesture_name][1]:
                print('Up Movement of ', gesture_name)
                self.actions[gesture_name]('Up', abs(y1-y0))

            else:
                change_base = False

            if change_base:
                self.base_pos[gesture_name] = new_pos

        else:
            self.base_pos[gesture_name] = new_pos

    def clear_base(self):
        for key, value in self.base_pos.items():
            self.base_pos[key] = None

    def clear_gesture(gesture_name):
        for key, value in self.base_pos.items():
            if key != gesture_name:
                self.base_pos[key] = None

     