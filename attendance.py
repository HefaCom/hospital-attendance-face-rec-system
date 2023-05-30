import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import datetime
import mysql.connector
import base64
import tkinter as tk
from tkinter import messagebox
def attendance():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance"
    )
    cursor = conn.cursor()
    # Create a table for storing the attendance records
    table_name = "attendance"
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),dName VARCHAR(255), image BLOB,date DATE)")

    path = 'images'
    images= []
    classN = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classN.append(os.path.splitext(cl)[0])
    print(classN)
    
    def findEnc(images):
        try:
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = fr.face_encodings(img)[0]
                encodeList.append(encode)
            messagebox.showinfo('Message', 'Encoding complete!')
            return encodeList
        except Exception as e:
            messagebox.showerror('Error', f'Error encoding images: {e} \n An image with a blurry face identified, \n DELETE IT FIRST!')
    # cursor.execute("CREATE TABLE  IF NOT EXISTS sessions (name VARCHAR(255),dName VARCHAR(255), date_time DATETIME)")

    # def markAtt(name):
    #     cursor = conn.cursor()
    #     # Check if the patient has already been marked present
    #     cursor.execute("SELECT * FROM sessions WHERE name = %s", (name,))
    #     result = cursor.fetchall()
    #     if len(result) == 0:
    #         # Insert a new row into the attendance table
    #         dtString = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #         sql = "INSERT INTO sessions (name, dName, date_time) VALUES (%s, %s,%s)"
    #         val = (name, dtString)
    #         cursor.execute(sql, val)
    #         conn.commit()
    # #markAtt('a')
    
    encodeListKnown =findEnc(images)
    print("Encoding complete!")
    print(f'{len(encodeListKnown)} images were found and encoded!')


    cap = cv2.VideoCapture(0)
    #cap.set(3,1280)
    #cap.set(4,720)
    while True:
        success,img = cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        #cv2.imshow("Attendance Check:",img)
        #cv2.waitKey(1)


        facesCurFrame = fr.face_locations(imgS)

        encodeCurFrame = fr.face_encodings(imgS,facesCurFrame)
        for encodeF, faceLoc in zip(encodeCurFrame,facesCurFrame):
            matches = fr.compare_faces(encodeListKnown,encodeF)
            faceD = fr.face_distance(encodeListKnown,encodeF)
            print(faceD)
            matchInd = np.argmin(faceD)
            if matches[matchInd]:
                name = classN[matchInd].upper()
                today = datetime.now().date()

                cursor.execute("SELECT room as room_number, dName as doctor_name  FROM bookings WHERE name = %s AND appDate >= %s", (name, today,))
                results = cursor.fetchall()
                if len(results) > 0:
                    room_number, doctor_name = results[0]
                else:
                    room_number, doctor_name = "Expired app!", None
                                
                print(name)
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)

                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)

                cv2.putText(img, f"Patient Found: {name }!", (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),2)
                cv2.putText(img, f"Meet: {doctor_name}, in room: {room_number}", (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),2)
                cv2.putText(img,name.upper(),(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                # Convert the image to JPEG format
                _, jpeg_image = cv2.imencode('.jpg', img)

                # Encode the image as base64 string
                b64_image = base64.b64encode(jpeg_image).decode('utf-8')

                # Save the image and name in the database
                t = datetime.now()
                dtString = t.strftime('%d/%m/%Y %H:%M:%S')
                k= cv2.waitKey(1)
               # markAtt(name)
                if k%256==32:
                    #markAtt(name)
                    cursor = conn.cursor()
                    cursor.execute(f'INSERT INTO  {table_name} (name, dName,image,date) VALUES (%s, %s,%s,%s)', (name,doctor_name, b64_image,t))
                    conn.commit()



            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, 'No Booking Found', (200,  50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "Unknown.!", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # Exit if the user presses the 'q' key or captured 20 images
        if cv2.waitKey(1) == ord('q') :
            break

        cv2.imshow("Attendance", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

