from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from io import BytesIO
import webbrowser
import os

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
webbrowser.open('file://' + os.path.realpath('template/OCR-test.html'))
app = Flask(__name__, template_folder='template')
CORS(app)

@app.route('/process_image', methods=['POST'])
def process_image():
    image_file = request.files.get('image')
    file_bytes = image_file.read()
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img_resized = cv2.resize(img, (400, 400))
    if len(img_resized.shape) == 2: 
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2BGR)

    ret,thresh = cv2.threshold(img_resized,70,255,0)
    seg_x = []
    seg_y = []
    for i in range(len(thresh[0])):
        for j in range(len(thresh[1])):
            if thresh[i][j][0] == 0 :
                seg_x.append(i)
                seg_y.append(j)
                
    img = cv2.resize(img_resized[min(seg_x):max(seg_x),min(seg_y):max(seg_y)], target_img_shape)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    pred = model.predict(img_array)
    pred_cls = labels[np.argmax(pred, axis=-1)[0]]
    print("prediction: ", pred_cls)
    result = f"เลข: {pred_cls}"

    _, buffer = cv2.imencode('.png', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'result': result, 'processed_image': img_base64})

if __name__ == '__main__':
    app.run()
