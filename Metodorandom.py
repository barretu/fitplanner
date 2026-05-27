import random

sugestoes = {
    "1": {
        "objetivo": "Perder Peso",
        "exercicios": [
            "Musculação combinada com Corrida",
            "Treino de HIIT na esteira",
            "Ciclismo indoor intenso",
            "Circuito funcional com o peso do próprio corpo"
        ],
        "divisao": [
            "3 dias de musculação + 2 dias de cardio focado",
            "4 dias de treino no estilo Full Body (corpo todo)",
            "Alternando 1 dia de treino de força e 1 dia de cardio aeróbico"
        ],
        "habitos": [
            "Beber pelo menos 3L de água por dia",
            "Evitar telas de celular e TV 1 hora antes de dormir",
            "Trocar o elevador pelas escadas sempre que possível"
        ],
        "descanso": [
            "30 a 45 segundos entre as séries",
            "45 a 60 segundos para manter os batimentos cardíacos altos",
            "No máximo 1 minuto de pausa entre os blocos de exercícios"
        ],
        "alimentacao": [
            "Focar em um déficit calórico leve e boa ingestão de proteínas",
            "Aumentar o consumo de fibras e vegetais folhosos nas refeições",
            "Reduzir drasticamente o consumo de alimentos ultraprocessados e açúcar"
        ]
    },
    "2": {
        "objetivo": "Ganhar Massa Muscular",
        "exercicios": [
            "Treino de força com foco em exercícios compostos (Agachamento, Supino, Levantamento Terra)",
            "Musculação intensa com progressão de carga controlada",
            "Treino tensionado focado na fase excêntrica (descida) do movimento"
        ],
        "divisao": [
            "Divisão ABC tradicional (Peito/Tríceps, Costas/Bíceps, Pernas/Ombros)",
            "Divisão ABCD focando no extensão isolada de grandes grupos musculares",
            "Treino estruturado em Push/Pull/Legs (Empurrar, Puxar, Pernas)"
        ],
        "habitos": [
            "Dormir rigorosamente de 7 a 8 horas por noite para recuperação",
            "Anotar as cargas para garantir que está evoluindo os pesos nos treinos",
            "Evitar treinar em jejum prolongado para não perder rendimento"
        ],
        "descanso": [
            "60 a 90 segundos entre as séries",
            "1 a 2 minutos para recuperação total da força máxima",
            "90 segundos focados em restabelecer o fôlego antes da próxima carga pesada"
        ],
        "alimentacao": [
            "Manter um superávit calórico limpo com carboidratos complexos",
            "Inundar o corpo com proteínas de alto valor biológico em todas as refeições",
            "Consumir gorduras boas como abacate, ovos e castanhas"
        ]
    },
    "3": {
        "objetivo": "Melhorar Condicionamento Físico",
        "exercicios": [
            "Circuitos funcionais cronometrados sem descanso longo",
            "Natação de intensidade moderada a alta",
            "Corrida de rua intervalada ou treinos de Crossfit"
        ],
        "divisao": [
            "3 a 5 dias na semana alternando treinos de força e treinos de fôlego",
            "Treino de endurance intercalado com dias de descanso ativo (caminhada leve)",
            "Estrutura semanal focada em flexibilidade, mobilidade e resistência cardiovascular"
        ],
        "habitos": [
            "Praticar alongamentos diários ao acordar ou antes de dormir",
            "Controlar o ritmo respiratório e a postura durante as atividades do dia",
            "Manter a consistência na frequência semanal, mesmo em dias frios ou chuvosos"
        ],
        "descanso": [
            "30 a 45 segundos para manter a intensidade lá no alto",
            "Descanso dinâmico (como caminhar devagar enquanto aguarda o próximo round)",
            "Pausas curtas para simular situações reais de cansaço extremo"
        ],
        "alimentacao": [
            "Dieta rica em micronutrientes vindos de frutas de cores variadas",
            "Hidratação constante dividida antes, durante e logo após o treino",
            "Consumir carboidratos de rápida absorção logo antes de treinos longos de endurance"
        ]
    }
}

def exibir_sugestoes_aleatorias():
    print("\n--- Escolha seu Objetivo ---")
    print("1. Perder Peso")
    print("2. Ganhar Massa Muscular")
    print("3. Melhorar Condicionamento Físico")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao in sugestoes:
        dados = sugestoes[opcao]
        print(f"\n=== SUGESTÕES ALEATÓRIAS PARA: {dados['objetivo'].upper()} ===")
        print(f"Exercício: {random.choice(dados['exercicios'])}")
        print(f"Divisão Semanal: {random.choice(dados['divisao'])}")
        print(f"Hábito Saudável: {random.choice(dados['habitos'])}")
        print(f"Tempo de Descanso: {random.choice(dados['descanso'])}")
        print(f"Dica de Alimentação: {random.choice(dados['alimentacao'])}")
    else:
        print("\nOpção inválida.")

def menu():
    while True:
        print("\n--- Sistema de Sugestões Fitness ---")
        print("1. Gerar combinação de sugestões aleatórias")
        print("2. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            exibir_sugestoes_aleatorias()
        elif opcao == '2':
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

menu()
