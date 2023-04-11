import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class ChatPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        header_frame = tk.Frame(self, height=60)
        header_frame.pack(fill="x")

        user_label = tk.Label(header_frame, text="John Smith", font=("Helvetica", 18))
        user_label.pack(side="left", padx=10, pady=10)

        chat_frame = tk.Frame(self)
        chat_frame.pack(fill="both", expand=True)

        chat_history = ScrolledText(chat_frame, bd=0, wrap="word", state="disabled")
        chat_history.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        message_frame = tk.Frame(self, height=60)
        message_frame.pack(fill="x")

        message_entry = tk.Entry(message_frame, bd=0, font=("Helvetica", 14))
        message_entry.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        send_button = ttk.Button(message_frame, text="Send", command=lambda: self.send_message(message_entry, chat_history))
        send_button.pack(side="right", padx=20, pady=10)

        message_entry.bind("<Return>", lambda event: self.send_message(message_entry, chat_history))

    def send_message(self, message_entry, chat_history):
        message = message_entry.get().strip()
        if message:
            chat_history.config(state="normal")
            chat_history.insert("end", "You: " + message + "\n\n")
            chat_history.config(state="disabled")
            message_entry.delete(0, "end")


root = tk.Tk()
chat_page = ChatPage(root)
chat_page.pack(fill="both", expand=True)

root.mainloop()