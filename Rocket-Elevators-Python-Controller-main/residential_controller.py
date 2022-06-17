import time


class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators, _status="Active"):

        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.ID = _id
        self.status = _status
        self.elevatorList = []
        self.callButtonList = []
        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        for i in range(_amountOfFloors):
            callButtonID = i + 1
            if buttonFloor < _amountOfFloors:  # If it's not the last floor
                callButton = CallButton(callButtonID, buttonFloor, "up")
                self.callButtonList.append(callButton)
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, "down")  # id, status, floor, direction
                self.callButtonList.append(callButton)
            buttonFloor += 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        for i in range(_amountOfElevators):
            elevatorID = i + 1
            elevator = Elevator(elevatorID, 1)
            self.elevatorList.append(elevator)

    def requestElevator(self, floor, direction):

        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        elevator.operateDoors()
        return elevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = self.elevatorList[0]
        bestScore = 5
        referenceGap = 10000000

        for elevator in self.elevatorList:
            if requestedFloor == elevator.currentFloor and elevator.status == "stopped" and requestedDirection == \
                    elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap,
                                                                       bestElevator, requestedFloor)

            elif requestedFloor > elevator.currentFloor and elevator.direction == "up" and requestedDirection == \
                    elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap,
                                                                       bestElevator, requestedFloor)

            elif requestedFloor < elevator.currentFloor and elevator.direction == "down" and requestedDirection == \
                    elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap,
                                                                       bestElevator, requestedFloor)

            elif elevator.status == "idle":
                bestElevatorInformation = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap,
                                                                       bestElevator, requestedFloor)
            else:
                bestElevatorInformation = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap,
                                                                       bestElevator, requestedFloor)

            bestElevator = bestElevatorInformation.bestElevator
            bestScore = bestElevatorInformation.bestScore
            referenceGap = bestElevatorInformation.referenceGap

        return bestElevator

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)

        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
        return BestElevatorInfo(bestElevator, bestScore, referenceGap)


class Elevator:
    def __init__(self, _id, _currentFloor, _status="idle"):

        self.ID = _id
        self.status = _status
        self.currentFloor = _currentFloor
        self.direction = None
        door = Door(_id)
        self.door = door
        self.floorRequestList = []
        self.floorRequestButtonList = []
        self.createFloorRequestButtons(_currentFloor)

    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1

        for i in range(_amountOfFloors):
            floorRequestButtonID = i + 1
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            floorRequestButtonID += 1

    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.move()
        self.operateDoors()

    def move(self):
        while len(self.floorRequestList) > 0:
            destination = self.floorRequestList[0]
            self.status = "moving"
            if self.currentFloor > destination:
                self.direction = "down"
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor = self.currentFloor - 1
                    self.screenDisplay = self.currentFloor
            elif self.currentFloor < destination:
                self.direction = "up"
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor += 1
                    self.screenDisplay = self.currentFloor
            self.status = "stopped"
            self.floorRequestList.pop(0)
        self.status = "idle"

    def sortFloorList(self):
        if self.direction == "up":
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    def operateDoors(self):
        overweight = False
        obstruction = False
        self.door.status = "open"
        time.sleep(0.5)# nomralemnt c'Est 5 qui faut mettre mais a cause des test sa fait attendre 50 sec
        if overweight == False:
            self.door.status = "closing"
            if obstruction == False:
                self.door.status = "closed"






class BestElevatorInfo:
    def __init__(self, bestElevator, bestScore, referenceGap):
        self.bestElevator = bestElevator
        self.bestScore = bestScore
        self.referenceGap = referenceGap


class CallButton:
    def __init__(self, _id, _floor, _direction, _status="Active"):
        self.ID = _id
        self.status = _status
        self.floor = _floor
        self.direction = _direction


class FloorRequestButton:
    def __init__(self, _id, _floor, _status="Active"):
        self.ID = _id
        self.status = _status
        self.floor = _floor


class Door:
    def __init__(self, _id, _status="Active"):
        self.ID = _id
        self.status = _status
