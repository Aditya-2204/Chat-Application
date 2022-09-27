import socket
import threading
from cryptography.fernet import Fernet
import firebase_admin



key = Fernet.generate_key()
fernet = Fernet(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("127.0.0.1", 80))
print("SUCCESSFULLY BINDED")

s.listen()
print("LISTENING...")

clients = []
usernames = []

def broadcast(msg):#Broadcast all messages
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            broadcast(f"{username} has been removed")
            break

def receive():
    while True:
        client, addr = s.accept()
        print(f"--CONNECTED WITH: {str(addr)}")

        username, sep, remove = client.recv(1024).decode().partition(": ")

        usernames.append(username)
        clients.append(client)

        print(f"Client Username: {username}")
        broadcast(f"{username} Has Connected".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("SERVER IS RUNNING")        
receive()