from parking_lot import ParkingLot

class ParkingController:
    def __init__(self):
        self.lot = ParkingLot()

    def create_lot(self, capacity, ev_capacity, level):
        self.lot.initialize(capacity, ev_capacity, level)
        return f"Created parking lot: {capacity} regular, {ev_capacity} EV slots on level {level}."

    def park(self, regnum, make, model, color, is_electric, is_motorcycle):
        try:
            return self.lot.park_vehicle(regnum, make, model, color, is_electric, is_motorcycle)
        except Exception as e:
            return f"Error parking vehicle: {e}"

    def remove(self, regnum):
        return self.lot.remove_vehicle(regnum)

    def get_status(self):
        return self.lot.get_status()
