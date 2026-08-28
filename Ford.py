from Car import Car
from Animals import Animals
class Ford(Car, Animals):
    model = "none"
    def __init__(self, model="none"):
        # call base class constructor
        Car.__init__(self)
        Animals.__init__(self)

        # extend base class
        self.model = model
        print("Model = ", self.model)



class Toyota(Ford):
    def __init__(self, model):
        # call base class constructor
        Ford.__init__(self)
