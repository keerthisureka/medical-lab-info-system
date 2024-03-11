import tkinter as tk
from database import *
from tkinter import messagebox
from admin import *
from patient import *

conn, cursor = initialize_connection()
 
def center_window(width, height):
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


class WelcomeWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Welcome")
        center_window(240, 120)
         
        login_button = tk.Button(self, text="Login", width=10,
                          command=self.open_login_window)
        login_button.pack(padx=20, pady=(20, 10))
         
        register_button = tk.Button(self, text="Register", width=10, 
                          command=self.open_register_window)
        register_button.pack(pady=10)
        self.pack()
         
    def open_login_window(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        LoginWindow(self.master)
         
    def open_register_window(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        RegisterWindow(self.master)
 
 
class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Login")
        self.master.resizable(False, False)
        center_window(240, 150)
         
        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
         
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=2, column=1, sticky="e", padx=10, pady=(10, 0))
 
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()

    def submit(self):
        data = [self.username_entry.get(), self.password_entry.get()]
        if self.username_entry.get() == "" or self.password_entry.get() == "":
            messagebox.showerror("Error", "Fields cannot be empty!")
        elif login(cursor, data) != None:
            messagebox.showinfo("Success", "Logged In successfully!")
            if login(cursor, data) == "Admin":
                main_window_admin()
            else:
                main_window_patient(self.username_entry.get())
        else:
            messagebox.showerror("Error", "Incorrect Login Details!")
 
    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)
 
 
class RegisterWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Register")
        self.master.resizable(False, False)
        center_window(320, 350)
         
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self, width=26)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Email:").grid(row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(self, width=26)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*", width=26)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="UserType:").grid(row=6, column=0, sticky="w")
        self.option = ["Admin", "Patient"]
        self.sel_option=tk.StringVar()
        self.usertype_entry = tk.OptionMenu(self, self.sel_option, *self.option)
        self.usertype_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Age:").grid(row=5, column=0, sticky="w")
        self.age_entry = tk.Entry(self, width=10)
        self.age_entry.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Gender:").grid(row=4, column=0, sticky="w")
        self.gender_entry = tk.Entry(self, width=10)
        self.gender_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")
         
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=7, column=1, padx=10, pady=10, sticky="e")
 
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()
         
    def submit(self):
        if self.name_entry.get() == "" or self.email_entry.get() == "" or self.password_entry.get() == "" or self.sel_option.get() == "" or self.age_entry.get() == "" or self.gender_entry.get() == "":
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            data = {"Name": self.name_entry.get(), "Email": self.email_entry.get(), "Password": self.password_entry.get(), "UserType": self.sel_option.get(), "Age": self.age_entry.get(), "Gender": self.gender_entry.get()}
            register(cursor, data)
            messagebox.showinfo("Success", "Registered successfully!")
            if data["UserType"] == "Admin":
                main_window_admin()
            else:
                main_window_patient(self.email_entry.get())

    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)

root = tk.Tk()
root.eval('tk::PlaceWindow . center')
WelcomeWindow(root)
root.mainloop()