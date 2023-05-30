import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
import doctors
# create a database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="attendance"
)

# create a cursor object
mycursor = mydb.cursor()
def doc_window():
    # define function to display all doctors in the database
    def show_doctors():
        # clear existing entries from the treeview widget
        for i in treeview.get_children():
            treeview.delete(i)

        # select all doctors from the database
        mycursor.execute("SELECT * FROM doctors")
        result = mycursor.fetchall()

        # insert each doctor's details as a row in the treeview widget
        for i in result:
            treeview.insert("", END, text=i[0], values=(i[1], i[2], i[3], i[4], i[5], i[6]))
        
        # set scrollbar to bottom
        treeview.yview_moveto(1)

    # define function to delete a doctor from the database
    def delete_doctor():
        # get the selected doctor's ID
        try:
            selected_item = treeview.selection()[0]
        except IndexError:
            messagebox.showerror("Error", "No doctor selected!")
            return
        doctor_id = treeview.item(selected_item)['text']

        # ask for user confirmation
        confirmed = messagebox.askyesno("Confirm", f"Are you sure you want to delete doctor {doctor_id}?")

        if not confirmed:
            return

        # delete the doctor from the database
        mycursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
        mydb.commit()

        # display success message
        messagebox.showinfo("Success", "Doctor deleted successfully!")

        # refresh the treeview widget
        show_doctors()

    # create a new tkinter window
    root = tk.Tk()
    root.configure(bg='gray')
    root.title("Doctor Appointment System")

    # Set the window size and position
    w = 800
    h = 600
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


    
    label = tk.Label(root, text='Doctor Appointment System ', font=('TkDefaultFont', 16, 'bold'), foreground='red',background="gray")
    label.pack(pady=10)
    label = tk.Label(root, text=' Manage Doctors ', font=('TkDefaultFont', 16, 'bold'), foreground='blue',background="gray")
    label.pack(pady=20)
    # create a frame for the treeview widget and scrollbar
    frame1 = Frame(root)
    frame1.pack(pady=10)

    # create a treeview widget to display the doctors
    treeview = ttk.Treeview(frame1, columns=("Name", "Specialization", "Department", "Email", "Phone", "Address"), show="headings")
    treeview.column("Name", width=100)
    treeview.column("Specialization", width=100)
    treeview.column("Department", width=100)
    treeview.column("Email", width=150)
    treeview.column("Phone", width=100)
    treeview.column("Address", width=150)
    treeview.heading("Name", text="Name", anchor=CENTER)
    treeview.heading("Specialization", text="Specialization", anchor=CENTER)
    treeview.heading("Department", text="Department", anchor=CENTER)
    treeview.heading("Email", text="Email", anchor=CENTER)
    treeview.heading("Phone", text="Phone", anchor=CENTER)
    treeview.heading("Address", text="Address", anchor=CENTER)

    # configure the headings to be bold with a blue background and white font
    treeview.tag_configure("heading", font=("TkDefaultFont", 12, "bold"), foreground="white", background="blue")

    # add a scrollbar to the frame
    scrollbar = ttk.Scrollbar(frame1, orient=VERTICAL, command=treeview.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    treeview.configure(yscrollcommand=scrollbar.set)

    # pack the treeview widget to the left of the frame
    treeview.pack(side=LEFT, fill=BOTH, expand=True)

    # create a button to show all doctors
    # show_button = Button(root, text="Show Doctors", command=show_doctors,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='blue',width=15)
    # show_button.pack(pady=10)
    global frame2
    # create a frame for the control buttons
    frame2 = Frame(root)
    frame2.pack(pady=10)

    # create a button to delete the selected doctor
    delete_button = Button(frame2, text="Delete Doctor", command=delete_doctor,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='red',width=15)
    delete_button.pack(side=LEFT, padx=2)

    # def addDoc():
    #     doctors.add_doc
    #     frame2.destroy()
    # # create a button to edit the selected doctor (not implemented in this example)
    edit_button = Button(frame2, text="Add Doctor",command=doctors.add_doc,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='red',width=15)
    edit_button.pack(side=LEFT, padx=2)
    show_doctors()
    root.mainloop()
