## Parking Lot Manager (Refactored)
### Overview

The Parking Lot Manager is a modular, Tkinter-based desktop application designed to simulate a smart vehicle parking system.
This refactored version implements object-oriented design principles and multiple software design patterns to enhance maintainability, scalability, and readability.

The project was developed as part of the Software Design and Architecture coursework.

### System Architecture

The system adopts a Model–View–Controller (MVC) structure to ensure separation of concerns:

| Layer | File | Responsibility |
|----------|----------|----------|
| Model    | parking_lot.py     | Core business logic – manages vehicles, slots, and fee calculation|
| View    | ui.py     | Tkinter-based user interface for interacting with the system|
| Controller | controller.py | Mediates between View and Model, handling user commands|
| Main | main.py | Entry point – initializes and launches the application|

*Additional design patterns integrated into the architecture include:*
- Singleton Pattern – Ensures only one instance of ParkingLot exists.
- Factory Pattern – Centralizes vehicle object creation in VehicleFactory.
- Strategy Pattern – Provides flexible fee calculation via interchangeable strategies (RegularFee, ElectricFee).

### Features
- Create parking lots with separate slots for regular and electric vehicles.
- Park or remove vehicles dynamically.
- Calculate and display parking fees using pluggable strategy classes.
- View live parking status directly from the interface.
- Modular, extensible architecture following OOP and design pattern best practices.

### Folder Structure
```
Software-Design-and-Architecture/
│
├── main.py              # Application entry point
├── ui.py                # Tkinter UI (View)
├── controller.py        # MVC Controller
├── parking_lot.py       # ParkingLot model + Singleton
├── vehicle_factory.py   # Factory Pattern implementation
├── fee_strategy.py      # Strategy Pattern (RegularFee, ElectricFee)
└── README.md            # Project documentation
```
### How to Run
Install Requirements
Python 3.8+ and Tkinter (bundled with most Python installations).

**Clone or Download the Project**
```
git clone https://github.com/J-Ngei/Software-Design-and-Architecture.git
cd Software-Design-and-Architecture
```

**Run the Application**
```
python main.py
```
The Tkinter GUI will launch. You can then:
1. Enter parking lot capacity and click “Create Lot”
2. Add or remove vehicles
3. View parking status and applied fees

### Design Patterns Summary
|Pattern |	Implemented In |	Purpose |
|----------|----------|----------|
|MVC |	ui.py, controller.py, parking_lot.py |	Separates user interface, control, and logic layers |
|Singleton |	parking_lot.py (ParkingLot)	| Ensures one global parking lot instance |
|Factory |	vehicle_factory.py |	Encapsulates creation of vehicle subclasses |
|Strategy |	fee_strategy.py |	Allows interchangeable fee algorithms for vehicle types |

### Extensibility
The design supports easy future enhancements:
- Adding new vehicle categories (e.g., Trucks, Buses) by extending VehicleFactory.
- Integrating time-based fee strategies by adding new FeeStrategy subclasses.
- Implementing an Observer Pattern to auto-update the UI on model changes.
- Expanding to a web-based interface using the same MVC foundation.

### 🧑‍💻 Contributors
- [James Ngei](https://github.com/J-Ngei/)
- [Wendy Wanjiru](https://github.com/wendyshiro/)


### 📚 Acknowledgment
Developed as part of the **MSc in Software Engineering – Software Design and Architecture Project**  
**Quantic School of Business and Technology**
