import tkinter as tk
from ChatPage import ChatPage
from Database import Database

class LoginWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=True)

        self.db = Database()

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, padx=10, anchor='center')

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5, padx=10, anchor='center')

        self.status_label = tk.Label(self, fg="red")
        self.status_label.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        back_label = tk.Label(self, text="Back to home screen", cursor="hand2")
        back_label.pack(side="bottom", pady=10)
        back_label.bind("<Button-1>", self.go_to_home)

        master.center_frame(self)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db.check_user_credentials(username, password)
        
        if user:
            self.destroy()

            chat_page = ChatPage(self.master, username = username)
            chat_page.pack(fill="both", expand=True)
        else:
            self.status_label.config(text="Wrong username or password")
            return
        
    def go_to_home(self, event):
        self.master.destroy()
        self.master.__init__()