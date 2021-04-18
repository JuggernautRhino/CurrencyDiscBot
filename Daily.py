with open('daily', 'r') as f:
    daily = eval(f.read())

def save_daily():
    with open('daily', 'w') as f:
        f.write(repr(daily))

