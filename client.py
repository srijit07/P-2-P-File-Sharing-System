'''
import socket

c_size = 1024

def client(ip, port, file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send(file.encode())

        with open(f"Downloaded_{file}", 'wb') as f:
            while True:
                packet = client_socket.recv(c_size)
                if not packet:
                    break
                if packet == b"File not found!":
                    print("File not found on the server.")
                    break
                f.write(packet)
        print(f"File {file} downloaded!")
    except Exception as e:
        print(f"Error during download: {e}")
    finally:
        client_socket.close()

def list_files(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send("LIST_FILES".encode())

        files = client_socket.recv(4096).decode()  # Adjust buffer size as necessary
        print("Available files:\n")
        print(files)
    except Exception as e:
        print(f"Error listing files: {e}")
    finally:
        client_socket.close()

def main():
    while True:
        print("1. List files\n2. Download a file\n3. Quit")
        choice = input("Enter your choice: ")
        if choice == '1':
            ip = input("Enter server IP address: ")
            port = int(input("Enter port number: "))
            list_files(ip, port)
        elif choice == '2':
            ip = input("Enter server IP address: ")
            port = int(input("Enter port number: "))
            file = input("Enter filename to download: ")
            client(ip, port, file)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
'''
'''
import socket
import tkinter as tk
from tkinter import messagebox, filedialog

c_size = 1024

def client(ip, port, file, download_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send(file.encode())
        
        save_path = f"{download_path}/{file}"
        with open(save_path, 'wb') as f:
            while True:
                packet = client_socket.recv(c_size)
                if not packet:
                    break
                if packet == b"File not found!":
                    messagebox.showerror("Error", "File not found on the server.")
                    break
                f.write(packet)
        messagebox.showinfo("Success", f"File {file} downloaded!")
    except Exception as e:
        messagebox.showerror("Error", f"Error during download: {e}")
    finally:
        client_socket.close()

def list_files(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send("LIST_FILES".encode())

        files = client_socket.recv(4096).decode()
        return files.split('\n')
    except Exception as e:
        messagebox.showerror("Error", f"Error listing files: {e}")
        return []
    finally:
        client_socket.close()

def start_gui():
    def download_file():
        ip = entry_ip.get()
        port = int(entry_port.get())
        file = file_listbox.get(tk.ACTIVE)
        download_path = filedialog.askdirectory()
        if file and download_path:
            client(ip, port, file, download_path)

    def refresh_files():
        ip = entry_ip.get()
        port = int(entry_port.get())
        files = list_files(ip, port)
        file_listbox.delete(0, tk.END)
        for file in files:
            file_listbox.insert(tk.END, file)

    window = tk.Tk()
    window.title("File Transfer Client")
    tk.Label(window, text="Server IP:").grid(row=0, column=0, padx=10, pady=5)
    entry_ip = tk.Entry(window)
    entry_ip.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(window, text="Port:").grid(row=1, column=0, padx=10, pady=5)
    entry_port = tk.Entry(window)
    entry_port.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Available Files:").grid(row=2, column=0, columnspan=2)
    file_listbox = tk.Listbox(window, width=50, height=10)
    file_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    refresh_button = tk.Button(window, text="Refresh File List", command=refresh_files)
    refresh_button.grid(row=4, column=0, columnspan=2, pady=5)

    download_button = tk.Button(window, text="Download Selected File", command=download_file)
    download_button.grid(row=5, column=0, columnspan=2, pady=10)

    window.mainloop()

if __name__ == "__main__":
    start_gui()
'''

