import os
from util.SystemUtil import AudioUtility

audio = AudioUtility()

class Actions(object):
    
    def palm_action(movement, diff):
        command = "xte 'keydown Control_L' 'keydown Alt_L' 'keydown {}' 'keyup Control_L' 'keyup Alt_L' 'keyup {}'".format(movement, movement)
        os.system(command)
    

    def curve_action(movement, diff):
        if movement == 'Right':
            audio.increaseVolume()
        elif movement == 'Left':
            audio.decreaseVolume()
            #command = "xte 'keydown Page_Up'  'keyup Page_Up'"
            #os.system(command)

        elif movement == 'Up':
            command = "xte 'keydown Control_L' 'keydown Alt_L' 'keydown T' 'keyup Control_L' 'keyup Alt_L' 'keyup T'"
            os.system(command)

        else:
            command = "xte 'keydown Super_L' 'keydown L' 'keyup Super_L' 'keyup L'"
            os.system(command)


    def angle_action(movement, diff):
        if movement == 'Right':
            pass
        elif movement == 'Left':
            pass
            #command = 
            #os.system(command)

        elif movement == 'Up':
            command = "xte 'keydown Page_Up'  'keyup Page_Up'"
            os.system(command)

        else:
            command = "xte 'keydown Page_Down'  'keyup Page_Down'"
            os.system(command)
        

class Motion(object):
    """docstring for """
    def __init__(self):
        self.base_pos = {}
        self.base_pos['Palm'] = None
        self.base_pos['Curve'] = None
        self.base_pos['Angle'] = None

        self.actions = {}
        self.actions['Palm'] =  Actions.palm_action
        self.actions['Curve'] = Actions.curve_action
        self.actions['Angle'] = Actions.angle_action
        
        self.motion_thresh = {}
        self.motion_thresh['Palm'] = (70, 70) #Horizontal, Vertical
        self.motion_thresh['Curve'] = (50, 100) #Horizontal, Vertical
        self.motion_thresh['Angle'] = (30, 30) #Horizontal, Vertical


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

    def clear_gesture(self, gesture_name):
        for key, value in self.base_pos.items():
            if key != gesture_name:
                self.base_pos[key] = None


     