from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional
from Vehicle import ElectricVehicle, ElectricCar, ElectricBike, VehicleType

# ==============================
# ENUMS
# ==============================

class ChargerStatus(Enum):
    AVAILABLE = auto()
    OCCUPIED = auto()
    OUT_OF_SERVICE = auto()


# ==============================
# DOMAIN ENTITIES
# ==============================

@dataclass
class Charger:
    charger_id: str
    connector_type: str
    max_kw: float
    status: ChargerStatus = ChargerStatus.AVAILABLE

    def occupy(self):
        if self.status == ChargerStatus.AVAILABLE:
            self.status = ChargerStatus.OCCUPIED
        else:
            raise RuntimeError(f"Charger {self.charger_id} not available.")

    def release(self):
        self.status = ChargerStatus.AVAILABLE


@dataclass
class ChargingSession:
    session_id: str
    charger_id: str
    vehicle: ElectricVehicle
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    kwh_used: float = 0.0
    rate_per_kwh: float = 50.0  # base rate (KES)
    cost: float = 0.0

    def end_session(self, kwh_used: float):
        self.end_time = datetime.now()
        self.kwh_used = kwh_used
        self.cost = round(self.kwh_used * self.rate_per_kwh, 2)
        self.vehicle.charge = min(100.0, self.vehicle.charge + (kwh_used / 0.8))  # Simulate charge increase


# ==============================
# MANAGER
# ==============================

class EVChargingManager:
    def __init__(self):
        self.chargers: Dict[str, Charger] = {}
        self.sessions: Dict[str, ChargingSession] = {}

    def register_charger(self, charger_id: str, connector_type: str, max_kw: float):
        if charger_id in self.chargers:
            raise ValueError(f"Charger {charger_id} already exists.")
        self.chargers[charger_id] = Charger(charger_id, connector_type, max_kw)
        print(f"✅ Registered charger {charger_id} ({connector_type}, {max_kw}kW).")

    def start_session(self, session_id: str, charger_id: str, vehicle: ElectricVehicle):
        charger = self.chargers.get(charger_id)
        if not charger:
            raise ValueError(f"Charger {charger_id} not found.")
        if charger.status != ChargerStatus.AVAILABLE:
            raise RuntimeError(f"Charger {charger_id} is not available.")

        if vehicle.vehicle_type not in [VehicleType.ELECTRIC_CAR, VehicleType.ELECTRIC_BIKE]:
            raise TypeError("Only electric vehicles can start a charging session.")

        charger.occupy()
        session = ChargingSession(session_id, charger_id, vehicle)
        self.sessions[session_id] = session
        print(f"⚡ Charging started for {vehicle} on charger {charger_id} at {session.start_time}.")

    def stop_session(self, session_id: str, kwh_used: float):
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found.")

        session.end_session(kwh_used)
        charger = self.chargers.get(session.charger_id)
        charger.release()

        print(f"🔋 Charging stopped for {session.vehicle}.")
        print(f"⚙️ Total: {session.kwh_used} kWh used at {session.rate_per_kwh} KES/kWh = {session.cost} KES.")
        print(f"Vehicle now charged to {session.vehicle.charge}%.")

        return session

    def get_charger_status(self, charger_id: str) -> ChargerStatus:
        charger = self.chargers.get(charger_id)
        if not charger:
            raise ValueError(f"Charger {charger_id} not found.")
        return charger.status

    def list_chargers(self):
        for c in self.chargers.values():
            print(f"{c.charger_id}: {c.status.name} ({c.connector_type}, {c.max_kw}kW)")


# ==============================
# SAMPLE TEST
# ==============================

if __name__ == "__main__":
    from Vehicle import VehicleFactory

    # Create manager and register chargers
    manager = EVChargingManager()
    manager.register_charger("EV001", "Type2", 22)
    manager.register_charger("EV002", "CCS", 50)

    # Create an electric vehicle
    ev = VehicleFactory.create_vehicle(
        vehicle_type=VehicleType.ELECTRIC_CAR,
        regnum="TESLA123",
        make="Tesla",
        model="Model 3",
        color="White",
        charge=30
    )

    # Start and stop a charging session
    manager.start_session("S001", "EV001", ev)
    manager.stop_session("S001", kwh_used=12.5)
