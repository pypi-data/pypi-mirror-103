
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def display(self):
      return "Name: {name}, Age: {age}".format(name=self.name, age=self.age)  


if __name__ == "__main__":

    p1 = Person("John", 36)

    print(p1.display())

