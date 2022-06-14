# elevatorID = 1
floorRequestButtonID = 1
# callButtonID = 1


class Column:
    def __init__(self, _id, _status, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = _status
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1

        for i in range(_amountOfFloors):
            callButtonID = 1
            if buttonFloor < _amountOfFloors:
                callButton = CallButton(callButtonID, "OFF", buttonFloor, "Up")
                self.callButtonList.append(callButton)
                callButtonID += 1
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, "OFF", buttonFloor, "Down")
                self.callButtonList.append(callButton)
                callButtonID += 1
        buttonFloor += 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):

        for i in range(_amountOfElevators):
            elevatorID = 1
            elevator = Elevator(elevatorID, "idle", _amountOfFloors, 1)
            self.elevatorList.append(elevator)
            elevatorID += 1
            print(self.elevatorList)


class Elevator:
    def __init__(self, _id, _status, _amountOfFloors, _currentFloor):
        self._id = 1
        self._amountOfFloors = _amountOfFloors


class CallButton:
    def __init__(self, _id, _floor, _direction):
        self._id = 1
        self._floor = _floor
        self._direction = _direction


class FloorRequestButton:
    def __init__(self, _id, _floor):
        self._id = 1
        self._floor = _floor


class Door:
    def __init__(self, _id):
        self._id = _id


# print("hello world")

test = Column(1, "OFF", 10, 10)

