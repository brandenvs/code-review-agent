# Course
class Course():
    name = "Fundamentals of Computer Science" # Parent course
    contact_website = "www.hyperiondev.com"
    head_office = "Cape Town (CPT)"

    # Prints course contact details
    def contact_details(self):
        print("\t\033[1mPlease contact us by visiting", self.contact_website, "\033[1m")

    # Prints head office location
    def get_location(self):
        print("\t\033[1mOur head office location is\033[1m", self.head_office)

# Subclass of Course
class OOPCourse(Course):
    def __init__(self, course_id=12345, description="OOP Fundamentals", trainer="Mr Anon A. Mouse"):
        self.course_id = course_id
        self.description = description
        self.trainer = trainer

    # Returns trainer and course details
    def trainer_details(self):
        output = f'''
        Course: \033[1m{self.name}
        Module: \033[1mObject Orientated Programming (OOP)\033[1m
        Trainer: \033[1m{self.trainer}\033[1m
        
        {self.description}'''
        print(output)
        
        return output

    # Returns course ID
    def show_course_id(self):
        print(self.course_id)
        return self.course_id

course_1 = OOPCourse()

print('Overview:')
course_1.trainer_details() # Prints course trainer

print('\nCourse ID:')
course_1.show_course_id() # Prints course ID

print('\nContact Details:')
course_1.contact_details() # Prints institution contact details
