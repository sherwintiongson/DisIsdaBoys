class Car(object):
    brand = 0
    years = 0
    speed = 0
    plate_number = 0
    def __init__(self, brand="None", years=1950, speed=0, plate_number= "ST1234"):
        self.brand = brand
        self.years = years
        self.speed = speed
        self.plate_number = plate_number
        print("Car plate number is", self.plate_number)
    def accelerate(self, new_speed):
        if(self.speed <= new_speed):
            self.speed = new_speed
        print("Accelerating to", self.speed, "km/hour")

    def slowdown(self, new_speed):
        if(self.speed > new_speed):
            self.speed = new_speed
        print("Slow down to", self.speed, "km/hour")

    def stop(self):
        self.speed = 0
        print("Breaking to", self.speed, "km/hour")

    def turn_left(self):
        print("Turning left at speed of", self.speed, "km/hour")

    def turn_right(self):
        print("Turning right at speed of", self.speed, "km/hour")

    def ride_straight(self):
        print("Ride straight at speed of", self.speed, "km/hour")







