'''
import socket
import threading
import os

c_size = 1024
downloads_dir = 'C:\\Users\\Srijit Sen\\Downloads'

def client_request(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        print(f"Client requested: {request}")
        
        if request == "LIST_FILES":
            files = os.listdir(downloads_dir)
            files_list = "\n".join(files)
            client_socket.send(files_list.encode())
        
        elif request.startswith("UPLOAD"):
            file_name = request.split(" ")[1]
            file_path = os.path.join(downloads_dir, file_name)
            client_socket.send(b"READY")
            with open(file_path, 'wb') as f:
                print(f"Receiving file: {file_name}")
                while True:
                    data = client_socket.recv(c_size)
                    if not data:
                        break
                    f.write(data)
            print(f"File {file_name} uploaded successfully!")
            client_socket.send(b"Upload successful.")
        
        else:
            file_path = os.path.join(downloads_dir, request)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                client_socket.send(file_size.to_bytes(8, 'big'))  # Send file size first
                
                with open(file_path, 'rb') as f:
                    packet = f.read(c_size)
                    while packet:
                        client_socket.send(packet)
                        packet = f.read(c_size)
                print(f"File {request} sent successfully!")
            else:
                client_socket.send(b"File not found!")
                print(f"File {request} not found!")

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Server listening on port: {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from: {addr}")
        threading.Thread(target=client_request, args=(client_socket,)).start()

if __name__ == "__main__":
    port = 8080
    server(port)
'''

import socket
import threading
import os

c_size = 1024
downloads_dir = r'C:\Users\Srijit Sen\Downloads'

def client_request(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        print(f"Client requested: {request}")
        
        if request == "LIST_FILES":
            try:
                files = os.listdir(downloads_dir)
                files_list = "\n".join(files)
                client_socket.send(files_list.encode())
            except Exception as e:
                client_socket.send(b"Error retrieving file list.")
                print(f"Error listing files: {e}")

        elif request.startswith("UPLOAD"):
            try:
                file_name = request.split(" ", 1)[1]
                file_path = os.path.join(downloads_dir, file_name)
                if os.path.exists(file_path):
                    client_socket.send(b"File already exists. Please choose a different name.")
                    return
                client_socket.send(b"READY")
                with open(file_path, 'wb') as f:
                    print(f"Receiving file: {file_name}")
                    while True:
                        data = client_socket.recv(c_size)
                        if not data:
                            break
                        f.write(data)
                print(f"File {file_name} uploaded successfully!")
                client_socket.send(b"Upload successful.")
            
            except Exception as e:
                print(f"Error handling upload request: {e}")
                client_socket.send(b"Upload failed.")

        
        else:
            file_path = os.path.join(downloads_dir, request)
            if not os.path.abspath(file_path).startswith(os.path.abspath(downloads_dir)):
                client_socket.send(b"Invalid file path.")
                return
            
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                client_socket.send(file_size.to_bytes(8, 'big'))
                
                with open(file_path, 'rb') as f:
                    packet = f.read(c_size)
                    while packet:
                        client_socket.send(packet)
                        packet = f.read(c_size)
                print(f"File {request} sent successfully!")
            else:
                client_socket.send(b"File not found!")
                print(f"File {request} not found!")

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Server listening on port: {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from: {addr}")
        threading.Thread(target=client_request, args=(client_socket,)).start()

if __name__ == "__main__":
    port = 8080
    server(port)
