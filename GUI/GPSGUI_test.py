import tkinter as tk
from tkinter import ttk, messagebox
import serial #pip install pyserial
import threading
import re

WIN_WIDTH = 1100
WIN_HEIGHT = 600
PAD = 10

# class DevicePanel:
#     def __init__(self, parent, title):
#         self.frame = ttk.LabelFrame(parent, text=title)
#         self.frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#         self.serial_port = None
#         self.running = False

#         self.create_widgets()

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual GPS Monitor")
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")

        self.left_frame = tk.Frame(root, bg="red")
        self.left_frame.pack(padx=10, pady=10, side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.right_frame = tk.Frame(root, bg="blue")
        self.right_frame.pack(padx=10, pady=10, side=tk.RIGHT, expand=1, fill=tk.BOTH)

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()