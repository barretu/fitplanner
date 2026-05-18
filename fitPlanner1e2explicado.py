# Lista que vai armazenar todos os treinos cadastrados
# Aqui criamos uma lista vazia que vai guardar todos os treinos.
# Cada treino será um dicionário com suas informações.
treinos = []

# Função para cadastrar um novo treino
def cadastrar_treino():
    print("\n--- Cadastrar treino ---")
    print("Exemplo: Treino 1")

    # Coleta de informações básicas do treino
    nome = input("Nome do treino: ")
    print("Exemplo: musculação, cardio, funcional, corrida")
    tipo = input("Tipo do treino: ")
    data = input("Data XX/XX/XXXX: ")
    duracao = input("Duração: ")
    objetivo = input("Objetivo: ")

    # Estrutura do treino: um dicionário com os dados e lista de exercícios
    treino = {
        "nome": nome,
        "tipo": tipo,
        "data": data,
        "duracao": duracao,
        "objetivo": objetivo,
        "exercicios": []  # inicialmente vazio
    }
    # Esse dicionário organiza os dados do treino.
    # "exercicios" começa como uma lista vazia, que será preenchida depois.

    # Pergunta se o usuário quer adicionar exercícios
    adicionar = input("Deseja adicionar exercício nesse treino? ").lower()

    # Enquanto o usuário responder "sim", adiciona exercícios
    while adicionar == "sim":
        nome_exercicio = input("Nome do exercício: ")
        series = input("Séries: ")
        repeticoes = input("Repetições: ")
        tempo = input("Tempo, se tiver: ")
        distancia = input("Distância, se tiver: ")

        # Cada exercício também é um dicionário
        exercicio = {
            "nome": nome_exercicio,
            "series": series,
            "repeticoes": repeticoes,
            "tempo": tempo,
            "distancia": distancia
        }

        # Exercício é adicionado à lista de exercícios do treino
        treino["exercicios"].append(exercicio)

        # Pergunta se deseja adicionar outro exercício
        adicionar = input("Deseja adicionar outro exercício? ").lower()

    # Depois de cadastrar, adiciona o treino completo na lista principal
    treinos.append(treino)
    print("Treino cadastrado.")


# Função para visualizar todos os treinos cadastrados
def visualizar_treinos():
    if len(treinos) == 0:
        print("\nNenhum treino cadastrado.")
    else:
        contador = 1

        # Percorre cada treino e mostra suas informações
        for treino in treinos:
            print("\nTreino", contador)
            print("Nome:", treino["nome"])
            print("Tipo:", treino["tipo"])
            print("Data:", treino["data"])
            print("Duração:", treino["duracao"])
            print("Objetivo:", treino["objetivo"])

            # Verifica se há exercícios cadastrados
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
            # Esse contador serve para numerar os treinos ao exibir.
            # Assim o usuário sabe qual número digitar para editar ou excluir.


# Função para editar um treino existente
def editar_treino():
    visualizar_treinos()

    numero = int(input("\nDigite o número do treino que deseja editar: "))

    # Verifica se o número é válido
    if numero >= 1 and numero <= len(treinos):
        treino = treinos[numero - 1]

        # Atualiza os dados do treino
        treino["nome"] = input("Novo nome do treino: ")
        treino["tipo"] = input("Novo tipo: ")
        treino["data"] = input("Nova data: ")
        treino["duracao"] = input("Nova duração: ")
        treino["objetivo"] = input("Novo objetivo: ")

        print("Treino editado.")
    else:
        print("Treino não encontrado.")


# Função para excluir um treino
def excluir_treino():
    visualizar_treinos()

    numero = int(input("\nDigite o número do treino que deseja excluir: "))

    # Se o número for válido, remove o treino da lista
    if numero >= 1 and numero <= len(treinos):
        treinos.pop(numero - 1)
        # Remove um treino da lista pelo índice.
        # Como o usuário escolhe o número começando em 1, usamos "numero - 1"
        # para ajustar ao índice correto da lista (que começa em 0).
        print("Treino excluído.")
    else:
        print("Treino não encontrado.")


# Cria um loop infinito para manter o menu rodando.
# Só vai parar quando o usuário escolher a opção 5 (break).
while True:
    print("\n--- FitPlanner ---")
    print("1 - Adicionar treino")
    print("2 - Visualizar treinos")
    print("3 - Editar treino")
    print("4 - Excluir treino")
    print("5 - Parar")

    opcao = int(input("Digite a opção: "))

    # Chama a função correspondente à opção escolhida
    if opcao == 1:
        cadastrar_treino() # executa a função
    elif opcao == 2:
        visualizar_treinos() # executa a função
    elif opcao == 3:
        editar_treino() # executa a função
    elif opcao == 4:
        excluir_treino() # executa a função
    elif opcao == 5:
        print("Programa finalizado.")
        break
    else:
        print("Opção inválida.")
