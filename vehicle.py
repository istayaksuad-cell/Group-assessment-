from abc import ABC, abstractmethod


class Vehicle(ABC):
    
    def __init__(self, registrationNumber):
        self.registrationNumber = registrationNumber
        self.vehicleType = None
    
    @abstractmethod
    def VehicleType(self):
        pass
    
    @abstractmethod
    def SpaceRequired(self):
        pass
    
    def PlateNumber(self):
        return self.registrationNumber
    
    def __str__(self):
        return f"{self.vehicleType} - {self.registrationNumber}"


class Car(Vehicle):
    
    def __init__(self, registrationNumber):
        super().__init__(registrationNumber)
        self.vehicleType = "Car"
    
    def VehicleType(self):
        return "Car"
    
    def SpaceRequired(self):
        return 1


class Bike(Vehicle):
    
    def __init__(self, registrationNumber):
        super().__init__(registrationNumber)
        self.vehicleType = "Motorcycle"
    
    def VehicleType(self):
        return "Motorcycle"
    
    def SpaceRequired(self):
        return 1


class Track(Vehicle):
    
    def __init__(self, registrationNumber):
        super().__init__(registrationNumber)
        self.vehicleType = "Truck"
    
    def VehicleType(self):
        return "Truck"
    
    def SpaceRequired(self):
        return 2


class Bus(Vehicle):
    
    def __init__(self, registrationNumber):
        super().__init__(registrationNumber)
        self.vehicleType = "Bus"
    
    def VehicleType(self):
        return "Bus"
    
    def SpaceRequired(self):
        return 3
