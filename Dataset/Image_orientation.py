import os 
import cv2

data = 'D:/test_Pro/OCR-ThaiNumber/Dataset/HandWrite'
folders = os.listdir(data)
print(folders)

images = []
labels = []

def save(name,frame):
	ret,thresh = cv2.threshold(frame,70,255,0)
	seg_x = []
	seg_y = []
	for i in range(len(thresh[0])):
		for j in range(len(thresh[1])):
			if thresh[i][j] == 0 :
				seg_x.append(i)
				seg_y.append(j)

	file_save = "Dataset/"+"HandWrite"+"/"+str(folder)+"/"+name
	print(file_save+" save")
	cv2.imwrite(file_save,frame[min(seg_x):max(seg_x),min(seg_y):max(seg_y)])

for folder in folders:
    folder_path = os.path.join(data, folder)
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (100, 100))
        save(image_name,image)