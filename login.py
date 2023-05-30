import tkinter as tk
from tkinter import messagebox
import mysql.connector
#import register
import admin
# create tkinter window
root = tk.Tk()
root.configure(bg='gray')
root.title('Login Form')

# Set the window size and position
w = 400
h = 400
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw - w) / 2
y = (sh - h) / 2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))



label = tk.Label(root, text='Doctor Appointment System ', font=('TkDefaultFont', 16, 'bold'), foreground='red',background="gray")
label.pack(pady=10)
label = tk.Label(root, text=' User Login ', font=('TkDefaultFont', 16, 'bold'), foreground='blue',background="gray")
label.pack(pady=20)
# create entry widgets
label_username = tk.Label(root, text='Username: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
label_username.pack(pady=5)
entry_username = tk.Entry(root, width=20, background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
entry_username.pack()
label_password = tk.Label(root, text='Password: ',font=('TkDefaultFont', 14, 'bold'), foreground='black',background="gray")
label_password.pack(pady=5)

entry_password = tk.Entry(root, width=20, show='*',background='#EFEFEF', foreground='black', font=('Arial', 12), borderwidth=2)
entry_password.pack()

# function to check login credentials
def login():
    # connect to MySQL database
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="attendance"
        )
        cursor = db.cursor()
    except mysql.connector.Error as err:
        messagebox.showerror('Error', f'Error connecting to MySQL database: {err}')
        return
    
    # check login credentials
    username = entry_username.get()
    password = entry_password.get()
    query = f'SELECT * FROM users WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    
    if result:
        #messagebox.showinfo('Success', 'Login successful!')
        # close login form
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        root.destroy() 
        admin.admin()
        
    else:
        messagebox.showerror('Error', 'Invalid username or password')
    
    db.close()

# create button to login
button_login = tk.Button(root, text='Login', command=login,font=('TkDefaultFont', 14, 'bold'), foreground='white',background='blue',width=15)
button_login.pack(pady=10)

# start the main tkinter event loop
root.mainloop()