'''
import socket
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageDraw, ImageTk
import threading
import re

c_size = 1024

def client(ip, port, file, download_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send(file.encode())

        save_path = f"{download_path}/{file}"
        with open(save_path, 'wb') as f:
            while True:
                packet = client_socket.recv(c_size)
                if not packet:
                    break
                if packet == b"File not found!":
                    messagebox.showerror("Error", "File not found on the server.")
                    return
                f.write(packet)
        messagebox.showinfo("Success", f"File {file} downloaded!")
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during download: {e}")
    finally:
        client_socket.close()

def list_files(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send("LIST_FILES".encode())
        files = client_socket.recv(4096).decode()
        return files.split('\n')
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Connection Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error listing files: {e}")
        return []
    finally:
        client_socket.close()

def validate_ip_port(ip, port):
    ip_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not ip_pattern.match(ip):
        messagebox.showerror("Input Error", "Please enter a valid IP address.")
        return False
    if not port.isdigit() or not (0 <= int(port) <= 65535):
        messagebox.showerror("Input Error", "Please enter a valid port number (0-65535).")
        return False
    return True

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

def remove_placeholder(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, "end")
        event.widget.config(fg="black")

def restore_placeholder(event, placeholder):
    if event.widget.get() == "":
        add_placeholder(event.widget, placeholder)

def start_gui():
    def download_file():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        selected_files = file_listbox.curselection()
        if not selected_files:
            messagebox.showerror("Selection Error", "Please select at least one file to download.")
            return
        download_path = filedialog.askdirectory()
        if download_path:
            for i in selected_files:
                file = file_listbox.get(i)
                threading.Thread(target=client, args=(ip, port, file, download_path)).start()

    def refresh_files():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        threading.Thread(target=update_file_list, args=(ip, port)).start()

    def update_file_list(ip, port):
        files = list_files(ip, port)
        file_listbox.delete(0, tk.END)
        for file in files:
            file_listbox.insert(tk.END, file)

    window = tk.Tk()
    window.title("File Transfer Client")
    window.geometry("500x400")
    window.configure(bg='#e0e5ec')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Rounded.TButton", font=("Product Sans", 11), padding=10, relief="flat", background="#4C7DFF", foreground="white", borderwidth=0, anchor="center")
    style.map("Rounded.TButton", background=[("active", "#354B7E")])
    style.configure("TLabel", font=("Product Sans", 12), background='#e0e5ec')
    
    canvas = tk.Canvas(window, width=500, height=400, bg="#e0e5ec")
    canvas.grid(row=0, column=0, columnspan=2)

    tk.Label(window, text="Server IP:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=30)
    entry_ip = tk.Entry(window, font=("Product Sans", 11), relief="flat", highlightbackground="#ccc", highlightthickness=1)
    entry_ip.place(x=140, y=30, width=250, height=30)
    add_placeholder(entry_ip, "Enter IP address")
    entry_ip.bind("<FocusIn>", lambda event: remove_placeholder(event, "Enter IP address"))
    entry_ip.bind("<FocusOut>", lambda event: restore_placeholder(event, "Enter IP address"))

    tk.Label(window, text="Port:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=70)
    entry_port = tk.Entry(window, font=("Product Sans", 11), relief="flat", highlightbackground="#ccc", highlightthickness=1)
    entry_port.place(x=140, y=70, width=250, height=30)
    add_placeholder(entry_port, "Enter port number")
    entry_port.bind("<FocusIn>", lambda event: remove_placeholder(event, "Enter port number"))
    entry_port.bind("<FocusOut>", lambda event: restore_placeholder(event, "Enter port number"))

    tk.Label(window, text="Available Files:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=110)
    file_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, font=("Product Sans", 10), relief="flat", bg="#F5F7FA", bd=0, highlightthickness=1, highlightbackground="#c0c5ce")
    file_listbox.place(x=30, y=140, width=440, height=120)

    refresh_button = ttk.Button(window, text="Refresh File List", command=refresh_files, style="Rounded.TButton")
    refresh_button.place(x=30, y=270, width=200)

    download_button = ttk.Button(window, text="Download Selected Files", command=download_file, style="Rounded.TButton")
    download_button.place(x=270, y=270, width=200)

    def create_tooltip(widget, text):
        tooltip = tk.Toplevel(widget, bg="#333", padx=5, pady=5)
        tooltip.wm_overrideredirect(True)
        tooltip.withdraw()
        tk.Label(tooltip, text=text, fg="white", bg="#333", font=("Product Sans", 10)).pack()

        def show_tooltip(event):
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    create_tooltip(entry_ip, "Enter the server IP address here.")
    create_tooltip(entry_port, "Enter the port number here.")

    window.mainloop()

if __name__ == "__main__":
    start_gui()
'''


