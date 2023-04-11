import tkinter as tk

class LoginWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=True)

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, padx=10, anchor='center')

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5, padx=10, anchor='center')

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        master.center_frame(self)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Username: {username}, Password: {password}")