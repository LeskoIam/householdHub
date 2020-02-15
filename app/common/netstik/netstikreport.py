# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    num: int
    date_1: datetime
    date_2: datetime
    amount_out: float
    amount_in: float
    balance: float
    person: str
    comment: str
    purpose_code: str


@dataclass
class ReportData:
    header: str
    details: str
    transaction_details: str
    transactions: str
    footer: str


class NetstikReport:

    def __init__(self, report_file: str):
        self.report_file = report_file
        self.report_data = None
        self.__load_report()

    def __load_report(self):
        with open(self.report_file, "r", encoding="utf-8") as report_file:
            report_data = report_file.read()
        m = re.split(r"---*", report_data)
        if m:
            self.report_data = ReportData(*m)
        else:
            raise ValueError("Can't load report file sections")

    @property
    def transactions(self):
        all_transactions = []
        transactions = self.report_data.transactions.split("\n\n")[:-1]
        for line in transactions:
            line = line.strip()
            data, metadata = line.split("\n")
            data = re.split(r"\s{1,20}", data)
            metadata = re.split(r"\s{4,50}", metadata)

            num, date_1, date_2, amount_out, amount_in, balance = data

            if len(metadata) < 3:
                person, comment = None, " ".join(metadata)
            else:
                _, person, comment = metadata
                person = person.strip()

            if ";" in comment:
                comment, purpose_code = comment.split(";")
                purpose_code = purpose_code.strip()
            else:
                purpose_code = None

            all_transactions.append(Transaction(num=num,
                                                date_1=self.__date_to_datetime(date_1),
                                                date_2=self.__date_to_datetime(date_2.strip("()")),
                                                amount_out=self.__slo_decimal_to_float(amount_out),
                                                amount_in=self.__slo_decimal_to_float(amount_in),
                                                balance=self.__slo_decimal_to_float(balance),
                                                person=person,
                                                comment=comment.strip(),
                                                purpose_code=purpose_code))
        return all_transactions

    @staticmethod
    def __slo_decimal_to_float(slo_dec: str, silence: bool = True):
        if silence and len(slo_dec) < 1:
            return 0.
        return float(slo_dec.replace(".", "").replace(",", "."))

    @staticmethod
    def __date_to_datetime(date_str: str):
        return datetime.strptime(date_str, "%d.%m.%Y")


if __name__ == '__main__':
    t = NetstikReport("promet_34000-1014995560.txt")
    print(t.transactions[0].purpose_code)