'''
import socket
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import re
import time
import os

c_size = 1024

def client(ip, port, file, download_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send(file.encode())
        window = tk.Tk()

        file_size_data = client_socket.recv(8)
        if file_size_data == b"File not found!":
            messagebox.showerror("Error", "File not found on the server.")
            return
        file_size = int.from_bytes(file_size_data, 'big')

        progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
        progress_bar.place(x=100, y=350)

        save_path = f"{download_path}/{file}"
        with open(save_path, 'wb') as f:
            received = 0
            while received < file_size:
                packet = client_socket.recv(min(c_size, file_size - received))
                if not packet:
                    break
                f.write(packet)
                received += len(packet)
                progress_bar['value'] = (received / file_size) * 100
                window.update_idletasks()
                time.sleep(0.1)
        progress_bar.destroy()
        messagebox.showinfo("Success", f"File {file} downloaded!")
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during download: {e}")
    finally:
        client_socket.close()
        if 'progress_bar' in locals():
            progress_bar.destroy()

def upload_file(ip, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    window = tk.Tk()
    try:
        client_socket.connect((ip, port))
        file_name = file_path.split('/')[-1]
        client_socket.send(f"UPLOAD {file_name}".encode())
        ready = client_socket.recv(1024).decode()
        
        if ready == "READY":
            file_size = os.path.getsize(file_path)
            progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
            progress_bar.place(x=100, y=350)

            with open(file_path, 'rb') as f:
                sent = 0
                while True:
                    packet = f.read(c_size)
                    if not packet:
                        break
                    client_socket.send(packet)
                    sent += len(packet)
                    progress_bar["value"] = (sent / file_size) * 100
                    time.sleep(0.1)
            messagebox.showinfo("Upload Success", f"File {file_name} uploaded!")
        else:
            messagebox.showerror("Upload Error", "Server not ready for upload.")
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during upload: {e}")
    finally:
        client_socket.close()
        if progress_bar:
            progress_bar.destroy()

def list_files(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send("LIST_FILES".encode())
        files = client_socket.recv(4096).decode()
        return files.split('\n')
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Connection Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error listing files: {e}")
        return []
    finally:
        client_socket.close()

def validate_ip_port(ip, port):
    ip_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not ip_pattern.match(ip):
        messagebox.showerror("Input Error", "Please enter a valid IP address.")
        return False
    if not port.isdigit() or not (0 <= int(port) <= 65535):
        messagebox.showerror("Input Error", "Please enter a valid port number (0-65535).")
        return False
    return True

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

def remove_placeholder(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, "end")
        event.widget.config(fg="black")

def restore_placeholder(event, placeholder):
    if event.widget.get() == "":
        add_placeholder(event.widget, placeholder)

def start_gui():
    def download_file():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        selected_files = file_listbox.curselection()
        if not selected_files:
            messagebox.showerror("Selection Error", "Please select at least one file to download.")
            return
        download_path = filedialog.askdirectory()
        if download_path:
            for i in selected_files:
                file = file_listbox.get(i)
                threading.Thread(target=client, args=(ip, port, file, download_path)).start()

    def upload_selected_file():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        file_path = filedialog.askopenfilename()
        if file_path:
            threading.Thread(target=upload_file, args=(ip, port, file_path)).start()

    def refresh_files():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        threading.Thread(target=update_file_list, args=(ip, port)).start()

    def update_file_list(ip, port):
        files = list_files(ip, port)
        file_listbox.delete(0, tk.END)
        for file in files:
            file_listbox.insert(tk.END, file)

    window = tk.Tk()
    window.title("File Transfer Client")
    window.geometry("500x400")
    window.configure(bg='#e0e5ec')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Rounded.TButton", font=("Product Sans", 11), padding=10, relief="flat", background="#4C7DFF", foreground="white", borderwidth=0, anchor="center")
    style.map("Rounded.TButton", background=[("active", "#354B7E")])
    style.configure("TLabel", font=("Product Sans", 12), background='#e0e5ec')

    canvas = tk.Canvas(window, width=500, height=400, bg="#e0e5ec")
    canvas.grid(row=0, column=0, columnspan=2)

    tk.Label(window, text="Server IP:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=30)
    entry_ip = tk.Entry(window, font=("Product Sans", 11), relief="flat", highlightbackground="#ccc", highlightthickness=1)
    entry_ip.place(x=140, y=30, width=250, height=30)
    add_placeholder(entry_ip, "Enter IP address")
    entry_ip.bind("<FocusIn>", lambda event: remove_placeholder(event, "Enter IP address"))
    entry_ip.bind("<FocusOut>", lambda event: restore_placeholder(event, "Enter IP address"))

    tk.Label(window, text="Port:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=70)
    entry_port = tk.Entry(window, font=("Product Sans", 11), relief="flat", highlightbackground="#ccc", highlightthickness=1)
    entry_port.place(x=140, y=70, width=250, height=30)
    add_placeholder(entry_port, "Enter port number")
    entry_port.bind("<FocusIn>", lambda event: remove_placeholder(event, "Enter port number"))
    entry_port.bind("<FocusOut>", lambda event: restore_placeholder(event, "Enter port number"))

    tk.Label(window, text="Available Files:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=110)
    file_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, font=("Product Sans", 10), relief="flat", bg="#F5F7FA", bd=0, highlightthickness=1, highlightbackground="#c0c5ce")
    file_listbox.place(x=30, y=140, width=440, height=120)

    refresh_button = ttk.Button(window, text="Refresh File List", command=refresh_files, style="Rounded.TButton")
    refresh_button.place(x=30, y=270, width=200)

    download_button = ttk.Button(window, text="Download Selected Files", command=download_file, style="Rounded.TButton")
    download_button.place(x=270, y=270, width=200)

    upload_button = ttk.Button(window, text="Upload File", command=upload_selected_file, style="Rounded.TButton")
    upload_button.place(x=150, y=320, width=200)

    def create_tooltip(widget, text):
        tooltip = tk.Toplevel(widget, bg="#333", padx=5, pady=5)
        tooltip.wm_overrideredirect(True)
        tooltip.withdraw()
        tk.Label(tooltip, text=text, fg="white", bg="#333", font=("Product Sans", 10)).pack()

        def show_tooltip(event):
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    create_tooltip(entry_ip, "Enter the server IP address here.")
    create_tooltip(entry_port, "Enter the port number here.")

    window.mainloop()

if __name__ == "__main__":
    start_gui()
'''



