import tkinter as tk
from client import *

class ClientGUI:
    def __init__(self):
        self.C = Client()

        self.root = tk.Tk()
        self.root.title("CrossdeviseChat")
        self.root.geometry("800x600")

        # Chat display (read-only)
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.chat_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.chat_text.yview)

        # Input area with send button
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame, textvariable=self.input_var)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # bind Enter to send
        self.input_entry.bind('<Return>', self.send_message)

        self.root.mainloop()

    def send_message(self):
        msg = self.input_var.get().strip()
        if not msg:
            return
        
        self.chat_text.config(state=tk.NORMAL)

        self.chat_text.insert(tk.END, f"You: {msg}\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)
        self.input_var.set("")

if __name__ == "__main__":
    GUI = ClientGUI()