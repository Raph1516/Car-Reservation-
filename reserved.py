from tkinter import *
from tkinter import ttk
import sqlite3

def setup_database():
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            address TEXT NOT NULL,
            car TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

setup_database()

def showChooseWindow():
    window.withdraw()
    choose_window = Toplevel()
    choose_window.geometry('600x400+485+175')
    choose_window.title('Car Reservation System')
    choose_window.config(background='#FEFEF2', pady=40)

    Label(choose_window, text='Choose', font=('Poppins', 18), bg='#FFFDC8').pack(pady=20)

    Button(choose_window, text='Log In', font=('Consolas', 15), padx=15,
           command=lambda: [choose_window.destroy(), logIn()],
           bg='blue', fg='white', activebackground='darkblue').pack(pady=10)

    Button(choose_window, text='Sign Up', font=('Consolas', 15), padx=15,
           command=lambda: [choose_window.destroy(), signUp()],
           bg='blue', fg='white', activebackground='darkblue').pack(pady=10)

    choose_window.protocol("WM_DELETE_WINDOW", lambda: [choose_window.destroy(), window.deiconify()])

def signUp():
    def toggle_password_visibility(entry, show_button):
        if entry.cget('show') == '*':
            entry.config(show='')
            show_button.config(text='Hide')
        else:
            entry.config(show='*')
            show_button.config(text='Show')

    def sign_up_action():
        username_val = username.get().strip()
        password_val = pw.get().strip()
        confirm_pw_val = confirm_pw.get().strip()

        if not username_val or not password_val or not confirm_pw_val:
            error_label.config(text="All fields are required!", fg="red")
            return

        if password_val != confirm_pw_val:
            error_label.config(text="Passwords do not match!", fg="red")
            return

        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username_val, password_val))
            conn.commit()
            error_label.config(text="Account created successfully!", fg="green")
            signup.after(2000, lambda: [signup.destroy(), showChooseWindow()])
        except sqlite3.IntegrityError:
            error_label.config(text="Username already exists!", fg="red")
        finally:
            conn.close()

    signup = Toplevel()
    signup.geometry("500x400+485+175")
    signup.title('SignUp Form')

    username = StringVar()
    pw = StringVar()
    confirm_pw = StringVar()

    Label(signup, text='Sign Up', font=('Consolas', 25)).pack(pady=10)

    frame = Frame(signup)
    frame.pack(pady=10)

    Label(frame, text='Username:', font=('Poppins', 15)).grid(row=0, column=0, sticky=E)
    Entry(frame, textvariable=username).grid(row=0, column=1, pady=5)

    Label(frame, text='Password:', font=('Poppins', 15)).grid(row=1, column=0, sticky=E)
    password_entry = Entry(frame, textvariable=pw, show='*')
    password_entry.grid(row=1, column=1, pady=5)

    show_password_btn = Button(frame, text='Show', command=lambda: toggle_password_visibility(password_entry, show_password_btn))
    show_password_btn.grid(row=1, column=2)

    Label(frame, text='Confirm Password:', font=('Poppins', 15)).grid(row=2, column=0, sticky=E)
    confirm_pw_entry = Entry(frame, textvariable=confirm_pw, show='*')
    confirm_pw_entry.grid(row=2, column=1, pady=5)

    show_confirm_password_btn = Button(frame, text='Show', command=lambda: toggle_password_visibility(confirm_pw_entry, show_confirm_password_btn))
    show_confirm_password_btn.grid(row=2, column=2)

    error_label = Label(signup, text="", font=('Poppins', 12))
    error_label.pack(pady=10)

    Button(signup, text='Sign Up', command=sign_up_action, font=('Consolas', 15), padx=10, pady=5,
           bg='blue', fg='white', activebackground='darkblue').pack(pady=10)

def show_main_menu():
    main_menu = Toplevel()
    main_menu.geometry('500x400+490+175')
    main_menu.title('Main Menu')
    main_menu.config(background='#FFFACD')

    Label(main_menu, text='Main Menu', font=('Consolas', 25), bg='#FFFACD').pack(pady=20)

    Button(main_menu, text='Customer Form', font=('Consolas', 15), padx=15,
           bg='blue', fg='white', activebackground='darkblue', command=open_customer_window).pack(pady=10)
    Button(main_menu, text='Show Data', font=('Consolas', 15), bg='blue', fg='white',
           command=show_database).pack(pady=20)
    Button(main_menu, text='Logout', font=('Consolas', 15), padx=15,
           bg='blue', fg='white', activebackground='darkblue',
           command=main_menu.destroy).pack(pady=10)

