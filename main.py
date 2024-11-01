import socket
import threading
import tkinter as tk

# Twitch IRC server details
SERVER = 'irc.chat.twitch.tv'
PORT = 6667
NICK = 'username'
TOKEN = 'oauth:'  # Replace with your token from twitchapps.com/tmi
CHANNEL = '#channel'

# Connect to Twitch IRC
def connect_to_twitch():
    sock = socket.socket()
    sock.connect((SERVER, PORT))
    sock.send(f"PASS {TOKEN}\n".encode('utf-8'))
    sock.send(f"NICK {NICK}\n".encode('utf-8'))
    sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))
    return sock

# GUI class for displaying chat
class ChatDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitch Chat")
        self.root.geometry("400x600")
        self.root.configure(bg="#d4a5f4")  # Pastel purple background

        # Chat display area
        self.chat_text = tk.Text(
            self.root,
            bg="#d4a5f4",  # Pastel purple background
            fg="#ffffff",  # White text color
            font=("Fancake", 16),
            wrap="word",
            state="disabled",
            padx=10,
            pady=10
        )
        self.chat_text.pack(expand=True, fill="both")

        # Start the connection to Twitch
        self.sock = connect_to_twitch()
        self.listen_to_chat()

    # Function to display new messages in the chat window
    def display_message(self, message):
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", message + "\n")
        self.chat_text.see("end")  # Scroll to the latest message
        self.chat_text.configure(state="disabled")

    # Listen for chat messages from the Twitch IRC server
    def listen_to_chat(self):
        def chat_listener():
            while True:
                response = self.sock.recv(2048).decode('utf-8')

                if response.startswith('PING'):
                    self.sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                elif "PRIVMSG" in response:
                    # Parse the message to get username and text
                    user = response.split("!", 1)[0][1:]
                    message = response.split("PRIVMSG", 1)[1].split(":", 1)[1]
                    display_message = f"{user}: {message.strip()}"
                    self.display_message(display_message)

        # Start chat listener in a separate thread
        threading.Thread(target=chat_listener, daemon=True).start()

# Run the chat display window
if __name__ == "__main__":
    root = tk.Tk()
    chat_display = ChatDisplay(root)
    root.mainloop()
