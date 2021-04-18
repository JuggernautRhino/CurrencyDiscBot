with open('monthly', 'r') as f:
    monthly = eval(f.read())

def save_monthly():
    with open('monthly', 'w') as f:
        f.write(repr(monthly))