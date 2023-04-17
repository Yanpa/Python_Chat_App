import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from Database import Database
from AccountPage import Account

class ChatPage(tk.Frame):

    def __init__(self, master, username):
        master.title(f"Chat App - {username}")
        tk.Frame.__init__(self, master)

        self.username = username
        self.selected_friend = None

        self.db = Database()

        header_frame = tk.Frame(self, height=60)
        header_frame.pack(fill="x")

        self.user_label = tk.Label(header_frame, text="", font=("Helvetica", 18))
        self.user_label.pack(side="right", padx=10, pady=10)

        sidebar_frame = tk.Frame(self)
        sidebar_frame.pack(fill="y", side="left")

        friends_frame = tk.LabelFrame(sidebar_frame, text="Friends list")
        friends_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.populate_friends_frame(friends_frame)

        account_button = ttk.Button(sidebar_frame, text="Account", command=self.show_account_frame)
        account_button.pack(side="bottom", pady=10)

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

    def populate_friends_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        friends = self.db.return_all_users_friends(self.username)

        for friend in friends:
            friend_frame = tk.Frame(frame, height=60)
            friend_frame.pack(fill="x")

            friend_name_button = ttk.Button(friend_frame, text=friend, command=lambda friend=friend: self.select_friend(friend))
            friend_name_button.pack(side="left", padx=10, pady=10)

        self.after(1000, self.populate_friends_frame, frame)

    def show_account_frame(self):
        Account(self, self.db.get_user_info_by_username(self.username))

    def select_friend(self, friend):
        self.selected_friend = friend
        self.show_chat_with_friend()

    def show_chat_with_friend(self):
        if self.selected_friend is None:
            return

        self.user_label.config(text=f"You talk with {self.selected_friend}")
        self.message_entry.config(state="normal")
        self.chat_history.config(state="normal")
        self.chat_history.delete("1.0", "end")

        self.db.show_updated_chat(self.selected_friend, self.chat_history)

        self.chat_history.config(state="disabled")

        self.after(1000, self.show_chat_with_friend)
        
    def send_message(self, message_entry, chat_history):
        message = message_entry.get().strip()

        if message:
            self.db.import_message_in_db(self.selected_friend, message)

            message_entry.delete(0, "end")
    
    def __del__(self):
        self.db.close_connection()