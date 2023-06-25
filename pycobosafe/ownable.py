from brownie import network

from .utils import ZERO_ADDRESS, load_contract, s32


class BaseOwnable(object):
    def __init__(self, addr) -> None:
        self.contract = load_contract(self.__class__.__name__, addr)

    def initialize(self, owner_address):
        self.contract.get_by_sig("initialize(address)")(owner_address)

    @property
    def address(self):
        return self.contract.address

    @property
    def name(self):
        try:
            return s32(self.contract.NAME())
        except Exception:
            return None

    @property
    def version(self):
        return self.contract.VERSION()

    @property
    def owner(self):
        return self.contract.owner()

    @property
    def pending_owner(self):
        return self.contract.pendingOwner()

    @classmethod
    def match(cls, addr):
        return BaseOwnable(addr).name == cls.__name__

    def dump(self, full=False):
        print("Name:", self.name)
        print("Address:", self.address)
        print("Version:", self.version)
        try:
            print("Owner:", self.owner)
            pending = self.pending_owner
            if pending != ZERO_ADDRESS:
                print("Pending owner:", pending)
        except Exception:
            pass


class ERC20(object):
    _CACHE = {}

    def __init__(self, addr) -> None:
        self.contract = load_contract("ERC20", addr)

    @property
    def address(self):
        return self.contract.address

    @property
    def symbol(self):
        tag = f"{network.chain.id} {self.address}"

        # Cache to speed.
        if tag not in ERC20._CACHE:
            ERC20._CACHE[tag] = self.contract.symbol()

        return ERC20._CACHE[tag]
