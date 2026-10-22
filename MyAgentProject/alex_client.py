




# alex_client.py
import socket
import customtkinter as ctk

def send_message():

    msg = entry.get()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost",5555))
    client.send(msg.encode())

    reply = client.recv(1024).decode()

    chat.insert("end", f"Alex: {msg}\n")
    chat.insert("end", f"{reply}\n\n")

    entry.delete(0,"end")

app = ctk.CTk()
app.title("Alex Chat Window")
app.geometry("400x400")

chat = ctk.CTkTextbox(app,width=350,height=250)
chat.pack(pady=10)

entry = ctk.CTkEntry(app,width=250)
entry.pack(pady=10)

btn = ctk.CTkButton(app,text="Send",command=send_message)
btn.pack()

app.mainloop()