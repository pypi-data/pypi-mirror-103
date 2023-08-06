import time

from typing import Any, List, ContextManager, Dict
from enum import Enum
from contextlib import contextmanager

from ..instrument import Instrument
from ..prologix import PrologixController
from ..types import InstrumentType
from .types import Switch, RelayAddress, RelayRange

_HP3488_TERMINATOR = "\r\n"


class HPSwitchType(Enum):
    """
    Represents the specific HP switch used in the below helper class decorator.
    """
    HP3488 = 0


class _HP3488SwitchContext(Switch):
    def __init__(self,
                 controller: PrologixController,
                 address: int,
                 switch_type: HPSwitchType,
                 inst_capabilities=None,
                 channel_capabilities=[]):
        """
        Initializes the switch context, commanding the switch with the given `controller`, `address`, and `switch_type`
        """
        super(_HP3488SwitchContext, self).__init__()
        self.controller = controller
        self.address = address
        self.switch_type = switch_type
        self.inst_capabilities = inst_capabilities
        self.channel_capabilities = channel_capabilities
        self.name = switch_type.name

    def _write_cmd(self, cmd_str: str):
        """Writes a command to the prologix controller, postfixing a newline to the end."""
        self.controller.write(self.address, f'{cmd_str}\n'.encode('ascii'))

    def change_single_relay(self, relay_address: RelayAddress, is_closed: bool):
        """
        Toggles whether a single relay switch on the module is open or closed

        :param relay_address: The address of the relay switch to toggle
        :param is_closed: True if should be closed, False if should be opened
        """
        action = "CLOSE" if is_closed else "OPEN"
        channel_num = relay_address.slot_number * 100 + relay_address.channel_number
        self._write_cmd(f"{action} {channel_num}")

    def single_relay_state(self, relay_address: RelayAddress) -> bool:
        """
        Queries the state of a single relay switch on the module

        :param relay_address: The address of the relay switch to query
        :return: Returns True if the channel is open
        """
        channel_num = relay_address.slot_number * 100 + relay_address.channel_number
        self._write_cmd(f"VIEW {channel_num}")
        resp = str(self.controller.read_until(self.address, _HP3488_TERMINATOR.encode('ascii')), 'ascii')
        resp = resp[:resp.index(_HP3488_TERMINATOR)]
        if resp == "OPEN   1":
            return True
        elif resp == "CLOSED 0":
            return False
        else:
            raise ValueError(f"Response was {resp} on {channel_num}, expected OPEN 1 or CLOSED 0")

    def change_multi_relay(self, relay_addresses: List[RelayAddress], is_closed: bool):
        """
        Toggles whether several relay switches on the module are open or closed

        :param relay_addresses: List of addresses to toggle
        :param is_closed: True if should be closed, False if should be opened
        """
        action = "CLOSE" if is_closed else "OPEN"
        for relay_address in relay_addresses:
            channel_num = relay_address.slot_number * 100 + relay_address.channel_number
            self._write_cmd(f"{action} {channel_num}")
            # sleep due to hardware limitations, explained in manual for HP3488
            time.sleep(0.250)

    def multi_relay_state(self, relay_addresses: List[RelayAddress]) -> Dict[RelayAddress, bool]:
        """
        Queries the state of multiple relay switches on the module

        :param relay_addresses: List of addresses to query
        :return: Dictiionary with each address and state, True means open
        """
        states = {}
        for relay_address in relay_addresses:
            channel_num = relay_address.slot_number * 100 + relay_address.channel_number
            self._write_cmd(f"VIEW {channel_num}")
            resp = str(self.controller.read_until(self.address, _HP3488_TERMINATOR.encode('ascii')), 'ascii')
            resp = resp[:resp.index(_HP3488_TERMINATOR)]
            if resp == "OPEN   1":
                states[relay_address] = True
            elif resp == "CLOSED 0":
                states[relay_address] = False
            else:
                raise ValueError(f"Received {resp} on {channel_num}, expected OPEN 1 or CLOSED 0")
        return states

    def change_range_relay(self, relay_range: RelayRange, is_closed: bool):
        """
        Toggles wither a range of relay switches are open or closed

        :param relay_range: Range of addresses to toggle
        :param is_closed: True if should be closed, False if should be opened
        """
        action = "CLOSE" if is_closed else "OPEN"
        for relay_address in range(relay_range.channel_start, relay_range.channel_end+1):
            channel_num = relay_range.slot_number * 100 + relay_address
            self._write_cmd(f"{action} {channel_num}")
            # sleep due to hardware limitations, explained in manual for HP3488
            time.sleep(0.250)

    def range_relay_state(self, relay_range: RelayRange) -> List[bool]:
        """
        Queries the state of a range of relay switches on the module

        :param relay_range: Range of addresses to query
        :return: List of current states, True means open
        """
        states = []
        for relay_address in range(relay_range.channel_start, relay_range.channel_end):
            channel_num = relay_range.slot_number * 100 + relay_address
            self._write_cmd(f"VIEW {channel_num}")
            resp = str(self.controller.read_until(self.address, _HP3488_TERMINATOR.encode('ascii')), 'ascii')
            resp = resp[:resp.index(_HP3488_TERMINATOR)]
            if resp == "OPEN   1":
                states.append(True)
            elif resp == "CLOSED 0":
                states.append(False)
            else:
                raise ValueError(f"Received {resp} on {channel_num}, expected OPEN 1 or CLOSED 0")

    def reset(self):
        """Sets all channels on all five slots to open"""
        for i in range(1, 6):
            self._write_cmd(f"CRESET{i}")
            time.sleep(0.250)

    def close(self):
        self.reset()


def HP3488Instrument(switch_type):
    context = _HP3488SwitchContext

    def wrap(c):
        class _HP3488Switch(Instrument, c):
            def __init__(self, controller: PrologixController, gpib_address: int):
                self.controller = controller
                self.address = gpib_address

            @classmethod
            def instrument_type(cls) -> InstrumentType:
                return InstrumentType.Switch
            
            @classmethod
            def instrument_capabilities(cls) -> Any:
                # No instrument capabilities on switch
                return None
            
            @classmethod
            def channel_capabilities(cls) -> List[Any]:
                # No channel capabilities on switch
                return []

            @contextmanager
            def use(self) -> ContextManager[Switch]:
                switch = context(self.controller, self.address, switch_type)
                switch.reset()
                yield switch
                switch.close()

        return _HP3488Switch

    return wrap


@HP3488Instrument(HPSwitchType.HP3488)
class HP3488:
    pass
