import tkinter as tk
from tkinter import ttk, messagebox
import serial #pip install pyserial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# import numpy as np
from cartopy import crs as ccrs, feature as cfeature # pip install cartopy
import threading
import re


'''
TODO
map
add scrolling to raw data
track movement on map?
add radio modification bits
add callsign entry
figure out pyinstaller
'''
WIN_WIDTH = 925
WIN_HEIGHT = 220
PAD = 5

DFEAULT_PORT = "COM9"
DEFAULT_BAUD = 115200

MOD_1_COLOR = "thistle1"
MOD_2_COLOR = "lightcyan2"
TAB_COLOR = "darkseagreen2"

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual GPS Monitor")
        self.root.geometry(f"{WIN_WIDTH}x{3*WIN_HEIGHT}")
        self.root.minsize(width=WIN_WIDTH, height=WIN_HEIGHT)
        # self.root.pack_propogate(False)
        self.icon = tk.PhotoImage(file="GUI_icon.png")
        self.root.iconphoto(False, self.icon)

        # print(f"{self.root.winfo_rootx()} , {self.root.winfo_rooty()}")
        # print(self.root.winfo_geometry())

        # self.frame = tk.LabelFrame(root, text=title)
        # self.frame.pack(padx=PAD, pady=PAD, side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.parser = parser()

        #subframes
        self.controls = self.subframe(root, tk.TOP)
        # self.coords = self.subframe(self.frame, tk.TOP)
        self.left_controls = controlPane(self.controls, self.parser, "Module 1 Configuration", MOD_1_COLOR)
        self.right_controls = controlPane(self.controls, self.parser, "Module 2 Configuration", MOD_2_COLOR)
        self.tab_window = tk.Frame(master=root)
        self.tab_window.pack(side=tk.TOP, padx=PAD, expand=1, fill=tk.BOTH)
        
        #Widgets

        #   data tab
        #       tab options buttons
        self.tab = tk.StringVar(value="Raw Data")
        self.tab_sel_frame=self.subframe(self.tab_window, tk.TOP)
        self.tab1 = self.RadioSetup(self.tab_sel_frame, "Raw Data")
        self.tab2 = self.RadioSetup(self.tab_sel_frame, "Map")
        self.tab3 = self.RadioSetup(self.tab_sel_frame, "Tab 3 that i probably need to remove now")

        #       tab content
        self.tab_cont_frame = tk.Frame(self.tab_window)
        self.tab_cont_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.raw_data = dataFrame(self.tab_cont_frame, self.parser)
        # self.map = mapCont(self.tab_cont_frame)
        self.map = tk.Label(self.tab_cont_frame, text="Map tab")
        self.tab_3 = tk.Label(self.tab_cont_frame, text="Tab 3")
        self.tab_switch()

        self.loop()

    def loop(self):
        self.left_controls.update_outputs()
        self.right_controls.update_outputs()

        self.root.after(500,self.loop)

    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    def tab_switch(self):
        self.raw_data.pack_forget()
        self.map.pack_forget()
        self.tab_3.pack_forget()

        match self.tab.get():
            case "Raw Data":
                self.raw_data.pack()
            case "Map":
                self.map.pack()
            case "Tab 3 that i probably need to remove now":
                self.tab_3.pack()

    # def pack_frame(self, frame, place):
    #     frame.pack(padx=PAD, pady=PAD, side=place, expand=1, fill=tk.BOTH)

    def subframe(self, parent, pack=tk.TOP):
        subframe = tk.Frame(master=parent)
        subframe.pack(padx=PAD, pady=PAD, side=pack, expand=0, fill=tk.X)
        return subframe
    
    def RadioSetup(self, parent, text):
        return tk.Radiobutton(parent, text=text, variable=self.tab, value=text, indicator=0, command=self.tab_switch, background=TAB_COLOR).pack(side=tk.LEFT)

        # self.left_frame = DevicePanel(self, "Module 1")
        # self.left_frame = DevicePanel(self, "Module 2")

class parser:
    def __init__(self):
        self.serial_port = None
        self.running = False

        self.port_entry = DFEAULT_PORT
        self.baud_entry = DEFAULT_BAUD

        self.line = "1"
        self.new_line = "2"

    def toggle_connection(self, button):
        if not self.running:
            try:
                self.serial_port = serial.Serial(self.port_entry, self.baud_entry, timeout=1)
                self.running = True
                # self.connect_btn.config(text="Disconnect")
                button.config(text="Disconnect")

                threading.Thread(target=self.read_serial, daemon=True).start()
                # print("connection ON")

            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.running = False
            if self.serial_port:
                self.serial_port.close()
            # self.connect_btn.config(text="Connect")
            button.config(text="Connect")
            # print("connection OFF")
    
    def get_line(self):
        if self.line != self.new_line:
            self.line = self.new_line
            return self.line
        else:
            return ""

    def read_serial(self):
        while self.running:
            try:
                line = self.serial_port.readline().decode(errors="ignore").strip()
                if line:
                    # self.raw_text.insert("end", line + "\n")
                    # self.raw_text.see("end")
                    # self.parse_line(line)
                    self.new_line = line
                    # print("line updated")
            except:
                break
    
    def set_port(self, value=DFEAULT_PORT):
        self.port_entry = value
    
    def set_baud(self, value=DEFAULT_BAUD):
        self.baud_entry = int(value)
    
    def get_running(self):
        return self.running

