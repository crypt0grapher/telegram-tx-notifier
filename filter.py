import re


class Filter:
    def __init__(self, from_addresses, to_addresses, fresh_from, fresh_to, amount_from, amount_to):
        self.addr_from = from_addresses
        self.addr_to = to_addresses
        self.fresh_from = fresh_from
        self.fresh_to = fresh_to
        self.amount_from = amount_from
        self.amount_to = amount_to
        if self.addr_from == "" and self.addr_to == "":
            raise ValueError("<b>Error:</b> <code>from</code> and <code>to</code> cannot be both empty")

    def __init__(self, params_to_parse):
        self.addr_from = ""
        self.addr_to = ""
        self.fresh_from = 5
        self.fresh_to = 3
        self.amount_from = 0
        self.amount_to = 0.01
        self.parse_params(params_to_parse)
        if self.addr_from == "" and self.addr_to == "":
            raise ValueError("Error: from and to cannot be both empty")

    def __str__(self):
        return f"from: {self.addr_from}, to: {self.addr_to}, fresh_from: {self.fresh_from}, fresh_to: {self.fresh_to}, amount_from: {self.amount_from}, amount_to: {self.amount_to}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__str__())

    def __ne__(self, other):
        return not self.__eq__(other)

    def parse_params(self, params_to_parse):

        output_message = ""
        # Remove leading and trailing whitespaces
        line = params_to_parse.strip()

        # Split the remaining line by comma
        tokens = line.split(',')

        # Remove leading and trailing whitespaces from tokens
        tokens = [token.strip() for token in tokens]
        for token in tokens:
            key = token.split(' ')[0]
            if key in ['from', 'to']:
                addresses = re.findall(r'0x[a-fA-F0-9]+', token)
                if addresses:
                    setattr(self, f"addr_{key}", addresses)
                else:
                    raise ValueError("Invalid {} format. ".format(key))

            elif key in ['fresh_from', 'fresh_to', 'amt_from', 'amt_to']:
                try:
                    value = float(token.split(' ')[1]) if 'amt' in key else int(token.split(' ')[1])
                    setattr(self, key, value)
                except (IndexError, ValueError):
                    raise ValueError("Invalid {} format. ".format(key))
