""" 
Author: 
- Diogo Santos (ist1110262)

Date:
- 12/10/2023 (Doze de Outubro de 2023)

Description: 
- This file contains the functions that are used on the FProg project1.

"""


# Verify if the territory is valid
def eh_territorio(territorio: tuple[tuple[int]]) -> bool:
    """
    Checks if the given territory is valid.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - True if the territory is valid, False otherwise.
    """
    # Check if the territorio is a tuple
    if not isinstance(territorio, tuple):
        return False

    # Check if the territorio is empty or larger than expected
    if len(territorio) < 1 or len(territorio) > 26:
        return False

    first_collumn = territorio[0]
    # Check if the collumns have the same lenght
    for collumn in territorio:
        # Check if the arg is a tuple
        if not isinstance(collumn, tuple):
            return False

        # Check if the tuple is empty or larger than expected
        if len(collumn) < 1 or len(collumn) > 99:
            return False

        # Check if the collumn has the same lenght as the first collumn
        if len(collumn) != len(first_collumn):
            return False

        # Check if the collumn has only 0 or 1
        for cell in collumn:
            # Check if cell is int
            if type(cell) != int:
                return False

            if cell not in {0, 1}:
                return False

    return True


# Return a valid last interception (top right) based on the territory
def obtem_ultima_intersecao(territorio: tuple[tuple[int]]) -> tuple[str, int]:
    """
    Returns the coordinates of the last interception (top right) based on the given territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - A tuple of a string and an integer representing the coordinates of the last interception (top right) of the territory
    """
    return (chr(ord('A') - 1 + len(territorio)), len(territorio[0]))


# Verify if the interception is valid
def eh_intersecao(intersecao: tuple[str, int]) -> bool:
    """
    Verifies if the given intersection is valid.

    Parameters:
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - True if the intersection is valid, False otherwise.
    """
    # Check if the intersecao is a tuple
    if not isinstance(intersecao, tuple):
        return False

    # Check if the intersecao is the expected size
    if len(intersecao) != 2:
        return False

    # Create a set with all the valid strings
    valid_strings = {chr(ord('A') + i) for i in range(26)}

    # Check if the first element is a string
    if not isinstance(intersecao[0], str):
        return False

    # Check if the second element is a int
    if type(intersecao[1]) != int:
        return False

    # Check if the first element is a valid string
    if intersecao[0] not in valid_strings:
        return False

    # Check if the second element is a valid int
    if intersecao[1] < 1 or intersecao[1] > 99:
        return False

    return True


# Verify if the interception is in the territory
def eh_intersecao_valida(
    territorio: tuple[tuple[int]], intersecao: tuple[str, int]
) -> bool:
    """
    Verifies if the given intersection is within the territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - True if the intersection is within the territory, False otherwise.
    """
    max_collumns, max_lines = obtem_ultima_intersecao(territorio)
    collumn, line = intersecao

    # Check if the collumn is larger than the maximum allowed for collumns
    if collumn > max_collumns:
        return False

    # Check if the line is larger than the maximum allowed for lines
    if line > max_lines:
        return False

    return True


# Verify if the interception is free
def eh_intersecao_livre(
    territorio: tuple[tuple[int]], intersecao: tuple[str, int]
) -> bool:
    """
    Checks if the intersection is free in the given territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - A boolean value indicating whether the intersection is free (True) or occupied (False).
    """
    collumn, line = convert_intersecao(intersecao)
    return territorio[collumn][line] == 0


# Return the adjacent interceptions
def obtem_intersecoes_adjacentes(
    territorio: tuple[tuple[int]], intersecao: tuple[str, int]
) -> tuple[tuple[str, int]]:
    """
    Returns the adjacent intersections of the given intersection in the territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - A tuple containing the adjacent intersections of the given intersection in the territory, where each element is a tuple containing the column as a string and the line as an integer.
    """
    collumn, line = convert_intersecao(intersecao)
    max_collumns, max_lines = obtem_ultima_intersecao(territorio)
    inter_adjs = ()

    # Add the bottom adjacent interception
    if line > 0:
        inter_adjs += ((chr(collumn + ord('A') - 1 + 1), line),)

    # Add the left adjacent interception
    if collumn > 0:
        inter_adjs += ((chr(collumn + ord('A') - 1), line + 1),)

    # Add the right adjacent interception
    if collumn + 2 <= ord(max_collumns) - ord('A') - 1:
        inter_adjs += ((chr(collumn + ord('A') - 1 + 2), line + 1),)

    # Add the top adjacent interception
    if line + 2 <= max_lines:
        inter_adjs += ((chr(collumn + ord('A') - 1 + 1), line + 2),)

    return inter_adjs


