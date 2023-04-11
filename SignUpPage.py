import tkinter as tk

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

        signup_button = tk.Button(self, text="Signup", command=self.signup)
        signup_button.pack(pady=5)

        self.status_label = tk.Label(self, fg="red")
        self.status_label.pack()

        master.center_frame(self)

    def signup(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if password != confirm_password:
            self.status_label.config(text="Passwords do not match")
            return
        
        print(f"Username: {username}, Email: {email}, Password: {password}")