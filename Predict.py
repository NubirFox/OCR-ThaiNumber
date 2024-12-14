import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
import numpy as np

train_dir = 'Dataset/Handwrite_orientation/Train/'
val_dir = 'Dataset/Handwrite_orientation/Test/'
target_img_shape = (70,70)
nclass = 10

train_datagen = ImageDataGenerator()
train_set = train_datagen.flow_from_directory(train_dir,target_size=target_img_shape,batch_size=32,class_mode = 'categorical')

val_datagen = ImageDataGenerator()
val_set = val_datagen.flow_from_directory(val_dir,shuffle=False,target_size=target_img_shape,batch_size=32,class_mode = 'categorical')

labels =(train_set.class_indices)
labels = dict((v,k) for k,v in labels.items())

model = load_model('Model/OCR-number-TH.h5')

img = cv2.imread("9.png")
img = cv2.resize(img, target_img_shape)
img_array = img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

pred = model.predict(img_array)
pred_cls = labels[np.argmax(pred, axis=-1)[0]]
print("prediction: ", pred_cls)