# Order the Intersections by left to right, bottom to top
def ordena_intersecoes(intersecoes: tuple[tuple[str, int]]) -> tuple[tuple[str, int]]:
    """
    Sorts the intersections by their position from left to right and bottom to top.

    Args:
    - intersecoes: A tuple of tuples representing intersections, where each inner tuple contains a string representing the
    intersection's collumn and an integer representing the intersection's line.

    Returns:
    - A tuple of tuples representing intersections sorted by their position from left to right and bottom to top.
    """
    # sort based on the number(line), then based on the letter(collumn)
    return tuple(sorted(intersecoes, key=lambda x: (x[1], x[0])))


# Return the territory as a string
def territorio_para_str(territorio: tuple[tuple[int]]) -> str:
    """
    Returns a string representation of a territory, where each intersection is represented by an X or a . depending on
    whether it is occupied or not, respectively. The territory is formatted as a grid with letters representing columns
    and numbers representing rows.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - A string representation of the territory, formatted as a grid with letters representing columns and numbers
    representing rows.

    Raises:
    - ValueError: If the given territory is invalid.
    """
    # Check if territory is valid
    if not eh_territorio(territorio):
        raise ValueError("territorio_para_str: argumento invalido")

    # Get the maximum collumns and lines
    max_collumns, max_lines = obtem_ultima_intersecao(territorio)
    max_collumns = ord(max_collumns) - ord('A') - 1

    # Add a Letters line
    s = ["  "] + [" " + chr(ord('A') - 1 + x) for x in range(1, max_collumns + 1)] + ["\n"]

    # Create the lines (number, values, number)
    for x in range(max_lines, 0, -1):
        # Create the values
        string_terrain = [
            " " + ("X" if territorio[y][x - 1] == 1 else ".")
            for y in range(max_collumns)
        ]

        # Add the lines to the string dynamically
        if x > 9:
            s += [str(x)] + string_terrain + [" " + str(x) + "\n"]
        else:
            s += [" " + str(x)] + string_terrain + ["  " + str(x) + "\n"]

    # Add a Letters line
    s += ["  "] + [" " + chr(ord('A') - 1 + x) for x in range(1, max_collumns + 1)]

    # Join the string
    return "".join(s)


# Return the chain of interceptions
def obtem_cadeia(
    territorio: tuple[tuple[int]], intersecao: tuple[str, int]
) -> tuple[tuple[str, int]]:
    """
    Returns a sequence of adjacent intersections that have the same value in a territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - A tuple of tuples representing a sequence of adjacent intersections that have the same value in the territory.

    Raises:
    - ValueError: If the given territory or intersection are invalid.
    """
    # Check if territorio and intersection are valid
    if not eh_territorio(territorio) or not eh_intersecao(intersecao):
        raise ValueError("obtem_cadeia: argumentos invalidos")

    # Check if intersecao is part of territorio
    if not eh_intersecao_valida(territorio, intersecao):
        raise ValueError("obtem_cadeia: argumentos invalidos")

    # Check if intersecao is free
    is_free = eh_intersecao_livre(territorio, intersecao)
    visited = []

    # Create recursive function to check if the adjacent interceptions are also the same as freedom
    def recursive_check(territorio, intersecao, visited):
        # Add the intersecao to the list
        chain = (intersecao,)
        visited += chain

        # Check if the adjacent interceptions are equal to the freedom
        for inter in obtem_intersecoes_adjacentes(territorio, intersecao):
            if (
                inter not in visited
                and eh_intersecao_livre(territorio, inter) == is_free
            ):
                chain += recursive_check(territorio, inter, visited)

        return chain

    # Get the list of interceptions
    chain = recursive_check(territorio, intersecao, visited)

    return ordena_intersecoes(chain)


