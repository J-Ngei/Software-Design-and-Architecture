# Vehicle Module Documentation

## Overview
The Vehicle module provides a flexible and extensible system for managing different types of vehicles in the Parking Manager system. It's designed using Object-Oriented Programming principles with a focus on maintainability and scalability.

## Core Components

### 1. VehicleType Enum
- Defines all supported vehicle types:
  - `CAR`, `TRUCK`, `MOTORCYCLE`, `BUS`, `ELECTRIC_CAR`, `ELECTRIC_BIKE`
- Uses Python's `enum.auto()` for automatic value assignment

### 2. Base Vehicle Class (`Vehicle`)
- Abstract Base Class (ABC) that serves as the foundation for all vehicle types
- Properties:
  - `regnum`: Vehicle registration number (string)
  - `make`: Vehicle manufacturer (string)
  - `model`: Vehicle model (string)
  - `color`: Vehicle color (string)
- Abstract property `vehicle_type` that must be implemented by all subclasses
- Includes proper getters and setters with type hints
- `__str__` method provides a human-readable representation

### 3. Standard Vehicle Classes
- `Car`, `Truck`, `Motorcycle`, `Bus`
- Each implements the `vehicle_type` property to return the appropriate `VehicleType`
- Inherit all base properties from `Vehicle`

### 4. Electric Vehicle Support
- `ElectricVehicle` (abstract base class extending `Vehicle`)
  - Adds `charge` property (float between 0-100%)
  - Includes charge validation in the setter
  - Overrides `__str__` to include charge level
- Concrete implementations:
  - `ElectricCar`
  - `ElectricBike`

### 5. VehicleFactory (Factory Pattern)
- Centralized creation of vehicle instances
- Uses a class-level dictionary to map `VehicleType` to concrete classes
- `create_vehicle` class method for instantiating vehicles
  - Takes `vehicle_type` and `**kwargs` for vehicle properties
  - Handles validation and error cases

## Usage Examples

```python
# Create a standard car
car = VehicleFactory.create_vehicle(
    vehicle_type=VehicleType.CAR,
    regnum="ABC123",
    make="Toyota",
    model="Corolla",
    color="Red"
)

# Create an electric car with charge
electric_car = VehicleFactory.create_vehicle(
    vehicle_type=VehicleType.ELECTRIC_CAR,
    regnum="TESLA123",
    make="Tesla",
    model="Model 3",
    color="White",
    charge=85.5
)
```

## Design Decisions

1. **Abstract Base Class (ABC)**: Used to enforce implementation of required methods in subclasses
2. **Factory Pattern**: Centralizes object creation logic, making it easier to add new vehicle types
3. **Properties with Type Hints**: Improves code readability and enables better IDE support
4. **Encapsulation**: Internal attributes are protected with getters/setters
5. **Extensibility**: New vehicle types can be added by:
   - Adding to the `VehicleType` enum
   - Creating a new subclass of `Vehicle` (or `ElectricVehicle`)
   - Updating the `_vehicle_map` in `VehicleFactory`

## Notes for Refactoring ParkingManager

1. **Type Checking**: Use `isinstance(vehicle, ElectricVehicle)` to check for electric vehicles
2. **Vehicle Creation**: Always use `VehicleFactory` to create new vehicle instances
3. **String Representation**: The `__str__` method provides a consistent format for display
4. **Error Handling**: The factory includes validation for unknown vehicle types
5. **Extensibility**: The design makes it easy to add new vehicle types with minimal changes to existing code

## Testing

The module includes example usage in the `if __name__ == "__main__":` block that demonstrates creating different vehicle types and printing their string representations.
