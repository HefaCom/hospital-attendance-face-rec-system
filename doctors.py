import tkinter as tk
from tkinter import messagebox
import mysql.connector
import show_doctors
# create tkinter window
def add_doc():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance"
    )
    root = tk.Tk()
    root.configure(bg='gray')
    root.title('Login Form')

    # Set the window size and position
    w = 600
    h = 500
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))



    label = tk.Label(root, text='Doctor Appointment System ', font=('TkDefaultFont', 16, 'bold'), foreground='red',background="gray")
    label.pack(pady=5)
    label = tk.Label(root, text=' Add Doctor', font=('TkDefaultFont', 16, 'bold'), foreground='blue',background="gray")
    label.pack(pady=5)
    # create entry widgets
    d_username = tk.Label(root, text='Doctor Name: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
    d_username.pack(pady=5)
    d_username = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
    d_username.pack()

    spe = tk.Label(root, text='Specialization: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
    spe.pack(pady=5)
    spe_entry = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
    spe_entry.pack()

    d = tk.Label(root, text='Department: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
    d.pack(pady=5)
    dep_entry = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
    dep_entry.pack()

    e = tk.Label(root, text='Email: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
    e.pack(pady=5)
    email_entry = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
    email_entry.pack()

    p = tk.Label(root, text='Phone: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
    p.pack(pady=5)
    phone_entry = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
    phone_entry.pack()

    add = tk.Label(root, text='Address: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
    add.pack(pady=5)
    address_entry = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
    address_entry.pack()


    # get cursor object
    cursor = mydb.cursor()

    # define insert function
    def insert_data():
        # get values from entry widgets
        doctor_name = d_username.get()
        specialization = spe_entry.get()
        department = dep_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()

        # insert data into database if all fields are not empty
        if doctor_name and specialization and department and email and phone and address:
            sql = "INSERT INTO doctors (name, specialization, department, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (doctor_name, specialization, department, email, phone, address)
            cursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Insertion Status", "Doctor details added successfully!")
            show_doctors.doc_window
            # Clear the input fields
            d_username.delete(0, tk.END)
            spe_entry.delete(0, tk.END)
            dep_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            address_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Insertion Status", "All fields are required.")
    def show():
        insert_data()
        show_doctors.doc_window()
        root.destroy()
    # create button to login
    button_login = tk.Button(root, text='Add Doctor', command=insert_data,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='blue',width=15)
    button_login.pack(pady=10)

    # start the main tkinter event loop
    root.mainloop()
