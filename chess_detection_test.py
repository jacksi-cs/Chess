from re import X
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import os
from numpy.core.numeric import indices
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow.compat.v1 as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image, ImageGrab, ImageDraw

# imported for screen capture
from mss import mss


from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

import cv2
import time
from stopwatch import Stopwatch, profile



"Will probably move this to a more suitable place"
cypher_list = [] # Used alongside board_list and piece_list, showing which elements represent which boxes on the board
for letter in ["a","b","c","d","e","f","g","h"]:
    for number in range(1,9):
        cypher_list.append(letter+str(number))

def indices_to_move(i1, i2):
    if i1 == None or i2 == None:
        return None
    return cypher_list[i1] + cypher_list[i2]

def update_piece_list(move):
    print("placeholder")

# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.
#
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# In[4]:

# What model to download.
MODEL_NAME = 'new_graph'
OFFSET_PATH = 'models/research/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = OFFSET_PATH + MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(OFFSET_PATH +'data', 'object-detection.pbtxt')

NUM_CLASSES = 12


# ## Download Model

# In[5]:

# opener = urllib.request.URLopener()
# opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
# tar_file = tarfile.open(MODEL_FILE)
# for file in tar_file.getmembers():
#     file_name = os.path.basename(file.name)
#     if 'frozen_inference_graph.pb' in file_name:
#         tar_file.extract(file, os.getcwd())


# ## Load a (frozen) Tensorflow model into memory.

# In[6]:

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

# In[7]:

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# ## Helper code

# In[8]:

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


# # Detection

# In[9]:

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]  # change this value if you want to add more pictures to test

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


# In[10]:

# top = 170
# left = 268
# width = 841
# height = 841

top = 169
left = 284
width = 822
height = 822

# top = 322
# left = 284
# width = 822
# height = 500

# top = 168
# left = 284
# width = 822
# height = 204

mon = {'top': top, 'left': left, 'width': width, 'height': height}
#sct = mss()

"Generating the board list"

# x = [321,427,530,636,742,846,953,1057] # from a to h
# y= [966,860,744,636,530,430,336,227] # from 1 to 8

x = [52,157,262,367,472,577,682,787]
y = [787,682,577,472,367,262,157,52]
board_list = [] # The center coordinates for each box on the board (a1,...,a8,...b1,...)
piece_list = [] # The piece at each box on the board (a1,...,a8,...b1,...)

for x_coord in x:
    for y_coord in y:
        piece_id = None
        x_index = x.index(x_coord)
        y_index = y.index(y_coord)
        if x_index == 0 or x_index == 7:
            if y_index == 0:
                piece_id = 7.0 # White rook
            elif y_index == 7:
                piece_id = 1.0 # Black rook
            elif y_index == 1:
                piece_id = 12.0 # White pawn
            elif y_index == 6:
                piece_id = 6.0 # Black pawn
        elif x_index == 1 or x_index == 6:
            if y_index == 0:
                piece_id = 8.0 # White knight
            elif y_index == 7:
                piece_id = 2.0 # Black knight
            elif y_index == 1:
                piece_id = 12.0
            elif y_index == 6:
                piece_id = 6.0
        elif x_index == 2 or x_index == 5:
            if y_index == 0:
                piece_id = 9.0 # White bishop
            elif y_index == 7:
                piece_id = 3.0 # Black bishop
            elif y_index == 1:
                piece_id = 12.0
            elif y_index == 6:
                piece_id = 6.0
        elif x_index == 3:
            if y_index == 0:
                piece_id = 10.0 # White queen
            elif y_index == 7:
                piece_id = 4.0 # Black queen
            elif y_index == 1:
                piece_id = 12.0
            elif y_index == 6:
                piece_id = 6.0
        elif x_index == 4:
            if y_index == 0:
                piece_id = 11.0 # White king
            elif y_index == 7:
                piece_id = 5.0 # Black king
            elif y_index == 1:
                piece_id = 12.0
            elif y_index == 6:
                piece_id = 6.0
        board_list.append((x_coord, y_coord))
        piece_list.append(piece_id)


with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        while True:
            # sct.get_pixels(mon)
            image = ImageGrab.grab(bbox=(left,top,left+width,top+height)) #.resize((300,300))
            image_np = np.array(image) # bbox is (left, upper, right, lower)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)

            new_piece_list = [None for i in range(0,64)]

            for box in boxes:
                for b in range(0, np.size(box,0)-1):
                    if scores[0][b] > 0.70:
                        ymin = int((box[b][0]*height))
                        xmin = int((box[b][1]*width))
                        ymax = int((box[b][2]*height))
                        xmax = int((box[b][3]*width))
                        x_avr = (xmin + xmax)/2
                        y_avr = (ymin + ymax)/2
                        counter = 0 # debugging purposes
                        min_test = [1000,1000] # debugging purposes
                        for index in range(0,len(board_list)):                             
                            if int(x_avr) in range(board_list[index][0]-25, board_list[index][0]+25) and int(y_avr) in range(board_list[index][1]-25, board_list[index][1]+25):
                                # if classes[0][b] != piece_list[index]:
                                    # print("MOVED! Found: ", classes[0][b], (x_avr, y_avr), "In List: ", piece_list[index], board_list[index])
                                "Actually important component of code"
                                new_piece_list[index] = classes[0][b]
            i1 = None
            i2 = None
            for i in range(0,len(piece_list)):
                if new_piece_list[i] != piece_list[i]:
                    "This is where the piece moved FROM"
                    if new_piece_list[i] == None:
                        i1 = i
                    else:
                        i2 = i
            
            move = indices_to_move(i1,i2)
            if (move != None):
                print(move)
                piece_list = new_piece_list

            cv2.imshow('object detection', image_np)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break