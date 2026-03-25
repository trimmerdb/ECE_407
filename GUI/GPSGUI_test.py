import tkinter as tk
from tkinter import ttk, messagebox
import serial #pip install pyserial
import threading
import re


'''
TODO
map
add scrolling to raw data
track movement on map?
add radio modification bits
add callsign
'''
WIN_WIDTH = 1100
WIN_HEIGHT = 600
PAD = 5

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual GPS Monitor")
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

        # self.frame = tk.LabelFrame(root, text=title)
        # self.frame.pack(padx=PAD, pady=PAD, side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.serial_port = None
        self.running = False

        #subframes
        self.controls = self.subframe(root, tk.TOP)
        # self.coords = self.subframe(self.frame, tk.TOP)
        self.left_controls = controlPane(self.controls, "Module 1 Configuration")
        self.right_controls = controlPane(self.controls, "Module 2 Configuration")
        self.tab_window = tk.Frame(master=root)
        self.tab_window.pack(side=tk.TOP, padx=PAD, expand=1, fill=tk.BOTH)
        
        #Widgets

        #   data tab
        #       tab options buttons
        self.tab = tk.StringVar(value="Raw Data")
        self.tab_sel_frame=self.subframe(self.tab_window, tk.TOP)
        self.tab1 = self.RadioSetup(self.tab_sel_frame, "Raw Data")
        self.tab2 = self.RadioSetup(self.tab_sel_frame, "Map")
        self.tab3 = self.RadioSetup(self.tab_sel_frame, "Tab 3 that is very important")

        #       tab content
        self.tab_cont_frame = tk.Frame(self.tab_window)
        self.tab_cont_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.raw_data = dataFrame(self.tab_cont_frame)
        self.map = tk.Label(self.tab_cont_frame, text="Map tab")
        self.tab_3 = tk.Label(self.tab_cont_frame, text="Tab 3")
        self.tab_switch()

    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    # def toggle_connection(self):
    #     if not self.running:
    #         try:
    #             port = self.port_entry.get()
    #             baud = int(self.baud_entry.get())

    #             self.serial_port = serial.Serial(port, baud, timeout=1)
    #             self.running = True
    #             self.connect_btn.config(text="Disconnect")

    #             threading.Thread(target=self.read_serial, daemon=True).start()

    #         except Exception as e:
    #             messagebox.showerror("Error", str(e))
    #     else:
    #         self.running = False
    #         if self.serial_port:
    #             self.serial_port.close()
    #         self.connect_btn.config(text="Connect")
        
    # def read_serial(self):
    #     while self.running:
    #         try:
    #             line = self.serial_port.readline().decode(errors="ignore").strip()
    #             if line:
    #                 self.raw_text.insert("end", line + "\n")
    #                 self.raw_text.see("end")
    #                 self.parse_line(line)
    #         except:
    #             break

    # def parse_line(self, line):
    #     """
    #     Example:
    #     109s714:Node 1 | Lat: 37.8325760 Lon: -76.9354560 Fix: 1 Alt: 56 m
    #     """

    #     pattern = r"Node\s+(\d+)\s+\|\s+Lat:\s+([-\d.]+)\s+Lon:\s+([-\d.]+)\s+Fix:\s+(\d+)\s+Alt:\s+([-\d.]+)"
    #     match = re.search(pattern, line)

    #     if match:
    #         node, lat, lon, fix, alt = match.groups()

    #         self.node_var.set(node)
    #         self.lat_var.set(f"{float(lat):.6f}")
    #         self.lon_var.set(f"{float(lon):.6f}")
    #         self.fix_var.set(fix)
    #         self.alt_var.set(f"{float(alt):.1f}")

    def tab_switch(self):
        self.raw_data.pack_forget()
        self.map.pack_forget()
        self.tab_3.pack_forget()

        match self.tab.get():
            case "Raw Data":
                self.raw_data.pack()
            case "Map":
                self.map.pack()
            case "Tab 3":
                self.tab_3.pack()

    # def pack_frame(self, frame, place):
    #     frame.pack(padx=PAD, pady=PAD, side=place, expand=1, fill=tk.BOTH)

    def subframe(self, parent, pack=tk.TOP):
        subframe = tk.Frame(master=parent)
        subframe.pack(padx=PAD, pady=PAD, side=pack, expand=0, fill=tk.X)
        return subframe
    
    def RadioSetup(self, parent, text):
        return tk.Radiobutton(parent, text=text, variable=self.tab, value=text, indicator=0, command=self.tab_switch, background="pink").pack(side=tk.LEFT)

        # self.left_frame = DevicePanel(self, "Module 1")
        # self.left_frame = DevicePanel(self, "Module 2")

