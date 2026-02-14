from datetime import datetime


class ParkingPass:
    
    tokenCounter = 1500 
    
    def __init__(self, vehicle, assignedSlots):
        ParkingPass.tokenCounter += 1
        self.tokenNumber = ParkingPass.tokenCounter
        
        self.vehicle = vehicle
        self.registrationNumber = vehicle.PlateNumber()
        self.vehicleType = vehicle.VehicleType()
        
        self.assignedSlots = assignedSlots
        
        self.checkInTime = datetime.now()
        self.checkOutTime = None
        
        self.parkingCharge = 0.0
        self.paymentStatus = False
        self.pricingPlan = None
    
    def logExitTime(self):
        self.checkOutTime = datetime.now()
    
    def calculateParkingTime(self):
        endTime = self.checkOutTime if self.checkOutTime else datetime.now()
        duration = endTime - self.checkInTime
        hoursParked = duration.total_seconds() / 3600
        return hoursParked
    
    def displayTimeSpent(self):
        hoursParked = self.calculateParkingTime()
        hours = int(hoursParked)
        minutes = int((hoursParked - hours) * 60)
        return f"{hours} hours, {minutes} minutes"
    
    def assignParkingFee(self, fee, strategyName):
        self.parkingCharge = fee
        self.pricingPlan = strategyName
    
    def confirmPayment(self):
        self.paymentStatus = True
    
    def passDetails(self):
        status = "Settled" if self.paymentStatus else "Pending"
        exitTimeStr = self.checkOutTime.strftime('%Y-%m-%d %H:%M') if self.checkOutTime else "Currently Parked"
        
        details = f"""
        ********** TOKEN DETAILS **********
        Token Number: {self.tokenNumber}
        
        VEHICLE DATA:
        Registration: {self.registrationNumber}
        Category: {self.vehicleType}
        
        PARKING INFO:
        Assigned Slot(s): {', '.join(map(str, self.assignedSlots))}
        Check-In: {self.checkInTime.strftime('%Y-%m-%d %H:%M')}
        Check-Out: {exitTimeStr}
        Duration: {self.displayTimeSpent()}
        
        BILLING SUMMARY:
        Rate Applied: {self.pricingPlan if self.pricingPlan else 'Pending calculation'}
        Total Charge: ${self.parkingCharge:.2f}
        Payment Status: {status}
        **********************************
        """
        return details
    
    def createCheckInReceipt(self):
        receipt = f"""
        ****** URBAN CITY PARKING ******
           ARRIVAL CONFIRMATION
        
        Token #: {self.tokenNumber}
        Date: {self.checkInTime.strftime('%Y-%m-%d')}
        Time: {self.checkInTime.strftime('%H:%M:%S')}
        
        Vehicle: {self.vehicleType}
        Registration: {self.registrationNumber}
        Assigned Slot(s): {', '.join(map(str, self.assignedSlots))}
        
        Retain this receipt for exit.
        Required for payment processing.
        ********************************
        """
        return receipt
    
    def createCheckOutReceipt(self):
        if not self.paymentStatus:
            return "Payment processing incomplete!"
        
        receipt = f"""
        ****** URBAN CITY PARKING ******
          DEPARTURE CONFIRMATION
        
        Token #: {self.tokenNumber}
        
        Arrival: {self.checkInTime.strftime('%Y-%m-%d %H:%M')}
        Departure: {self.checkOutTime.strftime('%Y-%m-%d %H:%M')}
        Parked For: {self.displayTimeSpent()}
        
        Vehicle: {self.vehicleType}
        Registration: {self.registrationNumber}
        
        Rate Plan: {self.pricingPlan}
        Total Paid: ${self.parkingCharge:.2f}
        
        Safe travels! Visit again soon.
        ********************************
        """
        return receipt
