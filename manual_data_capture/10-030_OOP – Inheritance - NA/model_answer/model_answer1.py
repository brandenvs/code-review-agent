# Adult
class Adult:
    def __init__(self, name: str, age: int, hair_colour: str, eye_colour: str):
        self.name = name
        self.age = age
        self.hair_colour = hair_colour
        self.eye_colour = eye_colour

    def can_drive(self, updated_text='is a big boy and can drive😎.'):
        print(f"{self.name} {updated_text}")

# Subclass of Adult
class Child(Adult):
    def __init__(self, name, age, hair_colour, eye_colour):
        super().__init__(name, age, hair_colour, eye_colour)

    def can_drive(self, text='is too young to be driving👶.'):
        return super().can_drive(text)

# Create a human
def create_person(name: str, age: int, hair_colour: str, eye_colour: str):
    if age >= 18:
        # Create an Adult human(object) respective of age
        adult = Adult(
            name=name,
            age=age,
            hair_colour=hair_colour,
            eye_colour=eye_colour
        )
        print(adult.can_drive())
    else:
        # Create a Child human(object) respective of age        
        child = Child(
            name=name,
            age=age,
            hair_colour=hair_colour,
            eye_colour=eye_colour
        )
        print(child.can_drive())

def define_person():
    # Get person's details
    name = input("Please enter person's name:\n> ")
    age = int(input("Please enter person's age:\n> "))
    hair_colour = input("Please enter person's hair_colour:\n> ")
    eye_colour = input("Please enter person's eye_colour:\n> ")

    # Call appropriate function
    create_person(name, age, hair_colour, eye_colour)

if __name__ == "__main__":
    define_person()
