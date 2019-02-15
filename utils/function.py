import random


def generateImageCode():
    str = '1234567890qwertyuiop'
    code = ''
    for _ in range(4):
        code += random.choice(str)
    return code