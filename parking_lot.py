from Vehicle import VehicleFactory, VehicleType
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

    def park_vehicle(self, regnum, make, model, color, is_electric=False, is_motorcycle=False):
        if is_electric:
            v_type = VehicleType.ELECTRIC_BIKE if is_motorcycle else VehicleType.ELECTRIC_CAR
        else:
            v_type = VehicleType.MOTORCYCLE if is_motorcycle else VehicleType.CAR

        vehicle = self.factory.create_vehicle(
            vehicle_type=v_type,
            regnum=regnum,
            make=make,
            model=model,
            color=color
        )
        if is_electric and len(self.ev_slots) < self.ev_capacity:
            self.ev_slots.append(vehicle)
            fee = ElectricFee().calculate_fee()
            return f"EV {regnum} parked in slot {len(self.ev_slots)} (Fee: ${fee})"
        elif not is_electric and len(self.slots) < self.capacity:
            self.slots.append(vehicle)
            fee = RegularFee().calculate_fee()
            return f"Vehicle {regnum} parked in slot {len(self.slots)} (Fee: ${fee})"
        else:
            return "No available slot."

    def remove_vehicle(self, regnum):
        for lst in (self.slots, self.ev_slots):
            for v in lst:
                if v.regnum == regnum:
                    lst.remove(v)
                    return f"Vehicle {regnum} removed."
        return "Vehicle not found."

    def get_status(self):
        status = ["--- Parking Lot Status ---"]
        for v in self.slots:
            status.append(f"Regular: {v.regnum} ({v.color} {v.make} {v.model})")
        for v in self.ev_slots:
            status.append(f"EV: {v.regnum} ({v.color} {v.make} {v.model})")
        return "\n".join(status)
