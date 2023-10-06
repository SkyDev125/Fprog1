# Verify if the territory is valid
def eh_territorio(territorio):
    # Check if the territorio is a tuple
    if not isinstance(territorio, tuple):
        return False

    # Check if the territorio is empty or larger than expected
    if len(territorio) < 1 or len(territorio) > 26:
        return False

    firstCollumn = territorio[0]
    # Check if the collumns have the same lenght
    for collumn in territorio:
        # Check if the arg is a tuple
        if not isinstance(collumn, tuple):
            return False

        # Check if the tuple is empty or larger than expected
        if len(collumn) < 1 or len(collumn) > 99:
            return False

        # Check if the collumn has the same lenght as the first collumn
        if len(collumn) != len(firstCollumn):
            return False

        # Check if the collumn has only 0 or 1
        for cell in collumn:
            if cell not in (0, 1):
                return False

    return True


# Return a valid last interception (top right) based on the territory
def obtem_ultima_intersecao(territorio):
    return (chr(64 + len(territorio)), len(territorio[0]))


# Verify if the interception is valid
def eh_intersecao(intersecao):
    # Check if the intersecao is a tuple
    if not isinstance(intersecao, tuple):
        return False

    # Check if the intersecao is the expected size
    if len(intersecao) != 2:
        return False

    # Create a set with all the valid strings
    valid_strings = {chr(65 + i) for i in range(26)}

    # Check if the first element is a string
    if not isinstance(intersecao[0], str):
        return False

    # Check if the second element is a int
    if not isinstance(intersecao[1], int):
        return False

    # Check if the first element is a valid string
    if intersecao[0] not in valid_strings:
        return False

    # Check if the second element is a valid int
    if intersecao[1] < 1 or intersecao[1] > 99:
        return False

    return True


# Verify if the interception is in the territory
def eh_intersecao_valida(territorio, intersecao):
    max_collumns, max_lines = obtem_ultima_intersecao(territorio)
    collumn, line = intersecao

    # Check if the collumn
    if collumn > max_collumns:
        return False

    if line > max_lines:
        return False

    return True


# Return the chain of the interception
def convert_intersecao(intersecao):
    collumn, line = intersecao
    return (ord(collumn) - 64 - 1, line - 1)


# Verify if the interception is free
def eh_intersecao_livre(territorio, intersecao):
    collumn, line = convert_intersecao(intersecao)
    return territorio[collumn][line] == 0


def obtem_intersecoes_adjacentes(territorio, intersecao):
    collumn, line = convert_intersecao(intersecao)
    max_collumns, max_lines = obtem_ultima_intersecao(territorio)
    inter_adjs = ()

    # Add the top adjacent interception
    if line > 0:
        inter_adjs += ((chr(collumn + 64 + 1), line),)

    # Add the left adjacent interception
    if collumn > 0:
        inter_adjs += ((chr(collumn + 64), line + 1),)

    # Add the right adjacent interception
    if collumn + 2 <= ord(max_collumns) - 64:
        inter_adjs += ((chr(collumn + 64 + 2), line + 1),)

    # Add the bottom adjacent interception
    if line + 2 <= max_lines:
        inter_adjs += ((chr(collumn + 64 + 1), line + 2),)

    return inter_adjs

def ordena_intersecoes(intersecoes):
    # sort based on the number(line), then based on the letter(collumn)
    return tuple(sorted(intersecoes, key=lambda x: (x[1], x[0])))

def territorio_para_str(territorio):
    max_collumns, max_lines = obtem_ultima_intersecao(territorio)
    # Create the string with the collumns
    s = ['  '] + [' ' + chr(64+x) for x in range(1,ord(max_collumns)-64+1)] + ["\n"]

    for x in range(max_lines, 0, -1):
        s += [' ' + str(x)] + [' ' + ('X' if territorio[y][x - 1] == 1 else ".") for y in range(ord(max_collumns) - 64)] + [' ' + str(x) + '\n']

    s += ['  '] + [' ' + chr(64+x) for x in range(1,ord(max_collumns)-64+1)] + ["\n"]

    s = ''.join(s)

    return s

print(territorio_para_str(((0, 1, 0, 0), (0, 0, 0, 0))))


