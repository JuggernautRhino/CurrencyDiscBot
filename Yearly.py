with open('yearly', 'r') as f:
    yearly = eval(f.read())

def save_yearly():
    with open('yearly', 'w') as f:
        f.write(repr(yearly))