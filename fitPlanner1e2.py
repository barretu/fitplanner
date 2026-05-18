treinos = []

def cadastrar_treino():
    print("\n--- Cadastrar treino ---")
    print("Exemplo: Treino 1")

    nome = input("Nome do treino: ")
    print("Exemplo: musculação, cardio, funcional, corrida")
    tipo = input("Tipo do treino: ")
    data = input("Data DD/MM/AAAA: ")
    duracao = input("Duração: ")
    objetivo = input("Objetivo: ")

    treino = {
        "nome": nome,
        "tipo": tipo,
        "data": data,
        "duracao": duracao,
        "objetivo": objetivo,
        "exercicios": []
    }

    adicionar = input("Deseja adicionar exercício nesse treino? ").lower()

    while adicionar == "sim":
        nome_exercicio = input("Nome do exercício: ")
        series = input("Séries: ")
        repeticoes = input("Repetições: ")
        tempo = input("Tempo, se tiver: ")
        distancia = input("Distância, se tiver: ")

        exercicio = {
            "nome": nome_exercicio,
            "series": series,
            "repeticoes": repeticoes,
            "tempo": tempo,
            "distancia": distancia
        }

        treino["exercicios"].append(exercicio)

        adicionar = input("Deseja adicionar outro exercício? ").lower()

    treinos.append(treino)
    print("Treino cadastrado.")


def visualizar_treinos():
    if len(treinos) == 0:
        print("\nNenhum treino cadastrado.")
    else:
        contador = 1

        for treino in treinos:
            print("\nTreino", contador)
            print("Nome:", treino["nome"])
            print("Tipo:", treino["tipo"])
            print("Data:", treino["data"])
            print("Duração:", treino["duracao"])
            print("Objetivo:", treino["objetivo"])

            if len(treino["exercicios"]) == 0:
                print("Nenhum exercício cadastrado nesse treino.")
            else:
                print("Exercícios:")
                for exercicio in treino["exercicios"]:
                    print("- Nome:", exercicio["nome"])
                    print("  Séries:", exercicio["series"])
                    print("  Repetições:", exercicio["repeticoes"])
                    print("  Tempo:", exercicio["tempo"])
                    print("  Distância:", exercicio["distancia"])

            contador = contador + 1


def editar_treino():
    visualizar_treinos()

    numero = int(input("\nDigite o número do treino que deseja editar: "))

    if numero >= 1 and numero <= len(treinos):
        treino = treinos[numero - 1]

        treino["nome"] = input("Novo nome do treino: ")
        treino["tipo"] = input("Novo tipo: ")
        treino["data"] = input("Nova data: ")
        treino["duracao"] = input("Nova duração: ")
        treino["objetivo"] = input("Novo objetivo: ")

        print("Treino editado.")
    else:
        print("Treino não encontrado.")


def excluir_treino():
    visualizar_treinos()

    numero = int(input("\nDigite o número do treino que deseja excluir: "))

    if numero >= 1 and numero <= len(treinos):
        treinos.pop(numero - 1)
        print("Treino excluído.")
    else:
        print("Treino não encontrado.")


while True:
    print("\n--- FitPlanner ---")
    print("1 - Adicionar treino")
    print("2 - Visualizar treinos")
    print("3 - Editar treino")
    print("4 - Excluir treino")
    print("5 - Parar")

    opcao = int(input("Digite a opção: "))

    if opcao == 1:
        cadastrar_treino()
    elif opcao == 2:
        visualizar_treinos()
    elif opcao == 3:
        editar_treino()
    elif opcao == 4:
        excluir_treino()
    elif opcao == 5:
        print("Programa finalizado.")
        break
    else:
        print("Opção inválida.")
