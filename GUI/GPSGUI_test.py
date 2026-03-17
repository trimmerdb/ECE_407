import tkinter as tk
from tkinter import ttk, messagebox
import serial #pip install pyserial
import threading
import re

WIN_WIDTH = 1100
WIN_HEIGHT = 600
PAD = 5

class DevicePanel:
    def __init__(self, parent, title):
        self.frame = tk.LabelFrame(root, text=title)
        self.frame.pack(padx=PAD, pady=PAD, side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.serial_port = None
        self.running = False

        #Widgets
        self.COM_widget()
        self.baud_widget

        # self.connect_btn = ttk.Button(self.frame, text="Connect",
        #                               command=self.toggle_connection)
        # self.connect_btn.grid(row=0, column=4, padx=5)


        #Placement
        self.COM_place(tk.LEFT)
        self.spacer(tk.LEFT)
        self.baud_place(tk.LEFT)

    def spacer(self, place):
        ttk.Separator(self.frame).pack(side=place)

    def COM_widget(self):
        self.COM = ttk.Label(self.frame, text="COM Port:")
        self.port_entry = ttk.Entry(self.frame, width=10)
        self.port_entry.insert(0, "COM3")
    
    def COM_place(self, place):
        self.COM.pack(side=place, padx=PAD)
        self.port_entry.pack(side=place, padx=PAD)

    def baud_widget(self):
        self.baud = ttk.Label(self.frame, text="Baud:")
        self.baud_entry = ttk.Entry(self.frame, width=8)
        self.baud_entry.insert(0, "115200")

    def baud_place(self, place):
        self.baud.pack(side=place, padx=PAD)
        self.port_entry.pack(side=place, padx=PAD)

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual GPS Monitor")
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

        self.left_frame = DevicePanel(self, "Module 1")
        self.left_frame = DevicePanel(self, "Module 2")

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()