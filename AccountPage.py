import tkinter as tk
from tkinter import ttk

class Account():
    def __init__(self, master, user):
        self.user = user
        account_window = tk.Toplevel(master)
        account_window.title(f"{user[1]} Account")

        info_label = tk.Label(account_window, text="Account info:")
        info_label.pack()

        self.info_text = tk.Text(account_window)
        self.info_text.pack()

        self.info_text.insert(tk.END, f"Username: {user[1]}\n\n")
        self.info_text.insert(tk.END, f"Email: {user[3]}\n\n")
        self.info_text.insert(tk.END, "Friends:\n")

        self.friends = master.db.return_all_users_friends(user[1])
        for friend in self.friends:
            self.info_text.insert(tk.END, friend + '| ')

        self.info_text.config(state='disable')

        self.btn_add_friend = tk.Button(account_window, text="Add friend", command=lambda: self.add_new_friend(master, account_window, self.btn_add_friend))
        self.btn_add_friend.pack()

        self.btn_remove_friend = tk.Button(account_window, text="Remove friend", command=lambda: self.remove_friend(master, account_window, self.btn_remove_friend))
        self.btn_remove_friend.pack()

        if self.friends == []:
            self.btn_remove_friend.config(state="disabled")

    def add_new_friend(self, master, account_window, button):
        button.config(state='disabled')
        add_friend_frame = tk.Frame(account_window)
        add_friend_frame.pack(fill="both", expand=True)

        username_label = tk.Label(add_friend_frame, text="Username:")
        username_label.pack(side="left", padx=10, pady=10)

        username_entry = tk.Entry(add_friend_frame)
        username_entry.pack(side="left", padx=10, pady=10)

        add_button = ttk.Button(add_friend_frame, text="Add",
                                command=lambda: new_friend(master, username_entry.get()))
        add_button.pack(side="left", padx=10, pady=10)

        cancel_button = ttk.Button(add_friend_frame, text="Cancel", command=lambda: close_add_friend())
        cancel_button.pack(side="left", padx=10, pady=10)

        # self.status_label = tk.Label(self, fg="red")
        # self.status_label.pack()

        def new_friend(master, username):
            if master.db.check_if_username_exist(username):
                if master.db.are_friends(self.user[0], master.db.get_user_id_by_username(username)):
                    close_add_friend()
                else:
                    master.db.add_friend(username)
                    self.update_info(master, self.friends)
                    close_add_friend()
            else:
                # self.status_label.config(text="Username doesn't exist")
                return

        def close_add_friend():
            button.config(state='normal')
            add_friend_frame.destroy()

    def remove_friend(self, master, account_window, button):
        button.config(state='disabled')
        remove_friend_frame = tk.Frame(account_window)
        remove_friend_frame.pack(fill="both", expand=True)

        username_label = tk.Label(remove_friend_frame, text="Friends list:")
        username_label.pack(side="left", padx=10, pady=10)
        
        friend_options = master.db.return_all_users_friends(self.user[1])
        
        friend_var = tk.StringVar(remove_friend_frame)
        friend_var.set(friend_options[0])

        username_entry = tk.OptionMenu(remove_friend_frame, friend_var, *friend_options)
        username_entry.pack(side="left", padx=10, pady=10)

        add_button = ttk.Button(remove_friend_frame, text="Remove",
                                command=lambda: remove_friend(master, friend_var.get()))
        add_button.pack(side="left", padx=10, pady=10)

        cancel_button = ttk.Button(remove_friend_frame, text="Cancel", command=lambda: close_remove_friend())
        cancel_button.pack(side="left", padx=10, pady=10)

        def remove_friend(master, friend_username):
            master.db.remove_friend(master.db.get_user_id_by_username(friend_username), self.user[0])
            self.update_info(master, self.friends)
            close_remove_friend()

        def close_remove_friend():
            button.config(state='normal')
            remove_friend_frame.destroy()

    def update_info(self, master, friends):
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)

        self.info_text.insert(tk.END, f"Username: {self.user[1]}\n\n")
        self.info_text.insert(tk.END, f"Email: {self.user[3]}\n\n")
        self.info_text.insert(tk.END, "Friends:\n")

        friends = master.db.return_all_users_friends(self.user[1])
        for friend in friends:
            self.info_text.insert(tk.END, friend + '| ')

        self.info_text.config(state='disable')

        if friends == []:
            self.btn_remove_friend.config(state="disabled")
        else:
            self.btn_remove_friend.config(state="normal")