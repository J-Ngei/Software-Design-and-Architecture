from Vehicle import VehicleFactory, VehicleType, Truck, Bus
from fee_strategy import RegularFee, ElectricFee

class ParkingLot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ParkingLot, cls).__new__(cls)
        return cls._instance

    def initialize(self, capacity, ev_capacity, level):
        self.capacity = capacity
        self.ev_capacity = ev_capacity
        self.level = level
        self.slots = []
        self.ev_slots = []
        self.factory = VehicleFactory()

    def park_vehicle(self, regnum, make, model, color, is_electric=False, is_motorcycle=False, vehicle_type=None):
        """
        Park a vehicle in the parking lot.
        
        Args:
            regnum: Vehicle registration number
            make: Vehicle make
            model: Vehicle model
            color: Vehicle color
            is_electric: Whether the vehicle is electric (for backward compatibility)
            is_motorcycle: Whether the vehicle is a motorcycle (for backward compatibility)
            vehicle_type: Explicit vehicle type (overrides is_electric and is_motorcycle)
        """
        if vehicle_type is None:
            # Backward compatibility with old parameters
            if is_electric:
                v_type = VehicleType.ELECTRIC_BIKE if is_motorcycle else VehicleType.ELECTRIC_CAR
            else:
                v_type = VehicleType.MOTORCYCLE if is_motorcycle else VehicleType.CAR
        else:
            v_type = vehicle_type

        # Create the appropriate vehicle using the factory
        vehicle = self.factory.create_vehicle(
            vehicle_type=v_type,
            regnum=regnum,
            make=make,
            model=model,
            color=color
        )
        # Determine the appropriate slot and fee based on vehicle type
        if v_type in (VehicleType.ELECTRIC_CAR, VehicleType.ELECTRIC_BIKE):
            if len(self.ev_slots) < self.ev_capacity:
                self.ev_slots.append(vehicle)
                fee = ElectricFee().calculate_fee()
                return f"{v_type.name.replace('_', ' ')} {regnum} parked in EV slot {len(self.ev_slots)} (Fee: ${fee})"
            else:
                return "No available EV slots."
        else:
            # For non-EV vehicles, check if they can fit in regular slots
            # Buses and trucks might take more space
            space_needed = 1  # Default space for cars and motorcycles
            if v_type == VehicleType.BUS:
                space_needed = 2
            elif v_type == VehicleType.TRUCK:
                space_needed = 3
                
            if len(self.slots) + space_needed <= self.capacity:
                self.slots.append(vehicle)
                # Add placeholders for larger vehicles
                for _ in range(space_needed - 1):
                    self.slots.append(None)
                fee = RegularFee().calculate_fee() * space_needed
                return f"{v_type.name} {regnum} parked in slot {len(self.slots) - space_needed + 1} (Fee: ${fee})"
            else:
                return f"Not enough space for {v_type.name.lower()}. {self.capacity - len(self.slots)} regular spots left, need {space_needed}."

    def remove_vehicle(self, regnum):
        # First check EV slots
        for i, v in enumerate(self.ev_slots):
            if v is not None and v.regnum == regnum:
                self.ev_slots[i] = None
                return f"EV {regnum} removed."
                
        # Then check regular slots
        for i, v in enumerate(self.slots):
            if v is not None and v.regnum == regnum:
                # Remove the vehicle and any placeholders
                space_freed = 1
                if isinstance(v, (Truck, Bus)):
                    space_freed = 3 if isinstance(v, Truck) else 2
                
                # Clear the vehicle and its placeholders
                for j in range(i, min(i + space_freed, len(self.slots))):
                    self.slots[j] = None
                
                # Clean up any None placeholders
                self.slots = [v for v in self.slots if v is not None]
                return f"{type(v).__name__} {regnum} removed and {space_freed} spot(s) freed."
                
        return "Vehicle not found."

    def get_status(self):
        status = ["--- Parking Lot Status ---"]
        for v in self.slots:
            status.append(f"Regular: {v.regnum} ({v.color} {v.make} {v.model})")
        for v in self.ev_slots:
            status.append(f"EV: {v.regnum} ({v.color} {v.make} {v.model})")
        return "\n".join(status)
        
    def get_parked_vehicles(self):
        """Return a list of all parked vehicles (both regular and EV)."""
        return self.slots + self.ev_slots
