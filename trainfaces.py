import cv2

import numpy as np
import face_recognition as fr

imgE = fr.load_image_file('images/Elon Test.jpg')
imgE = cv2.cvtColor(imgE,cv2.COLOR_BGR2RGB)

imgT = fr.load_image_file('images/Elon Musk.jpg')
imgT = cv2.cvtColor(imgT,cv2.COLOR_BGR2RGB)

faceL=fr.face_locations(imgE)[0]
encodeE=fr.face_encodings(imgE)[0]
cv2.rectangle(imgE,(faceL[3],faceL[0]),(faceL[1],faceL[2]),(255,0,255),2)

faceLT=fr.face_locations(imgT)[0]
encodeT=fr.face_encodings(imgT)[0]
cv2.rectangle(imgT,(faceLT[3],faceLT[0]),(faceLT[1],faceLT[2]),(255,0,255),2)

res = fr.compare_faces([encodeE],encodeT)
faceD=fr.face_distance([encodeE],encodeT)
cv2.putText(imgT, f'{res}{round(faceD[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
print(res,faceD)

cv2.imshow("Image E",imgE)
cv2.imshow("Image T",imgT)
cv2.waitKey(0)
cv2.destroyAllWindows()
