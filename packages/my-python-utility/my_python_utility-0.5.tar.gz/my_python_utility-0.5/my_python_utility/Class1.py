from my_python_utility.Class2 import Class2

class Class1:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)

        p1 = Class2("Jingle", 36)
        p1.myfunc()