import tkinter as tk
from LoginPage import LoginWindow
from SignUpPage import SignupWindow

class ChatApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Chat App")
        self.geometry("650x500")
        self.resizable(True, True)
        self._frame = None
        self.switch_frame(LandingWindow)

    def center_frame(self, frame:tk.Frame):
        frame.update_idletasks()
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()

        total_width = frame_width
        total_height = frame_height

        for child in frame.winfo_children():
            child_width = child.winfo_width()
            child_height = child.winfo_height()

            total_width = max(total_width, child_width)
            total_height += child_height

        screen_width = frame.winfo_toplevel().winfo_screenwidth()
        screen_height = frame.winfo_toplevel().winfo_screenheight()

        x = int((screen_width/2) - (total_width/2))
        y = int((screen_height/2) - (total_height/2))

        frame.winfo_toplevel().geometry(f'+{x}+{y}')

    def switch_frame(self, frame_class: tk.Frame):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.pack_forget()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()



class LandingWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=True)

        welcome_label = tk.Label(self, text="Welcome to my chat app")
        welcome_label.pack(pady=50)

        login_button = tk.Button(self, text="Login", command=lambda: master.switch_frame(LoginWindow))
        login_button.pack(pady=10)

        signup_button = tk.Button(self, text="Signup", command=lambda: master.switch_frame(SignupWindow))
        signup_button.pack(pady=10)

        master.center_frame(self)

if __name__ == "__main__":
    chat_app = ChatApp()
    chat_app.mainloop()