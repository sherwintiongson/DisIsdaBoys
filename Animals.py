
class Animals:
    # class variable
    species = 'mammal'
    def __init__(self, state="default",
                        age="default",
                        type="default"):
        # instance variables
        self.state = state
        self.age = age
        self.type = type
    def run(self):
        self.state = "Running"
        self.print_state()

    def walk(self):
        self.state = "Walking"
        self.print_state()

    def VoidFunction(self):
        pass  # place holder

    def print_state(self):
        print("My state is", self.state)
        return

    def get_state(self):
        return self.state

    def get_age(self):
        return self.age

    def get_type(self):
        return self.type

    def set_state(self, state):
        self.state = state

    def set_age(self, age):
        self.age = age

    def set_type(self, type):
        self.type = type

class Circle():

    # class attributes
    pi = 3.1416
    def __init__(self,radius=1):

        # instance attributes
        self.radius = radius
    def get_area(self):
        return Circle.pi * self.radius * self.radius

    def get_diameter(self):
        return 2 * self.radius

    def get_circumference(self):
        return 2 * Circle.pi * self.radius

class Dog(Animals):
    def __init__(self):
        Animals.__init__(self)


if __name__ == '__main__':
    print('Animals.py is run directly')
else:
    print('Animals.py is imported and run indirectly')


