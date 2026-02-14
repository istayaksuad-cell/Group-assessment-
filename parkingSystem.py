from datetime import datetime
from vehicle import Car, Bike, Track, Bus
from slotAllocator import SpaceAllocator
from membershipCard import MonthlySubscription, DayPass
from chargeScheme import ChargeController
from receiptToken import ParkingPass


class GarageManager:
    
    def __init__(self):
        self.slotCoordinator = SpaceAllocator(300)
        self.rateCoordinator = ChargeController()
        self.currentReceipts = {}
        self.passRecords = []
        self.monthlyPermits = {}
        self.singlePermits = {}
        
        self.monthlyIDCounter = 6000  
        self.singleIDCounter = 9000  
        
        self.garageName = "Urban City Parking"
        self.maximumSlots = 300
        
        print(f"\n{self.garageName} System Initialized")
        print(f"Total Parking Capacity: {self.maximumSlots} spaces\n")
    
    def createVehicle(self, vehicleType, registrationNumber):
        vehicleType = vehicleType.lower()
        
        vehicleMap = {
            "car": Car,
            "motorcycle": Bike,
            "truck": Track,
            "bus": Bus
        }
        
        if vehicleType in vehicleMap:
            return vehicleMap[vehicleType](registrationNumber)
        else:
            print(f"Unrecognized vehicle category: {vehicleType}")
            return None
    
    def verifyMonthlySubscription(self, registrationNumber):
        if registrationNumber in self.monthlyPermits:
            return self.monthlyPermits[registrationNumber].checkValidity()
        return False
    
    def checkDayPass(self, registrationNumber):
        if registrationNumber in self.singlePermits:
            return self.singlePermits[registrationNumber].checkValidity()
        return False
    
    def verifySubscription(self, registrationNumber):
        return self.verifyMonthlySubscription(registrationNumber) or self.checkDayPass(registrationNumber)
    
    def handleCheckIn(self, vehicleType, registrationNumber):
        if registrationNumber in self.currentReceipts:
            print(f"\nAlert: Vehicle {registrationNumber} already has active token!")
            return None
        
        vehicle = self.createVehicle(vehicleType, registrationNumber)
        if vehicle is None:
            return None
        
        hasValidPass = self.verifySubscription(registrationNumber)
        
        slotsNeeded = vehicle.SpaceRequired()
        if not self._checkSlotAvailability(slotsNeeded):
            return None
        
        reservedSlots = self.slotCoordinator.allocateSpace(vehicle)
        if reservedSlots is None:
            print("\nError: Slot allocation failed.")
            return None
        
        ticket = ParkingPass(vehicle, reservedSlots)
        self.currentReceipts[registrationNumber] = ticket
        
        self._displayCheckInConfirmation(ticket, registrationNumber, vehicle, reservedSlots, hasValidPass)
        
        return ticket
    
    def _checkSlotAvailability(self, slotsNeeded):
        availableSlots = self.slotCoordinator.availableSpaces()
        if availableSlots < slotsNeeded:
            print(f"\nInsufficient capacity!")
            print(f"Needed: {slotsNeeded} | Available: {availableSlots}")
            return False
        return True
    
    def _displayCheckInConfirmation(self, ticket, registrationNumber, vehicle, reservedSlots, hasValidPass):
        print("\n" + "*" * 40)
        print("        CHECK-IN COMPLETED")
        print("*" * 40)
        print(f"Registration: {registrationNumber}")
        print(f"Category: {vehicle.VehicleType()}")
        print(f"Assigned Slot(s): {', '.join(map(str, reservedSlots))}")
        print(f"Arrival Time: {ticket.checkInTime.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if hasValidPass:
            print(f"Subscription: ACTIVE MEMBERSHIP VERIFIED")
        
        print("*" * 40)
        print(ticket.createCheckInReceipt())
    
    def handleCheckOut(self, registrationNumber):
        if registrationNumber not in self.currentReceipts:
            print(f"\nAlert: No active token found for {registrationNumber}!")
            return None
        
        ticket = self.currentReceipts[registrationNumber]
        ticket.logExitTime()
        
        fee, strategyName = self._calculateDepartureFee(ticket, registrationNumber)
        ticket.assignParkingFee(fee, strategyName)
        
        self._displayDepartureSummary(ticket, registrationNumber, strategyName, fee)
        
        return ticket, fee
    
    def _calculateDepartureFee(self, ticket, registrationNumber):
        if self.verifyMonthlySubscription(registrationNumber):
            print("\nMonthly Subscription Applied - Complimentary parking!")
            return 0.0, "Monthly Subscription - No Charge"
        elif self.checkDayPass(registrationNumber):
            print("\nDay Pass Redeemed - Prepaid entry!")
            self.singlePermits[registrationNumber].usePass()
            return 0.0, "Single Entry Pass - Prepaid"
        else:
            duration = ticket.calculateParkingTime()
            fee, strategyName = self.rateCoordinator.determineParkingCost(
                ticket.vehicleType, duration
            )
            return fee, strategyName
    
    def _displayDepartureSummary(self, ticket, registrationNumber, strategyName, fee):
        print("\n" + "*" * 40)
        print("      DEPARTURE IN PROGRESS")
        print("*" * 40)
        print(f"Token ID: {ticket.tokenNumber}")
        print(f"Registration: {registrationNumber}")
        print(f"Parked For: {ticket.displayTimeSpent()}")
        print(f"Rate Plan: {strategyName}")
        print(f"Amount Due: ${fee:.2f}")
        print("*" * 40)
    
    def paymentProcess(self, registrationNumber):
        if registrationNumber not in self.currentReceipts:
            print(f"\nAlert: No pending transaction for {registrationNumber}")
            return False
        
        ticket = self.currentReceipts[registrationNumber]
        ticket.confirmPayment()
        
        self.slotCoordinator.freeAllocatedSlots(ticket.assignedSlots)
        self.passRecords.append(ticket)
        del self.currentReceipts[registrationNumber]
        
        print("\n" + "*" * 40)
        print("       PAYMENT CONFIRMED")
        print("*" * 40)
        print(ticket.createCheckOutReceipt())
        
        return True
    
    def buyMonthlySubscription(self, registrationNumber, vehicleType):
        self.monthlyIDCounter += 1
        permitID = f"MP-{self.monthlyIDCounter}"
        
        newPass = MonthlySubscription(permitID, registrationNumber, vehicleType)
        self.monthlyPermits[registrationNumber] = newPass
        
        print("\n" + "*" * 40)
        print("  MONTHLY SUBSCRIPTION ACTIVATED")
        print("*" * 40)
        print(newPass.passDetails())
        
        return newPass
    
    def buyOneTimeTicket(self, registrationNumber, vehicleType):
        self.singleIDCounter += 1
        permitID = f"SE-{self.singleIDCounter}"
        
        newPass = DayPass(permitID, registrationNumber, vehicleType)
        self.singlePermits[registrationNumber] = newPass
        
        print("\n" + "*" * 40)
        print("    DAY PASS ACTIVATED")
        print("*" * 40)
        print(newPass.passDetails())
        
        return newPass
    
    def showSubscriptionData(self, registrationNumber):
        found = False
        
        if registrationNumber in self.monthlyPermits:
            print(self.monthlyPermits[registrationNumber].passDetails())
            found = True
        
        if registrationNumber in self.singlePermits:
            print(self.singlePermits[registrationNumber].passDetails())
            found = True
        
        if not found:
            print(f"\nNo subscription found for: {registrationNumber}")
    
    def trackVehicle(self, registrationNumber):
        slotIDs = self.slotCoordinator.searchVehicle(registrationNumber)
        
        if slotIDs:
            ticket = self.currentReceipts.get(registrationNumber)
            print("\n" + "*" * 40)
            print("      VEHICLE LOCATED")
            print("*" * 40)
            print(f"Registration: {registrationNumber}")
            print(f"Located At: {', '.join(map(str, slotIDs))}")
            if ticket:
                print(f"Checked In: {ticket.checkInTime.strftime('%Y-%m-%d %H:%M')}")
                print(f"Parked For: {ticket.displayTimeSpent()}")
            print("*" * 40)
            return True
        else:
            print(f"\nVehicle {registrationNumber} not currently in facility.")
            return False
    
    def checkCapacity(self):
        print(self.slotCoordinator.generateStatusSummary())
        return self.slotCoordinator.availableSpaces()
    
    def displayChargeInfo(self):
        print(self.rateCoordinator.displayChargeDetails())
    
    def showCurrentCharges(self):
        strategy = self.rateCoordinator.determineActiveRate()
        print(f"\nActive Rate Plan: {strategy.planTitle()}")
        return strategy.planTitle()
    
    def generateDailySummary(self):
        today = datetime.now().date()
        
        stats = self._calculateDailyStatistics(today)
        
        report = f"""
        ********** DAILY SUMMARY **********
        Report Date: {today.strftime('%Y-%m-%d')}
        
        TRAFFIC ANALYSIS:
        Total Check-Ins: {stats['entries']}
        Total Departures: {stats['exits']}
        Currently Active: {stats['active']}
        
        CAPACITY STATUS:
        Available Slots: {stats['available']}
        Occupied Slots: {stats['occupied']}
        
        REVENUE SUMMARY:
        Daily Collection: ${stats['revenue']:.2f}
        
        SUBSCRIPTIONS:
        Active Monthly: {stats['monthly']}
        Active Day Pass: {stats['daily']}
        **********************************
        """
        print(report)
        return report
    
    def _calculateDailyStatistics(self, today):
        todayEntries = 0
        todayExits = 0
        todayRevenue = 0.0
        
        for ticket in self.passRecords:
            if ticket.checkInTime.date() == today:
                todayEntries += 1
            if ticket.checkOutTime and ticket.checkOutTime.date() == today:
                todayExits += 1
                todayRevenue += ticket.parkingCharge
        
        for registrationNumber in self.currentReceipts:
            ticket = self.currentReceipts[registrationNumber]
            if ticket.checkInTime.date() == today:
                todayEntries += 1
        
        return {
            'entries': todayEntries,
            'exits': todayExits,
            'active': len(self.currentReceipts),
            'available': self.slotCoordinator.availableSpaces(),
            'occupied': self.slotCoordinator.OccupiedSpaces(),
            'revenue': todayRevenue,
            'monthly': len([p for p in self.monthlyPermits.values() if p.checkValidity()]),
            'daily': len([p for p in self.singlePermits.values() if p.checkValidity()])
        }
