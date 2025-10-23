import tkinter as tk
from controller import ParkingController

class ParkingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Lot Manager (Refactored)")
        self.root.geometry("700x800")
        self.root.resizable(0, 0)

        self.controller = ParkingController()
        self.setup_ui()

    def setup_ui(self):
        lbl_title = tk.Label(self.root, text="Parking Lot Manager", font="Arial 16 bold")
        lbl_title.pack(pady=10)

        # Create Lot Controls
        frame_lot = tk.LabelFrame(self.root, text="Create Parking Lot", font="Arial 12 bold", padx=10, pady=10)
        frame_lot.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_lot, text="Regular Slots").grid(row=0, column=0, padx=5, pady=5)
        self.entry_regular = tk.Entry(frame_lot, width=8)
        self.entry_regular.grid(row=0, column=1, padx=5)

        tk.Label(frame_lot, text="EV Slots").grid(row=0, column=2, padx=5, pady=5)
        self.entry_ev = tk.Entry(frame_lot, width=8)
        self.entry_ev.grid(row=0, column=3, padx=5)

        tk.Label(frame_lot, text="Level").grid(row=0, column=4, padx=5, pady=5)
        self.entry_level = tk.Entry(frame_lot, width=6)
        self.entry_level.grid(row=0, column=5, padx=5)

        tk.Button(frame_lot, text="Create Lot", command=self.create_lot).grid(row=0, column=6, padx=10)

        # Vehicle Controls
        frame_vehicle = tk.LabelFrame(self.root, text="Vehicle Management", font="Arial 12 bold", padx=10, pady=10)
        frame_vehicle.pack(padx=10, pady=10, fill="x")

        self.reg = tk.Entry(frame_vehicle, width=10)
        self.make = tk.Entry(frame_vehicle, width=10)
        self.model = tk.Entry(frame_vehicle, width=10)
        self.color = tk.Entry(frame_vehicle, width=10)

        tk.Label(frame_vehicle, text="Reg No").grid(row=0, column=0)
        self.reg.grid(row=0, column=1)
        tk.Label(frame_vehicle, text="Make").grid(row=0, column=2)
        self.make.grid(row=0, column=3)
        tk.Label(frame_vehicle, text="Model").grid(row=0, column=4)
        self.model.grid(row=0, column=5)
        tk.Label(frame_vehicle, text="Color").grid(row=0, column=6)
        self.color.grid(row=0, column=7)

        self.ev = tk.IntVar()
        self.motor = tk.IntVar()
        tk.Checkbutton(frame_vehicle, text="Electric", variable=self.ev).grid(row=1, column=1)
        tk.Checkbutton(frame_vehicle, text="Motorcycle", variable=self.motor).grid(row=1, column=2)

        tk.Button(frame_vehicle, text="Park Vehicle", command=self.park_vehicle).grid(row=1, column=4)
        tk.Button(frame_vehicle, text="Remove Vehicle", command=self.remove_vehicle).grid(row=1, column=5)
        tk.Button(frame_vehicle, text="View Status", command=self.view_status).grid(row=1, column=6)

        # Output Text Area
        self.output = tk.Text(self.root, width=80, height=25)
        self.output.pack(padx=10, pady=10)

    def create_lot(self):
        msg = self.controller.create_lot(
            int(self.entry_regular.get() or 0),
            int(self.entry_ev.get() or 0),
            int(self.entry_level.get() or 1)
        )
        self.display(msg)

    def park_vehicle(self):
        msg = self.controller.park(
            self.reg.get(),
            self.make.get(),
            self.model.get(),
            self.color.get(),
            bool(self.ev.get()),
            bool(self.motor.get())
        )
        self.display(msg)

    def remove_vehicle(self):
        msg = self.controller.remove(self.reg.get())
        self.display(msg)

    def view_status(self):
        msg = self.controller.get_status()
        self.display(msg)

    def display(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
