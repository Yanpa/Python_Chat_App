import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import psycopg2

class ChatPage(tk.Frame):
    def __init__(self, master, username):
        master.title(f"Chat App - {username}")
        tk.Frame.__init__(self, master)
        self.username = username

        # Connect to the PostgresDB
        self.conn = psycopg2.connect(
                dbname="chatapp",
                user="panayotyanev",
                password="123",
                host="localhost",
                port="5432"
            )
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT * FROM users WHERE username = %s", (self.username,))
        self.current_user_info = self.cur.fetchone()

        self.cur.execute("SELECT friend_id FROM friends WHERE user_id = %s", (self.current_user_info[0],))
        friend_ids = self.cur.fetchall()

        friends = []
        for friend_id in friend_ids:
            self.cur.execute("SELECT username FROM users WHERE id = %s", (friend_id[0],))
            friends.append(self.cur.fetchone())

        print(friends)

        # Create the header
        header_frame = tk.Frame(self, height=60)
        header_frame.pack(fill="x")

        self.user_label = tk.Label(header_frame, text="", font=("Helvetica", 18))
        self.user_label.pack(side="right", padx=10, pady=10)

        # Create the side-bar
        sidebar_frame = tk.Frame(self, width=200)
        sidebar_frame.pack(fill="y", side="left")

        # Add a canvas to the side-bar
        canvas = tk.Canvas(sidebar_frame)
        canvas.pack(side="left", fill="y")

        # Add a scrollbar to the side-bar
        scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add the friend circles to the canvas
        friends_frame = tk.LabelFrame(canvas, text="Friends list")
        canvas.create_window((0, 0), window=friends_frame, anchor='nw')

        for friend in friends:
            friend_frame = tk.Frame(friends_frame, height=60, width=200)
            friend_frame.pack(fill="x")

            friend_name_label = tk.Label(friend_frame, text=friend[0], font=("Helvetica", 14))
            friend_name_label.pack(side="left", padx=10, pady=10)

            friend_frame.bind("<Button-1>", lambda event, name=friend[0]: self.show_chat_with_friend(name))

        # Update the canvas scroll region
        friends_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create a button to add a friend
        add_friend_button = ttk.Button(sidebar_frame, text="Add friend", command=self.show_add_friend_frame)
        add_friend_button.pack(side="bottom",pady=10)

        # Create the chat history
        chat_frame = tk.Frame(self)
        chat_frame.pack(fill="both", expand=True)

        self.chat_history = ScrolledText(chat_frame, bd=0, wrap="word", state="disabled")
        self.chat_history.tag_config("right", justify="right")
        self.chat_history.pack(side="left", fill="both", expand=True, padx=20, pady=10)


        # Create the message input field and send button
        message_frame = tk.Frame(self, height=60)
        message_frame.pack(fill="x")

        self.message_entry = tk.Entry(message_frame, bd=0, font=("Helvetica", 14), state="disabled")
        self.message_entry.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        send_button = ttk.Button(message_frame, text="Send", command=lambda: self.send_message(self.message_entry, self.chat_history))
        send_button.pack(side="right", padx=20, pady=10)

        self.message_entry.bind("<Return>", lambda event: self.send_message(self.message_entry, self.chat_history))

    def show_add_friend_frame(self):
        # Create a new window to display the "Add Friend" frame
        add_friend_window = tk.Toplevel(self)
        add_friend_window.title("Add Friend")

        # Create the "Add Friend" frame
        add_friend_frame = tk.Frame(add_friend_window)
        add_friend_frame.pack(fill="both", expand=True)

        # Create the label and entry field for entering the friend's username
        username_label = tk.Label(add_friend_frame, text="Username:")
        username_label.pack(side="left", padx=10, pady=10)

        username_entry = tk.Entry(add_friend_frame)
        username_entry.pack(side="left", padx=10, pady=10)

        # Create the "Add" button to add the friend
        add_button = ttk.Button(add_friend_frame, text="Add",
                                command=lambda: add_friend(username_entry.get()))
        add_button.pack(side="left", padx=10, pady=10)

        # Create the "Cancel" button to close the window
        cancel_button = ttk.Button(add_friend_frame, text="Cancel", command=add_friend_window.destroy)
        cancel_button.pack(side="left", padx=10, pady=10)

        def add_friend(username):
            # Check if the username exists in the users table
            self.cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            new_friend = self.cur.fetchone()

            if new_friend is None:
                return
            else:
                self.cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)", (self.current_user_info[0], new_friend[0]))
                self.conn.commit()
                self.cur.close()
                self.conn.close()
                add_friend_window.destroy()     

            self.cur.close()
            self.conn.close()       


    def show_chat_with_friend(self, friend_name):
        self.user_label.config(text=f"You talk with {friend_name}")
        self.message_entry.config(state="normal")
        self.chat_history.config(state="normal")
        self.chat_history.delete("1.0", "end")
        self.chat_history.insert("end", f"Showing chat with {friend_name}\n\n")
        self.chat_history.config(state="disabled")

    def send_message(self, message_entry, chat_history):
        message = message_entry.get().strip()
        if message:
            chat_history.config(state="normal")
            chat_history.insert("end", message + "\n", "right")
            chat_history.config(state="disabled")
            message_entry.delete(0, "end")

            chat_history.see("end")
