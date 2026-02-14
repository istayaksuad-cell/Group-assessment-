from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class MembershipCard(ABC):
    
    def __init__(self, permitID, registrationNumber):
        self.permitID = permitID
        self.registrationNumber = registrationNumber
        self.activationDate = datetime.now()
        self.activeStatus = True
    
    @abstractmethod
    def checkValidity(self):
        pass
    
    @abstractmethod
    def passType(self):
        pass
    
    @abstractmethod
    def passDetails(self):
        pass
    
    def subscriptionID(self):
        return self.permitID
    
    def licensePlate(self):
        return self.registrationNumber
    
    def suspendPermit(self):
        self.activeStatus = False


class MonthlySubscription(MembershipCard):
    
    def __init__(self, permitID, registrationNumber, vehicleType):
        super().__init__(permitID, registrationNumber)
        self.vehicleType = vehicleType
        self.terminationDate = self.activationDate + timedelta(days=30)
        self.subscriptionCost = self.purchaseAmount()
    
    def purchaseAmount(self):
        prices = {
            "Car": 150.00,
            "Motorcycle": 75.00,
            "Truck": 250.00,
            "Bus": 300.00
        }
        return prices.get(self.vehicleType, 150.00)
    
    def checkValidity(self):
        currentTime = datetime.now()
        if self.activeStatus and currentTime <= self.terminationDate:
            return True
        return False
    
    def passType(self):
        return "Monthly Pass"
    
    def passDetails(self):
        status = "Active" if self.checkValidity() else "Expired"
        details = f"""
        Pass ID: {self.permitID}
        License Plate: {self.registrationNumber}
        Vehicle Type: {self.vehicleType}
        Issue Date: {self.activationDate.strftime('%Y-%m-%d %H:%M')}
        Expiry Date: {self.terminationDate.strftime('%Y-%m-%d %H:%M')}
        Status: {status}
        Price Paid: ${self.subscriptionCost:.2f}
        ==================================
        """
        return details
    
    def calculateRemainingDays(self):
        if not self.checkValidity():
            return 0
        remaining = self.terminationDate - datetime.now()
        return remaining.days


class DayPass(MembershipCard):

    
    def __init__(self, permitID, registrationNumber, vehicleType):
        super().__init__(permitID, registrationNumber)
        self.vehicleType = vehicleType
        self.redemptionStatus = False
        self.terminationDate = self.activationDate + timedelta(hours=24)
        self.subscriptionCost = self.purchaseAmount()
    
    def purchaseAmount(self):
        prices = {
            "Car": 15.00,
            "Motorcycle": 8.00,
            "Truck": 25.00,
            "Bus": 30.00
        }
        return prices.get(self.vehicleType, 15.00)
    
    def checkValidity(self):
        currentTime = datetime.now()
        if self.activeStatus and not self.redemptionStatus and currentTime <= self.terminationDate:
            return True
        return False
    
    def usePass(self):
        if self.checkValidity():
            self.redemptionStatus = True
            return True
        return False
    
    def passType(self):
        return "Single Entry Pass"
    
    def passDetails(self):
        if self.redemptionStatus:
            status = "Used"
        elif self.checkValidity():
            status = "Active"
        else:
            status = "Expired"
        
        details = f"""
        ======== SINGLE ENTRY PASS ========
        Pass ID: {self.permitID}
        License Plate: {self.registrationNumber}
        Vehicle Type: {self.vehicleType}
        Issue Date: {self.activationDate.strftime('%Y-%m-%d %H:%M')}
        Valid Until: {self.terminationDate.strftime('%Y-%m-%d %H:%M')}
        Status: {status}
        Price: ${self.subscriptionCost:.2f}
        ===================================
        """
        return details
