treinos = []

def cadastrar_treino():
    try:
        print("\n--- Cadastrar treino ---")
        print("Exemplo: Treino 1")

        nome = input("Nome do treino: ").strip()
        if nome == "":
            print("Erro: O nome do treino não pode ser vazio.")
            return

        print("Exemplo: musculação, cardio, funcional, corrida")
        tipo = input("Tipo do treino: ").strip()
        data = input("Data DD/MM/AAAA: ").strip()
        duracao = input("Duração: ").strip()
        objetivo = input("Objetivo: ").strip()

        treino = {
            "nome": nome,
            "tipo": tipo,
            "data": data,
            "duracao": duracao,
            "objetivo": objetivo,
            "exercicios": []
        }

        adicionar = input("Deseja adicionar exercício nesse treino? (sim/não) ").lower()

        while adicionar == "sim":
            try:
                nome_exercicio = input("Nome do exercício: ").strip()
                if nome_exercicio == "":
                    print("Erro: O nome do exercício não pode ser vazio.")
                    continue

                try:
                    series = int(input("Séries: "))
                    repeticoes = int(input("Repetições: "))
                except ValueError:
                    print("Erro: Séries e repetições devem ser números.")
                    continue

                tempo = input("Tempo, se tiver: ").strip()
                distancia = input("Distância, se tiver: ").strip()

                exercicio = {
                    "nome": nome_exercicio,
                    "series": series,
                    "repeticoes": repeticoes,
                    "tempo": tempo,
                    "distancia": distancia
                }

                treino["exercicios"].append(exercicio)
                print("Exercício adicionado com sucesso!")

            except ValueError:
                print("Erro: Digite os valores corretamente dentro do exercício.")

            adicionar = input("Deseja adicionar outro exercício? (sim/não) ").lower()

        treinos.append(treino)
        print("Treino cadastrado com sucesso!")

    except ValueError:
        print("Erro: Digite os valores corretamente no cadastro do treino.")
    else:
        print("Cadastro finalizado sem erros.")


def visualizar_treinos():
    try:
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
                
    except ValueError:
        print("Erro: valor inválido ao acessar os treinos.")
    else:
        print("\nVisualização concluída sem erros.")


def editar_treino():
    visualizar_treinos()

   try:
        numero = int(input("\nDigite o número do treino que deseja editar: "))

        if numero >= 1 and numero <= len(treinos):
            treino = treinos[numero - 1]

            if len(treino["exercicios"]) == 0:
                print("Esse treino ainda não possui exercícios.")
                adicionar = input("Deseja adicionar um exercício? ").lower()

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

                print("Exercícios editados.")
            else:
                print("\nExercícios do treino:")

                contador = 1
                for exercicio in treino["exercicios"]:
                    print("\nExercício", contador)
                    print("Nome:", exercicio["nome"])
                    print("Séries:", exercicio["series"])
                    print("Repetições:", exercicio["repeticoes"])
                    print("Tempo:", exercicio["tempo"])
                    print("Distância:", exercicio["distancia"])

                    contador = contador + 1

                numero_exercicio = int(input("\nDigite o número do exercício que deseja editar: "))

                if numero_exercicio >= 1 and numero_exercicio <= len(treino["exercicios"]):
                    exercicio = treino["exercicios"][numero_exercicio - 1]

                    exercicio["nome"] = input("Novo nome do exercício: ")
                    exercicio["series"] = input("Novas séries: ")
                    exercicio["repeticoes"] = input("Novas repetições: ")
                    exercicio["tempo"] = input("Novo tempo, se tiver: ")
                    exercicio["distancia"] = input("Nova distância, se tiver: ")

                    print("Exercício editado.")
                else:
                    print("Exercício não encontrado.")
        else:
            print("Treino não encontrado.")
    
    except ValueError:
        print ("Digite apenas algarismos")

    except NameError:
        print("Digite o número de um treino existente")

    except TypeError:
        print("Digite apenas algarismos")


def excluir_treino():
    visualizar_treinos()
    try:

        numero = int(input("\nDigite o número do treino que deseja excluir: "))

        if numero >= 1 and numero <= len(treinos):
                treinos.pop(numero - 1)
                print("Treino excluído.")
        else:
                print("Treino não encontrado.")

    except ValueError:
        print("Digite apenas algarismos")


while True:
    print("\n--- FitPlanner ---")
    print("1 - Adicionar treino")
    print("2 - Visualizar treinos")
    print("3 - Editar treino")
    print("4 - Excluir treino")
    print("5 - Parar")

    print()
    try:
        opcao = int(input("Digite a opção: "))

    except ValueError:
        print("Digite apenas algarismos entre as opções")
        continue

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
