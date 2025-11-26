class Student:
    def __init__(self, group_number, average_score, name, age):
        self.group_number= group_number
        self.average_score = average_score
        self.name = name
        self.age = age

    def display_info(self):
        print(f"name: {self.name}, age: {self.age}, group number: {self.group_number}, average score: {self.average_score}")

    def scholarship(self):
        if self.average_score == 5:
            return 6000
        elif self.average_score < 5:
            return 4000
        else:
            return 0

    def compare_scholarship(self, other):
        if self.scholarship() > other.scholarship():
            return "больше"
        elif self.scholarship() < other.scholarship():
            return "меньше"
        else:
            return "равны"


class GraduateStudent(Student):
    def __init__(self, group_number, average_score, name, age, research_work):
        super().__init__(group_number, average_score, name, age)
        self.research_work = research_work

    def display_info(self):
        print(f"name: {self.name}, age: {self.age}, group number: {self.group_number}, average score: {self.average_score}, research_work: {self.research_work}")

    def scholarship(self):
        if self.average_score == 5:
            return 8000
        elif self.average_score < 5:
            return 6000
        else:
            return 0

student = Student(group_number=8, average_score=5, name="Игорь", age=19)
graduate_student = GraduateStudent(group_number=17, average_score=4, name="Борис", age=22, research_work="научной работы")

student.display_info()
print(f"scholarship: {student.scholarship()}р")

graduate_student.display_info()
print(f"scholarship: {graduate_student.scholarship()}р")

print(student.compare_scholarship(graduate_student))