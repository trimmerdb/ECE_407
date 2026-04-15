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


DEFAULT_PORT = "COM9"
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

        self.serial_left = serialConnection("Left", self.data_updates)
        self.serial_right = serialConnection("Right", self.data_updates)

        #subframes
        self.controls = self.subframe(root, tk.TOP)
        self.left_controls = controlFrame(self.controls, self, self.serial_left, "Module 1 Configuration", MOD_1_COLOR)
        self.right_controls = controlFrame(self.controls, self, self.serial_right, "Module 2 Configuration", MOD_2_COLOR)
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
        self.raw_data = dataFrame(self.tab_cont_frame)
        # self.map = mapCont(self.tab_cont_frame)
        self.map = tk.Label(self.tab_cont_frame, text="Map tab")
        self.tab_3 = tk.Label(self.tab_cont_frame, text="Tab 3")
        self.tab_switch()

    def data_updates(self, name, line):
        # print("newline")
        match name:
            case "Left":
                self.left_controls.update_outputs(line)
                self.raw_data.update_left_text(line)
                # print("left line updated")
            case "Right":
                self.right_controls.update_outputs(line)
                self.raw_data.update_right_text(line)

        # self.raw_data.check_for_newline(self.serial_left, self.serial_right)

        # self.map.check_for_newline(self.serial_left)
        # self.map.chekc_for_newline(self.serial_right)

    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    def subframe(self, parent, pack=tk.TOP):
        subframe = tk.Frame(master=parent)
        subframe.pack(padx=PAD, pady=PAD, side=pack, expand=0, fill=tk.X)
        return subframe
    
    def RadioSetup(self, parent, text):
        return tk.Radiobutton(parent, text=text, variable=self.tab, value=text, indicator=0, command=self.tab_switch, background=TAB_COLOR).pack(side=tk.LEFT)

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

class serialConnection:
    def __init__(self, name, func, com_port=DEFAULT_PORT, baud_rate=DEFAULT_BAUD):
        self.name = name
        self.func = func
        self.serial_port = None
        self.running = False
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.line = None

    def set_com(self, com_port):
        self.com_port = com_port
    
    def set_baud(self, baud_rate):
        self.baud_rate = baud_rate

    def toggle_connection(self):
        if not self.running:
            try:
                self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=1)
                self.running = True

                threading.Thread(target=self.read_serial, name = "serial read", daemon=True).start()
            except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            self.running = False
            if self.serial_port:
                self.serial_port.close()

    # def get_line(self):
    #     # if self.line != self.new_line:
    #     #     self.line = self.new_line
    #     return self.line
    #     # else:
    #     #     return ""

    def read_serial(self):
        while self.running:
            try:
                line = self.serial_port.readline().decode(errors="ignore").strip()
                if line:
                    # threading.Thread(target=self.func, args=[self.name, line], name = "main func call", daemon=True).start()
                    self.func(self.name, line)
                    # self.line = line
                    # print(self.line)
            except:
                break

    def get_running(self):
        return self.running

