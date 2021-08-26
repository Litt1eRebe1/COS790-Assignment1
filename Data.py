

class Data:
    def __init__(self):
        with open('Data/TA001.txt') as f:
            contents = f.read()
            print(contents)