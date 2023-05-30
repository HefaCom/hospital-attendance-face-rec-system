import cv2
import os
import mysql.connector
import tkinter as tk
import appointments
from datetime import datetime, timedelta
from tkinter import ttk
from tkinter import *
import attendance
import tkinter.messagebox as messagebox
import show_doctors
import patient_reg
#import logout
def admin():
    # Create a window for the GUI
    root = tk.Tk()
    root.configure(bg='gray')
    root.title("Patient Booking System")
    # Set the window size and position
    w = 1200
    h = 700
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    label = tk.Label(root, text='Doctor Appointment System.', font=('TkDefaultFont', 16, 'bold'), foreground='red')
    label.pack(pady=10)
    label = tk.Label(root, text='Admin Panel', font=('TkDefaultFont', 14, 'bold'), foreground='blue')
    label.pack(pady=50)

    frame2 = Frame(root)
    frame2.pack(pady=10)
    capture_button = tk.Button(frame2, text="Make Appointments", command=appointments.register,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='blue',width=20)
    capture_button.pack(padx=15, pady=15) 

    attendance_button = tk.Button(frame2, text="Patient Check-in", command=attendance.attendance, font=('TkDefaultFont', 14, 'bold'), foreground='white', background='cyan', width=20)
    attendance_button.pack(padx=15, pady=15)

    doc_button = tk.Button(frame2, text="View Doctors", command=show_doctors.doc_window, font=('TkDefaultFont', 14, 'bold'), foreground='white', background='red', width=20)
    doc_button.pack(padx=15, pady=15)

    doc_button = tk.Button(frame2, text="Register Patient", command=patient_reg.patient_reg, font=('TkDefaultFont', 14, 'bold'), foreground='white', background='green', width=20)
    doc_button.pack(padx=15, pady=15)
    root.mainloop()