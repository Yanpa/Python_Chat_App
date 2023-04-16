import tkinter as tk
import re
from ChatPage import ChatPage
from Database import Database

class SignupWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=True)

        self.db = Database()

        username_label = tk.Label(self, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, padx=10, anchor='center')

        email_label = tk.Label(self, text="Email:")
        email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5, padx=10, anchor='center')

        password_label = tk.Label(self, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5, padx=10, anchor='center')

        confirm_password_label = tk.Label(self, text="Confirm Password:")
        confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack(pady=5, padx=10, anchor='center')

        self.status_label = tk.Label(self, fg="red")
        self.status_label.pack()

        signup_button = tk.Button(self, text="Signup", command=self.signup)
        signup_button.pack(pady=5)

        back_label = tk.Label(self, text="Back to home screen", cursor="hand2")
        back_label.pack(side="bottom", pady=10)
        back_label.bind("<Button-1>", self.go_to_home)

        master.center_frame(self)

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def signup(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            self.status_label.config(text="Passwords do not match\n")
        elif len(username) < 3:
            self.status_label.config(text="Username must be at least 3 chars long\n")
        elif not self.is_valid_email(email):
            self.status_label.config(text="Email is not the correct format\n")
        elif self.db.check_if_username_exist(username):
            self.status_label.config(text="Username already exists\n")
        elif self.db.check_if_email_is_used(email):
            self.status_label.config(text="Email is already used\n")
        else:
            self.db.create_new_user(username, email, password)

            self.destroy()

            chat_page = ChatPage(self.master, username = username)
            chat_page.pack(fill="both", expand=True)


    def go_to_home(self, event):
        self.master.destroy()
        self.master.__init__()