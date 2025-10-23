from Vehicle import Car, Motorcycle
from ElectricVehicle import ElectricCar, ElectricBike

class VehicleFactory:
    def create_vehicle(self, regnum, make, model, color, is_electric, is_motorcycle):
        if is_electric:
            return ElectricBike(regnum, make, model, color) if is_motorcycle else ElectricCar(regnum, make, model, color)
        else:
            return Motorcycle(regnum, make, model, color) if is_motorcycle else Car(regnum, make, model, color)
