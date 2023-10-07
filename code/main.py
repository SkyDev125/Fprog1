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

    # Check if the collumn is larger than the maximum allowed for collumns
    if collumn > max_collumns:
        return False

    # Check if the line is larger than the maximum allowed for lines
    if line > max_lines:
        return False

    return True


# Return the interseption in usable values for coding (1 -> 0) (A -> 0)
def convert_intersecao(intersecao):
    collumn, line = intersecao
    return (ord(collumn) - 64 - 1, line - 1)


# Verify if the interception is free
def eh_intersecao_livre(territorio, intersecao):
    collumn, line = convert_intersecao(intersecao)
    return territorio[collumn][line] == 0


# Return the adjacent interceptions
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


# Order the Intersections by left to right, bottom to top
def ordena_intersecoes(intersecoes):
    # sort based on the number(line), then based on the letter(collumn)
    return tuple(sorted(intersecoes, key=lambda x: (x[1], x[0])))


# Return the territory as a string
def territorio_para_str(territorio):
    # Check if territory is valid
    if not eh_territorio(territorio):
        raise ValueError("territorio_para_str: argumento invalido")

    max_collumns, max_lines = obtem_ultima_intersecao(territorio)

    # Create a Letters line
    s = (
        ["  "]
        + [" " + chr(64 + x) for x in range(1, ord(max_collumns) - 64 + 1)]
        + ["\n"]
    )

    # Create the lines (number, values, number)
    for x in range(max_lines, 0, -1):
        if x > 9:
            s += (
                [str(x)]
                + [
                    " " + ("X" if territorio[y][x - 1] == 1 else ".")
                    for y in range(ord(max_collumns) - 64)
                ]
                + [" " + str(x) + "\n"]
            )
        else:
            s += (
                [" " + str(x)]
                + [
                    " " + ("X" if territorio[y][x - 1] == 1 else ".")
                    for y in range(ord(max_collumns) - 64)
                ]
                + ["  " + str(x) + "\n"]
            )

    # Create a Letters line
    s += ["  "] + [" " + chr(64 + x) for x in range(1, ord(max_collumns) - 64 + 1)]

    # Join the strings
    s = "".join(s)

    return s


# Return the chain of interceptions
def obtem_cadeia(territorio, intersecao):
    # Check if territorio and intersection are valid
    if not eh_territorio(territorio) or not eh_intersecao(intersecao):
        raise ValueError("obtem_cadeia: argumentos invalidos")

    # Check if intersecao is part of territorio
    if not eh_intersecao_valida(territorio, intersecao):
        raise ValueError("obtem_cadeia: argumentos invalidos")

    # Check if intersecao is free
    freedom = eh_intersecao_livre(territorio, intersecao)

    # Create recursive function to check if the adjacent interceptions are also free
    def recursive_check(territorio, intersecao, visited=()):
        # Add the intersecao to the list
        chain = (intersecao,)
        visited += chain

        # Check if the adjacent interceptions are equal to the freedom
        for inter in obtem_intersecoes_adjacentes(territorio, intersecao):
            if (
                eh_intersecao_livre(territorio, inter) == freedom
                and inter not in visited
            ):
                chain += recursive_check(territorio, inter, visited)

        return chain

    # Get the list of interceptions
    chain = recursive_check(territorio, intersecao)

    # Clean duplicates
    chain = tuple(set(chain))

    return ordena_intersecoes(chain)


# Return the valleys around a mountain
def obtem_vale(territorio, intersecao):
    # Check if territorio and intercesao are valid
    if not eh_territorio(territorio) or not eh_intersecao(intersecao):
        raise ValueError("obtem_vale: argumentos invalidos")

    # Check if intersecao is part of territorio
    if not eh_intersecao_valida(territorio, intersecao):
        raise ValueError("obtem_vale: argumentos invalidos")

    # Check if intersecao is mountain
    if eh_intersecao_livre(territorio, intersecao):
        raise ValueError("obtem_vale: argumentos invalidos")

    valleys = ()

    # Get the chain of interceptions
    for inter in obtem_cadeia(territorio, intersecao):
        # Get the adjacent interceptions
        for adj in obtem_intersecoes_adjacentes(territorio, inter):
            # Check if the adjacent interceptions are free
            if eh_intersecao_livre(territorio, adj) and adj not in valleys:
                valleys += (adj,)

    return ordena_intersecoes(valleys)


# Verify if the interceptions are connected (mountain->mountain or free->free)
def verifica_conexao(territorio, intersecao1, intersecao2):
    # Check if territorio is valid
    if not eh_territorio(territorio):
        raise ValueError("verifica_conexao: argumentos invalidos")

    # Check if intersecao1 and intersecao2 are valid
    if not eh_intersecao(intersecao1) or not eh_intersecao(intersecao2):
        raise ValueError("verifica_conexao: argumentos invalidos")

    # Check if intersecao is part of territorio
    if not eh_intersecao_valida(territorio, intersecao1) or not eh_intersecao_valida(
        territorio, intersecao2
    ):
        raise ValueError("verifica_conexao: argumentos invalidos")

    return obtem_cadeia(territorio, intersecao1) == obtem_cadeia(
        territorio, intersecao2
    )


# Return the number of occupied interceptions
def calcula_numero_montanhas(territorio):
    # Check if territorio is valid
    if not eh_territorio(territorio):
        raise ValueError("calcula_numero_montanhas: argumento invalido")

    # Count the number of occupied interceptions
    count = 0
    for collumn in territorio:
        for cell in collumn:
            if cell == 1:
                count += 1

    return count
