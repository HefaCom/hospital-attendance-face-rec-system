import cv2
import os
import mysql.connector
import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from tkinter import ttk
import attendance
import tkinter.messagebox as messagebox
import show_doctors
#import logout
# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attendance"
)

cursor = db.cursor()


# Create a table for storing the user's images
table_name = "bookings"
cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), dName  VARCHAR(255), room VARCHAR(255),phone VARCHAR(255),address VARCHAR(255), image BLOB, appDate  DATETIME DEFAULT CURRENT_TIMESTAMP(), time VARCHAR(255)  , bDate DATETIME DEFAULT CURRENT_TIMESTAMP())")

cursor.execute(f"CREATE TABLE IF NOT EXISTS doctors (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),department VARCHAR(255), major VARCHAR(255))")
# Load the pre-trained frontal face classifier XML file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



def register():
    # Create a window for the GUI
    root = tk.Tk()
    root.title("Patient Booking System")
    # Set the window size and position
    w = 800
    h = 750
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    label = tk.Label(root, text='Doctor Appointment System.', font=('TkDefaultFont', 16, 'bold'), foreground='red')
    label.pack(pady=10)
    result_label = tk.Label(root, text="")
    # Define the function to query the database
    def query_database():
               
        search_id =search_entry.get()
        # Execute the MySQL query
        cursor = db.cursor()
        # execute the SQL query
        sql = "SELECT name,phone,address FROM patients WHERE id=%s"
        val = (search_entry.get(),)
        cursor.execute(sql, val)
        
        # fetch the results
        result = cursor.fetchone()

        # Check if a result was found
        if result is not None:
            # Display the results in the text boxes
            name_entry.delete(0, tk.END)
            name_entry.insert(0, result[0])
            contact_entry.delete(0, tk.END)
            contact_entry.insert(0, result[1])
            address_entry.delete(0, tk.END)
            address_entry.insert(0, result[2])
            result_label.config(text="Record found.")
        else:
            result_label.config(text="Record not found.", fg="red")
            messagebox.showinfo("No Results", "No results found for '" + search_id + "'.")
            name_entry.delete(0, tk.END)
            contact_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)

    
    search_entry = tk.Entry(root ,background='#EFEFEF', foreground='black', font=('Arial', 14), borderwidth=2)
    search_entry.pack()
    search_button = tk.Button(root, text="Search with ID", command=query_database,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='green',width=20)
    search_button.pack(padx=10, pady=5) 
    # Prompt the user for their name
    name_label = tk.Label(root, text="Enter patient name:",font=('TkDefaultFont', 13, 'bold'), foreground='black')
    name_label.pack(padx=10, pady=5)
    name_entry = tk.Entry(root ,background='#EFEFEF', foreground='black', font=('Arial', 14), borderwidth=2)
    name_entry.pack()

    contact_label = tk.Label(root, text="Enter patient contact:",font=('TkDefaultFont', 13, 'bold'), foreground='black')
    contact_label.pack(padx=10, pady=5)
    
    contact_entry = tk.Entry(root ,background='#EFEFEF', foreground='black', font=('Arial', 14), borderwidth=2)
    contact_entry.pack()

    address_label = tk.Label(root, text="Enter patient address:",font=('TkDefaultFont', 13, 'bold'), foreground='black')
    
    address_label.pack(padx=10, pady=5)
    address_entry = tk.Entry(root ,background='#EFEFEF', foreground='black', font=('Arial', 14), borderwidth=2)
    address_entry.pack()


    room_label = tk.Label(root, text="Pick room:",font=('TkDefaultFont', 13, 'bold'), foreground='black')
    room_label.pack(padx=10, pady=5)
    rooms = ["Room 1", "Room 2", "Room 3"]
    combo_box1 = ttk.Combobox(root, values=rooms,background='#EFEFEF', foreground='black', font=('Arial', 14))
    combo_box1.current(0)
    combo_box1.pack()

    # gender_label = tk.Label(root, text="Gender:",font=('TkDefaultFont', 13, 'bold'), foreground='black')
    # gender_label.pack(padx=10, pady=5)
    # gender = ["Male", "Female"]
    # combo_box2 = ttk.Combobox(root, values=gender,background='#EFEFEF', foreground='black', font=('Arial', 14))
    # combo_box2.pack()
    
    # Execute a SELECT query to retrieve data from the database
    cursor.execute("SELECT name FROM doctors")

    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Extract the values from the rows and store them in a list
    items = [row[0] for row in rows]



    # Create a tkinter combobox widget and set its values
    doc_label = tk.Label(root, text="Pick doctor:",font=('TkDefaultFont', 13, 'bold'), foreground='black')
    doc_label.pack(padx=10, pady=5)
    combo_box = ttk.Combobox(root, values=items,background='#EFEFEF', foreground='black', font=('Arial', 14), )

    # Set the default value for the combo box
    combo_box.current(0)

    # Pack the combo box widget
    combo_box.pack(padx=10, pady=10)
  
    
        # set minimum date to today
    today = datetime.now().date()

    # disable weekends
    def check_weekend(date):
        return date.weekday() in [5, 6]

    # create date label and entry widget
    date_label = tk.Label(root, text="Pick Date:", font=('TkDefaultFont', 13, 'bold'), foreground='black')
    date_label.pack(padx=10)
    date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', 
                        borderwidth=2, date_pattern='yyyy-mm-dd', mindate=today, 
                        state='readonly', disabledforeground='red',
                        disabledbackground=root.cget('bg'), 
                        #disabledforeground=root.cget('fg'), 
                        disabledweekendforeground='red', 
                        weekenddisabled=check_weekend)
    date_entry.pack()
    
    time_label = tk.Label(root, text='Pick time:')
    time_label.pack(side='left', padx=10)
    
    time_combobox = ttk.Combobox(root, values=["9:00", "12:00","3:00","6:00"], state='readonly', width=5)
    time_combobox.current(0)
    time_combobox.pack(side='left')

    # create meridian combobox
    meridian_label = tk.Label(root, text='Meridian:')
    meridian_label.pack(side='left', padx=10)
    meridian_combobox = ttk.Combobox(root, values=['AM', 'PM'], state='readonly', width=5)
    meridian_combobox.current(0)
    meridian_combobox.pack(side='left')


    # function to get selected time
    
      
    dataset_dir = "images"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Create a label for the feedback message
    feedback_label = tk.Label(root)
    feedback_label.pack()

    # Define a function to capture the patient's face
    def capture_face():
        
        name = name_entry.get()
        room = combo_box1.get()
        doctor = combo_box.get()
        phone = contact_entry.get()
        address = address_entry.get()
        # gender = combo_box2.get()
        appDate = date_entry.get_date()
        time = time_combobox.get()+" "+ meridian_combobox.get()
        print("Booking time",time)
        # Capture the user's images and store them in the dataset directory
        image_count = 0
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect the faces in the grayscale image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            # Draw a rectangle around each detected face and save the image
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                image_count += 1
                k= cv2.waitKey(1)
                

                if k%256==32:
                    image_path = os.path.join(dataset_dir, f"{name.upper()}.jpg")
                    cv2.imwrite(image_path, frame[y:y + h, x:x + w])
                    
                    cursor.execute(f"INSERT INTO {table_name} (name,dName,room, phone, address, image, appDate,time) VALUES (%s, %s,%s,  %s,%s,%s,  %s,%s)", (name,doctor,room,phone,address, open(image_path, "rb").read(),appDate,time))
                    messagebox.showinfo("Booking Success", f"{name.upper()} details captured successfully!\n to come on {appDate} at {time}")
                    name_entry.delete(0, tk.END)
                    contact_entry.delete(0, tk.END)
                    address_entry.delete(0, tk.END)
                   
                    db.commit()

            # Display the frame
            cv2.imshow('frame', frame)

            # Exit if the user presses the 'q' key or captured 20 images
            if cv2.waitKey(1) == ord('q') or image_count == 500:
                break

        # Release the webcam and close the window
        cap.release()
        cv2.destroyAllWindows()

    # Create a button for capturing the patient's face
    label = tk.Label(root, text='Actions ', font=('TkDefaultFont', 12, 'bold'), foreground='red')
    label.pack(pady=5)
    

    def capture():
        if not all(entry.get() for entry in (name_entry, address_entry, contact_entry)):
            messagebox.showerror("EntryError", "Please fill all the entries.")
        else:
            capture_face()

    capture_button = tk.Button(root, text="Make Appointment", command=capture,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='blue',width=20)
    capture_button.pack(padx=10, pady=5) 

    # attendance_button = tk.Button(root, text="Mark Attendance", command=attendance.attendance, font=('TkDefaultFont', 14, 'bold'), foreground='white', background='cyan', width=20)
    # attendance_button.pack(padx=10, pady=5)

    # attendance_button = tk.Button(root, text="Show Doctors", command=show_doctors.doc_window, font=('TkDefaultFont', 14, 'bold'), foreground='white', background='red', width=20)
    # attendance_button.pack(padx=10, pady=5)
    

    # create logout button
   # logout_button = tk.Button(root, text='Logout', command=logout)
   # logout_button.pack(pady=5)
    # Run the GUI window
    root.mainloop()
