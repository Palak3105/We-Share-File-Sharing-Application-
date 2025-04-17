import os
import socket
import globals
import logging
import subprocess
import tkinter as tk
from generator import generateQRCode
from tkinter import END, filedialog

logging.basicConfig(level=logging.DEBUG)


def browse(Path):
    directory = filedialog.askdirectory()
    logging.info("Selected directory: {name}".format(name=directory))
    Path.delete(0, END)
    Path.insert(0, directory)
    globals.sharepath = directory


def generateQR(msgLabel):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        logging.info("IP address: {addr}".format(addr=IP))
        s.close()
        text = (
            "Scan below QR code to access files or use url http://{addr}:9000".format(
                addr=IP
            )
        )
        msgLabel.configure(text=text)
        qr = generateQRCode(IP)
        image = tk.PhotoImage(file=globals.sharepath + "/qr.png")
        globals.qrImage = image
        globals.codeLabel.config(image=globals.qrImage, width=200, height=166)

    except:
        print("Failed to get QR")


def share(msgLabel):
    os.chdir(globals.sharepath)
    p = subprocess.Popen(["python", "-m", "http.server", "9000"])
    logging.info("Python server started with PID:{pid}".format(pid=p.pid))
    globals.pid = p.pid
    generateQR(msgLabel)


def stop(msgLabel):
    logging.info("Terminating process running with PID:{pid}".format(pid=globals.pid))
    try:
        os.system("taskkill /PID {pid} /f".format(pid=globals.pid))
        text = "FileShare engine has been stopped! You are no-longer sharing."
        msgLabel.configure(text=text)
    except:
        print("Failed to stop server..")


def main():
    logging.info("Main process started with PID:{pid}".format(pid=os.getpid()))
    root = tk.Tk()
    root.title("FileShare")
    root.geometry("650x400")
    root.resizable(0, 0)
    root.configure(background="white")

    tk.Label(
        root,
        text="Welcome to FileShare",
        background="#8EE5EE",
        anchor="sw",
        padx=27,
        height=2,
        font="Helvetica 10 bold",
        width=80,
    ).grid(row=0, column=0)

    tk.Label(
        root,
        text="Select the folder that you want to share in your local network.",
        background="#8EE5EE",
        anchor="nw",
        padx=27,
        height=2,
        font="Helvetica 10",
        width=80,
    ).grid(row=1, column=0)

    Path = tk.Entry(root, font="Helvetica 10", width=68, border=0)
    Path.grid(row=2, column=0, sticky="W", padx=40, pady=10, ipady=2)
    tk.Button(
        root,
        text="Browse",
        background="#8EE5EE",
        command=lambda: browse(Path),
        width=10,
        border=0,
    ).grid(row=2, column=0, sticky="E", padx=100)

    msg = tk.StringVar()
    msgLabel = tk.Label(
        root,
        text="",
        width=59,
        background="white",
        height=1,
        anchor="w",
        font="Helvetica 10",
    )
    msgLabel.grid(row=3, column=0, sticky="W", padx=40)
    logo = tk.PhotoImage(file=globals.currPath + "\images\\logo.png")

    globals.codeLabel = tk.Label(root, image=logo, border=0)
    globals.codeLabel.grid(row=4, column=0, sticky="W", padx=40, pady=10)

    tk.Button(
        root,
        text="Share",
        background="#8EE5EE",
        width=10,
        border=0,
        command=lambda: share(msgLabel),
    ).grid(row=5, column=0, sticky="E", padx=200)
    tk.Button(
        root,
        text="Stop",
        background="#8EE5EE",
        width=10,
        border=0,
        command=lambda: stop(msgLabel),
    ).grid(row=5, column=0, sticky="E", padx=100)

    tk.Label(
        root,
        text="",
        background="white",
        anchor="nw",
        padx=27,
        height=1,
        font="Helvetica 10",
        width=80,
    ).grid(row=6, column=0)

    tk.Label(
        root,
        text="",
        background="#8EE5EE",
        anchor="nw",
        padx=27,
        height=1,
        font="Helvetica 10",
        width=80,
    ).grid(row=7, column=0)

    root.mainloop()


if __name__ == "__main__":
    main()
