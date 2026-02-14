from datetime import datetime


class ParkingSlot:
    
    def __init__(self, slotID):
        self.slotID = slotID
        self.slotTaken = False
        self.vehicle = None
        self.checkInTime = None
    
    def assignSlot(self, vehicle):
        if not self.slotTaken:
            self.slotTaken = True
            self.vehicle = vehicle
            self.checkInTime = datetime.now()
            return True
        return False
    
    def releaseSlot(self):
        if self.slotTaken:
            vehicle = self.vehicle
            checkInTime = self.checkInTime
            self.slotTaken = False
            self.vehicle = None
            self.checkInTime = None
            return vehicle, checkInTime
        return None, None
    
    def SlotInfo(self):
        status = "Occupied" if self.slotTaken else "Available"
        info = f"Space #{self.slotID}: {status}"
        if self.slotTaken:
            info += f" | Vehicle: {self.vehicle.PlateNumber()}"
        return info


class SpaceAllocator:
    
    def __init__(self, maximumCapacity=300):
        self.maximumCapacity = maximumCapacity
        self.spaceCollection = {}
        for i in range(1, maximumCapacity + 1):
            self.spaceCollection[i] = ParkingSlot(i)
    
    def availableSpaces(self):
        count = 0
        for slotID in self.spaceCollection:
            if not self.spaceCollection[slotID].slotTaken:
                count += 1
        return count
    
    def OccupiedSpaces(self):
        return self.maximumCapacity - self.availableSpaces()
    
    def searchFreeSpace(self, slotsNeeded=1):
        continuousSlots = 0
        firstSpace = None
        
        for slotID in range(1, self.maximumCapacity + 1):
            if not self.spaceCollection[slotID].slotTaken:
                if continuousSlots == 0:
                    firstSpace = slotID
                continuousSlots += 1
                if continuousSlots >= slotsNeeded:
                    return firstSpace
            else:
                continuousSlots = 0
                firstSpace = None
        
        return None
    
    def allocateSpace(self, vehicle):
        slotsNeeded = vehicle.SpaceRequired()
        firstSpace = self.searchFreeSpace(slotsNeeded)
        
        if firstSpace is None:
            return None 
        
        reservedSlots = []
        for i in range(slotsNeeded):
            slotID = firstSpace + i
            self.spaceCollection[slotID].assignSlot(vehicle)
            reservedSlots.append(slotID)
        
        return reservedSlots
    
    def freeAllocatedSlots(self, assignedSlots):
        vehicleInfo = None
        checkInTime = None
        
        for slotID in assignedSlots:
            if slotID in self.spaceCollection:
                vehicle, entry = self.spaceCollection[slotID].releaseSlot()
                if vehicle is not None:
                    vehicleInfo = vehicle
                    checkInTime = entry
        
        return vehicleInfo, checkInTime
    
    def searchVehicle(self, registrationNumber):
        foundSpaces = []
        for slotID in self.spaceCollection:
            space = self.spaceCollection[slotID]
            if space.slotTaken and space.vehicle.PlateNumber() == registrationNumber:
                foundSpaces.append(slotID)
        return foundSpaces if foundSpaces else None
    
    def generateStatusSummary(self):
        available = self.availableSpaces()
        occupied = self.OccupiedSpaces()
        
        report = f"""
        ====== PARKING SPACE STATUS ======
        Total Spaces: {self.maximumCapacity}
        Available: {available}
        Occupied: {occupied}
        Occupancy Rate: {(occupied/self.maximumCapacity)*100:.1f}%
        ==================================
        """
        return report