def logIn():
    def toggle_password_visibility(entry, show_button):
        if entry.cget('show') == '*':
            entry.config(show='')
            show_button.config(text='Hide')
        else:
            entry.config(show='*')
            show_button.config(text='Show')

    def log_in_action():
        username_val = username.get().strip()
        password_val = pw.get().strip()

        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username_val, password_val))
        user = cursor.fetchone()
        conn.close()

        if user:
            error_label.config(text="Login successful!", fg="green")
            login.after(1000, lambda: [login.destroy(), show_main_menu()]) 
        else:
            error_label.config(text="Invalid username or password", fg="red")

    login = Toplevel()
    login.geometry("500x400+485+175")
    login.title('Log In')

    username = StringVar()
    pw = StringVar()
  
    Label(login, text='Log In', font=('Consolas', 25)).pack(pady=10)

    frame = Frame(login)
    frame.pack(pady=10)

    Label(frame, text='Username:', font=('Poppins', 15)).grid(row=0, column=0, sticky=E)
    Entry(frame, textvariable=username).grid(row=0, column=1, pady=5)

    Label(frame, text='Password:', font=('Poppins', 15)).grid(row=1, column=0, sticky=E)
    password_entry = Entry(frame, textvariable=pw, show='*')
    password_entry.grid(row=1, column=1, pady=5)
    
    show_password_btn = Button(frame, text='Show', command=lambda: toggle_password_visibility(password_entry, show_password_btn))
    show_password_btn.grid(row=1, column=2)

    error_label = Label(login, text="", font=('Poppins', 12))
    error_label.pack(pady=10)

    Button(login, text='Log In', command=log_in_action, font=('Consolas', 15), padx=10, pady=5,
           bg='blue', fg='white', activebackground='darkblue').pack(pady=10)

def open_customer_window():
    customer_window = Toplevel()
    customer_window.geometry('600x600+485+175')
    customer_window.title('Customer Details')
    customer_window.config(background='#FFFACD')

    Label(customer_window, text='Customer Details', font=('Consolas', 20), bg='#FFFACD').pack(pady=20)

    Label(customer_window, text='Name:', font=('Consolas', 12), bg='#FFFACD').pack(anchor=W, padx=20, pady=5)
    name_entry = Entry(customer_window, font=('Consolas', 12))
    name_entry.pack(padx=20, fill=X)

    Label(customer_window, text='Contact No.:', font=('Consolas', 12), bg='#FFFACD').pack(anchor=W, padx=20, pady=5)
    contact_entry = Entry(customer_window, font=('Consolas', 12))
    contact_entry.pack(padx=20, fill=X)

    Label(customer_window, text='Address:', font=('Consolas', 12), bg='#FFFACD').pack(anchor=W, padx=20, pady=5)
    address_entry = Entry(customer_window, font=('Consolas', 12))
    address_entry.pack(padx=20, fill=X)

    Label(customer_window, text='Car to be Reserved:', font=('Consolas', 12), bg='#FFFACD').pack(anchor=W, padx=20, pady=5)

    selected_car = StringVar()
    selected_car.set("None")

    def select_car(car):
        selected_car.set(car)

    car_frame = Frame(customer_window, bg='#FFFACD')
    car_frame.pack(pady=10)

    cars = ['Toyota Fortuner 2025', 'Toyota Rush 2025', 'Toyota Inova 2025']
    for car in cars:
        Button(car_frame, text=car, font=('Consolas', 12), bg='blue', fg='white', activebackground='darkblue',
               command=lambda c=car: select_car(c)).pack(side=LEFT, padx=5)

    Label(customer_window, textvariable=selected_car, font=('Consolas', 12), bg='#FFFACD').pack(pady=5)

    Label(customer_window, text='Quantity:', font=('Consolas', 12), bg='#FFFACD').pack(anchor=W, padx=20, pady=5)
    quantity_entry = Entry(customer_window, font=('Consolas', 12))
    quantity_entry.pack(padx=20, fill=X)

    def submit_details():
        name = name_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()
        car = selected_car.get()
        quantity = quantity_entry.get()

        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, contact, address, car, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, contact, address, car, quantity))
        conn.commit()
        conn.close()

        customer_window.destroy()

    Button(customer_window, text='Submit', font=('Consolas', 15), bg='green', fg='white',
           command=submit_details).pack(pady=10)

def show_database():
        def fetch_data():
            conn = sqlite3.connect('customers.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
            conn.close()
            return rows

        def delete_customer():
            selected_item = tree.selection()
            if not selected_item:
                return

            customer_id = tree.item(selected_item[0])["values"][0]
            conn = sqlite3.connect('customers.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM customers")
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'customers'")

            conn.commit()
            conn.close()

            tree.delete(selected_item)


        database_window = Toplevel()
        database_window.title("Customer Data")
        database_window.geometry("800x400+450+175")

        frame = Frame(database_window)
        frame.pack(fill=BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact", "Address", "Car", "Quantity"), show="headings")
        tree.pack(fill=BOTH, expand=True, side=LEFT)

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.configure(yscroll=scrollbar.set)

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Contact", text="Contact")
        tree.heading("Address", text="Address")
        tree.heading("Car", text="Car")
        tree.heading("Quantity", text="Quantity")

        tree.column("ID", width=50, anchor=CENTER)
        tree.column("Name", width=100, anchor=W)
        tree.column("Contact", width=100, anchor=W)
        tree.column("Address", width=150, anchor=W)
        tree.column("Car", width=100, anchor=W)
        tree.column("Quantity", width=80, anchor=CENTER)

        for row in fetch_data():
            tree.insert("", END, values=row)

        delete_button = Button(database_window, text="Delete Selected", font=('Consolas', 12), bg='red', fg='white',
                               command=delete_customer)
        delete_button.pack(pady=20)


window = Tk()
window.geometry("800x400+400+150")
window.title('Car Reservation System')
window.config(background='#FEFEF2', padx=80, pady=60)

Label(window, text='Welcome to Car Reservation System!', font=('Consolas', 18), bg='#FFFDC8').pack(pady=20)
Button(window, text='Start', font=('Consolas', 15), padx=15, command=showChooseWindow,
       bg='blue', fg='white', activebackground='darkblue').pack(pady=20)

window.mainloop()
    