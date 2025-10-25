from datetime import datetime
from parking_lot import ParkingLot
from EVChargingManager import EVChargingManager, ChargerStatus
from Vehicle import VehicleFactory, VehicleType, ElectricVehicle

class ParkingController:
    def __init__(self):
        self.lot = ParkingLot()
        self.ev_charging_mgr = EVChargingManager()

    def create_lot(self, capacity, ev_capacity, level):
        self.lot.initialize(capacity, ev_capacity, level)
        # Register EV chargers based on EV capacity
        for i in range(1, ev_capacity + 1):
            charger_id = f"EV{str(i).zfill(3)}"
            connector_type = "CCS" if i % 2 == 0 else "Type2"  # Alternate charger types
            max_kw = 50.0 if i % 2 == 0 else 22.0  # Different power levels
            self.ev_charging_mgr.register_charger(charger_id, connector_type, max_kw)
        return f"Created parking lot: {capacity} regular, {ev_capacity} EV slots on level {level}. Registered {ev_capacity} EV chargers."

    def park(self, regnum, make, model, color, is_electric=None, is_motorcycle=None, vehicle_type=None):
        """
        Park a vehicle in the parking lot.
        
        Args:
            regnum: Vehicle registration number
            make: Vehicle make
            model: Vehicle model
            color: Vehicle color
            is_electric: (Optional) Whether the vehicle is electric
            is_motorcycle: (Optional) Whether the vehicle is a motorcycle
            vehicle_type: (Optional) Explicit VehicleType enum value
        """
        try:
            # If vehicle_type is provided, determine is_electric and is_motorcycle from it
            if vehicle_type is not None:
                is_electric = vehicle_type in (VehicleType.ELECTRIC_CAR, VehicleType.ELECTRIC_BIKE)
                is_motorcycle = vehicle_type in (VehicleType.MOTORCYCLE, VehicleType.ELECTRIC_BIKE)
            elif is_electric is None or is_motorcycle is None:
                raise ValueError("Either vehicle_type or both is_electric and is_motorcycle must be provided")
                
            # Park the vehicle
            result = self.lot.park_vehicle(
                regnum=regnum,
                make=make,
                model=model,
                color=color,
                is_electric=is_electric,
                is_motorcycle=is_motorcycle,
                vehicle_type=vehicle_type
            )
            
            # If it's an electric vehicle, try to start a charging session
            if is_electric:
                ev_vehicle_type = VehicleType.ELECTRIC_BIKE if is_motorcycle else VehicleType.ELECTRIC_CAR
                ev = VehicleFactory.create_vehicle(
                    vehicle_type=ev_vehicle_type,
                    regnum=regnum,
                    make=make,
                    model=model,
                    color=color,
                    charge=0.0  # Default charge level
                )
                # Find an available charger
                for charger_id, charger in self.ev_charging_mgr.chargers.items():
                    if charger.status == ChargerStatus.AVAILABLE:
                        session_id = f"SESS_{regnum}"
                        self.ev_charging_mgr.start_session(session_id, charger_id, ev)
                        return f"{result} and started charging at {charger_id}"
                return f"{result} (No charging stations available)"
                
            return result
            
        except Exception as e:
            return f"Error parking vehicle: {e}"

    def remove(self, regnum):
        # First check if the vehicle is in a charging session
        for session_id, session in self.ev_charging_mgr.sessions.items():
            if session.vehicle.regnum == regnum:
                self.ev_charging_mgr.stop_session(session_id, kwh_used=10.0)  # Example: 10kWh used
                break
        return self.lot.remove_vehicle(regnum)

    def get_status(self):
        status = self.lot.get_status()
        status += "\n\nEV Charging Status:\n"
        
        # Add charging station status
        for charger_id, charger in self.ev_charging_mgr.chargers.items():
            status += f"{charger_id}: {charger.status.name} ({charger.connector_type}, {charger.max_kw}kW)"
            # Find if this charger has an active session
            for session in self.ev_charging_mgr.sessions.values():
                if session.charger_id == charger_id and not session.end_time:
                    status += f" - Charging {session.vehicle.regnum}"
            status += "\n"
            
        # Add waiting vehicles if any
        waiting = [
            v.regnum for v in self.lot.get_parked_vehicles() 
            if isinstance(v, ElectricVehicle) and 
               v.regnum not in [s.vehicle.regnum for s in self.ev_charging_mgr.sessions.values()
                               if not s.end_time]
        ]
        
        if waiting:
            status += "\nVehicles waiting to charge:\n"
            for regnum in waiting:
                status += f"- {regnum}\n"
                
        return status
        
    def get_charging_status(self):
        """Get detailed charging status for all charging stations and sessions."""
        result = ""
        for session_id, session in self.ev_charging_mgr.sessions.items():
            duration = (datetime.now() - session.start_time).total_seconds() / 60  # in minutes
            result += (
                f"Session {session_id}:\n"
                f"  Vehicle: {session.vehicle.regnum}\n"
                f"  Charger: {session.charger_id}\n"
                f"  Started: {session.start_time}\n"
                f"  Duration: {duration:.1f} minutes\n"
            )
            if session.end_time:
                result += f"  Status: Completed\n"
                result += f"  Energy used: {session.kwh_used:.2f} kWh\n"
                result += f"  Cost: {session.cost} KES\n"
            else:
                result += "  Status: Charging\n"
        return result if result else "No active charging sessions."
