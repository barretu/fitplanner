exercicios = []

def cadastrar_exercicio():
    print("\n--- Cadastro de exercício ---")

    nome = input("Exercício: ")
    series = input("Séries: ")
    repeticoes = input("Repetições: ")
    tempo = input("Tempo, se tiver: ")
    distancia = input("Distância, se tiver: ")

    novo_exercicio = {
        "nome": nome,
        "series": series,
        "repeticoes": repeticoes,
        "tempo": tempo,
        "distancia": distancia
    }

    exercicios.append(novo_exercicio)
    print("Exercício cadastrado.\n")

def mostrar_exercicios():
    if len(exercicios) == 0:
        print("\nNenhum exercício foi cadastrado ainda.")
    else:
        print("\nExercícios cadastrados:")

        contador = 1
        for exercicio in exercicios:
            print("\nExercício", contador)
            print("Nome:", exercicio["nome"])
            print("Séries:", exercicio["series"])
            print("Repetições:", exercicio["repeticoes"])
            print("Tempo:", exercicio["tempo"])
            print("Distância:", exercicio["distancia"])
            contador = contador + 1

opcao = ""

while opcao != "0":
    print("\nFITPLANNER")
    print("1 - Cadastrar exercício")
    print("2 - Ver exercícios cadastrados")
    print("0 - Sair")

    opcao = input("Opção: ")

    if opcao == "1":
        cadastrar_exercicio()
    elif opcao == "2":
        mostrar_exercicios()
    elif opcao == "0":
        print("Programa finalizado.")
    else:
        print("Opção inválida.")