class controlPane:
    def __init__(self, parent, parser, title, color):
        self.frame_pack = tk.TOP
        self.cont_pack = tk.LEFT
        self.frame = tk.LabelFrame(parent, text=title)
        self.frame.pack(side=tk.LEFT)
        self.parent = parent
        self.parser = parser
        self.parsing_now = False

        self.controls = self.subframe(self.frame, self.frame_pack)
        self.coords = self.subframe(self.frame, self.frame_pack)
        # self.controls.setPallete(color)

        #   control widgets
        self.COM = ttk.Label(self.controls, text="COM Port:").pack(side=self.cont_pack, padx=PAD)
        self.port_entry = ttk.Entry(self.controls, width=10)
        self.port_entry.insert(0, DFEAULT_PORT)
        self.port_entry.pack(side=self.cont_pack, padx=PAD)

        self.spacer(self.controls, multiplier=2)

        self.baud = ttk.Label(self.controls, text="Baud:").pack(side=self.cont_pack, padx=PAD)
        self.baud_entry = ttk.Entry(self.controls, width=8)
        self.baud_entry.insert(0, DEFAULT_BAUD)
        self.baud_entry.pack(side=self.cont_pack, padx=PAD)

        self.spacer(self.controls, multiplier=8)

        self.connect_btn = ttk.Button(self.controls, text="Connect", command=self.update_entries)
        self.connect_btn.pack(side=self.cont_pack, padx=PAD)

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

        self.recolor_children(self.frame, color)
    
    def update_outputs(self):
        # print("attempted value update")
        if(self.parser.get_running() and not self.parsing_now):
            # print("parsing")
            self.parse_line(self.parser.get_line())

    def parse_line(self, line):
        """
        Example:
        109s714:Node 1 | Lat: 37.8325760 Lon: -76.9354560 Fix: 1 Alt: 56 m
        """
        self.parsing_now = True

        pattern = r"Node\s+(\d+)\s+\|\s+Lat:\s+([-\d.]+)\s+Lon:\s+([-\d.]+)\s+Fix:\s+(\d+)\s+Alt:\s+([-\d.]+)"
        match = re.search(pattern, line)

        if match:
            node, lat, lon, fix, alt = match.groups()

            self.node_var.set(node)
            self.lat_var.set(f"{float(lat):.6f}")
            self.lon_var.set(f"{float(lon):.6f}")
            self.fix_var.set(fix)
            self.alt_var.set(f"{float(alt):.1f}")
        
        self.parsing_now = False
    
    def update_entries(self):
        self.parser.set_port(self.port_entry.get())
        self.parser.set_baud(self.baud_entry.get())
        self.parser.toggle_connection(self.connect_btn)

    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    def subframe(self, parent, pack=tk.TOP):
            subframe = tk.Frame(master=parent)
            subframe.pack(padx=PAD, pady=PAD, side=pack, expand=0, fill=tk.X)
            return subframe
    
    def recolor_children(self, frame, color):
        for child in frame.winfo_children():
            child_type = child.winfo_class()
            match child_type:
                case "Frame":
                    self.recolor_children(child, color)
                    # child.configure(bg=color)
                case "TLabel":
                    child.configure(background=color)
                case "TEntry":
                    pass
                case "TSeparator":
                    pass
                case "TButton":
                    pass
                case _:
                    print(child.winfo_class() + " Not recolored")
            frame.configure(bg=color)

class dataFrame:
    def __init__(self, parent, parser):
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

        self.recolor_children(self.frame_left, MOD_1_COLOR)
        self.recolor_children(self.frame_right, MOD_2_COLOR)

    def pack(self):
        self.frame_left.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def pack_forget(self):
        self.frame_left.pack_forget()
        self.frame_right.pack_forget()

    def recolor_children(self, frame, color):
        for child in frame.winfo_children():
            child_type = child.winfo_class()
            match child_type:
                case "Frame":
                    self.recolor_children(child, color)
                    # child.configure(bg=color)
                case "Label":
                    child.configure(background=color)
                case "Text":
                    pass
                case _:
                    print(child.winfo_class() + " Not recolored")
            frame.configure(bg=color)

    def read_serial(self):
        while self.running:
            try:
                line = self.get_line()
                if line:
                    self.raw_text.insert("end", line + "\n")
                    self.raw_text.see("end")
                    # self.parse_line(line)
            except:
                break

class mapCont:
    def __init__(self, parent):
        self.map_frame = tk.Frame(master=parent, bg = "pink")

        # map config
        self.fig = plt.figure(frameon=False, layout="constrained", figsize=[WIN_WIDTH, WIN_HEIGHT])
        # self.ax = plt.subplot(projection=ccrs.PlateCarree(central_longitude=-75))

        # self.ax.coastlines()
        # self.ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='black')
        # self.ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown')

        # map to frame
        # self.canvas = FigureCanvasTkAgg(self.fig, master = self.map_frame)
        # self.canvas.draw()
        # creating the Matplotlib toolbar
        # self.toolbar = NavigationToolbar2Tk(self.canvas, self.map_frame)
        # self.toolbar.update()

        # placing the toolbar on the Tkinter window
        # self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        
    def pack(self):
        self.map_frame.pack(expand=True, fill=tk.BOTH)

        # self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def pack_forget(self):
        self.map_frame.pack_forget()

        # self.canvas.get_tk_widget().pack_forget()


def quit_me():
        root.quit()
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", quit_me)
    app = SerialGUI(root)
    root.mainloop()