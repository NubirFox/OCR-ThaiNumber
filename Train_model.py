import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Flatten, Conv2D, MaxPool2D, Dropout
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

import keras

train_dir = 'Dataset/Handwrite_orientation/Train/'
val_dir = 'Dataset/Handwrite_orientation/Test/'
target_img_shape = (70,70)
nclass = 10

train_datagen = ImageDataGenerator()
train_set = train_datagen.flow_from_directory(train_dir,target_size=target_img_shape,batch_size=32,class_mode = 'categorical')

nplots = 8

for j in range(0,nclass):
    augmented_images = [train_set[j][0][0] for i in range(nplots)]
    
print("")

val_datagen = ImageDataGenerator()
val_set = val_datagen.flow_from_directory(val_dir,shuffle=False,target_size=target_img_shape,batch_size=32,class_mode = 'categorical')


print(train_set.class_indices)

print("training data set")
ids, counts = np.unique(train_set.classes,return_counts = True)
print(ids)
print(counts)
labels =(train_set.class_indices)
labels = dict((v,k) for k,v in labels.items())
labels
for i in ids:
    print("{:>10} = {}".format(labels[i], counts[i]))

print("")

print("Validation data set")
ids,counts = np.unique(val_set.classes,return_counts = True)
print(ids)
print(counts)
labels =(val_set.class_indices)
labels = dict((v,k) for k,v in labels.items())
labels

for i in ids:
    print("{:>10} = {}".format(labels[i], counts[i]))

_,train_count = np.unique(train_set.classes,return_counts=True)
_,val_count = np.unique(val_set.classes,return_counts=True)

print("")
print('Ratio Validation/Training set :')
for i in ids:
    print("{:>10} = {:.2f}".format(labels[i],val_count[i]/train_count[i]*100))
print("")

input_shape = (target_img_shape[0],target_img_shape[1],3)

model = Sequential()
model.add(Conv2D(32,(3,3),activation='relu',input_shape=input_shape))
model.add(MaxPool2D(2,2))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPool2D(2,2))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(MaxPool2D(2,2))
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dropout(0.5)) 
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(nclass, activation="softmax"))

print("Input_shape = ", input_shape)
model.summary()
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
history = model.fit(train_set, validation_data=val_set, epochs=1, verbose=1)

# model.save('Model/OCR-number-TH.h5')

y_true = val_set.classes
y_pred = model.predict(val_set)

y_pred_classes = np.argmax(y_pred, axis=1)

conf_mat = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 8))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues', xticklabels=val_set.class_indices.keys(),
        yticklabels=val_set.class_indices.keys())
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()