# Return the valleys around a mountain
def obtem_vale(
    territorio: tuple[tuple[int]], intersecao: tuple[str, int]
) -> tuple[tuple[str, int]]:
    """
    Returns the valleys around a mountain in a territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - A tuple of tuples representing valleys around the given mountain in the territory, sorted by their
    position from left to right and bottom to top.
    Raises:
    - ValueError: If the given territory or intersection are invalid, or if the given intersection is not a mountain.
    """
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
def verifica_conexao(
    territorio: tuple[tuple[int]],
    intersecao1: tuple[str, int],
    intersecao2: tuple[str, int],
) -> bool:
    """
    Returns a boolean indicating whether two intersections in a territory are connected, where a connection exists if there
    is a chain of adjacent intersections between them that are either both free or both occupied.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.
    - intersecao1: A tuple containing a string and an integer, representing an intersection.
    - intersecao2: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - A boolean indicating whether the two intersections are connected.

    Raises:
    - ValueError: If the given territory or intersections are invalid, or if the given intersections are not part of the
    territory.
    """
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
def calcula_numero_montanhas(territorio: tuple[tuple[int]]) -> int:
    """
    Returns the number of mountains in a territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - An integer representing the number mountains in a territory.

    Raises:
    - ValueError: If the given territory is invalid.
    """
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


# Return the number of mountain chains
def calcula_numero_cadeias_montanhas(territorio: tuple[tuple[int]]) -> int:
    """
    Returns the number of connected mountains in a territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - An integer representing the number of connected mountains in a territory.

    Raises:
    - ValueError: If the given territory is invalid.
    """
    # Check if territorio is valid
    if not eh_territorio(territorio):
        raise ValueError("calcula_numero_cadeias_montanhas: argumento invalido")

    # Get the occupied interceptions
    occupied = get_occupied_intersecao(territorio)
    visited = ()
    count = 0
    for occupied_intercesao in occupied:
        # Verify if the intercesao has been checked already
        if occupied_intercesao not in visited:
            visited += obtem_cadeia(territorio, occupied_intercesao)
            count += 1

    return count


# Return the number of valeys
def calcula_tamanho_vales(territorio: tuple[tuple[int]]) -> int:
    """
    Returns the number of valleys in a territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - An integer representing the number of valleys in a territory.

    Raises:
    - ValueError: If the given territory is invalid.
    """
    # Check if territorio is valid
    if not eh_territorio(territorio):
        raise ValueError("calcula_tamanho_vales: argumento invalido")

    # Get the occupied interceptions
    occupied = get_occupied_intersecao(territorio)
    visited = ()
    valeys = ()
    # Get the valeys
    for occupied_intercesao in occupied:
        # Verify if the intercesao has been checked already
        if occupied_intercesao not in visited:
            visited += obtem_cadeia(territorio, occupied_intercesao)
            valeys += obtem_vale(territorio, occupied_intercesao)

    # Clean duplicates
    return len(set(valeys))


"""
Auxiliary Functions

"""


# Return a tuple of interceptions that are occupied
def get_occupied_intersecao(territorio: tuple[tuple[int]]) -> tuple[tuple[str, int]]:
    """
    Returns the occupied intersections in a territory.

    Args:
    - territorio: a tuple representing the territory, where each element is a tuple representing a column of the territory.
    Each cell of the column can be either 0 or 1.

    Returns:
    - A tuple of tuples representing occupied intersections in the territory, sorted by their position from left to right
    and bottom to top.

    Raises:
    - ValueError: If the given territory is invalid.
    """
    # Create a list of interceptions
    occupied = ()

    # Check all the interceptions
    for collumn in range(len(territorio)):
        for cell in range(len(territorio[collumn])):
            # Convert to intercesao (0 -> A) (0 -> 1)
            intercesao = (chr(ord('A') + collumn), 1 + cell)

            # Check if the intercesao is free
            if not eh_intersecao_livre(territorio, intercesao):
                occupied += (intercesao,)

    return ordena_intersecoes(occupied)


# Return the interseption in usable values for coding (A -> 0) (1 -> 0)
def convert_intersecao(intersecao: tuple[str, int]) -> tuple[int, int]:
    """
    Converts the intersection coordinates from a tuple of strings and integers to a tuple of usable integers.

    Args:
    - intersecao: A tuple containing a string and an integer, representing an intersection.

    Returns:
    - A tuple containing the column number as an integer (starting from 0) and the line number as an integer (starting from 0).
    """
    collumn, line = intersecao
    return (ord(collumn) - ord('A') - 1 - 1, line - 1)
