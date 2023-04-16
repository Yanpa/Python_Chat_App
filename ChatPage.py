import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading

from Database import Database

class ChatPage(tk.Frame):
    global selected_friend

    def __init__(self, master, username):
        master.title(f"Chat App - {username}")
        tk.Frame.__init__(self, master)
        self.username = username

        self.db = Database()
        # self.update_timer = threading.Timer(1, self.show_chat_with_friend(selected_friend))
        # self.update_timer.start()

        header_frame = tk.Frame(self, height=60)
        header_frame.pack(fill="x")

        self.user_label = tk.Label(header_frame, text="", font=("Helvetica", 18))
        self.user_label.pack(side="right", padx=10, pady=10)

        sidebar_frame = tk.Frame(self)
        sidebar_frame.pack(fill="y", side="left")

        canvas = tk.Canvas(sidebar_frame)
        canvas.pack(side="left", fill="y")

        scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        friends_frame = tk.LabelFrame(canvas, text="Friends list")
        canvas.create_window((0, 0), window=friends_frame, anchor='nw')

        friends = self.db.return_all_users_friends(self.username)

        for friend in friends:
            friend_frame = tk.Frame(friends_frame, height=60, width=200)
            friend_frame.pack(fill="x")

            friend_name_label = tk.Label(friend_frame, text=friend[0], font=("Helvetica", 14))
            friend_name_label.pack(side="left", padx=10, pady=10)

            friend_frame.bind("<Button-1>", lambda event, name=friend[0]: self.show_chat_with_friend(name))

        friends_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        add_friend_button = ttk.Button(sidebar_frame, text="Add friend", command=self.show_add_friend_frame)
        add_friend_button.pack(side="left",pady=10)

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

    def show_add_friend_frame(self):
        add_friend_window = tk.Toplevel(self)
        add_friend_window.title("Add Friend")

        add_friend_frame = tk.Frame(add_friend_window)
        add_friend_frame.pack(fill="both", expand=True)

        username_label = tk.Label(add_friend_frame, text="Username:")
        username_label.pack(side="left", padx=10, pady=10)

        username_entry = tk.Entry(add_friend_frame)
        username_entry.pack(side="left", padx=10, pady=10)

        add_button = ttk.Button(add_friend_frame, text="Add",
                                command=lambda: self.db.add_friend(username_entry.get(), add_friend_window))
        add_button.pack(side="left", padx=10, pady=10)

        cancel_button = ttk.Button(add_friend_frame, text="Cancel", command=add_friend_window.destroy)
        cancel_button.pack(side="left", padx=10, pady=10)

    def show_chat_with_friend(self, friend_name):
        global selected_friend
        selected_friend = friend_name
        
        self.user_label.config(text=f"You talk with {friend_name}")
        self.message_entry.config(state="normal")
        self.chat_history.config(state="normal")
        self.chat_history.delete("1.0", "end")
        
        self.db.show_updated_chat(selected_friend, self.chat_history)
        
        self.chat_history.config(state="disabled")
        

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