# defining the global var to access expense db
def cal_percentage(amount, val = list()):
    n = len(val)
    quotient = 1 / n
    percentage = quotient * 100
    return percentage

def calculate_split_ammount(expensetype, values, ammount):
    ans = 0
    if expensetype == "percentage":
        if values:
            ans = cal_percentage(ammount, len(values))
    if expensetype == "equals":
        ans = ammount / len(values)

    return ans


