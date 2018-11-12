import cv2
import time
import os
import numpy as np
import tensorflow as tf

from util.ObjectDetectionUtils import label_map_util
from util.MotionUtil import Motion


MODEL_NAME = 'gesture_fist_5_L_C'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH ='TrainedModels/' + MODEL_NAME + '/inference_graph' + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'TrainedModels/' + MODEL_NAME + '/class_map.pbtxt'

ROW, COLUMN = 224, 224

CLASS_NAME = {
    1: 'Palm',
    2: 'Fist',
    3: 'Angle',
    4: 'Curve'
}

CLASS_COLOR = {
    1: (255, 0, 0),
    2: (0, 0, 255),
    3: (0, 255, 0),
    4: (0, 0, 0)
}


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def run():
    motion = Motion()
    #palm_pos = (-1, -1)
    # Load Frozen model
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')


    #Load Label Map
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

    cap = cv2.VideoCapture(0)

    with detection_graph.as_default():
        with tf.Session() as sess:
            
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            key_list = [
              'detection_boxes', 'detection_scores',
              'detection_classes'
            ]
            for key in key_list:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                  tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

                
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
                
            while True:
                _, frame = cap.read()
                img = frame[..., ::-1]
                img = cv2.resize(img, (ROW, COLUMN))
                img_expanded = np.expand_dims(img, axis=0)

                # Run inference
                output_dict = sess.run(tensor_dict,
                                     feed_dict={image_tensor: img_expanded})

                output_dict['detection_classes'] = output_dict[
                  'detection_classes'][0][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0][0]

                # os.system('clear')

                # print('Detection Scores: ', output_dict['detection_scores'])
                # print('Detection Classes: ', output_dict['detection_classes'])
                # print('Detection Boxes: ', output_dict['detection_boxes'])

                if output_dict['detection_scores'] > 0.85:
                    y1 = int(output_dict['detection_boxes'][0] * frame.shape[0])
                    x1 = int(output_dict['detection_boxes'][1] * frame.shape[1])
                    y2 = int(output_dict['detection_boxes'][2] * frame.shape[0])
                    x2 = int(output_dict['detection_boxes'][3] * frame.shape[1])

                    class_id = output_dict['detection_classes']

                    cv2.rectangle(frame, (x1, y1), (x2, y2), CLASS_COLOR[class_id], 4)

                    
                    cv2.putText(frame, CLASS_NAME[class_id] , (x1+15, y1+5), cv2.FONT_HERSHEY_DUPLEX, 2.0, (255, 255, 255))

                    new_pos = ((x1+x2)/2, (y1+y2)/2)
                    
                    # motion.detect(new_pos,CLASS_NAME[class_id])

                else:
                    motion.clear_base()


                cv2.imshow('frame', frame)
                cv2.moveWindow('frame', 1000, 100)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    run()


