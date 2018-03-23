class Human(object):
    def __init__(self, input_gender):
        self.gender = input_gender

    def output_gender(self):
        print(self.gender)


fuxinyu = Human("male")
print(fuxinyu.gender)