def inp(prompt, constraints = []):
    while True:
        x = raw_input(prompt + "\n> ")
        fail = False
        for c in constraints:
            if not eval(c):
                print("'{c}' not met".format(**locals()))
                fail = True
        if not fail:
            return x
        else:
            print("Try again")
