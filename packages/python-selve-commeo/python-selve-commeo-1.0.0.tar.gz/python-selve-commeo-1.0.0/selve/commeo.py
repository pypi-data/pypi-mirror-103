from enum import Enum

from selve.protocol import MethodCall
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.utils import singlemask
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class CommeoCommand(Enum):
    GETINFO = "getInfo"
    GETIDS = "getIDs"
    GETVALUES = "getValues"
    RESULT = "result"
    DEVICE = "device"

class GatewayDeviceCommand(MethodCall):
    #For every gateway device command starting with selve.GW.device
    def __init__(self, method_name, parameters = []):
         super().__init__("selve.GW.device." + method_name.value, parameters)

class CommandGatewayGetIDs(GatewayDeviceCommand):
    #selve.GW.device.getIDs
    def __init__(self):
        super().__init__(CommeoCommand.GETIDS)

    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommandGatewayGetProperties(GatewayDeviceCommand):
    #selve.GW.device.getInfo
    #for CommeoDevice.discover_properties
    def __init__(self, commeoID):
        super().__init__(CommeoCommand.GETINFO, [(ParameterType.INT, commeoID)])

    def process_response(self, methodResponse):
        self.name = methodResponse.parameters[0][1]
        self.activity = methodResponse.parameters[2][1]
        self.deviceType = DeviceType(int(methodResponse.parameters[3][1]))

class CommandGatewayGetState(GatewayDeviceCommand):
    #selve.GW.device.getValues
    def __init__(self, commeoID):
        super().__init__(CommeoCommand.GETVALUES, [(ParameterType.INT, commeoID)])

    def process_response(self, methodResponse):
        self.position = methodResponse.parameters[3][1]
        self.status = methodResponse.parameters[2][1]

class CommandCommeo(MethodCall):
    # For every commeo command starting with selve.GW.command.
    def __init__(self, method_name, parameters = []):
         super().__init__("selve.GW.command." + method_name.value, parameters)

class CommandCommeoDevice(CommandCommeo):
    #selve.GW.command.device
    def __init__(self, commeoID, command, mode = 1, parameter = 0): #mode 1 = manuell, mode 2 = automatik
        super().__init__(CommeoCommand.DEVICE, [(ParameterType.INT, commeoID), (ParameterType.INT, command.value), (ParameterType.INT, mode), (ParameterType.INT, parameter)])

class State:
    def __init__(self, status = 0, position = 0):
        self.status = int(status)
        self.position = int(position)

    def setstate(self, status, position):
        self.position = int(position)
        self.status = int(status)

class CommeoDevice:
    def __init__(self, gateway, commeoID, discover=False):
        self.state = State()
        self.commeoID = commeoID
        self.gateway = gateway
        self.device_type = DeviceType.UNKNOWN
        self.name = "Not defined"
        if discover:
            self.discover_properties()
        self.updateState()

    def stop(self, automatic=False):
        self.executeCommand(CommandType.STOP, automatic)

    def moveDown(self, automatic=False):
        self.executeCommand(CommandType.DEPARTURE, automatic)

    def moveUp(self, automatic=False):
        self.executeCommand(CommandType.DRIVEAWAY, automatic)

    def moveIntermediatePosition1(self, automatic=False):
        self.executeCommand(CommandType.POSITION_1, automatic)

    def moveIntermediatePosition2(self, automatic=False):
        self.executeCommand(CommandType.POSITION_2, automatic)

    def moveToPosition(self, pos, automatic=False):
        pos = round(pos*655.35)
        self.executeCommand(CommandType.DrivePos, automatic, pos)

    def executeCommand(self, commandType, automatic=False, parameter = 0):
        if automatic:
            command = CommandCommeoDevice(self.commeoID, commandType, 2, parameter)
        else:
            command = CommandCommeoDevice(self.commeoID, commandType, 1, parameter)
        command.execute(self.gateway)
        return command

    def discover_properties(self):
        command = CommandGatewayGetProperties(self.commeoID)
        command.execute(self.gateway)
        self.device_type = command.deviceType
        self.name = command.name

    def updateState(self):
        command = CommandGatewayGetState(self.commeoID)
        command.execute(self.gateway)
        self.state.setstate(command.status, command.position)

    def __str__(self):
        return "Device of type: " + self.device_type.name + " on channel " + str(
            self.commeoID) + " with name " + self.name
