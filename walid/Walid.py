from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier(r'/home/pi/magic/MagicMirror/modules/facerecognition/haarcascade_frontalface_default.xml')
model=load_model(r'/Users/Ron/Projects/Backend/MagicMirror/Emotion_little_vgg.h5')

emotions = ['angry','happy','neutral','sad','surprise']

cap = cv2.VideoCapture(0)
cap.set(3,840)
cap.set(4,640)



while True:
    # Grab a single frame of video
    ret, img = cap.read()
    labels = []
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48))
    # rect,face,image = face_detector(frame)


        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

        # make a prediction on the ROI, then lookup the class

            prediction = model.predict(roi)[0]
            label=emotions[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(img,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),2)
        
    cv2.imshow('Expression-recognition',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
