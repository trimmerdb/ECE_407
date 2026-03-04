import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import re


class DevicePanel:
    def __init__(self, parent, title):
        self.frame = ttk.LabelFrame(parent, text=title)
        self.frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.serial_port = None
        self.running = False

        self.create_widgets()

    def create_widgets(self):

        # Connection controls
        ttk.Label(self.frame, text="COM Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_entry = ttk.Entry(self.frame, width=10)
        self.port_entry.grid(row=0, column=1)
        self.port_entry.insert(0, "COM3")

        ttk.Label(self.frame, text="Baud:").grid(row=0, column=2)
        self.baud_entry = ttk.Entry(self.frame, width=8)
        self.baud_entry.grid(row=0, column=3)
        self.baud_entry.insert(0, "115200")

        self.connect_btn = ttk.Button(self.frame, text="Connect",
                                      command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=4, padx=5)

        # Parsed Data
        ttk.Separator(self.frame, orient="horizontal").grid(row=1, columnspan=5, sticky="ew", pady=5)

        self.node_var = tk.StringVar(value="--")
        self.lat_var = tk.StringVar(value="--")
        self.lon_var = tk.StringVar(value="--")
        self.fix_var = tk.StringVar(value="--")
        self.alt_var = tk.StringVar(value="--")

        ttk.Label(self.frame, text="Node:").grid(row=2, column=0, sticky="w")
        ttk.Label(self.frame, textvariable=self.node_var, font=("Arial", 11, "bold")).grid(row=2, column=1)

        ttk.Label(self.frame, text="Latitude:").grid(row=3, column=0, sticky="w")
        ttk.Label(self.frame, textvariable=self.lat_var).grid(row=3, column=1)

        ttk.Label(self.frame, text="Longitude:").grid(row=4, column=0, sticky="w")
        ttk.Label(self.frame, textvariable=self.lon_var).grid(row=4, column=1)

        ttk.Label(self.frame, text="Fix:").grid(row=5, column=0, sticky="w")
        ttk.Label(self.frame, textvariable=self.fix_var).grid(row=5, column=1)

        ttk.Label(self.frame, text="Altitude (m):").grid(row=6, column=0, sticky="w")
        ttk.Label(self.frame, textvariable=self.alt_var).grid(row=6, column=1)

        # Raw data box
        self.raw_text = tk.Text(self.frame, height=10)
        self.raw_text.grid(row=7, column=0, columnspan=5, sticky="nsew", pady=5)

        self.frame.rowconfigure(7, weight=1)
        self.frame.columnconfigure(4, weight=1)

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


class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual GPS Monitor")
        self.root.geometry("1100x600")

        self.device1 = DevicePanel(root, "Device 1")
        self.device2 = DevicePanel(root, "Device 2")


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()