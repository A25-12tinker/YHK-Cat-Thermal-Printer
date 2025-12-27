#!/usr/bin/env python3
import os
import socket
import struct
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from time import sleep

PREVIEW_WIDTH = 384
PRINTER_WIDTH = 384
ENV_MAC = "THERMAL_PRINTER_MAC"

def initilizePrinter(soc):
    soc.send(b"\x1b\x40")

def sendStartPrintSequence(soc):
    soc.send(b"\x1d\x49\xf0\x19")

def sendEndPrintSequence(soc):
    soc.send(b"\x0a\x0a\x0a\x0a")

def printImage(mac, port, image_path, status_cb):
    try:
        status_cb("Connecting...")
        s = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
        )
        s.connect((mac, port))
        status_cb("Processing...")

        im = Image.open(image_path)
        if im.width > PRINTER_WIDTH:
            h = int(im.height * (PRINTER_WIDTH / im.width))
            im = im.resize((PRINTER_WIDTH, h))
        if im.width < PRINTER_WIDTH:
            padded = Image.new("1", (PRINTER_WIDTH, im.height), 1)
            padded.paste(im)
            im = padded

        im = im.rotate(180)
        if im.mode != "1":
            im = im.convert("1")
        if im.width % 8:
            im2 = Image.new(
                "1", (im.width + 8 - im.width % 8, im.height), 1
            )
            im2.paste(im)
            im = im2
        im = ImageOps.invert(im.convert("L")).convert("1")

        buf = b"".join((
            b"\x1d\x76\x30\x00",
            struct.pack(
                "2B", int(im.width / 8 % 256), int(im.width / 8 / 256)
            ),
            struct.pack("2B", int(im.height % 256), int(im.height / 256)),
            im.tobytes()
        ))

        status_cb("Printing...")
        initilizePrinter(s)
        sleep(0.3)
        sendStartPrintSequence(s)
        sleep(0.3)
        s.send(buf)
        sleep(0.3)
        sendEndPrintSequence(s)
        s.close()
        status_cb("Done")
    except Exception as e:
        status_cb(f"Error: {e}")

class PrinterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YHK Cat Thermal Printer")
        self.geometry("500x700")
        self.image_path = None
        self.preview_img = None

        instructions = (
            "#sh \n"
            "sdptool add --channel=N SP #modify N\n"
            "sudo rfcomm bind N xx:xx:xx:xx:xx:xx #mod.y N and xx:..."
        )
        self.text_instructions = tk.Text(self, height=3, wrap="word")
        self.text_instructions.insert("1.0", instructions)
        self.text_instructions.configure(state="normal")  # można kopiować
        self.text_instructions.pack(fill="x", padx=10, pady=10)

        tk.Label(self, text="MAC:").pack(anchor="w", padx=10, pady=(10, 0))
        self.mac_var = tk.StringVar(value=os.environ.get(ENV_MAC, ""))
        tk.Entry(self, textvariable=self.mac_var).pack(fill="x", padx=10)

        tk.Label(self, text="RFCOMM Port:").pack(anchor="w", padx=10, pady=(10, 0))
        self.port_var = tk.StringVar(value="2")
        tk.Entry(self, textvariable=self.port_var).pack(fill="x", padx=10)

        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.canvas = tk.Canvas(frame, width=PREVIEW_WIDTH)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        tk.Button(self, text="Select picture", command=self.choose_image).pack(pady=5)
        tk.Button(self, text="Print", command=self.print_image).pack(pady=5)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(
            self, textvariable=self.status_var, relief="sunken", anchor="w"
        ).pack(side="bottom", fill="x")

    def set_status(self, msg):
        self.status_var.set(msg)
        self.update_idletasks()

    def choose_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Pictures", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not path:
            return
        self.image_path = path
        img = Image.open(path)
        ratio = PREVIEW_WIDTH / img.width
        img = img.resize((PREVIEW_WIDTH, int(img.height * ratio)))
        self.preview_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_img)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.set_status("Picture loaded")

    def print_image(self):
        if not self.image_path:
            messagebox.showwarning("No picture", "Select picture to print")
            return
        mac = self.mac_var.get()
        if not mac:
            messagebox.showwarning("No MAC", "Input MAC address")
            return
        try:
            port = int(self.port_var.get())
        except ValueError:
            messagebox.showwarning("Invalid port", "RFCOMM port must be a number")
            return
        threading.Thread(
            target=printImage, args=(mac, port, self.image_path, self.set_status), daemon=True
        ).start()

if __name__ == "__main__":
    app = PrinterGUI()
    app.mainloop()

