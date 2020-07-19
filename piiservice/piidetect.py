from functools import reduce

from piiservice.regexdata import RegexExp
from piiservice.nltkpii import NltkPii


class PiiDetect(object):

    def __init__(self, data):
        self.data = data
        self.regextype = RegexExp()
        self.getpii = NltkPii()

    @staticmethod
    def remove_duplicates(ranges):
        if len(ranges) <= 1:
            return ranges
        ranges.sort()
        reducers = (lambda acc, el: acc[:-1:] + [(min(*acc[-1], *el), max(*acc[-1], *el))] if acc[-1][1] > el[
            0] else acc + [el])
        return reduce(reducers, ranges[1::], [ranges[0]])

    def process_data(self):
        data_string = self.data
        indices = []
        if not data_string.strip():
            return indices
        indices.extend(p.span() for p in self.regextype.emails(data_string))
        indices.extend(p.span() for p in self.regextype.phones(data_string))
        indices.extend(p.span() for p in self.regextype.ssn_number(data_string))
        indices.extend(p.span() for p in self.regextype.po_boxes(data_string))
        indices.extend(p.span() for p in self.regextype.zip_codes(data_string))
        indices.extend(p.span() for p in self.regextype.street_addresses(data_string))
        indices.extend(p.span() for p in self.regextype.btc_addresses(data_string))
        indices.extend(p.span() for p in self.regextype.credit_cards(data_string))

        indices.extend(self.getpii(data_string))

        indices = self.remove_duplicates(indices)

        return indices
