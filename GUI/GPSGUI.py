import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import re

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial GPS Parser")
        self.root.geometry("600x500")

        self.serial_port = None
        self.running = False

        self.create_widgets()

    def create_widgets(self):

        # --- Connection Frame ---
        conn_frame = ttk.LabelFrame(self.root, text="Connection")
        conn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(conn_frame, text="COM Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_entry = ttk.Entry(conn_frame, width=15)
        self.port_entry.grid(row=0, column=1, padx=5)
        self.port_entry.insert(0, "COM3")

        ttk.Label(conn_frame, text="Baud Rate:").grid(row=0, column=2, padx=5)
        self.baud_entry = ttk.Entry(conn_frame, width=10)
        self.baud_entry.grid(row=0, column=3, padx=5)
        self.baud_entry.insert(0, "115200")

        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=4, padx=10)

        # --- Parsed Data Frame ---
        data_frame = ttk.LabelFrame(self.root, text="Parsed Data")
        data_frame.pack(fill="x", padx=10, pady=5)

        self.node_var = tk.StringVar(value="--")
        self.lat_var = tk.StringVar(value="--")
        self.lon_var = tk.StringVar(value="--")
        self.speed_var = tk.StringVar(value="--")

        ttk.Label(data_frame, text="Node:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(data_frame, textvariable=self.node_var, font=("Arial", 12, "bold")).grid(row=0, column=1)

        ttk.Label(data_frame, text="Latitude:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(data_frame, textvariable=self.lat_var, font=("Arial", 12)).grid(row=1, column=1)

        ttk.Label(data_frame, text="Longitude:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(data_frame, textvariable=self.lon_var, font=("Arial", 12)).grid(row=2, column=1)

        ttk.Label(data_frame, text="Speed (m/s):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(data_frame, textvariable=self.speed_var, font=("Arial", 12)).grid(row=3, column=1)

        # --- Raw Data Frame ---
        raw_frame = ttk.LabelFrame(self.root, text="Raw Incoming Data")
        raw_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.raw_text = tk.Text(raw_frame, height=10)
        self.raw_text.pack(fill="both", expand=True)

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
                line = self.serial_port.readline().decode(errors='ignore').strip()
                if line:
                    self.raw_text.insert("end", line + "\n")
                    self.raw_text.see("end")
                    self.parse_line(line)
            except:
                break

    def parse_line(self, line):
        """
        Example input:
        97s200:Node 1 | Lat: 37.8325600 Lon: -76.9355008 Speed: 0.20
        """

        pattern = r"Node\s+(\d+)\s+\|\s+Lat:\s+([-\d.]+)\s+Lon:\s+([-\d.]+)\s+Speed:\s+([-\d.]+)"
        match = re.search(pattern, line)

        if match:
            node, lat, lon, speed = match.groups()

            self.node_var.set(node)
            self.lat_var.set(f"{float(lat):.6f}")
            self.lon_var.set(f"{float(lon):.6f}")
            self.speed_var.set(f"{float(speed):.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()