treinos = []
metas = []

arquivo_treinos = "treinos.txt"
arquivo_metas = "metas.txt"

def salvar_treinos():
    arquivo = open(arquivo_treinos, "w", encoding="utf-8")

    for treino in treinos:
        meta = treino.get("meta", "")

        linha = (
            treino["nome"] + "|" +
            treino["tipo"] + "|" +
            treino["data"] + "|" +
            treino["duracao"] + "|" +
            treino["objetivo"] + "|" +
            meta + "\n"
        )

        arquivo.write(linha)

    arquivo.close()

def salvar_metas():
    arquivo = open(arquivo_metas, "w", encoding="utf-8")

    for meta in metas:
        linha = (
            meta["descricao"] + "|" +
            meta["prazo"] + "|" +
            meta["status"] + "\n"
        )

        arquivo.write(linha)

    arquivo.close()

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

        salvar_treinos()

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

                if "meta" in treino:
                    print("Meta vinculada:", treino["meta"])

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

        print(f"Há {len(treinos)} treino(s) no seu fitplanner")
        print(f"Suas metas são: {metas}")

        concluir = input("Alguma meta já foi alcançada(sim ou não)? ").lower()

        if concluir == "sim" or concluir == "Sim":
            print("Parabéns!")

            qtd_concluidas = int(input("Digite o número de metas concluídas: "))

            for i in range (qtd_concluidas):
                meta_concluida = input("Qual meta foi concluida")
                metas_concluidas = []
                metas_concluidas.append(meta_concluida)

        elif concluir == "não" or concluir == "nao":
            dias_treinados = input("A quantidade de treinos realizados corresponde a sua meta? ").lower()
            if dias_treinados == "sim":
                print("Parabéns! Continue assim.")

            elif dias_treinados == "não" or dias_treinados == "nao":
                print("Para concluir suas metas é preciso que a rotina planejada seja realista")

            else:
                print("Resposta inválida")

        else:
            print("Resposta inválida")

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

                salvar_treinos()

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

                    salvar_treinos()

                    print("Exercício editado.")
                else:
                    print("Exercício não encontrado.")
        else:
            print("Treino não encontrado.")

    except ValueError:
        print("Digite apenas algarismos")

    except NameError:
        print("Digite o número de um treino existente")

    except TypeError:
        print("Digite apenas algarismos")


def carregar_treinos():
    try:
        arquivo = open(arquivo_treinos, "r", encoding="utf-8")

        for linha in arquivo.readlines():
            dados = linha.strip().split("|")

            if len(dados) >= 5:

                treino = {
                    "nome": dados[0],
                    "tipo": dados[1],
                    "data": dados[2],
                    "duracao": dados[3],
                    "objetivo": dados[4],
                    "exercicios": []
                }

                if len(dados) >= 6:
                    treino["meta"] = dados[5]

                treinos.append(treino)

        arquivo.close()

    except FileNotFoundError:
        pass


def cadastrar_meta():
    try:
        print("\n--- Cadastrar meta ---")
        print("Exemplo: perder peso, ganhar massa muscular, melhorar condicionamento")

        descricao = input("Descrição da meta: ").strip()
        if descricao == "":
            print("Erro: A descrição da meta não pode ser vazia.")
            return

        prazo = input("Prazo para atingir a meta (DD/MM/AAAA): ").strip()
        status = "Em andamento"
        rotina = int(input("Qual sua meta de treinos por semana: "))

        meta = {
            "descricao": descricao,
            "prazo": prazo,
            "status": status,
            "rotina": rotina
        }

        metas.append(meta)

        salvar_metas()

        print("Meta cadastrada com sucesso!")

    except ValueError:
        print("Erro: Digite os valores corretamente no cadastro da meta.")
    else:
        print("Cadastro de meta finalizado sem erros.")


def visualizar_metas():
    try:
        if len(metas) == 0:
            print("\nNenhuma meta cadastrada.")
        else:
            contador = 1
            for meta in metas:
                print("\nMeta", contador)
                print("Descrição:", meta["descricao"])
                print("Prazo:", meta["prazo"])
                print("Status:", meta["status"])
                contador += 1
    except ValueError:
        print("Erro ao acessar metas.")
    else:
        print("\nVisualização de metas concluída sem erros.")


def editar_meta():
    visualizar_metas()
    try:
        numero = int(input("\nDigite o número da meta que deseja editar: "))
        if numero >= 1 and numero <= len(metas):
            meta = metas[numero - 1]
            meta["descricao"] = input("Nova descrição da meta: ").strip()
            meta["prazo"] = input("Novo prazo (DD/MM/AAAA): ").strip()
            meta["status"] = input("Novo status (Em andamento/Concluída): ").strip()

            salvar_metas()

            print("Meta editada com sucesso!")
        else:
            print("Meta não encontrada.")
    except ValueError:
        print("Digite apenas algarismos.")


def excluir_meta():
    visualizar_metas()
    try:
        numero = int(input("\nDigite o número da meta que deseja excluir: "))
        if numero >= 1 and numero <= len(metas):

            metas.pop(numero - 1)

            salvar_metas()

            print("Meta excluída.")
        else:
            print("Meta não encontrada.")
    except ValueError:
        print("Digite apenas algarismos.")


def vincular_meta_ao_treino():
    visualizar_treinos()
    visualizar_metas()
    try:
        numero_treino = int(input("\nDigite o número do treino que deseja vincular: "))
        numero_meta = int(input("Digite o número da meta que deseja associar: "))

        if numero_treino >= 1 and numero_treino <= len(treinos) and numero_meta >= 1 and numero_meta <= len(metas):
            treino = treinos[numero_treino - 1]
            meta = metas[numero_meta - 1]

            treino["meta"] = meta["descricao"]

            salvar_treinos()

            print(f"Meta '{meta['descricao']}' vinculada ao treino '{treino['nome']}' com sucesso!")
        else:
            print("Treino ou meta não encontrados.")
    except ValueError:
        print("Digite apenas algarismos.")


def carregar_metas():
    try:
        arquivo = open(arquivo_metas, "r", encoding="utf-8")

        for linha in arquivo.readlines():
            dados = linha.strip().split("|")

            if len(dados) == 3:
                meta = {
                    "descricao": dados[0],
                    "prazo": dados[1],
                    "status": dados[2]
                }

                metas.append(meta)

        arquivo.close()

    except FileNotFoundError:
        pass


def excluir_treino():
    visualizar_treinos()
    try:

        numero = int(input("\nDigite o número do treino que deseja excluir: "))

        if numero >= 1 and numero <= len(treinos):

            treinos.pop(numero - 1)

            salvar_treinos()

            print("Treino excluído.")
        else:
            print("Treino não encontrado.")

    except ValueError:
        print("Digite apenas algarismos")


carregar_treinos()
carregar_metas()

while True:
    print("\n--- FitPlanner ---")
    print("1 - Adicionar treino")
    print("2 - Visualizar treinos")
    print("3 - Editar treino")
    print("4 - Excluir treino")
    print("5 - Adicionar meta")
    print("6 - Visualizar metas")
    print("7 - Editar meta")
    print("8 - Excluir meta")
    print("9 - Vincular meta a treino")
    print("10 - Parar")

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
        cadastrar_meta()

    elif opcao == 6:
        visualizar_metas()

    elif opcao == 7:
        editar_meta()

    elif opcao == 8:
        excluir_meta()

    elif opcao == 9:
        vincular_meta_ao_treino()

    elif opcao == 10:
        print("Programa finalizado.")
        break

    else:
        print("Opção inválida.")
