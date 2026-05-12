print("---Gerenciador de treinos---")
print("Opções: ")
print("1- Adicionar")
print("2- Visualizar")
print("3- Editar")
print("4- Excluir")
print("5- Parar")

nomes_dos_treinos = {}

while True:
    resposta = int(input("Digite o número correspondente a ação desejada: "))
    if resposta == 1 :
        print("Opções de treino")
        print("1- Musculação")
        print("2- Cardio")
        print("3- Funcional")
        print("4- Corrida")

        treino = input("Digite o treino que deseja adicionar: ")
        adicionar_exercício = input("Deseja adicionar um exercício nessa categoria?").lower()
        if adicionar_exercício== "sim":
            exercicio = input("Digite o exercício que deseja adicionar: ")
            nomes_dos_treinos[treino] = exercicio

        else:
            nomes_dos_treinos[treino]= ' '

    elif resposta == 2:
        print(nomes_dos_treinos)

    elif resposta == 3:
        editar = int(input("Digite o treino que deseja editar: "))
        if editar in nomes_dos_treinos: 
            novo = int(input("Digite o execício que deseja editar: "))
            nomes_dos_treinos[editar] = novo
        else:
            print("Opção inválida")

    elif resposta == 4:
        opcao = input("Você deseja excluir uma categoria de treino ou um exercício? ")
        if opcao.lower() == "categoria":
            categoria = input("Digite a categoria que deseja excluir: ")
            del nomes_dos_treinos [categoria]
            print(f"{categoria} excluida do seu gerenciador de treinos.")
        
        elif opcao.lower() == "exercicio" or opcao == "exercício":
            qual_categoria = input("Digite a categoria desse exercício: ")
            exercicio_excluir = input("Digite o exercício que você deseja excluir: ")
            nomes_dos_treinos[qual_categoria].remove(exercicio_excluir)
            print(f"O(A) {exercicio_excluir} foi excluído")

    elif resposta == 5:
        break

    else:
        print("Opção inválida")
