"""
Armar un programa que traduzca un texto (ingresado por input) a codigo morse

Signo	Código	 	Signo	Código	 	Signo	Código
A	· —	 	        N	— ·	 	        0	— — — — —
B	— · · ·	 	    Ñ	— — · — —	    1	· — — — —
C	— · — ·	 	    O	— — —	 	    2	· · — — —
CH	— — — —	 	    P	· — — ·	 	    3	· · · — —
D	— · ·	 	    Q	— — · —	 	    4	· · · · —
E	·	 	        R	· — ·	 	    5	· · · · ·
F	· · — ·	 	    S	· · ·	 	    6	— · · · ·
G	— — ·	 	    T	—	 	        7	— — · · ·
H	· · · ·	 	    U	· · —	 	    8	— — — · ·
I	· ·	 	        V	· · · —	 	    9	— — — — ·
J	· — — —	 	    W	· — —	 	    .	· — · — · —
K	— · —	 	    X	— · · —	 	    ,	— · — · — —
L	· — · ·	 	    Y	— · — —	 	    ?	· · — — · ·
M	— —	 	        Z	— — · ·	 	    "	· — · · — ·
!	— — · · — —

Si el texto tiene un caracter invalido, lanzar una exception. El programa principal debera capturar esa Exception y mostrar un mensaje de error

"""


morse_dictionary = {
    "a": ". -",
    "b": "- . . .",
    "c": "- . - .",
    "ch": "- - - -",
    "d": "- . .",
    "e": ".",
    "f": ". . - .",
    "g": "- - .",
    "h": ". . . .",
    "i": ". .",
    "j": ". - - -",
    "k": "- . -",
    "l": ". - . .",
    "m": "- -",
    "n": "- .",
    "ñ": "- - . - -",
    "o": "- - -",
    "p": ". - - .",
    "q": "- - .",
    "r": ". - .",
    "s": ". . .",
    "t": "-",
    "u": ". . -",
    "v": ". . . -",
    "w": ". - -",
    "x": "- . . -",
    "y": "- . - -",
    "z": "- - . .",
    "0": "— — — — —",
    "1": "· — — — —",
    "2": "· · — — —",
    "3": "· · · — —",
    "4": "· · · · —",
    "5": "· · · · ·",
    "6": "— · · · ·",
    "7": "— — · · ·",
    "8": "— — — · ·",
    "9": "— — — — ·",
    ".": "· — · — · —",
    ",": "— · — · — —",
    "?": "· · — — · ·",
    "!": "— — · · — —",
    "\"": "· — · · — ·",
    " ": "    ",
}


def text_to_morse (text):
    text = text.lower().strip()
    string = ""

    for position, char in enumerate(text):
        if char not in morse_dictionary:
            raise KeyError('Character "{}" is not in dictionary at position {}'.format(char, position + 1))
        else:
            code = morse_dictionary[char]
            string += code + "  "

    return string


try:
    encoded_text = text_to_morse('Hola "locuraaa"!')
    print(encoded_text)
except KeyError as e:
    print(e.args[0])


