from parkingSystem import GarageManager


def renderMenuScreen():
    print("\n" + "*" * 50)
    print("       URBAN CITY PARKING MANAGEMENT SYSTEM")
    print("*" * 50)
    print("1.  Vehicle Entry")
    print("2.  Vehicle Exit")
    print("3.  Find Vehicle")
    print("4.  Check Availability")
    print("5.  Purchase Monthly Pass")
    print("6.  Purchase Single Entry Pass")
    print("7.  View Pass Details")
    print("8.  View Pricing Information")
    print("9.  View Current Pricing")
    print("10. View Daily Report")
    print("0.  Exit System")
    print("*" * 50)


def vehicleType():
    print("\nSelect Vehicle Type:")
    print("1. Car")
    print("2. Motorcycle")
    print("3. Truck")
    print("4. Bus")
    
    userSelection = input("Enter choice (1-4): ").strip()
    
    vehicleTypes = {
        "1": "Car",
        "2": "Motorcycle",
        "3": "Truck",
        "4": "Bus"
    }
    
    return vehicleTypes.get(userSelection, None)


def main():
    garageController = GarageManager()
    
    while True:
        renderMenuScreen()
        
        userSelection = input("\nEnter your choice: ").strip()

        if userSelection == "1":
            vType = vehicleType()
            
            if vType is None:
                print("Invalid selection! Please try again.")
                continue
            
            registrationNumber = input("Enter License Plate: ").strip().upper()
            
            if registrationNumber == "":
                print("Registration cannot be empty!")
                continue
            
            garageController.handleCheckIn(vType, registrationNumber)
        
        elif userSelection == "2":
            registrationNumber = input("Enter License Plate: ").strip().upper()
            
            if registrationNumber == "":
                print("Registration cannot be empty!")
                continue
            
            result = garageController.handleCheckOut(registrationNumber)
            
            if result:
                ticket, fee = result
                
                if fee > 0:
                    print(f"\nTotal Amount: ${fee:.2f}")
                    confirm = input("Proceed with payment? (y/n): ").strip().lower()
                    
                    if confirm == "y":
                        garageController.paymentProcess(registrationNumber)
                    else:
                        print("Transaction cancelled. Vehicle remains parked.")
                else:
                    garageController.paymentProcess(registrationNumber)
        
        elif userSelection == "3":
            registrationNumber = input("Enter License Plate: ").strip().upper()
            
            if registrationNumber == "":
                print("Registration cannot be empty!")
                continue
            
            garageController.trackVehicle(registrationNumber)
        
        elif userSelection == "4":
            garageController.checkCapacity()
        
        elif userSelection == "5":
            vType = vehicleType()
            
            if vType is None:
                print("Invalid selection! Please try again.")
                continue
            
            registrationNumber = input("Enter License Plate: ").strip().upper()
            
            if registrationNumber == "":
                print("Registration cannot be empty!")
                continue
            
            garageController.buyMonthlySubscription(registrationNumber, vType)
        
        elif userSelection == "6":
            vType = vehicleType()
            
            if vType is None:
                print("Invalid selection! Please try again.")
                continue
            
            registrationNumber = input("Enter License Plate: ").strip().upper()
            
            if registrationNumber == "":
                print("Registration cannot be empty!")
                continue
            
            garageController.buyOneTimeTicket(registrationNumber, vType)
        
        elif userSelection == "7":
            registrationNumber = input("Enter License Plate: ").strip().upper()
            
            if registrationNumber == "":
                print("Registration cannot be empty!")
                continue
            
            garageController.showSubscriptionData(registrationNumber)
        
        elif userSelection == "8":
            garageController.displayChargeInfo()
        
        elif userSelection == "9":
            garageController.showCurrentCharges()
        
        elif userSelection == "10":
            garageController.generateDailySummary()
        
        elif userSelection == "0":
            print("\n" + "*" * 50)
            print("Thank you for choosing Urban City Parking!")
            print("Drive safely!")
            print("*" * 50)
            break
        
        else:
            print("\nInvalid option! Enter a number between 0 and 10.")
            
        input("\nPress Enter to continue...")
        
        
        
if __name__ == "__main__":
    main()
