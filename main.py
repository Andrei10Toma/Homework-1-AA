# ANALIZA ALGORITMILOR TEMA 1

# TOMA ANDREI 321CB

import sys

# encode - encodarea masinii Turing
# functie citire masina Turing data ca o encodare
def readtm(encode):
    final_states = []

    # initializare dictionar pentru citirea masinii turing cu cheile "number of states",
    # "final states", "transtions"
    TM = {}

    TM["number of states"] = encode[0]

    # parcurge linia cu stari finale, le adauga intr-o lista si dupa in dictionar
    for p in encode[1].split():
        final_states.append(p)
    TM["final states"] = final_states

    # parcurge urmatoarele linii cu tranzitii, le adauga intr-o lista si dupa in dictionar
    transitions = []
    for transition in encode[2:len(encode)]:
        transitions.append(transition)
    TM["transitions"] = transitions

    return TM


# TM - masina turing retinuta ca dictionar
# configuration - configuratia pe care trebuie sa se faca un pas
# functie care realizeaza un pas in configuratia data pe baza tranzitiilor din Masina Turing
def step(TM, configuration):
    # transfomare configuratie intr-o lista pe componente
    new_configuration = configuration.split(',')
    ok = 0

    for transition in TM["transitions"]:
        # transformare tranzitie intr-o lista pe componente
        new_transition = transition.split(' ')
        # verificare stare curenta
        if new_configuration[1] == new_transition[0]:
            # verificare caracter pe care se afla ciursorul
            if new_configuration[2][0] == new_transition[1]:
                # s-a gasit tranzitia corecta si urmeaza executarea pasului
                # actualizare stare
                new_configuration[1] = new_transition[2]
                ok = 1
                # actualizare configuratie in functie de pozitia urmatoare a cursorului
                if new_transition[4] == 'R':
                    new_configuration[0] += new_transition[3]
                    if len(new_configuration[2]) == 1:
                        new_configuration[2] = "#"
                    else:
                        new_configuration[2] = new_configuration[2][1:len(new_configuration[2])]
                elif new_transition[4] == 'H':
                    new_configuration[2] = new_transition[3] + new_configuration[2][1:len(new_configuration[2])]
                elif new_transition[4] == 'L':
                    new_configuration[2] = new_transition[3] + new_configuration[2][1:len(new_configuration[2])]
                    if len(new_configuration[0]) == 1:
                        new_configuration[2] = new_configuration[0] + new_configuration[2]
                        new_configuration[0] = "#"
                    else:
                        new_configuration[2] = new_configuration[0][len(new_configuration[0]) - 1] + \
                                               new_configuration[2]
                        new_configuration[0] = new_configuration[0][0:len(new_configuration[0]) - 1]
                # returnarea noii configuratii
                return '(' + new_configuration[0] + ',' + new_configuration[1] + ',' + new_configuration[2] + ')'
    # masina nu reuseasca sa faca un pas pentru configuratia data
    if ok == 0:
        return "False"


# configurations - stringul de configuratii dat de la input
# functia converteste stringul intr-o lista de configuratii si o returneaza
def convertStringToListStep(configurations):
    l = []
    for p in configurations.split(") ("):
        if p[0] == '(':
            l.append(p.replace('(', ''))
        elif p[len(p) - 1] == ')':
            l.append(p.replace(')', ''))
        else:
            l.append(p)

    return l


# words - cuvintele date la input care trebuie testate daca sunt acceptate de Masina Turing
# functia converteste stringul de cuvinte intr-o lista
def convertStringToListAccept(words):
    l = []
    for p in words.split(" "):
        l.append(p)
    return l


# word - cuvant scris normal de la input
# functia returneaza cuvantul scris ca o configuratie cu 3 componente
def convertWordToConfiguration(word):
    return "#,0," + word


# TM - Masina Turing retinuta in dictionar
# word - cuvant care trebuie testat daca este acceptat de Masina Turing
def accept(TM, word):
    # converteste cuvantul sub forma unei configuratii cu 3 elemente (u, q, v)
    configuration = convertWordToConfiguration(word)
    # converteste configuratia intr-o noua configuratie sub forma de lista
    new_configuration = configuration.split(',')
    while 1:
        for final_state in TM["final states"]:
            # verificare daca s-a ajuns intr-o stare finala
            if new_configuration[1] == final_state:
                return "True"
        configuration = step(TM, configuration)
        # daca nu se poate face un pas atunci masina s-a agatat
        if (configuration == "False"):
            return "False"
        # actualizare configuratie
        configuration = configuration[1:len(configuration) - 1]
        new_configuration = configuration.split(',')


# k - numarul de pasi care trebuie facut sa se verifice daca masina acceota cuvantul
# TM - Masina Turing retinuta in dictionar
# word - cuvantul care este testat daca este acceptat de TM in k pasi
def k_accept(k, TM, word):
    steps = 0
    configuration = convertWordToConfiguration(word)
    new_configuration = configuration.split(',')
    while steps <= int(k):
        for final_state in TM["final states"]:
            # verificare daca este in stare finala
            if new_configuration[1] == final_state:
                return "True"
        configuration = step(TM, configuration)
        if (configuration == "False"):
            return "False"
        # actualizare configuratie
        configuration = configuration[1:len(configuration) - 1]
        new_configuration = configuration.split(',')
        steps += 1
    return "False"


if __name__ == '__main__':

    # citire input
    lines = sys.stdin.read().splitlines()

    TM = readtm(lines[2:len(lines)])

    # in functie de prima linie apeleaza functia repspectiva
    if lines[0] == "step":
        configurations = convertStringToListStep(lines[1])
        for configuration in configurations:
            print(step(TM, configuration), end=" ")
    elif lines[0] == "accept":
        words = convertStringToListAccept(lines[1])
        for word in words:
            print(accept(TM, word), end=" ")
    elif lines[0] == "k_accept":
        k_words = convertStringToListAccept(lines[1])
        for k_word in k_words:
            word = k_word.split(',')[0]
            k = k_word.split(',')[1]
            print(k_accept(k, TM, word), end=" ")