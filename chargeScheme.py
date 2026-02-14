from abc import ABC, abstractmethod
from datetime import datetime


class RateCalculator(ABC):
    
    @abstractmethod
    def calculateFee(self, vehicleType, hoursParked):
        pass
    
    @abstractmethod
    def planTitle(self):
        pass


class RegularPricing(RateCalculator):
    
    def __init__(self):
        self.ratePerHour = {
            "Car": 5.00,
            "Motorcycle": 3.00,
            "Truck": 8.00,
            "Bus": 10.00
        }
    
    def calculateFee(self, vehicleType, hoursParked):
        rate = self.ratePerHour.get(vehicleType, 5.00)
        if hoursParked < 1:
            hoursParked = 1
        hours = int(hoursParked) + (1 if hoursParked % 1 > 0 else 0)
        return rate * hours
    
    def planTitle(self):
        return "Standard Pricing"


class RushHourRates(RateCalculator):
    
    def __init__(self):
        self.ratePerHour = {
            "Car": 7.50,
            "Motorcycle": 4.50,
            "Truck": 12.00,
            "Bus": 15.00
        }
    
    def calculateFee(self, vehicleType, hoursParked):
        rate = self.ratePerHour.get(vehicleType, 7.50)
        if hoursParked < 1:
            hoursParked = 1
        hours = int(hoursParked) + (1 if hoursParked % 1 > 0 else 0)
        return rate * hours
    
    def planTitle(self):
        return "Peak Hour Pricing"


class DiscountedRates(RateCalculator):
    
    def __init__(self):
        self.ratePerHour = {
            "Car": 3.50,
            "Motorcycle": 2.00,
            "Truck": 5.50,
            "Bus": 7.00
        }
    
    def calculateFee(self, vehicleType, hoursParked):
        rate = self.ratePerHour.get(vehicleType, 3.50)
        if hoursParked < 1:
            hoursParked = 1
        hours = int(hoursParked) + (1 if hoursParked % 1 > 0 else 0)
        return rate * hours
    
    def planTitle(self):
        return "Off-Peak Pricing"


class HolidayRates(RateCalculator):
    
    def __init__(self):
        self.ratePerHour = {
            "Car": 6.00,
            "Motorcycle": 3.50,
            "Truck": 9.00,
            "Bus": 12.00
        }
    
    def calculateFee(self, vehicleType, hoursParked):
        rate = self.ratePerHour.get(vehicleType, 6.00)
        if hoursParked < 1:
            hoursParked = 1
        hours = int(hoursParked) + (1 if hoursParked % 1 > 0 else 0)
        return rate * hours
    
    def planTitle(self):
        return "Weekend Pricing"


class ChargeController:
    
    def __init__(self):
        self.regularRates = RegularPricing()
        self.rushHourRates = RushHourRates()
        self.discountRates = DiscountedRates()
        self.holidayRates = HolidayRates()
    
    def determineActiveRate(self):
        now = datetime.now()
        dayOfWeek = now.weekday()
        currentHour = now.hour
        
        if dayOfWeek >= 5:
            return self.holidayRates
        
        if 8 <= currentHour < 18:
            return self.rushHourRates
        
        return self.discountRates
    
    def determineParkingCost(self, vehicleType, hoursParked):
        strategy = self.determineActiveRate()
        fee = strategy.calculateFee(vehicleType, hoursParked)
        return fee, strategy.planTitle()
    
    def displayChargeDetails(self):
        info = """
        ========== PRICING INFORMATION ==========
        
        STANDARD PRICING (Base Rates):
        - Car: $5.00/hour
        - Bike: $3.00/hour
        - Truck: $8.00/hour
        - Bus: $10.00/hour
        
        PEAK HOUR PRICING (8 AM - 6 PM Weekdays):
        - Car: $7.50/hour
        - Bike: $4.50/hour
        - Truck: $12.00/hour
        - Bus: $15.00/hour
        
        OFF-PEAK PRICING (6 PM - 8 AM Weekdays):
        - Car: $3.50/hour
        - Bike: $2.00/hour
        - Truck: $5.50/hour
        - Bus: $7.00/hour
        
        WEEKEND PRICING (Saturday & Sunday):
        - Car: $6.00/hour
        - Bike: $3.50/hour
        - Truck: $9.00/hour
        - Bus: $12.00/hour
        
        =========================================
        """
        return info
