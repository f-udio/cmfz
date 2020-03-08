import random


class Getcode(object):
    def getcode(self):
        code = random.randint(100000, 1000000)
        return code


# if __name__ == '__main__':
#     code = Getcode()
#     print(code.getcode())
