import tkinter as tk
from client import *
import threading
import hashlib
import json

class ClientGUI:
    def __init__(self):
        self.C = Client()
        self.Chat = self.C.GetChat

        self.root = tk.Tk()
        self.root.title("CrossdeviseChat")
        self.root.geometry("400x600")

        UpdChat = threading.Thread(target=self.UpdateChat)
        UpdChat.start()

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

    def WriteChat(self):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete("1.0", tk.END)

        for i in self.Chat:
            self.chat_text.insert(tk.END, i + "\n")
            self.chat_text.see(tk.END)

        self.chat_text.config(state=tk.DISABLED)



    def UpdateChat(self):
        while True:
            if self.C.IsThereNewMessage:
                self.Chat = self.C.GetChat

                self.WriteChat()

                self.C.IReadTheNewMessage()
            

    def send_message(self, event=None):
        msg = self.input_var.get().strip()
        self.input_var.set("")
        if not msg:
            return

        self.C.SendMessage(msg)

        

if __name__ == "__main__":
    GUI = ClientGUI()