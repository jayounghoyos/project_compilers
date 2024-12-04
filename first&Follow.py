import sys


def compute_first(grammar):
    first = {nonterminal: set() for nonterminal in grammar}
    changed = True
    while changed:
        changed = False
        for nonterminal, productions in grammar.items():
            for production in productions:
                for symbol in production:
                    if symbol.islower():  # Es un terminal (minúscula)
                        if symbol not in first[nonterminal]:
                            first[nonterminal].add(symbol)
                            changed = True
                        break
                    elif symbol == "e":  # Representación de la cadena vacía
                        if "e" not in first[nonterminal]:
                            first[nonterminal].add("e")
                            changed = True
                        break
                    else:  # Es un no-terminal (mayúscula)
                        new_symbols = first[symbol] - {"e"}
                        if not new_symbols.issubset(first[nonterminal]):
                            first[nonterminal].update(new_symbols)
                            changed = True
                        if "e" not in first[symbol]:
                            break
                else:
                    if "e" not in first[nonterminal]:
                        first[nonterminal].add("e")
                        changed = True
    return first


def compute_follow(grammar, first, start_symbol):
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add(
        "$"
    )  # Follow del símbolo inicial contiene el símbolo de finalización '$'
    changed = True
    while changed:
        changed = False
        for nonterminal, productions in grammar.items():
            for production in productions:
                trailer = follow[nonterminal].copy()
                for symbol in reversed(production):
                    if symbol.isupper():  # Si es un no-terminal (mayúscula)
                        if not trailer.issubset(follow[symbol]):
                            follow[symbol].update(trailer)
                            changed = True
                        if "e" in first[symbol]:
                            trailer.update(first[symbol] - {"e"})
                        else:
                            trailer = first[symbol]
                    else:
                        trailer = {symbol}  # Si es un terminal (minúscula)
    return follow


# Función principal para manejar el input y output de datos de gramáticas
def main():
    input_data = sys.stdin.read().splitlines()

    n = int(input_data[0])  # Número de casos
    index = 1
    for _ in range(n):
        m = int(input_data[index])  # Número de no-terminales
        index += 1
        grammar = {}
        for _ in range(m):
            line = input_data[index].split()
            nonterminal = line[0]
            productions = line[1:]
            grammar[nonterminal] = [prod for prod in productions]
            index += 1

        # Calcular conjuntos First y Follow de la gramática ingresada
        first = compute_first(grammar)
        follow = compute_follow(
            grammar, first, "S"
        )  # Se asume que 'S' es el símbolo inicial

        # Imprimir el conjunto First para cada no-terminal
        for nonterminal in grammar:
            print(f"First({nonterminal}) = {{{', '.join(first[nonterminal])}}}")
        # Imprimir el conjunto Follow para cada no-terminal
        for nonterminal in grammar:
            print(f"Follow({nonterminal}) = {{{', '.join(follow[nonterminal])}}}")
        print()


if __name__ == "__main__":
    main()
