exercicios = []

def cadastrar_exercicio():
    nome = input("Nome do exercício: ")
    series = input("Quantidade de séries: ")
    repeticoes = input("Quantidade de repetições: ")
    tempo = input("Tempo de exercícios: ")
    distancia = input("Distância: ")
    
    exercicio = {
        "nome": nome, 
        "series": series,
        "repeticoes": repeticoes,
        "tempo": tempo,
        "distancia": distancia
    }
    
    exercicios.append(exercicio)
    
    print("Exercício cadastrado com sucesso! ")
    
def listar_exercicios():
    if len(exercicios) == 0:
        print("Nenhum exercício cadastrado.")
    else: 
        for exercicio in exercicios:
            print("\n---EXERCÍCIO---")
            print(f"Nome: {exercicio['nome']}")
            print(f"Séries: {exercicio['series']}")
            print(f"Repetições: {exercicio['repeticoes']}")
            print(f"Tempo: {exercicio['tempo']}")
            print(f"Distância: {exercicio['distancia']}")

while True:
    print("\n---FITPLANNER---")
    print("1 - Cadastrar exercício")
    print("2 - Listar exercícios")
    print("0 - Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1": 
        cadastrar_exercicio()
    elif opcao == "2": 
        listar_exercicios()
    elif opcao == "3": 
        print("Programa encerrado. ")
        break 
    
    else: 
        print("Opção inválida.")
        
        
    
    
        
    
    