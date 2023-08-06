from copy import deepcopy
from collections import defaultdict

def split(*receipts: dict):
    """
    Compute equalization payments between roommates.
    All names listed for a given receipt will be considered to be financially responsible.
    The most efficient repayment scheme is computed for all receipts.

    Args:
        *receipts: Dictionaries of payment history.
    """

    # Make sure at least one receipt was passed
    if not receipts:
        print("ERROR: Please provide at least one receipt to the split function.")
        exit()

    # Type check
    for receipt in receipts:
        for name, price in receipt.items():
            if not isinstance(name, str):
                print(f"ERROR: Name {name} is not a valid string.")
                exit()
            if not isinstance(price, (float, int)):
                print(f"ERROR: Price {price} is not a valid float/int.")
                exit()

    # Track debts
    debts = defaultdict(float)
    for receipt in receipts:

        # Expected payment
        fair_split = sum(receipt.values()) / len(receipt)

        # Compute partial debt
        for name, price in receipt.items():
            debts[name] += fair_split - price
    
    # Separate payers and receivers
    sources = {name: +debt for name, debt in debts.items() if debt > 0}
    targets = {name: -debt for name, debt in debts.items() if debt < 0}

    # Determine the longest names
    s_max_len = max(len(name) for name in sources.keys())
    t_max_len = max(len(name) for name in targets.keys())

    # Format all pretty
    def payment(src_name, tar_name, amount):
        print(f"{src_name.ljust(s_max_len)} -> {tar_name.ljust(t_max_len)}: {amount:.2f}")

    # Determine transfers
    for s_name, s_debt in sources.items():
        for t_name, t_debt in deepcopy(targets).items():

            # Perfect offset
            if s_debt == t_debt:
                payment(s_name, t_name, t_debt)
                del targets[t_name]
                break

            # Source can clear their debt
            elif s_debt < t_debt:
                payment(s_name, t_name, s_debt)
                targets[t_name] -= s_debt
                break

            # Target is fully repayed
            else:
                payment(s_name, t_name, t_debt)
                del targets[t_name]
                s_debt -= t_debt
                continue
