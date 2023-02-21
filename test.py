class Test:
    def __init__(self):
        self.energy = 500

    def remove_energy(self):
        self.energy -= 1


test = Test()
print(test.energy)
test.remove_energy()
print(test.energy)