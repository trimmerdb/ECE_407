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

        #subframes
        self.controls = self.subframe(self.frame, tk.TOP)
        self.coords = self.subframe(self.frame, tk.TOP)
        self.tab_window = tk.LabelFrame(master=self.frame, background="pink")
        self.tab_window.pack(side=tk.TOP, padx=PAD, expand=1, fill=tk.BOTH)
        
        #Widgets
        #   control widgets
        self.COM = ttk.Label(self.controls, text="COM Port:").pack(side=tk.LEFT, padx=PAD)
        self.port_entry = ttk.Entry(self.controls, width=10)
        self.port_entry.insert(0, "COM3")
        self.port_entry.pack(side=tk.LEFT, padx=PAD)

        self.spacer(self.controls, multiplier=2)

        self.baud = ttk.Label(self.controls, text="Baud:").pack(side=tk.LEFT, padx=PAD)
        self.baud_entry = ttk.Entry(self.controls, width=8)
        self.baud_entry.insert(0, "115200")
        self.baud_entry.pack(side=tk.LEFT, padx=PAD)

        self.spacer(self.controls, multiplier=8)

        self.connect_btn = ttk.Button(self.controls, text="Connect", command=self.toggle_connection).pack(side=tk.LEFT, padx=PAD)

        #   coord widgets
        self.node = self.subframe(self.coords, tk.TOP)
        self.node_var = tk.StringVar(value="--")
        ttk.Label(self.node, text="Node:").pack(side=tk.LEFT)
        ttk.Label(self.node, textvariable=self.node_var, font=("Arial", 11, "bold")).pack(side=tk.LEFT)

        self.lat = self.subframe(self.coords, tk.TOP)
        self.lat_var = tk.StringVar(value="--")
        ttk.Label(self.lat, text="Latitude:").pack(side=tk.LEFT)
        ttk.Label(self.lat, textvariable=self.lat_var).pack(side=tk.LEFT)

        self.lon = self.subframe(self.coords, tk.TOP)
        self.lon_var = tk.StringVar(value="--")
        ttk.Label(self.lon, text="Longitude:").pack(side=tk.LEFT)
        ttk.Label(self.lon, textvariable=self.lon_var).pack(side=tk.LEFT)

        self.fix = self.subframe(self.coords, tk.TOP)
        self.fix_var = tk.StringVar(value="--")
        ttk.Label(self.fix, text="Fix:").pack(side=tk.LEFT)
        ttk.Label(self.fix, textvariable=self.fix_var).pack(side=tk.LEFT)

        self.alt = self.subframe(self.coords, tk.TOP)
        self.alt_var = tk.StringVar(value="--")
        ttk.Label(self.alt, text="Altitude (m):").pack(side=tk.LEFT)
        ttk.Label(self.alt, textvariable=self.alt_var).pack(side=tk.LEFT)

        #   data tab
        self.raw_data = tk.Text(self.tab_window, height=10, state=tk.DISABLED).pack(expand=True, fill=tk.BOTH)

    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

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
        
    def read_serial(self):
        while self.running:
            try:
                line = self.serial_port.readline().decode(errors="ignore").strip()
                if line:
                    self.raw_text.insert("end", line + "\n")
                    self.raw_text.see("end")
                    self.parse_line(line)
            except:
                break

    def parse_line(self, line):
        """
        Example:
        109s714:Node 1 | Lat: 37.8325760 Lon: -76.9354560 Fix: 1 Alt: 56 m
        """

        pattern = r"Node\s+(\d+)\s+\|\s+Lat:\s+([-\d.]+)\s+Lon:\s+([-\d.]+)\s+Fix:\s+(\d+)\s+Alt:\s+([-\d.]+)"
        match = re.search(pattern, line)

        if match:
            node, lat, lon, fix, alt = match.groups()

            self.node_var.set(node)
            self.lat_var.set(f"{float(lat):.6f}")
            self.lon_var.set(f"{float(lon):.6f}")
            self.fix_var.set(fix)
            self.alt_var.set(f"{float(alt):.1f}")

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