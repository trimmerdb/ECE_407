import tkinter as tk
from tkinter import ttk, messagebox
import serial #pip install pyserial
import threading
import re

WIN_WIDTH = 1100
WIN_HEIGHT = 600
PAD = 5

# class subframe:
#     def __init__(self, parent, pack):
#         self.subframe = tk.Frame(master=parent, background="purple")
#         self.subframe.pack(padx=PAD, pady=PAD, side=pack, expand=1, fill = tk.BOTH)

class DevicePanel:
    def __init__(self, parent, title):
        self.frame = tk.LabelFrame(root, text=title)
        self.frame.pack(padx=PAD, pady=PAD, side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.serial_port = None
        self.running = False

        #subframes
        self.controls = self.subframe(self.frame, tk.TOP)
        
        #Widgets
        self.COM_widget(self.controls)
        self.baud_widget(self.controls)
        self.connect_widget(self.controls)

        #Placement
        self.COM_place(tk.LEFT)
        self.spacer(self.controls, multiplier=2)
        self.baud_place(tk.LEFT)
        self.spacer(self.controls, multiplier=8)
        self.connect_place()

    #widget functions
    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    def COM_widget(self, parent):
        self.COM = ttk.Label(master=parent, text="COM Port:")
        self.port_entry = ttk.Entry(master=parent, width=10)
        self.port_entry.insert(0, "COM3")
    def COM_place(self, place = tk.LEFT):
        self.COM.pack(side=place, padx=PAD)
        self.port_entry.pack(side=place, padx=PAD)

    def baud_widget(self, parent):
        self.baud = ttk.Label(master=parent, text="Baud:")
        self.baud_entry = ttk.Entry(master=parent, width=8)
        self.baud_entry.insert(0, "115200")
    def baud_place(self, place = tk.LEFT):
        self.baud.pack(side=place, padx=PAD)
        self.baud_entry.pack(side=place, padx=PAD)

    def connect_widget(self, parent):
        self.connect_btn = ttk.Button(parent, text="Connect", command=self.toggle_connection)
    def connect_place(self, place = tk.LEFT):
        self.connect_btn.pack(side=place, padx=PAD)

    def toggle_connection(self):
        if not self.running:
            try:
                port = self.port_entry.get()
                baud = int(self.baud_entry.get())

                self.serial_port = serial.Serial(port, baud, timeout=1)
                self.running = True
                self.connect_btn.config(text="Disconnect")

                threading.Thread(target=self.read_serial, daemon=True).start()

            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.running = False
            if self.serial_port:
                self.serial_port.close()
            self.connect_btn.config(text="Connect")
        

    #
    def pack_frame(self, frame, place):
        frame.pack(padx=PAD, pady=PAD, side=place, expand=1, fill=tk.BOTH)

    def subframe(self, parent, pack):
        subframe = tk.Frame(master=parent, background="purple")
        subframe.pack(padx=PAD, pady=PAD, side=tk.TOP, expand=0, fill=tk.X)
        return subframe

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