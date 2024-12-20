import sqlite3
from tkinter import *

def reset_ids(table_name):
    try:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
        conn.commit()
        print(f"Auto-increment ID reset for table '{table_name}'.")
    except Exception as e:
        print(f"Error resetting IDs: {e}")

conn = sqlite3.connect('car_reservation_system.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    contact TEXT,
                    address TEXT,
                    car TEXT,
                    quantity INTEGER)''')
conn.commit()

reset_ids('users')
reset_ids('reservations')

root = Tk()
root.geometry('1000x750+300+20')
root.title("Car Reservation System")
root.resizable(False, False)

canvas = Canvas(root, width=1000, height=750, bg="black")
canvas.pack()

try:
    bg = PhotoImage(file='background.png')
    show_icon = PhotoImage(file="show.png")
    hide_icon = PhotoImage(file="unseen.png")
except TclError:
    bg = None
    show_icon, hide_icon = None, None

def reset_ids(table_name):
    try:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
        conn.commit()
        print(f"Auto-increment ID reset for table '{table_name}'.")
    except Exception as e:
        print(f"Error resetting IDs: {e}")

def clear_canvas():
    canvas.delete("all")
    if bg:
        canvas.create_image(0, 0, image=bg, anchor="nw")

def toggle_password(entry, button):
    if entry.cget("show") == "*":
        entry.config(show="")
        button.config(image=hide_icon)
    else:
        entry.config(show="*")
        button.config(image=show_icon)

def show_login():
    clear_canvas()
    canvas.create_text(500, 100, text="Login", font=("Arial", 25), fill="white")

    canvas.create_text(300, 200, text="Username:", font=("Arial", 15), fill="white", anchor="e")
    username_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 200, window=username_entry, width=300)

    canvas.create_text(300, 250, text="Password:", font=("Arial", 15), fill="white", anchor="e")
    password_entry = Entry(root, font=("Arial", 15), show="*")
    canvas.create_window(500, 250, window=password_entry, width=300)

    if show_icon:
        show_pw_btn = Button(root, image=show_icon, command=lambda: toggle_password(password_entry, show_pw_btn), borderwidth=0)
        canvas.create_window(670, 250, window=show_pw_btn, width=30, height=30)

    error_label = Label(root, text="", font=("Arial", 12), bg="black", fg="red")
    canvas.create_window(500, 300, window=error_label)

    def authenticate():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and user[0] == password:
            show_main_form(username)
        else:
            error_label.config(text="Invalid username or password!")

    login_btn = Button(root, text="Login", font=("Arial", 12), bg="blue", fg="white", command=authenticate)
    canvas.create_window(500, 350, window=login_btn, width=200)

    signup_btn = Button(root, text="Sign Up", font=("Arial", 12), bg="blue", fg="white", command=show_sign_up)
    canvas.create_window(500, 400, window=signup_btn, width=200)

def show_main_form(username):
    clear_canvas()
    canvas.create_text(500, 50, text=f"Welcome, {username}!", font=("Arial", 25), fill="white")

    customer_info_btn = Button(root, text="Customer Info", font=("Arial", 15), bg="blue", fg="white", command=lambda: show_customer_info(username))
    canvas.create_window(500, 200, window=customer_info_btn, width=200)

    show_data_btn = Button(root, text="Show Data", font=("Arial", 15), bg="blue", fg="white", command=lambda: show_data(username))
    canvas.create_window(500, 250, window=show_data_btn, width=200)

    logout_btn = Button(root, text="Log Out", font=("Arial", 15), bg="blue", fg="white", command=show_login)
    canvas.create_window(500, 300, window=logout_btn, width=200)

def show_data(username):
    print(f"Username passed to show_data: {username}")
    clear_canvas()
    canvas.create_text(500, 50, text="Reservation Data", font=("Arial", 25), fill="white")

    cursor.execute("SELECT * FROM reservations")
    rows = cursor.fetchall()

    selected_id = IntVar(value=-1)

    if rows:
        canvas.create_text(100, 100, text="Name", font=("Arial", 12, "bold"), fill="white", anchor="w")
        canvas.create_text(300, 100, text="Contact No.", font=("Arial", 12, "bold"), fill="white", anchor="w")
        canvas.create_text(470, 100, text="Address", font=("Arial", 12, "bold"), fill="white", anchor="w")
        canvas.create_text(650, 100, text="Car", font=("Arial", 12, "bold"), fill="white", anchor="w")
        canvas.create_text(820, 100, text="Quantity", font=("Arial", 12, "bold"), fill="white", anchor="w")

        for idx, row in enumerate(rows):
            y_position = 130 + idx * 30
    
            name_text = row[1] if len(row[1]) <= 20 else row[1][:17] + "..."
    
            name_btn = Button(
                root, text=name_text, font=("Arial", 12), bg="blue", fg="white", anchor="w",
                command=lambda r=row: selected_id.set(r[0])
            )
            canvas.create_window(100, y_position, window=name_btn, width=180, anchor="w")

            canvas.create_text(300, y_position, text=row[2], font=("Arial", 12), fill="white", anchor="w")
            canvas.create_text(470, y_position, text=row[3], font=("Arial", 12), fill="white", anchor="w")
            canvas.create_text(650, y_position, text=row[4], font=("Arial", 12), fill="white", anchor="w")
            canvas.create_text(820, y_position, text=str(row[5]), font=("Arial", 12), fill="white", anchor="w")

    else:
        canvas.create_text(500, 150, text="No data available", font=("Arial", 12), fill="white")

    def delete_reservation():
        selected = selected_id.get()
        if selected == -1:
            error_label.config(text="Please select a record to delete!", fg="red")
        else:
            cursor.execute("DELETE FROM reservations WHERE id = ?", (selected,))
            conn.commit()
            error_label.config(text="Record deleted successfully!", fg="green")
            show_data(username)
    
    def update_reservation():
        selected = selected_id.get()
        if selected == -1:
            error_label.config(text="Please select a record to update!", fg="red")
            return
        
        cursor.execute("SELECT * FROM reservations WHERE id = ?", (selected,))
        row = cursor.fetchone()
        if row:
            update_window = Toplevel(root)
            update_window.title("Update Reservation")
            update_window.geometry("250x300")
            update_window.configure(bg="gray")
            
            Label(update_window, text="Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
            name_entry = Entry(update_window)
            name_entry.grid(row=0, column=1, padx=10, pady=10)
            name_entry.insert(0, row[1])
            
            Label(update_window, text="Contact", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
            contact_entry = Entry(update_window)
            contact_entry.grid(row=1, column=1, padx=10, pady=10)
            contact_entry.insert(0, row[2])
            
            Label(update_window, text="Address", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
            address_entry = Entry(update_window)
            address_entry.grid(row=2, column=1, padx=10, pady=10)
            address_entry.insert(0, row[3])
            
            Label(update_window, text="Car", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
            car_entry = Entry(update_window)
            car_entry.grid(row=3, column=1, padx=10, pady=10)
            car_entry.insert(0, row[4])
            
            Label(update_window, text="Quantity", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10)
            quantity_entry = Entry(update_window)
            quantity_entry.grid(row=4, column=1, padx=10, pady=10)
            quantity_entry.insert(0, row[5])
            
            def save_updates():
                new_name = name_entry.get()
                new_contact = contact_entry.get()
                new_address = address_entry.get()
                new_car = car_entry.get()
                new_quantity = quantity_entry.get()
                
                cursor.execute(
                    "UPDATE reservations SET name = ?, contact = ?, address = ?, car = ?, quantity = ? WHERE id = ?", 
                    (new_name, new_contact, new_address, new_car, new_quantity, selected)
                )
                conn.commit()
                update_window.destroy()
                error_label.config(text="Record updated successfully!", fg="green")
                show_data(username)
            
            save_btn = Button(update_window, text="Save Changes", bg="green", command=save_updates)
            save_btn.grid(row=5, column=0, columnspan=2, pady=20)
    
    error_label = Label(root, text="", font=("Arial", 12), bg="black", fg="red")
    canvas.create_window(500, 500, window=error_label)
    
    delete_btn = Button(root, text="Delete Selected", font=("Arial", 12), bg="red", fg="white", command=delete_reservation)
    canvas.create_window(500, 550, window=delete_btn, width=200)
    
    update_btn = Button(root, text="Update Selected", font=("Arial", 12), bg="green", fg="white", command=update_reservation)
    canvas.create_window(500, 600, window=update_btn, width=200)
    
    back_btn = Button(root, text="Back", font=("Arial", 12), bg="blue", fg="white", command=lambda: show_main_form(username))
    canvas.create_window(500, 650, window=back_btn, width=200)



def show_customer_info(username):
    clear_canvas()
    canvas.create_text(500, 100, text="Customer Info", font=("Arial", 25), fill="white")

    canvas.create_text(300, 200, text="Name:", font=("Arial", 15), fill="white", anchor="e")
    name_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 200, window=name_entry, width=300)

    canvas.create_text(300, 250, text="Contact No.:", font=("Arial", 15), fill="white", anchor="e")
    contact_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 250, window=contact_entry, width=300)

    canvas.create_text(300, 300, text="Address:", font=("Arial", 15), fill="white", anchor="e")
    address_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 300, window=address_entry, width=300)

    canvas.create_text(300, 350, text="Car to be Reserved:", font=("Arial", 15), fill="white", anchor="e")

    selected_car_label = Label(root, text="Selected Car: None", font=("Arial", 12), bg="black", fg="white")
    canvas.create_window(500, 510, window=selected_car_label)

    car_buttons = [
        ("Toyota Fortuner 2025", 300, 420),
        ("Toyota Rush 2025", 500, 420),
        ("Toyota Vios 2025", 700, 420),
        ("Toyota Hi Ace 2025", 300, 460),
        ("Toyota Grandia 2025", 500, 460),
        ("Toyota Raize 2025", 700, 460),
    ]

    car_button_refs = [] 

    def select_car(car_name):
        selected_car_label.config(text=f"Selected Car: {car_name}")

    for car, x, y in car_buttons:
        btn = Button(root, text=car, font=("Arial", 10), command=lambda c=car: select_car(c))
        car_button_refs.append(btn) 
        canvas.create_window(x, y, window=btn, width=180, height=30)

    canvas.create_text(300, 550, text="Quantity:", font=("Arial", 15), fill="white", anchor="e")
    quantity_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 550, window=quantity_entry, width=100)

    def submit_customer_details():
        name = name_entry.get().strip()
        contact = contact_entry.get().strip()
        address = address_entry.get().strip()
        selected_car = selected_car_label.cget("text").replace("Selected Car: ", "")
        quantity = quantity_entry.get().strip()

        if not name or not contact or not address or selected_car == "None" or not quantity:
            error_label.config(text="Please fill out all fields!", fg="red")
        else:
            cursor.execute("INSERT INTO reservations (name, contact, address, car, quantity) VALUES (?, ?, ?, ?, ?)",
                           (name, contact, address, selected_car, int(quantity)))
            conn.commit()
            error_label.config(text="Details Submitted Successfully!", fg="green")
            print(f"Customer Details: Name={name}, Contact={contact}, Address={address}, Car={selected_car}, Quantity={quantity}")

    error_label = Label(root, text="", font=("Arial", 12), bg="black", fg="red")
    canvas.create_window(500, 600, window=error_label)

    submit_btn = Button(root, text="Submit", font=("Arial", 12), bg="blue", fg="white", command=submit_customer_details)
    canvas.create_window(500, 650, window=submit_btn, width=200)

    def cleanup_and_back():
        for btn in car_button_refs: 
            btn.destroy()
        selected_car_label.destroy() 
        show_main_form(username)

    back_btn = Button(root, text="Back", font=("Arial", 12), bg="blue", fg="white", command=cleanup_and_back)
    canvas.create_window(500, 700, window=back_btn, width=200)

def show_login():
    clear_canvas()
    canvas.create_text(500, 100, text="Login", font=("Arial", 25), fill="white")

    canvas.create_text(300, 200, text="Username:", font=("Arial", 15), fill="white", anchor="e")
    username_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 200, window=username_entry, width=300)

    canvas.create_text(300, 250, text="Password:", font=("Arial", 15), fill="white", anchor="e")
    password_entry = Entry(root, font=("Arial", 15), show="*")
    canvas.create_window(500, 250, window=password_entry, width=300)

    show_pw_btn = Button(root, image=show_icon, command=lambda: toggle_password(password_entry, show_pw_btn), borderwidth=0)
    canvas.create_window(670, 250, window=show_pw_btn, width=30, height=30)

    error_label = Label(root, text="", font=("Arial", 12), bg="black", fg="red")
    canvas.create_window(500, 300, window=error_label)

    def authenticate():
        username = username_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and user[0] == password:
            show_main_form(username)
        else:
            error_label.config(text="Invalid username or password!")

    login_btn = Button(root, text="Login", font=("Arial", 12), bg="blue", fg="white", command=authenticate)
    canvas.create_window(500, 350, window=login_btn, width=200)

    signup_btn = Button(root, text="Sign Up", font=("Arial", 12), bg="blue", fg="white", command=show_sign_up)
    canvas.create_window(500, 400, window=signup_btn, width=200)

def show_sign_up():
    clear_canvas()
    canvas.create_text(500, 100, text="Sign Up", font=("Arial", 25), fill="white")

    canvas.create_text(300, 200, text="Username:", font=("Arial", 15), fill="white", anchor="e")
    signup_username_entry = Entry(root, font=("Arial", 15))
    canvas.create_window(500, 200, window=signup_username_entry, width=300)

    canvas.create_text(300, 250, text="Password:", font=("Arial", 15), fill="white", anchor="e")
    signup_password_entry = Entry(root, font=("Arial", 15), show="*")
    canvas.create_window(500, 250, window=signup_password_entry, width=300)

    canvas.create_text(300, 300, text="Confirm Password:", font=("Arial", 15), fill="white", anchor="e")
    confirm_password_entry = Entry(root, font=("Arial", 15), show="*")
    canvas.create_window(500, 300, window=confirm_password_entry, width=300)

    
    show_pw_btn = Button(root, image=show_icon, command=lambda: toggle_password(signup_password_entry, show_pw_btn), borderwidth=0)
    canvas.create_window(670, 250, window=show_pw_btn, width=30, height=30)

    show_confirm_pw_btn = Button(root, image=show_icon, command=lambda: toggle_password(confirm_password_entry, show_confirm_pw_btn), borderwidth=0)
    canvas.create_window(670, 300, window=show_confirm_pw_btn, width=30, height=30)

    error_label = Label(root, text="", font=("Arial", 12), bg="black", fg="red")
    canvas.create_window(500, 350, window=error_label)

    def submit_signup():
        username = signup_username_entry.get().strip()
        password = signup_password_entry.get().strip()
        confirm_password = confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            error_label.config(text="Please fill out all fields!", fg="red")
        elif password != confirm_password:
            error_label.config(text="Passwords do not match!", fg="red")
        else:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                error_label.config(text="User created successfully!", fg="green")
                show_login()
            except sqlite3.IntegrityError:
                error_label.config(text="Username already exists!", fg="red")

    signup_btn = Button(root, text="Sign Up", font=("Arial", 12), bg="blue", fg="white", command=submit_signup)
    canvas.create_window(500, 400, window=signup_btn, width=200)

    back_btn = Button(root, text="Back", font=("Arial", 12), bg="blue", fg="white", command=show_login)
    canvas.create_window(500, 450, window=back_btn, width=200)

show_login()

root.mainloop()
