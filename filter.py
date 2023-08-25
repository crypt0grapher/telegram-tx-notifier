import re
from typing import List, Union
from helpers import is_valid_ethereum_address


class Filter:
    def __init__(self, params_to_parse: str = None,
                 to_filter: bool = False,
                 addresses: Union[str, List[str]] = None,
                 fresh: int = 0,
                 amount_from: float = 0,
                 amount_to: float = 0.01,
                 name: str = ""):
        if params_to_parse:
            to_filter, addresses, fresh, amount_from, amount_to, name = self.parse_params(params_to_parse)
        if addresses is None:
            ValueError("There should be at least one address")
        if name is None:
            ValueError("Name should be unique")
        if isinstance(addresses, str):
            addresses = [addresses]
        if not all([is_valid_ethereum_address(address) for address in addresses]):
                raise ValueError("Invalid address format")
        self.active = True
        self.to_filter = to_filter
        self.addresses = addresses
        self.fresh = fresh
        self.amount_from = amount_from
        self.amount_to = amount_to
        self.uptime = 0
        self.events = 0
        self.name = name

    def __str__(self):
        counterpary = ",freshness of sender: " if self.to_filter else ",freshness of receiver: "
        return (f"'<strong>{self.name}'</strong>:\n"
                f"{'to' if self.to_filter else 'from'} {', '.join(self.addresses)}"
                f" {counterpary + str(self.fresh) + ' txs max,' if self.fresh > 0 else ''} min {self.amount_from}, max {self.amount_to}\n")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.to_filter == other.to_filter and \
            self.addresses == other.addresses and \
            self.fresh == other.fresh and \
            self.amount_from == other.amount_from and \
            self.amount_to == other.amount_to

    def __hash__(self):
        return hash(self.__str__())

    def __ne__(self, other):
        return not self.__eq__(other)

    def parse_params(self, params_to_parse):
        line = params_to_parse.strip()
        tokens = line.split(',')
        tokens = [token.strip() for token in tokens]
        keys = [token.split(' ')[0] for token in tokens]
        if 'from' in keys and 'to' in keys:
            raise ValueError("Error: from and to cannot be both set,"
                             " a filter can be either <code>to</code> or <code>from</code>.")
        if 'from' not in keys and 'to' not in keys:
            raise ValueError("Error: from and to cannot be both empty")
        fresh = amt_from = 0
        amt_to = 0.01
        name = ""
        to_filter = False
        addresses = None
        for token in tokens:
            key = token.split(' ')[0]
            if key == 'name':
                name = token.split(' ')[1]
            if key in ['from', 'to']:
                addresses = re.findall(r'0x[a-fA-F0-9]+', token)
                if not addresses:
                    raise ValueError("Invalid {} format. ".format(key))
                else:
                    to_filter = True if key == 'to' else False
            elif key in ['fresh', 'min', 'max']:
                try:
                    match key:
                        case 'fresh':
                            fresh = int(token.split(' ')[1])
                        case 'min':
                            amt_from = float(token.split(' ')[1])
                        case 'max':
                            amt_to = float(token.split(' ')[1])
                except (IndexError, ValueError):
                    raise ValueError("Invalid {} format. ".format(key))

        return to_filter, addresses, fresh, amt_from, amt_to, name
