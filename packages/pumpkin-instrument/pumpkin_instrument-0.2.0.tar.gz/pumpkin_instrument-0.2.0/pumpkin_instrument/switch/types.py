from abc import abstractmethod
from dataclasses import dataclass
from typing import NamedTuple, List, Dict
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


@dataclass(frozen=True)
class RelayAddress:
    slot_number: int
    channel_number: int


class RelayRange:
    def __init__(self, slot_number, channel_start, channel_end):
        if channel_start < channel_end:
            self.slot_number = slot_number
            self.channel_start = channel_start
            self.channel_end = channel_end
        else:
            raise ValueError("Channel start cannot be greater than channel end")


class Switch(Protocol):
    @abstractmethod
    def change_single_relay(self, relay_address: RelayAddress, is_closed: bool):
        """
        Toggles whether a single relay switch on the module is open or closed

        :param relay_address: The address of the relay switch to toggle
        :param is_closed: Current state of the switch
        """
        raise NotImplementedError()

    @abstractmethod
    def single_relay_state(self, relay_address: RelayAddress) -> bool:
        """
        Queries the state of a single relay switch on the module

        :param relay_address: The address of the relay switch to query
        :return: Returns True if the channel is open
        """
        raise NotImplementedError()

    @abstractmethod
    def change_multi_relay(self, relay_addresses: List[RelayAddress], is_closed: bool):
        """
        Toggles whether several relay switches on the module are open or closed

        :param relay_addresses: List of addresses to toggle
        :param is_closed: Current state of the switches
        """
        raise NotImplementedError()

    @abstractmethod
    def multi_relay_state(self, relay_addresses: List[RelayAddress]) -> Dict[RelayAddress, bool]:
        """
        Queries the state of multiple relay switches on the module

        :param relay_addresses: List of addresses to query
        :return: Dictiionary with each address and state, True means open
        """
        raise NotImplementedError()

    @abstractmethod
    def change_range_relay(self, relay_range: RelayRange, is_closed: bool):
        """
        Toggles wither a range of relay switches are open or closed

        :param relay_range: Range of addresses to toggle
        :param is_closed: Current state of the switches
        """
        raise NotImplementedError()

    @abstractmethod
    def range_relay_state(self, relay_range: RelayRange) -> List[bool]:
        """
        Queries the state of a range of relay switches on the module

        :param relay_range: Range of addresses to query
        :return: List of current states, True means open
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """
        Sets all relays to OPEN state for safety
        """
        raise NotImplementedError()
