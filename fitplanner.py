# 'import os' traz o módulo 'os' que permite interagir com o sistema operacional,
# como criar pastas e verificar se arquivos existem
import os

# 'from datetime import datetime' importa só a classe 'datetime' do módulo 'datetime'
# Usamos ela pra validar se a data que o usuário digitou está no formato certo
from datetime import datetime


# -------------------------------------------
# TIPOS DE TREINO VÁLIDOS
# -------------------------------------------

# Lista com os tipos de treino aceitos pelo programa
# Usada pra validar o que o usuário digita
# Está em maiúsculas por convenção: variáveis assim são constantes (não mudam)
TIPOS_TREINO = ["musculacao", "cardio", "funcional", "corrida"]


# -------------------------------------------
# DADOS EM MEMÓRIA
# -------------------------------------------

# Dicionário que guarda todos os treinos enquanto o programa está rodando
# Chave = nome do treino (string), Valor = dicionário com os dados
# Exemplo do que fica dentro:
# {
#   "Treino A": {"tipo": "musculacao", "data": "17/05/2025", "duracao": "60", "objetivo": "Ganhar massa"}
# }
nomes_dos_treinos = {}

# Lista que guarda todos os exercícios enquanto o programa está rodando
# Cada item da lista é um dicionário com os dados de um exercício
# Exemplo do que fica dentro:
# [
#   {"nome": "Agachamento", "treino": "Treino A", "modo": "series", "series": "4", ...}
# ]
exercicios = []


# =====================================================
# FUNÇÕES DE ARQUIVO
# Responsáveis por salvar e carregar dados do disco
# =====================================================

def garantir_pasta():
    """Cria a pasta 'dados' se ela não existir."""

    # os.makedirs cria a pasta (e subpastas se precisar)
    # exist_ok=True faz com que não dê erro se a pasta já existir
    os.makedirs("dados", exist_ok=True)


def carregar_treinos():
    """
    Lê o arquivo treinos.txt e coloca os dados no dicionário global.
    Chamada uma vez no início do programa pra restaurar os dados salvos.
    """

    # 'global' indica que vamos usar a variável global nomes_dos_treinos
    # Sem isso, Python criaria uma variável local com o mesmo nome
    global nomes_dos_treinos

    # Garante que a pasta 'dados' existe antes de tentar ler
    garantir_pasta()

    # Se o arquivo ainda não existe (primeira vez rodando), não faz nada
    if not os.path.exists("dados/treinos.txt"):
        return

    # Abre o arquivo em modo leitura ("r")
    # 'with' garante que o arquivo seja fechado automaticamente ao terminar
    # encoding="utf-8" garante que acentos e caracteres especiais funcionem
    with open("dados/treinos.txt", "r", encoding="utf-8") as arquivo:

        # Percorre o arquivo linha por linha
        for linha in arquivo:

            # .strip() remove espaços e o "\n" (quebra de linha) do início e fim
            linha = linha.strip()

            # Pula linhas em branco, se houver
            if not linha:
                continue

            # .split("|") divide a linha pelo separador "|" e retorna uma lista
            # Exemplo: "Treino A|musculacao|17/05/2025|60|Ganhar massa"
            # Vira:    ["Treino A", "musculacao", "17/05/2025", "60", "Ganhar massa"]
            partes = linha.split("|")

            # O primeiro campo é o nome, que usamos como chave do dicionário
            nome = partes[0]

            # Os campos seguintes viram os valores do dicionário desse treino
            nomes_dos_treinos[nome] = {
                "tipo":     partes[1],
                "data":     partes[2],
                "duracao":  partes[3],
                "objetivo": partes[4]
            }


