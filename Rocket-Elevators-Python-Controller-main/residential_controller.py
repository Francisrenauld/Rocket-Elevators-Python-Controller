# elevatorID = 1
# floorRequestButtonID = 1


# "idle", _amountOfFloors
# _status, _amountOfFloors,
# callButtonID = 1
# _status


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
                callButton = CallButton(callButtonID, buttonFloor, "Up")
                self.callButtonList.append(callButton)
                # callButtonID += 1
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, "Down")  # id, status, floor, direction
                self.callButtonList.append(callButton)
                # callButtonID += 1
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
        # elevator.operateDoors
        return elevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = self.elevatorList[0]
        bestScore = 5
        referenceGap = 10000000

        for elevator in self.elevatorList:
            if requestedFloor == elevator.currentFloor and elevator.status == "STOP" and requestedDirection == elevator.direction:
                self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                bestElevatorInformation = BestElevatorInfo(bestElevator, bestScore, referenceGap)

                return bestElevatorInformation.bestElevator
            elif requestedFloor > elevator.currentFloor and elevator.direction == "Up" and requestedDirection == elevator.direction:
                self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                bestElevatorInformation = BestElevatorInfo(bestElevator, bestScore, referenceGap)

                return bestElevatorInformation.bestElevator
            elif requestedFloor < elevator.currentFloor and elevator.direction == "Down" and requestedDirection == elevator.direction:
                self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                bestElevatorInformation = BestElevatorInfo(bestElevator, bestScore, referenceGap)

                return bestElevatorInformation.bestElevator
            elif elevator.status == "idle":
                self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                bestElevatorInformation = BestElevatorInfo(bestElevator, bestScore, referenceGap)

                return bestElevatorInformation.bestElevator
            else:
                self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                bestElevatorInformation = BestElevatorInfo(bestElevator, bestScore, referenceGap)

                return bestElevatorInformation.bestElevator

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = newElevator.currentFloor - floor

        elif bestScore == scoreToCheck:
            gap = newElevator.currentFloor - floor
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
        return BestElevatorInfo(bestElevator, bestScore, referenceGap)


class Elevator:
    def __init__(self, _id, _currentFloor, _status="Active"):

        self.ID = _id
        self.status = _status
        self.currentFloor = _currentFloor
        self.direction = "Nothing"
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
        # self.operateDoors

    def move(self):
        while len(self.floorRequestList) > 0:
            destination = self.floorRequestList[0]
            self.status = "moving"
            if self.currentFloor > destination:
                self.direction = "Up"
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor += 1
                    self.screenDisplay = self.currentFloor
            elif self.currentFloor < destination:
                self.direction = "Down"
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor = self.currentFloor - 1
                    self.screenDisplay = self.currentFloor
            self.status = "Stopped"
            self.floorRequestList.pop(0)
        self.status = "idle"

    def sortFloorList(self):
        if self.direction == "Up":
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)


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

# print("hello world")
# celevator = Elevator(1, 10)

# print(elevator.floorRequestsButtonsList)
column1 = Column(1, 10, 10)
column1.elevatorList[0].currentFloor = 2
column1.elevatorList[0].status = 'idle'
column1.elevatorList[1].currentFloor = 6
column1.elevatorList[1].status = 'idle'
elevator = Elevator(1, 10)

# test.requestElevator(1, "Up")
# print(test)

# print(test.callButtonList)
