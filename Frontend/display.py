import tkinter as tk

root = tk.Tk()
root.title("CrossdeviseChat")
root.geometry("800x600")

# Chat display (read-only)
chat_frame = tk.Frame(root)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_text = tk.Text(chat_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, state=tk.DISABLED)
chat_text.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=chat_text.yview)

# Input area with send button
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=(0,10))

input_var = tk.StringVar()
input_entry = tk.Entry(input_frame, textvariable=input_var)
input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))

def send_message(event=None):
    msg = input_var.get().strip()
    if not msg:
        return
    # append to chat_text
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, f"You: {msg}\n")
    chat_text.see(tk.END)
    chat_text.config(state=tk.DISABLED)
    input_var.set("")

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

# bind Enter to send
input_entry.bind('<Return>', send_message)

if __name__ == "__main__":
    root.mainloop()