import socket
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import re
import time
import os

c_size = 1024

def client(ip, port, file, download_path, progress_bar):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send(file.encode())

        file_size_data = client_socket.recv(8)
        if file_size_data == b"File not found!":
            messagebox.showerror("Error", "File not found on the server.")
            return
        
        file_size = int.from_bytes(file_size_data, 'big')
        save_path = os.path.join(download_path, file)

        received = 0
        with open(save_path, 'wb') as f:
            while received < file_size:
                packet = client_socket.recv(min(c_size, file_size - received))
                if not packet:
                    break
                f.write(packet)
                received += len(packet)
                progress_bar['value'] = (received / file_size) * 100
                progress_bar.update_idletasks()
                #time.sleep(0.1)

        messagebox.showinfo("Success", f"File {file} downloaded!")
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during download: {e}")
    finally:
        client_socket.close()

def upload_file(ip, port, file_path, progress_bar):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        file_name = os.path.basename(file_path)
        client_socket.send(f"UPLOAD {file_name}".encode())

        # Receive and verify the server's "READY" response
        ready = client_socket.recv(1024).decode()
        if ready != "READY":
            messagebox.showerror("Upload Error", "Server not ready for upload.")
            return

        # Send file data if ready
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            sent = 0
            while True:
                packet = f.read(c_size)
                if not packet:
                    break
                client_socket.send(packet)
                sent += len(packet)
                progress_bar["value"] = (sent / file_size) * 100
                progress_bar.update_idletasks()

        messagebox.showinfo("Upload Success", f"File {file_name} uploaded!")
    
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during upload: {e}")
    finally:
        client_socket.close()


def download_file(ip, port, file, download_path, progress_bar):
    threading.Thread(target=client, args=(ip, port, file, download_path, progress_bar)).start()

def upload_selected_file(ip, port, file_path, progress_bar):
    threading.Thread(target=upload_file, args=(ip, port, file_path, progress_bar)).start()
    