class controlPane:
    def __init__(self, parent, title):
        self.frame_pack = tk.TOP
        self.cont_pack = tk.LEFT
        self.frame = tk.LabelFrame(parent, text=title)
        self.frame.pack(side=tk.LEFT)

        self.controls = self.subframe(self.frame, self.frame_pack)
        self.coords = self.subframe(self.frame, self.frame_pack)

        #   control widgets
        self.COM = ttk.Label(self.controls, text="COM Port:").pack(side=self.cont_pack, padx=PAD)
        self.port_entry = ttk.Entry(self.controls, width=10)
        self.port_entry.insert(0, "COM3")
        self.port_entry.pack(side=self.cont_pack, padx=PAD)

        self.spacer(self.controls, multiplier=2)

        self.baud = ttk.Label(self.controls, text="Baud:").pack(side=self.cont_pack, padx=PAD)
        self.baud_entry = ttk.Entry(self.controls, width=8)
        self.baud_entry.insert(0, "115200")
        self.baud_entry.pack(side=self.cont_pack, padx=PAD)

        self.spacer(self.controls, multiplier=8)

        self.connect_btn = ttk.Button(self.controls, text="Connect", command=self.toggle_connection).pack(side=self.cont_pack, padx=PAD)

        #   coord widgets
        self.node = self.subframe(self.coords, self.frame_pack)
        self.node_var = tk.StringVar(value="--")
        ttk.Label(self.node, text="Node:").pack(side=self.cont_pack)
        ttk.Label(self.node, textvariable=self.node_var, font=("Arial", 11, "bold")).pack(side=self.cont_pack)

        self.lat = self.subframe(self.coords, self.frame_pack)
        self.lat_var = tk.StringVar(value="--")
        ttk.Label(self.lat, text="Latitude:").pack(side=self.cont_pack)
        ttk.Label(self.lat, textvariable=self.lat_var).pack(side=self.cont_pack)

        self.lon = self.subframe(self.coords, self.frame_pack)
        self.lon_var = tk.StringVar(value="--")
        ttk.Label(self.lon, text="Longitude:").pack(side=self.cont_pack)
        ttk.Label(self.lon, textvariable=self.lon_var).pack(side=self.cont_pack)

        self.fix = self.subframe(self.coords, self.frame_pack)
        self.fix_var = tk.StringVar(value="--")
        ttk.Label(self.fix, text="Fix:").pack(side=self.cont_pack)
        ttk.Label(self.fix, textvariable=self.fix_var).pack(side=self.cont_pack)

        self.alt = self.subframe(self.coords, self.frame_pack)
        self.alt_var = tk.StringVar(value="--")
        ttk.Label(self.alt, text="Altitude (m):").pack(side=self.cont_pack)
        ttk.Label(self.alt, textvariable=self.alt_var).pack(side=self.cont_pack)

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
    
    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    def subframe(self, parent, pack=tk.TOP):
            subframe = tk.Frame(master=parent)
            subframe.pack(padx=PAD, pady=PAD, side=pack, expand=0, fill=tk.X)
            return subframe

class dataFrame:
    def __init__(self, parent):
        self.frame_left = tk.Frame(master=parent)
        self.frame_right = tk.Frame(master=parent)

        self.label_left = tk.Label(master=self.frame_left, text="Incoming Module 1 Data")
        self.label_left.pack(side=tk.TOP)
        self.label_right = tk.Label(master=self.frame_right, text="Incoming Module 2 Data")
        self.label_right.pack(side=tk.TOP)

        self.text_left = tk.Text(self.frame_left, width=10, height=10, state=tk.DISABLED)
        self.text_left.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=PAD, pady=PAD)
        self.text_right = tk.Text(self.frame_right, width=10, height=10, state=tk.DISABLED)
        self.text_right.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=PAD, pady=PAD)

    def pack(self):
        self.frame_left.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def pack_forget(self):
        self.frame_left.pack_forget()
        self.frame_right.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()