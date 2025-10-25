import tkinter as tk
from tkinter import messagebox
import tkinter as tk
from tkinter import messagebox, ttk
from controller import ParkingController
from Vehicle import VehicleType

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

        # Vehicle type selection
        tk.Label(frame_vehicle, text="Vehicle Type:").grid(row=1, column=1, padx=5)
        
        # Create a variable to hold the selected vehicle type
        self.vehicle_type = tk.StringVar()
        self.vehicle_type.set("CAR")  # Default to Car
        
        # Create the dropdown menu
        vehicle_types = [
            ("Car", "CAR"),
            ("Truck", "TRUCK"),
            ("Motorcycle", "MOTORCYCLE"),
            ("Bus", "BUS"),
            ("Electric Car", "ELECTRIC_CAR"),
            ("Electric Bike", "ELECTRIC_BIKE")
        ]
        
        # Create the dropdown menu
        self.vehicle_type_menu = tk.OptionMenu(
            frame_vehicle, 
            self.vehicle_type, 
            *[vt[1] for vt in vehicle_types],
            command=self.on_vehicle_type_change
        )
        self.vehicle_type_menu.config(width=12)
        self.vehicle_type_menu.grid(row=1, column=2, padx=5)
        
        # Store vehicle type mapping
        self.vehicle_type_map = {vt[1]: vt[0] for vt in vehicle_types}
        
        # Add a label to show the selected vehicle type
        self.vehicle_type_label = tk.Label(frame_vehicle, text="Car")
        self.vehicle_type_label.grid(row=1, column=3, padx=5)

        # Adjust button positions to accommodate the new dropdown
        tk.Button(frame_vehicle, text="Park Vehicle", command=self.park_vehicle).grid(row=1, column=4, padx=5)
        tk.Button(frame_vehicle, text="Remove Vehicle", command=self.remove_vehicle).grid(row=1, column=5, padx=5)
        tk.Button(frame_vehicle, text="View Status", command=self.view_status).grid(row=1, column=6, padx=5)

        # EV Charging Controls
        frame_charging = tk.LabelFrame(self.root, text="EV Charging Management", font="Arial 12 bold", padx=10, pady=10)
        frame_charging.pack(padx=10, pady=5, fill="x")
        
        tk.Button(frame_charging, text="View Charging Status", command=self.view_charging_status).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_charging, text="Stop Charging", command=self.stop_charging).pack(side=tk.LEFT, padx=5)
        
        # Output Text Area with Scrollbar
        frame_output = tk.Frame(self.root)
        frame_output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_output)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output = tk.Text(frame_output, width=80, height=25, yscrollcommand=scrollbar.set)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.output.yview)
        
        # Configure tags for better output formatting
        self.output.tag_configure('header', font=('Arial', 10, 'bold'))
        self.output.tag_configure('success', foreground='green')
        self.output.tag_configure('error', foreground='red')

    def create_lot(self):
        msg = self.controller.create_lot(
            int(self.entry_regular.get() or 0),
            int(self.entry_ev.get() or 0),
            int(self.entry_level.get() or 1)
        )
        self.display(msg)

    def on_vehicle_type_change(self, *args):
        """Update the vehicle type label when selection changes"""
        selected_type = self.vehicle_type.get()
        self.vehicle_type_label.config(text=self.vehicle_type_map.get(selected_type, selected_type))
        
    def park_vehicle(self):
        try:
            reg = self.reg.get().strip()
            make = self.make.get().strip()
            model = self.model.get().strip()
            color = self.color.get().strip()
            vehicle_type = self.vehicle_type.get()
            
            if not all([reg, make, model, color]):
                messagebox.showwarning("Input Required", "Please fill in all vehicle details")
                return
            
            # Map the vehicle type to the appropriate parameters
            is_electric = vehicle_type in ("ELECTRIC_CAR", "ELECTRIC_BIKE")
            is_motorcycle = vehicle_type in ("MOTORCYCLE", "ELECTRIC_BIKE")
                
            # Use the park method with vehicle type
            msg = self.controller.park(
                regnum=reg,
                make=make,
                model=model,
                color=color,
                is_electric=is_electric,
                is_motorcycle=is_motorcycle,
                vehicle_type=getattr(VehicleType, vehicle_type) if hasattr(VehicleType, vehicle_type) else None
            )
            self.display(f"✅ {msg}", 'success')
            self.view_status()  # Refresh status after parking
        except Exception as e:
            self.display(f"❌ Error parking vehicle: {str(e)}", 'error')

    def remove_vehicle(self):
        reg = self.reg.get().strip()
        if not reg:
            messagebox.showwarning("Input Required", "Please enter a registration number")
            return
            
        try:
            msg = self.controller.remove(reg)
            self.display(f"✅ {msg}", 'success')
            self.view_status()  # Refresh status after removal
        except Exception as e:
            self.display(f"❌ Error removing vehicle: {str(e)}", 'error')

    def view_status(self):
        try:
            self.output.delete(1.0, tk.END)
            self.display("=== Parking Lot Status ===", 'header')
            self.display(self.controller.get_status())
            self.display("\n=== EV Charging Status ===", 'header')
            self.display(self.controller.get_charging_status())
        except Exception as e:
            self.display(f"Error getting status: {str(e)}", 'error')
    
    def view_charging_status(self):
        try:
            status = self.controller.get_charging_status()
            self.output.delete(1.0, tk.END)
            self.display("=== Detailed EV Charging Status ===", 'header')
            self.display(status)
        except Exception as e:
            self.display(f"Error getting charging status: {str(e)}", 'error')
    
    def stop_charging(self):
        reg = self.reg.get()
        if not reg:
            messagebox.showwarning("Input Required", "Please enter a registration number")
            return
            
        try:
            # Find and stop the charging session for this vehicle
            msg = self.controller.remove(reg)  # This will also stop charging
            self.display(f"Stopped charging for {reg}", 'success')
            self.view_charging_status()  # Refresh charging status
        except Exception as e:
            self.display(f"Error stopping charging: {str(e)}", 'error')

    def display(self, text, tag=None):
        self.output.insert(tk.END, text + "\n", tag)
        self.output.see(tk.END)
        self.output.update()  # Ensure the display updates immediately