def list_files(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        client_socket.send("LIST_FILES".encode())
        files = client_socket.recv(4096).decode()
        return files.split('\n')
    except (ConnectionRefusedError, ConnectionResetError):
        messagebox.showerror("Connection Error", "Failed to connect to the server. Please check IP address and port number.")
    except Exception as e:
        messagebox.showerror("Error", f"Error listing files: {e}")
        return []
    finally:
        client_socket.close()

def validate_ip_port(ip, port):
    ip_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not ip_pattern.match(ip):
        messagebox.showerror("Input Error", "Please enter a valid IP address.")
        return False
    if not port.isdigit() or not (0 <= int(port) <= 65535):
        messagebox.showerror("Input Error", "Please enter a valid port number (0-65535).")
        return False
    return True
    
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

def remove_placeholder(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, "end")
        event.widget.config(fg="black")

def restore_placeholder(event, placeholder):
    if event.widget.get() == "":
        add_placeholder(event.widget, placeholder)

def start_gui():
    def download_file_wrapper():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        selected_files = file_listbox.curselection()
        if not selected_files:
            messagebox.showerror("Selection Error", "Please select at least one file to download.")
            return
        download_path = filedialog.askdirectory()
        if download_path:
            for i in selected_files:
                file = file_listbox.get(i)
                # Create a progress bar for each download
                progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
                progress_bar.place(x=100, y=370)
                download_file(ip, port, file, download_path, progress_bar)
                
    def refresh_files():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        threading.Thread(target=update_file_list, args=(ip, port)).start()
        
    def update_file_list(ip, port):
        files = list_files(ip, port)
        file_listbox.delete(0, tk.END)
        for file in files:
            file_listbox.insert(tk.END, file)

    def upload_file_wrapper():
        ip = entry_ip.get()
        port = entry_port.get()
        if not validate_ip_port(ip, port):
            return
        port = int(port)
        file_path = filedialog.askopenfilename()
        if file_path:
            progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
            progress_bar.place(x=100, y=370)
            upload_selected_file(ip, port, file_path, progress_bar)

    window = tk.Tk()
    window.title("File Transfer Client")
    window.geometry("500x400")
    window.configure(bg='#e0e5ec')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Rounded.TButton", font=("Product Sans", 11), padding=10, relief="flat", background="#4C7DFF", foreground="white", borderwidth=0, anchor="center")
    style.map("Rounded.TButton", background=[("active", "#354B7E")])
    style.configure("TLabel", font=("Product Sans", 12), background='#e0e5ec')

    tk.Label(window, text="Server IP:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=30)
    entry_ip = tk.Entry(window, font=("Product Sans", 11), relief="flat", highlightbackground="#ccc", highlightthickness=1)
    entry_ip.place(x=140, y=30, width=250, height=30)
    add_placeholder(entry_ip, "Enter IP address")
    entry_ip.bind("<FocusIn>", lambda event: remove_placeholder(event, "Enter IP address"))
    entry_ip.bind("<FocusOut>", lambda event: restore_placeholder(event, "Enter IP address"))

    tk.Label(window, text="Port:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=70)
    entry_port = tk.Entry(window, font=("Product Sans", 11), relief="flat", highlightbackground="#ccc", highlightthickness=1)
    entry_port.place(x=140, y=70, width=250, height=30)
    add_placeholder(entry_port, "Enter port number")
    entry_port.bind("<FocusIn>", lambda event: remove_placeholder(event, "Enter port number"))
    entry_port.bind("<FocusOut>", lambda event: restore_placeholder(event, "Enter port number"))

    tk.Label(window, text="Available Files:", bg='#e0e5ec', font=("Product Sans", 12)).place(x=30, y=110)
    file_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, font=("Product Sans", 10), relief="flat", bg="#F5F7FA", bd=0, highlightthickness=1, highlightbackground="#c0c5ce")
    file_listbox.place(x=30, y=140, width=440, height=120)

    refresh_button = ttk.Button(window, text="Refresh File List", command=refresh_files, style="Rounded.TButton")
    refresh_button.place(x=30, y=270, width=200)

    download_button = ttk.Button(window, text="Download Selected Files", command=download_file_wrapper, style="Rounded.TButton")
    download_button.place(x=270, y=270, width=200)

    upload_button = ttk.Button(window, text="Upload File", command=upload_file_wrapper, style="Rounded.TButton")
    upload_button.place(x=150, y=320, width=200)

    window.mainloop()

if __name__ == "__main__":
    start_gui()













'''
import sys
import re
import socket
import threading
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QProgressBar, QListWidget, QPushButton, QLabel, QLineEdit

c_size = 1024

class FileTransferClient(QtWidgets.QMainWindow):
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Transfer Client")
        self.setGeometry(100, 100, 500, 400)

        # Server IP Input
        self.label_ip = QLabel("Server IP:", self)
        self.label_ip.move(30, 30)
        self.entry_ip = QLineEdit(self)
        self.entry_ip.setPlaceholderText("Enter IP address")
        self.entry_ip.move(140, 30)
        self.entry_ip.resize(250, 25)

        # Port Input
        self.label_port = QLabel("Port:", self)
        self.label_port.move(30, 70)
        self.entry_port = QLineEdit(self)
        self.entry_port.setPlaceholderText("Enter port number")
        self.entry_port.move(140, 70)
        self.entry_port.resize(250, 25)

        # List Files Button
        self.btn_refresh = QPushButton("Refresh File List", self)
        self.btn_refresh.move(30, 270)
        self.btn_refresh.clicked.connect(self.refresh_files)

        # Download Files Button
        self.btn_download = QPushButton("Download Selected Files", self)
        self.btn_download.move(270, 270)
        self.btn_download.clicked.connect(self.download_files)

        # Upload File Button
        self.btn_upload = QPushButton("Upload File", self)
        self.btn_upload.move(150, 320)
        self.btn_upload.clicked.connect(self.upload_file)

        # Available Files List
        self.file_listbox = QListWidget(self)
        self.file_listbox.setSelectionMode(QListWidget.MultiSelection)
        self.file_listbox.move(30, 120)
        self.file_listbox.resize(440, 120)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 350, 300, 25)
        self.progress_bar.setVisible(False)

        # Connect the progress signal to the update_progress method
        self.progress_signal.connect(self.update_progress)

    def refresh_files(self):
        ip, port = self.entry_ip.text(), self.entry_port.text()
        if self.validate_ip_port(ip, port):
            port = int(port)
            threading.Thread(target=self.update_file_list, args=(ip, port)).start()

    def update_file_list(self, ip, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            client_socket.send("LIST_FILES".encode())
            files = client_socket.recv(4096).decode().split('\n')
            self.file_listbox.clear()
            self.file_listbox.addItems(files)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error listing files: {e}")
        finally:
            client_socket.close()

    def download_files(self):
        ip, port = self.entry_ip.text(), self.entry_port.text()
        if self.validate_ip_port(ip, port):
            port = int(port)
            selected_files = [self.file_listbox.item(i).text() for i in range(self.file_listbox.count()) if self.file_listbox.item(i).isSelected()]
            if selected_files:
                download_path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
                if download_path:
                    for file in selected_files:
                        threading.Thread(target=self.download_file, args=(ip, port, file, download_path)).start()

    def download_file(self, ip, port, file, download_path):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            client_socket.send(file.encode())

            # Receive file size first
            file_size_data = client_socket.recv(8)
            file_size = int.from_bytes(file_size_data, 'big')

            save_path = os.path.join(download_path, file)
            with open(save_path, 'wb') as f:
                self.progress_bar.setVisible(True)
                received = 0
                while received < file_size:
                    data = client_socket.recv(c_size)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
                    self.progress_signal.emit(int((received / file_size) * 100))
            QMessageBox.information(self, "Download Complete", f"File {file} downloaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Download Error", f"Error downloading file: {e}")
        finally:
            self.progress_bar.setVisible(False)
            client_socket.close()

    def upload_file(self):
        ip, port = self.entry_ip.text(), self.entry_port.text()
        if self.validate_ip_port(ip, port):
            port = int(port)
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
            if file_path:
                threading.Thread(target=self.upload_to_server, args=(ip, port, file_path)).start()

    def upload_to_server(self, ip, port, file_path):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            file_name = os.path.basename(file_path)
            client_socket.send(f"UPLOAD {file_name}".encode())
            
            ready = client_socket.recv(1024).decode()
            if ready == "READY":
                file_size = os.path.getsize(file_path)
                self.progress_bar.setVisible(True)
                sent = 0
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(c_size)
                        if not data:
                            break
                        client_socket.send(data)
                        sent += len(data)
                        self.progress_signal.emit(int((sent / file_size) * 100))
                QMessageBox.information(self, "Upload Success", f"File {file_name} uploaded successfully.")
            else:
                QMessageBox.critical(self, "Upload Error", "Server not ready for upload.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during upload: {e}")
        finally:
            self.progress_bar.setVisible(False)
            client_socket.close()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def validate_ip_port(self, ip, port):
        if not re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip) or not port.isdigit() or not (0 <= int(port) <= 65535):
            QMessageBox.critical(self, "Input Error", "Please enter a valid IP address and port number.")
            return False
        return True

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client_window = FileTransferClient()
    client_window.show()
    sys.exit(app.exec_())
'''
