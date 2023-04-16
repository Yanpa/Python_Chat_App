import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time

from Database import Database
from AccountPage import Account

class ChatPage(tk.Frame):
    global selected_friend

    def __init__(self, master, username):
        master.title(f"Chat App - {username}")
        tk.Frame.__init__(self, master)
        self.username = username

        self.db = Database()

        header_frame = tk.Frame(self, height=60)
        header_frame.pack(fill="x")

        self.user_label = tk.Label(header_frame, text="", font=("Helvetica", 18))
        self.user_label.pack(side="right", padx=10, pady=10)

        sidebar_frame = tk.Frame(self)
        sidebar_frame.pack(fill="y", side="left")

        friends_frame = tk.LabelFrame(sidebar_frame, text="Friends list")
        friends_frame.pack(fill="both", expand=True, padx=10, pady=10)

        friends = self.db.return_all_users_friends(self.username)

        for friend in friends:
            friend_frame = tk.Frame(friends_frame, height=60)
            friend_frame.pack(fill="x")

            friend_name_label = tk.Label(friend_frame, text=friend, font=("Helvetica", 14))
            friend_name_label.pack(side="left", padx=10, pady=10)

            friend_frame.bind("<Button-1>", lambda event, name=friend: self.update_chat_history(name))

        add_friend_button = ttk.Button(sidebar_frame, text="Account", command=self.show_account_frame)
        add_friend_button.pack(side="bottom", pady=10)

        chat_frame = tk.Frame(self)
        chat_frame.pack(fill="both", expand=True)

        self.chat_history = ScrolledText(chat_frame, bd=0, wrap="word", state="disabled")
        self.chat_history.tag_config("right", justify="right")
        self.chat_history.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        message_frame = tk.Frame(self, height=60)
        message_frame.pack(fill="x")

        self.message_entry = tk.Entry(message_frame, bd=0, font=("Helvetica", 14), state="disabled")
        self.message_entry.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        send_button = ttk.Button(message_frame, text="Send", command=lambda: self.send_message(self.message_entry, self.chat_history))
        send_button.pack(side="right", padx=20, pady=10)

        self.message_entry.bind("<Return>", lambda event: self.send_message(self.message_entry, self.chat_history))

    def show_account_frame(self):
        Account(self, self.db.get_user_info_by_username(self.username))

    def show_chat_with_friend(self, name):
        self.user_label.config(text=f"You talk with {name}")
        self.message_entry.config(state="normal")
        self.chat_history.config(state="normal")
        self.chat_history.delete("1.0", "end")

        self.db.show_updated_chat(name, self.chat_history)

    def update_chat_history(self, friend_name):
        global selected_friend
        selected_friend = friend_name

        self.show_chat_with_friend(selected_friend)
        self.after(1000, self.update_chat_history, friend_name)  # Update every 1000ms (1 second)
        
    def send_message(self, message_entry, chat_history):
        global selected_friend
        message = message_entry.get().strip()

        if message:
            self.db.import_message_in_db(selected_friend, message)

            chat_history.config(state="normal")
            chat_history.insert("end", "You:\n" + message + "\n", "right")
            chat_history.config(state="disabled")
            message_entry.delete(0, "end")

            chat_history.see("end")