class controlFrame:
    def __init__(self, parent, root, serial, title, color):
        self.frame_pack = tk.TOP
        self.cont_pack = tk.LEFT
        self.frame = tk.LabelFrame(parent, text=title)
        self.frame.pack(side=tk.LEFT)
        self.parent = parent
        self.root = root
        self.serial = serial

        self.controls = self.subframe(self.frame, self.frame_pack)
        self.coords = self.subframe(self.frame, self.frame_pack)

        #   control widgets
        self.COM = ttk.Label(self.controls, text="COM Port:").pack(side=self.cont_pack, padx=PAD)
        self.port_entry = ttk.Entry(self.controls, width=10)
        self.port_entry.insert(0, DEFAULT_PORT)
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
    
    def update_entries(self):
        self.serial.set_com(self.port_entry.get())
        self.serial.set_baud(int(self.baud_entry.get()))

        self.serial.toggle_connection()
        
        if self.serial.get_running():
            self.connect_btn.config(text="Disconnect")
            # self.thread = threading.Thread(target=self.update_outputs, name="controls thread", daemon=True).start()
            # self.root.data_updates()
        else:
            self.connect_btn.config(text="Connect")

    def update_outputs(self, line):
        # while(self.serial.running):
        self.parse_line(line)

    def parse_line(self, line):
        """
        Example:
        109s714:Node 1 | Lat: 37.8325760 Lon: -76.9354560 Fix: 1 Alt: 56 m
        """
        if(not line):
           return
        
        pattern = r"Node\s+(\d+)\s+\|\s+Lat:\s+([-\d.]+)\s+Lon:\s+([-\d.]+)\s+Fix:\s+(\d+)\s+Alt:\s+([-\d.]+)"
        match = re.search(pattern, line)

        if match:
            node, lat, lon, fix, alt = match.groups()

            self.node_var.set(node)
            self.lat_var.set(f"{float(lat):.7f}")
            self.lon_var.set(f"{float(lon):.7f}")
            self.fix_var.set(fix)
            self.alt_var.set(f"{float(alt):.1f}")

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
    def __init__(self, parent):
        self.prev_left = ""
        self.prev_right =""
        self.frame_left = tk.Frame(master=parent)
        self.frame_right = tk.Frame(master=parent)

        self.misc_left = tk.Frame(master=self.frame_left)
        self.misc_left.pack(side=tk.TOP)
        self.label_left = tk.Label(master=self.misc_left, text="Incoming Module 1 Data")
        self.label_left.pack(side=tk.LEFT)
        self.spacer(self.misc_left, multiplier=5)
        self.clear_left_button = tk.Button(master=self.misc_left, text="Clear Text", command=self.clear_left)
        self.clear_left_button.pack(side=tk.LEFT, pady=PAD)
        
        self.misc_right = tk.Frame(master=self.frame_right)
        self.misc_right.pack(side=tk.TOP)
        self.label_right = tk.Label(master=self.misc_right, text="Incoming Module 2 Data")
        self.label_right.pack(side=tk.LEFT)
        self.spacer(self.misc_right, multiplier=5)
        self.clear_right_button = tk.Button(master=self.misc_right, text="Clear Text", command=self.clear_right)
        self.clear_right_button.pack(side=tk.LEFT, pady=PAD)

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
                case "Label":
                    child.configure(background=color)
                case "Text":
                    pass
                case "Button":
                    pass
                case "TSeparator":
                    pass
                case _:
                    print(child.winfo_class() + " not recolored")
            frame.configure(bg=color)

    def spacer(self, parent, place = tk.LEFT, multiplier = 1):
        ttk.Separator(parent).pack(side= place, padx=PAD*multiplier)

    def clear_left(self):
        self.text_left.configure(state=tk.NORMAL)
        self.text_left.delete(1.0, "end")
        self.text_left.configure(state=tk.DISABLED)

    def clear_right(self):
        self.text_right.configure(state=tk.NORMAL)
        self.text_right.delete(1.0, "end")
        self.text_right.configure(state=tk.DISABLED)

    # def check_for_newline(self, serial1, serial2):
    #     if(serial1.get_running()):
    #         threading.Thread(target=self.update_text, args=[serial1], name="Data Left Thread", daemon=True).start()
    #     elif(serial2.get_running()):
    #         threading.Thread(target=self.update_text, args=[serial2], name="Data Right Thread", daemon=True).start()

    # def update_text(self, side, line):
    #     # while(serial.running):
    #     # line = serial.line
    #     # print(line)
    #     # if(line and line !=""):
    #     match side:
    #         case "Left":
    #         #     if(self.prev_left != line):
    #             self.text_left.configure(state=tk.NORMAL)
    #             self.text_left.insert("end", line + "\n")
    #             self.text_left.see("end")
    #             self.text_left.configure(state=tk.DISABLED)
    #             self.prev_left = line
    #         case "Right":
    #         #     if(self.prev_right != line):
    #             self.text_right.configure(state=tk.NORMAL)
    #             self.text_right.insert("end", line + "\n")
    #             self.text_right.see("end")
    #             self.text_right.configure(state=tk.DISABLED)
    #             self.prev_right = line

    def update_left_text(self, line):
        self.text_left.configure(state=tk.NORMAL)
        self.text_left.insert("end", line + "\n")
        self.text_left.see("end")
        self.text_left.configure(state=tk.DISABLED)
        self.prev_left = line

    def update_right_text(self, line):
        self.text_right.configure(state=tk.NORMAL)
        self.text_right.insert("end", line + "\n")
        self.text_right.see("end")
        self.text_right.configure(state=tk.DISABLED)
        self.prev_right = line

class mapCont:
    def __init__(self, parent):
        self.map_frame = tk.Frame(master=parent, bg = "pink")

        # map config
        self.fig = plt.figure(frameon=False, layout="constrained")
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
    
    def check_for_newline(self, side):
        if side.serial.get_running():
            threading.Thread(target=self.parse_line, args=side, name="Map Thread", daemon=True).start()

    def parse_line(self, side):
        while(side.serial.get_running()):
            line = self.parse_line(side.serial.get_line())
            """
            Example:
            109s714:Node 1 | Lat: 37.8325760 Lon: -76.9354560 Fix: 1 Alt: 56 m
            """
            # self.parsing_now = True
            if(not line):
                return
            
            pattern = r"Node\s+(\d+)\s+\|\s+Lat:\s+([-\d.]+)\s+Lon:\s+([-\d.]+)\s+Fix:\s+(\d+)\s+Alt:\s+([-\d.]+)"
            match = re.search(pattern, line)

            if match:
                node, lat, lon, fix, alt = match.groups()

                self.node_var.set(node)
                self.lat_var.set(f"{float(lat):.7f}")
                self.lon_var.set(f"{float(lon):.7f}")
                self.fix_var.set(fix)
                self.alt_var.set(f"{float(alt):.1f}")

def quit_me():
        root.quit()
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", quit_me)
    app = SerialGUI(root)
    root.mainloop()


# pyinstaller GPSGUI.py --name "Dual Redundant GPS GUI" --onefile --hide-console hide-early --icon ".\GUI_icon.png"