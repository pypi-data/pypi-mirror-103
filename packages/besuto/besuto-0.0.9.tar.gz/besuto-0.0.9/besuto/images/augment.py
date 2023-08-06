import numpy as np
from PIL import Image
from mtcnn import MTCNN
import os
import pandas as pd
import tensorflow as tf

# function for face detection with mtcnn
class imagedata:
  def __init__(
    self,
    augment = False,
    target_size = (256,256),
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
      horizontal_flip=True,
      brightness_range=[0.2,1.0],
      rotation_range = 37
      ),
    generation = 5
  ):
    self.augment = augment
    self.target_size = target_size
    self.datagen = datagen
    self.generation = generation
    tf.keras.backend.clear_session()
    tf.random.set_seed(51)
    token = [i for i in self.target_size].append(3)
    self.face_feature_extractor = VGGFace(
      model='resnet50',
      weights ='vggface',
      include_top =False,
      input_shape = tuple(token)
      )
    for layer in self.face_feature_extractor.layers:
        layer.trainable = False

  def extract_face(self,filename):
    '''
    this function use mtcnn to extract faces from image file to numpy array
    '''
    image = Image.open(filename)
    image = image.convert('RGB')
    array = np.asarray(image)
    detector = MTCNN()
    face_detected = detector.detect_faces(array)
    if face_detected ==[]:
      return []
    x1, y1, width, height = face_detected[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = array[y1:y2, x1:x2]
    face = Image.fromarray(face)
    face = face.resize(self.target_size)
    face = np.asarray(face)
    return face

  def Augment(self,array):
    '''
    this function increase the number of image data it will generate generation power of 3 sample
    '''
    result = []
    token = np.expand_dims(array,0)
    generate = self.datagen.flow(token,batch_size=1)
    for i in range(self.generation**3):
      batch = generate.next()
      image = batch[0].astype('uint8')
      result.append(np.asarray(image))
    return np.asarray(result)
  
  def load_faces_dataset(self,directory =''):
    '''
    the input is similar to flow_from_directory fom tensorflow's ImageDataGenerator and will 
    output as numpy array of raw label and 4 dims images
    '''
    X,y = [], []
    # loop every folder
    for folder in sorted(os.listdir(directory)):
      path = directory + folder+'/'
      if not os.path.isdir(path):
        continue
      faces = []
      for filename in os.listdir(path):
        face = extract_face(path + filename)
        if face != []:
          faces.append(face)
        else:
          pass
      faces = np.asarray(faces)
      augment = []
      if self.augment == True:
        for i in faces:
          augment.extend(Augment(i,generation=5))
      else:
        augment.extend(faces)
      labels = [folder for i in range(len(augment))]
      X.extend(augment)
      y.extend(labels)
    return np.asarray(X), np.asarray(y)
  
  def faces_get_feature(self,array):
    '''extract feature from face'''
    #load this to local and load_weightinput_shape
    layer_name ='activation_{}'.format(41)
    model = self.face_feature_extractor.get_layer(layer_name)
    feature = tf.keras.layers.Flatten()(model.predict(array))
    return feature