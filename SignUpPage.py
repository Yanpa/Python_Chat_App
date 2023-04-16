import tkinter as tk
import psycopg2
import re
from ChatPage import ChatPage

class SignupWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=True)

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

        # Back to home screen label
        back_label = tk.Label(self, text="Back to home screen", cursor="hand2")
        back_label.pack(side="bottom", pady=10)
        back_label.bind("<Button-1>", self.go_to_home)

        master.center_frame(self)

        self.conn = psycopg2.connect(
            dbname="chatapp",
            user="panayotyanev",
            password="123",
            host="localhost",
            port="5432"
        )

        self.cursor = self.conn.cursor()

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)
    
    def check_if_username_exist(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return self.cursor.fetchone() is not None

    def check_if_email_is_used(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return self.cursor.fetchone() is not None

    def signup(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            self.status_label.config(text="Passwords do not match\n")
        elif not self.is_valid_email(email):
            self.status_label.config(text="Email is not the correct format\n")
        elif self.check_if_username_exist(username):
            self.status_label.config(text="Username already exists\n")
        elif self.check_if_email_is_used(email):
            self.status_label.config(text="Email is already used\n")
        else:
            # Insert the new user into the database
            self.cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            self.conn.commit()
            self.destroy()

            chat_page = ChatPage(self.master, username = username)
            chat_page.pack(fill="both", expand=True)


    def go_to_home(self, event):
        self.master.destroy()
        self.master.__init__()