#needed imports
from enum import Enum, auto
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Dict


#VehicleType enum to rep different vehicle types
class VehicleType(Enum):
    CAR = auto()
    TRUCK = auto()
    MOTORCYCLE = auto()
    BUS = auto()
    ELECTRIC_CAR = auto()
    ELECTRIC_BIKE = auto()
#Vehicle class that is an abstract base class for all vehicle types
@dataclass
class Vehicle(ABC):
    """Base class for all vehicle types """
    regnum: str
    make: str
    model: str
    color: str

    @property
    @abstractmethod
    def vehicle_type(self) -> VehicleType:
        pass

    def __str__(self) -> str:
        return f"{self.vehicle_type.name.title()}: {self.make} {self.model} ({self.regnum})"
    
    # Properties with getters and setters for vehicle attributes
    @property
    def make(self) -> str:
        return self._make
        
    @make.setter
    def make(self, value: str) -> None:
        self._make = value
        
    @property
    def model(self) -> str:
        return self._model
        
    @model.setter
    def model(self, value: str) -> None:
        self._model = value
        
    @property
    def color(self) -> str:
        return self._color
        
    @color.setter
    def color(self, value: str) -> None:
        self._color = value
        
    @property
    def regNum(self) -> str:
        return self._regnum
        
    @regNum.setter
    def regNum(self, value: str) -> None:
        self._regnum = value

class Car(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.CAR

class Truck(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.TRUCK

class Motorcycle(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.MOTORCYCLE


class Bus(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.BUS

#ElectricVehicle Base class and its subclasses
class ElectricVehicle(Vehicle):
    "Base class for all electric vehicles"

    def __init__(self, regnum:str, make:str, model:str, color:str, charge: float = 0.0):
        super().__init__(regnum, make, model, color)
        self.charge = charge  # This will use the setter to validate the value
    
    @property
    def charge(self) -> float:
        "Get the current charge level (0-100)"
        return self._charge
    
    @charge.setter
    def charge(self,value:float) -> None:
        "Set the charge level (0-100)"
        self._charge = max(0.0, min(100.0, value))
    
    def __str__(self) -> str:
        return f"{super().__str__()} [Charge: {self.charge}%]"

class ElectricCar(ElectricVehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.ELECTRIC_CAR
class ElectricBike(ElectricVehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.ELECTRIC_BIKE


#Factory class for creating vehicle instances

class VehicleFactory:
    _vehicle_map ={
        VehicleType.CAR: Car,
        VehicleType.TRUCK: Truck,
        VehicleType.MOTORCYCLE: Motorcycle,
        VehicleType.BUS: Bus,
        VehicleType.ELECTRIC_CAR: ElectricCar,
        VehicleType.ELECTRIC_BIKE: ElectricBike,
    }

    @classmethod
    def create_vehicle(cls, vehicle_type: VehicleType, **kwargs) -> Vehicle:
        """
        Create a vehicle of the specified type.
        
        Args:
            vehicle_type: Type of vehicle to create
            **kwargs: Additional arguments to pass to the vehicle constructor
            
        Returns:
            A new instance of the specified vehicle type
            
        Raises:
            ValueError: If the vehicle type is unknown
        """
        try:
            vehicle_class = cls._vehicle_map[vehicle_type]
            return vehicle_class(**kwargs)
        except KeyError as e:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
if __name__ == "__main__":
    car = VehicleFactory.create_vehicle(
        vehicle_type=VehicleType.CAR,
        regnum="ABC123",
        make="Toyota",
        model="Corolla",
        color="Red"
    )
    electric_car = VehicleFactory.create_vehicle(
        vehicle_type=VehicleType.ELECTRIC_CAR,
        regnum="TESLA123",
        make="Tesla",
        model="Model 3",
        color="White",
        charge=85.5
    )
    print (car)
    print(electric_car)