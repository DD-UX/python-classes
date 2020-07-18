from random import randint


def dado():
    return randint(1, 6)


def tirar_dados(n = 5):
    return [dado() for i in range(n)]