def salvar_treinos():
    """
    Pega tudo que está no dicionário e salva no arquivo treinos.txt.
    Chamada toda vez que um treino é adicionado, editado ou excluído.
    """
    garantir_pasta()

    # Abre em modo escrita ("w"): apaga o conteúdo anterior e escreve do zero
    with open("dados/treinos.txt", "w", encoding="utf-8") as arquivo:

        # .items() retorna cada par (chave, valor) do dicionário
        # Aqui: nome = "Treino A", dados = {"tipo": "musculacao", ...}
        for nome, dados in nomes_dos_treinos.items():

            # "|".join([...]) junta todos os campos numa string separada por "|"
            # Exemplo: "Treino A|musculacao|17/05/2025|60|Ganhar massa"
            linha = "|".join([
                nome,
                dados["tipo"],
                dados["data"],
                dados["duracao"],
                dados["objetivo"]
            ])

            # Escreve a linha no arquivo e pula para a próxima com "\n"
            arquivo.write(linha + "\n")


def carregar_exercicios():
    """
    Lê o arquivo exercicios.txt e coloca os dados na lista global.
    Chamada uma vez no início do programa.
    """
    global exercicios
    garantir_pasta()

    if not os.path.exists("dados/exercicios.txt"):
        return

    with open("dados/exercicios.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha:
                continue

            partes = linha.split("|")

            # .append() adiciona um novo item ao final da lista
            exercicios.append({
                "nome":       partes[0],
                "treino":     partes[1],  # nome do treino ao qual esse exercício pertence
                "modo":       partes[2],  # "series", "tempo" ou "distancia"
                "series":     partes[3],
                "repeticoes": partes[4],
                "tempo":      partes[5],
                "distancia":  partes[6]
            })


def salvar_exercicios():
    """
    Salva todos os exercícios da lista no arquivo exercicios.txt.
    Chamada toda vez que um exercício é adicionado, editado ou excluído.
    """
    garantir_pasta()

    with open("dados/exercicios.txt", "w", encoding="utf-8") as arquivo:
        for ex in exercicios:
            linha = "|".join([
                ex["nome"],
                ex["treino"],
                ex["modo"],
                ex["series"],
                ex["repeticoes"],
                ex["tempo"],
                ex["distancia"]
            ])
            arquivo.write(linha + "\n")


# =====================================================
# FUNÇÕES DE TREINO
# =====================================================

def adicionar_treino():
    """Coleta os dados do usuário e adiciona um novo treino."""
    print("\n--- Adicionar Treino ---")

    # Mostra os tipos válidos antes de pedir o input
    # ', '.join(TIPOS_TREINO) transforma a lista em uma string separada por vírgula
    # Resultado: "musculacao, cardio, funcional, corrida"
    print(f"Tipos disponíveis: {', '.join(TIPOS_TREINO)}")

    # --- Validação do nome ---
    # .strip() remove espaços extras que o usuário possa ter digitado
    nome = input("Digite o nome do treino: ").strip()

    # 'if not nome' é True quando a string está vazia (usuário só apertou Enter)
    if not nome:
        print("Erro: o nome não pode ser vazio.")
        return  # 'return' sai da função imediatamente, sem continuar

    # Verifica se já existe um treino com esse nome no dicionário
    if nome in nomes_dos_treinos:
        print(f"Erro: já existe um treino chamado '{nome}'.")
        return

    # --- Validação do tipo ---
    # .lower() converte pra minúsculo, assim "Cardio" e "cardio" funcionam igual
    tipo = input("Digite o tipo do treino: ").strip().lower()

    # 'not in' verifica se o tipo NÃO está na lista de tipos válidos
    if tipo not in TIPOS_TREINO:
        print(f"Erro: tipo inválido. Escolha entre: {', '.join(TIPOS_TREINO)}")
        return

    # --- Validação da data ---
    data = input("Data do treino (DD/MM/AAAA): ").strip()

    # try/except tenta executar o bloco 'try'
    # Se der erro, vai pro 'except' em vez de travar o programa
    try:
        # datetime.strptime tenta converter a string pra um objeto de data
        # Se o formato estiver errado, lança um ValueError automaticamente
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        print("Erro: data inválida. Use o formato DD/MM/AAAA.")
        return

    # --- Validação da duração ---
    duracao_str = input("Duração em minutos: ").strip()
    try:
        # int() converte string pra número inteiro
        # Se o usuário digitar letra, int() lança ValueError
        duracao = int(duracao_str)

        if duracao <= 0:
            # 'raise ValueError' força um erro manualmente
            # Assim o except abaixo vai capturar tanto letras quanto números inválidos
            raise ValueError
    except ValueError:
        print("Erro: duração deve ser um número inteiro maior que zero.")
        return

    # --- Validação do objetivo ---
    objetivo = input("Objetivo do treino: ").strip()
    if not objetivo:
        print("Erro: o objetivo não pode ser vazio.")
        return

    # Se passou por todas as validações, adiciona o treino ao dicionário
    # str(duracao) converte o número de volta pra string, pois salvamos tudo como texto
    nomes_dos_treinos[nome] = {
        "tipo":     tipo,
        "data":     data,
        "duracao":  str(duracao),
        "objetivo": objetivo
    }

    # Salva no arquivo imediatamente após adicionar
    salvar_treinos()
    print(f"\nTreino '{nome}' adicionado com sucesso!")


def visualizar_treinos():
    """Exibe todos os treinos cadastrados de forma organizada."""
    print("\n--- Seus Treinos ---")

    # 'not nomes_dos_treinos' é True quando o dicionário está vazio
    if not nomes_dos_treinos:
        print("Nenhum treino cadastrado ainda.")
        return

    # Percorre cada par (nome, dados) do dicionário
    for nome, dados in nomes_dos_treinos.items():
        print("-" * 40)  # Imprime 40 traços como separador visual
        print(f"Nome:     {nome}")
        print(f"Tipo:     {dados['tipo']}")
        print(f"Data:     {dados['data']}")
        print(f"Duração:  {dados['duracao']} minutos")
        print(f"Objetivo: {dados['objetivo']}")

    print("-" * 40)

    # len() retorna o tamanho (quantidade de itens) do dicionário
    print(f"Total: {len(nomes_dos_treinos)} treino(s)")


def editar_treino():
    """Permite editar os campos de um treino existente."""
    print("\n--- Editar Treino ---")

    if not nomes_dos_treinos:
        print("Nenhum treino cadastrado ainda.")
        return

    # Mostra os treinos antes de pedir qual editar
    visualizar_treinos()

    nome = input("\nDigite o nome do treino que deseja editar: ").strip()

    if nome not in nomes_dos_treinos:
        print("Erro: treino não encontrado.")
        return

    # Pega a referência ao dicionário do treino encontrado
    # Qualquer alteração em 'dados' altera diretamente nomes_dos_treinos[nome]
    dados = nomes_dos_treinos[nome]
    print("\nDeixe em branco para manter o valor atual.")

    # --- Editar tipo ---
    print(f"Tipos disponíveis: {', '.join(TIPOS_TREINO)}")

    # O valor atual aparece entre colchetes como dica pro usuário
    novo_tipo = input(f"Tipo [{dados['tipo']}]: ").strip().lower()

    # Só atualiza se o usuário digitou algo (não deixou em branco)
    if novo_tipo:
        if novo_tipo not in TIPOS_TREINO:
            print(f"Tipo inválido. Mantendo '{dados['tipo']}'.")
        else:
            dados["tipo"] = novo_tipo

    # --- Editar data ---
    nova_data = input(f"Data [{dados['data']}]: ").strip()
    if nova_data:
        try:
            datetime.strptime(nova_data, "%d/%m/%Y")
            dados["data"] = nova_data
        except ValueError:
            print("Data inválida. Mantendo a data atual.")

    # --- Editar duração ---
    nova_duracao = input(f"Duração em minutos [{dados['duracao']}]: ").strip()
    if nova_duracao:
        try:
            duracao_int = int(nova_duracao)
            if duracao_int <= 0:
                raise ValueError
            dados["duracao"] = str(duracao_int)
        except ValueError:
            print("Duração inválida. Mantendo a duração atual.")

    # --- Editar objetivo ---
    novo_objetivo = input(f"Objetivo [{dados['objetivo']}]: ").strip()
    if novo_objetivo:
        dados["objetivo"] = novo_objetivo

    salvar_treinos()
    print("\nTreino atualizado com sucesso!")


def excluir_treino():
    """Remove um treino (e seus exercícios) ou um exercício específico."""
    print("\n--- Excluir ---")

    opcao = input("Deseja excluir um treino ou um exercício? ").strip().lower()

    if opcao == "treino":
        visualizar_treinos()
        nome = input("\nDigite o nome do treino que deseja excluir: ").strip()

        if nome not in nomes_dos_treinos:
            print("Erro: treino não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir '{nome}'? (sim/não): ").strip().lower()
        if confirmacao != "sim":
            print("Exclusão cancelada.")
            return

        # 'del' remove a chave e o valor do dicionário
        del nomes_dos_treinos[nome]

        # Guarda a quantidade de exercícios antes de filtrar
        exercicios_antes = len(exercicios)

        # exercicios[:] = [...] substitui o conteúdo da lista sem criar uma nova variável
        # Isso é necessário pois a variável 'exercicios' é global
        # [e for e in exercicios if e["treino"] != nome] é uma list comprehension:
        # cria uma nova lista só com os exercícios que NÃO pertencem ao treino excluído
        exercicios[:] = [e for e in exercicios if e["treino"] != nome]

        # Calcula quantos exercícios foram removidos
        removidos = exercicios_antes - len(exercicios)

        salvar_treinos()
        salvar_exercicios()

        print(f"Treino '{nome}' excluído com sucesso.")
        if removidos > 0:
            print(f"{removidos} exercício(s) vinculado(s) também foram removidos.")

    elif opcao in ("exercicio", "exercício"):
        # Aceita com ou sem acento
        if not exercicios:
            print("Nenhum exercício cadastrado.")
            return

        listar_exercicios()

        try:
            numero = int(input("\nDigite o número do exercício que deseja excluir: "))

            # Verifica se o número está dentro do intervalo válido
            if numero < 1 or numero > len(exercicios):
                raise ValueError
        except ValueError:
            print("Número inválido.")
            return

        ex = exercicios[numero - 1]  # -1 pois listas começam no índice 0
        confirmacao = input(f"Tem certeza que deseja excluir '{ex['nome']}'? (sim/não): ").strip().lower()
        if confirmacao != "sim":
            print("Exclusão cancelada.")
            return

        # .pop(índice) remove o item na posição informada
        exercicios.pop(numero - 1)
        salvar_exercicios()
        print("Exercício excluído com sucesso!")

    else:
        print("Opção inválida. Digite 'treino' ou 'exercicio'.")


# =====================================================
# FUNÇÕES DE EXERCÍCIO
# =====================================================

def cadastrar_exercicio():
    """Cadastra um novo exercício e vincula a um treino existente."""
    print("\n--- Cadastrar Exercício ---")

    # Não faz sentido cadastrar exercício se não há treinos
    if not nomes_dos_treinos:
        print("Nenhum treino cadastrado. Cadastre um treino primeiro.")
        return

    # Lista os treinos disponíveis para o usuário escolher
    print("\nTreinos disponíveis:")
    for nome in nomes_dos_treinos:
        print(f"  - {nome}")

    treino_escolhido = input("\nDigite o nome do treino: ").strip()
    if treino_escolhido not in nomes_dos_treinos:
        print("Erro: treino não encontrado.")
        return

    nome = input("Nome do exercício: ").strip()
    if not nome:
        print("Erro: o nome não pode ser vazio.")
        return

    # Pergunta o modo antes de coletar os valores
    # Assim evitamos perguntar séries pra um exercício de corrida, por exemplo
    print("\nComo esse exercício é medido?")
    print("  1 - Séries e repetições (ex: 4x12)")
    print("  2 - Tempo (ex: 60 segundos de prancha)")
    print("  3 - Distância (ex: 1000 metros de corrida)")

    modo_opcao = input("Escolha (1/2/3): ").strip()

    # Valores padrão: campos que não forem usados ficam como "0"
    series = "0"
    repeticoes = "0"
    tempo = "0"
    distancia = "0"
    modo = ""

    if modo_opcao == "1":
        modo = "series"

        try:
            series = str(int(input("Quantidade de séries: ").strip()))
            if int(series) <= 0:
                raise ValueError
        except ValueError:
            print("Erro: número de séries inválido.")
            return

        try:
            repeticoes = str(int(input("Quantidade de repetições: ").strip()))
            if int(repeticoes) <= 0:
                raise ValueError
        except ValueError:
            print("Erro: número de repetições inválido.")
            return

    elif modo_opcao == "2":
        modo = "tempo"

        try:
            tempo = str(int(input("Tempo em segundos: ").strip()))
            if int(tempo) <= 0:
                raise ValueError
        except ValueError:
            print("Erro: tempo inválido.")
            return

    elif modo_opcao == "3":
        modo = "distancia"

        try:
            distancia = str(int(input("Distância em metros: ").strip()))
            if int(distancia) <= 0:
                raise ValueError
        except ValueError:
            print("Erro: distância inválida.")
            return

    else:
        print("Opção inválida.")
        return

    # Monta o dicionário do exercício e adiciona na lista
    exercicios.append({
        "nome":       nome,
        "treino":     treino_escolhido,
        "modo":       modo,
        "series":     series,
        "repeticoes": repeticoes,
        "tempo":      tempo,
        "distancia":  distancia
    })

    salvar_exercicios()
    print(f"\nExercício '{nome}' cadastrado com sucesso!")


def listar_exercicios():
    """Exibe todos os exercícios cadastrados."""
    print("\n--- Exercícios Cadastrados ---")

    if not exercicios:
        print("Nenhum exercício cadastrado.")
        return

    # enumerate(exercicios, start=1) percorre a lista e retorna
    # o índice e o item ao mesmo tempo, começando do número 1
    # Sem o start=1, começaria do 0
    for i, ex in enumerate(exercicios, start=1):
        print(f"\n--- EXERCÍCIO {i} ---")
        print(f"Nome:   {ex['nome']}")
        print(f"Treino: {ex['treino']}")

        # Exibe os dados de forma diferente dependendo do modo
        if ex["modo"] == "series":
            print(f"Modo:   {ex['series']} séries x {ex['repeticoes']} repetições")
        elif ex["modo"] == "tempo":
            print(f"Modo:   {ex['tempo']} segundos")
        elif ex["modo"] == "distancia":
            print(f"Modo:   {ex['distancia']} metros")

    print(f"\nTotal: {len(exercicios)} exercício(s)")


def editar_exercicio():
    """Edita um exercício existente pelo número exibido na listagem."""
    print("\n--- Editar Exercício ---")

    if not exercicios:
        print("Nenhum exercício cadastrado ainda.")
        return

    listar_exercicios()

    try:
        numero = int(input("\nDigite o número do exercício que deseja editar: "))
        if numero < 1 or numero > len(exercicios):
            raise ValueError
    except ValueError:
        print("Número inválido.")
        return

    # Acessa o exercício na posição correta
    # numero - 1 porque a lista começa no índice 0, mas mostramos ao usuário começando do 1
    ex = exercicios[numero - 1]
    print("\nDeixe em branco para manter o valor atual.")

    novo_nome = input(f"Nome [{ex['nome']}]: ").strip()
    if novo_nome:
        ex["nome"] = novo_nome

    # Edita apenas os campos do modo atual do exercício
    if ex["modo"] == "series":
        nova_series = input(f"Séries [{ex['series']}]: ").strip()
        if nova_series:
            try:
                ex["series"] = str(int(nova_series))
            except ValueError:
                print("Valor inválido. Mantendo o atual.")

        nova_rep = input(f"Repetições [{ex['repeticoes']}]: ").strip()
        if nova_rep:
            try:
                ex["repeticoes"] = str(int(nova_rep))
            except ValueError:
                print("Valor inválido. Mantendo o atual.")

    elif ex["modo"] == "tempo":
        novo_tempo = input(f"Tempo em segundos [{ex['tempo']}]: ").strip()
        if novo_tempo:
            try:
                ex["tempo"] = str(int(novo_tempo))
            except ValueError:
                print("Valor inválido. Mantendo o atual.")

    elif ex["modo"] == "distancia":
        nova_dist = input(f"Distância em metros [{ex['distancia']}]: ").strip()
        if nova_dist:
            try:
                ex["distancia"] = str(int(nova_dist))
            except ValueError:
                print("Valor inválido. Mantendo o atual.")

    salvar_exercicios()
    print("\nExercício atualizado com sucesso!")


# =====================================================
# MENUS
# Cada menu fica num loop próprio (while True)
# O 'break' sai do loop quando o usuário escolhe voltar (opção 0)
# =====================================================

def menu_treinos():
    """Submenu de gerenciamento de treinos."""

    # Loop que mantém o menu aberto até o usuário escolher voltar
    while True:
        print("\n===== TREINOS =====")
        print("1 - Adicionar treino")
        print("2 - Visualizar treinos")
        print("3 - Editar treino")
        print("4 - Excluir treino ou exercício")
        print("0 - Voltar")

        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            # Se o usuário digitar letra em vez de número, avisa e volta pro topo do loop
            print("Opção inválida. Digite um número.")
            continue  # 'continue' pula o resto do loop e volta pro 'while True'

        if opcao == 1:
            adicionar_treino()
        elif opcao == 2:
            visualizar_treinos()
        elif opcao == 3:
            editar_treino()
        elif opcao == 4:
            excluir_treino()
        elif opcao == 0:
            break  # 'break' sai do while True e volta pro menu principal
        else:
            print("Opção inválida.")


def menu_exercicios():
    """Submenu de gerenciamento de exercícios."""
    while True:
        print("\n===== EXERCÍCIOS =====")
        print("1 - Cadastrar exercício")
        print("2 - Listar exercícios")
        print("3 - Editar exercício")
        print("0 - Voltar")

        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            print("Opção inválida. Digite um número.")
            continue

        if opcao == 1:
            cadastrar_exercicio()
        elif opcao == 2:
            listar_exercicios()
        elif opcao == 3:
            editar_exercicio()
        elif opcao == 0:
            break
        else:
            print("Opção inválida.")


def menu_principal():
    """Menu principal: ponto de entrada da navegação do programa."""
    while True:
        print("\n" + "=" * 40)
        print("        BEM-VINDO AO FITPLANNER")
        print("=" * 40)
        print("1 - Gerenciar Treinos")
        print("2 - Gerenciar Exercícios")
        print("0 - Sair")

        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            print("Opção inválida. Digite um número.")
            continue

        if opcao == 1:
            menu_treinos()      # Entra no submenu de treinos
        elif opcao == 2:
            menu_exercicios()   # Entra no submenu de exercícios
        elif opcao == 0:
            print("\nAté logo!")
            break               # Sai do programa
        else:
            print("Opção inválida.")


# =====================================================
# INÍCIO DO PROGRAMA
# =====================================================

# Carrega os dados salvos dos arquivos .txt antes de mostrar qualquer menu
# Assim o usuário vê os treinos e exercícios da sessão anterior
carregar_treinos()
carregar_exercicios()

# Chama o menu principal, que inicia todo o fluxo do programa
menu_principal()