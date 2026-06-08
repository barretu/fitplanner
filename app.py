# Flask é a biblioteca que transforma esse arquivo Python num servidor web.
# Quando você roda "python3 app.py", ele fica escutando requisições do navegador.
#
# Importamos três coisas do Flask:
# - Flask: a classe que cria o servidor
# - request: objeto que contém tudo que o navegador mandou (dados, parâmetros, etc)
# - jsonify: converte dicionários Python em JSON para devolver ao navegador
from flask import Flask, request, jsonify, send_from_directory

# 'os' permite interagir com o sistema operacional — criar pastas, verificar arquivos, etc
import os

# 'random' é usado na rota de sugestões para sortear exercícios e dicas
# Importado aqui no topo, seguindo a convenção Python (PEP8: imports no início do arquivo)
import random

# Cria o servidor Flask e guarda na variável 'app'
# '__name__' é uma variável especial do Python que contém o nome do arquivo atual
# O Flask usa isso internamente — é só uma convenção obrigatória
app = Flask(__name__)


# Serve arquivos estáticos (style.css, script.js)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), filename)

# ──────────────────────────────────────────
# CAMINHOS DOS ARQUIVOS
#
# Constantes (maiúsculas por convenção) que guardam onde ficam os arquivos .txt
# Centralizar aqui facilita: se precisar mudar o nome de um arquivo,
# muda só nessa linha em vez de procurar em todo o código
# ──────────────────────────────────────────

ARQUIVO_TREINOS    = "dados/treinos.txt"
ARQUIVO_METAS      = "dados/metas.txt"
ARQUIVO_EXERCICIOS = "dados/exercicios.txt"
ARQUIVO_EVOLUCOES  = "dados/evolucoes.txt"


# ──────────────────────────────────────────
# FUNÇÕES DE ARQUIVO
#
# Essas funções são responsáveis por ler e escrever nos arquivos .txt
# São chamadas dentro das rotas toda vez que precisamos acessar os dados
#
# IMPORTANTE: no Flask, cada requisição lê os dados frescos do arquivo.
# Diferente do fitplanner.py que usa variáveis globais, aqui não guardamos
# nada em memória — isso evita conflito se duas pessoas usarem ao mesmo tempo
# ──────────────────────────────────────────

def garantir_pasta():
    """
    Cria a pasta 'dados/' se ela ainda não existir.
    É chamada antes de qualquer leitura ou escrita pra nunca
    dar erro de 'pasta não encontrada'.
    O exist_ok=True evita erro caso a pasta já exista.
    """
    os.makedirs("dados", exist_ok=True)


# ── TREINOS ──

def carregar_treinos():
    """
    Lê o arquivo treinos.txt e retorna uma lista de dicionários.
    Cada linha do arquivo vira um dicionário com os dados do treino.

    Exemplo de linha no arquivo:
        Treino A|musculacao|17/05/2025|60|Ganhar massa|

    Retorna:
        Lista de dicionários, ex:
        [{"nome": "Treino A", "tipo": "musculacao", ...}]
    """
    garantir_pasta()

    # Começa com lista vazia — se o arquivo não existir, retorna ela assim mesmo
    treinos = []

    # Se o arquivo ainda não existe (primeira vez rodando), retorna lista vazia
    if not os.path.exists(ARQUIVO_TREINOS):
        return treinos

    # Abre o arquivo em modo leitura ("r") com suporte a acentos (utf-8)
    with open(ARQUIVO_TREINOS, "r", encoding="utf-8") as f:

        # Percorre o arquivo linha por linha
        for linha in f:

            # .strip() remove espaços e o \n (quebra de linha) do início e fim
            # .split("|") divide a linha pelo separador "|" e retorna uma lista
            # Exemplo: "Treino A|musculacao|17/05/2025|60|Ganhar massa|"
            # Vira:    ["Treino A", "musculacao", "17/05/2025", "60", "Ganhar massa", ""]
            dados = linha.strip().split("|")

            # Só processa a linha se tiver pelo menos 5 campos (evita linhas corrompidas)
            if len(dados) >= 5:
                treino = {
                    "nome":     dados[0],
                    "tipo":     dados[1],
                    "data":     dados[2],
                    "duracao":  dados[3],
                    "objetivo": dados[4],
                    # O campo 'meta' é opcional — se não existir, retorna string vazia
                    "meta":     dados[5] if len(dados) > 5 else ""
                }
                treinos.append(treino)

    return treinos


def salvar_treinos(treinos):
    """
    Recebe a lista de treinos e salva tudo no arquivo treinos.txt.
    Sobrescreve o arquivo inteiro a cada salvamento.

    Parâmetros:
        treinos: lista de dicionários com os treinos
    """
    garantir_pasta()

    # Abre em modo escrita ("w") — apaga o conteúdo anterior e escreve do zero
    with open(ARQUIVO_TREINOS, "w", encoding="utf-8") as f:
        for t in treinos:

            # .get("campo", "") é uma forma segura de acessar uma chave do dicionário
            # Se a chave não existir, retorna "" em vez de dar erro
            # "|".join([...]) junta todos os campos numa string separada por "|"
            linha = "|".join([
                t.get("nome", ""),
                t.get("tipo", ""),
                t.get("data", ""),
                t.get("duracao", ""),
                t.get("objetivo", ""),
                t.get("meta", "")
            ])

            # Escreve a linha e pula para a próxima com \n
            f.write(linha + "\n")


# ── EXERCÍCIOS ──

def carregar_exercicios():
    """
    Lê o arquivo exercicios.txt e retorna uma lista de dicionários.

    Exemplo de linha no arquivo:
        Agachamento|Treino A|series|4|12|0|0
    """
    garantir_pasta()
    exercicios = []

    if not os.path.exists(ARQUIVO_EXERCICIOS):
        return exercicios

    with open(ARQUIVO_EXERCICIOS, "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split("|")

            # Exercício tem 7 campos: nome, treino, modo, series, repeticoes, tempo, distancia
            if len(dados) >= 7:
                exercicios.append({
                    "nome":       dados[0],
                    "treino":     dados[1],  # nome do treino ao qual pertence
                    "modo":       dados[2],  # "series", "tempo" ou "distancia"
                    "series":     dados[3],
                    "repeticoes": dados[4],
                    "tempo":      dados[5],
                    "distancia":  dados[6]
                })

    return exercicios


def salvar_exercicios(exercicios):
    """Salva a lista de exercícios no arquivo exercicios.txt."""
    garantir_pasta()

    with open(ARQUIVO_EXERCICIOS, "w", encoding="utf-8") as f:
        for e in exercicios:
            linha = "|".join([
                e.get("nome", ""),
                e.get("treino", ""),
                e.get("modo", ""),
                # str() converte números pra string, pois o join exige que tudo seja texto
                str(e.get("series", 0)),
                str(e.get("repeticoes", 0)),
                str(e.get("tempo", 0)),
                str(e.get("distancia", 0))
            ])
            f.write(linha + "\n")


# ── METAS ──

def carregar_metas():
    """
    Lê o arquivo metas.txt e retorna uma lista de dicionários.

    Exemplo de linha no arquivo:
        Perder 5kg|31/12/2025|Em andamento
    """
    garantir_pasta()
    metas = []

    if not os.path.exists(ARQUIVO_METAS):
        return metas

    with open(ARQUIVO_METAS, "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split("|")

            if len(dados) >= 3:
                metas.append({
                    "descricao": dados[0],
                    "prazo":     dados[1],
                    "status":    dados[2]
                })

    return metas


def salvar_metas(metas):
    """Salva a lista de metas no arquivo metas.txt."""
    garantir_pasta()

    with open(ARQUIVO_METAS, "w", encoding="utf-8") as f:
        for m in metas:
            linha = "|".join([
                m.get("descricao", ""),
                m.get("prazo", ""),
                m.get("status", "Em andamento")
            ])
            f.write(linha + "\n")


# ── EVOLUÇÕES ──

def carregar_evolucoes():
    """
    Lê o arquivo evolucoes.txt e retorna uma lista de dicionários.

    Exemplo de linha no arquivo:
        17/05/2025|75.5|1.75|18.5
    """
    garantir_pasta()
    evolucoes = []

    if not os.path.exists(ARQUIVO_EVOLUCOES):
        return evolucoes

    with open(ARQUIVO_EVOLUCOES, "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split("|")

            if len(dados) >= 4:
                evolucoes.append({
                    "data":    dados[0],
                    "peso":    dados[1],
                    "altura":  dados[2],
                    "gordura": dados[3]
                })

    return evolucoes


def salvar_evolucoes(evolucoes):
    """Salva a lista de evoluções no arquivo evolucoes.txt."""
    garantir_pasta()

    with open(ARQUIVO_EVOLUCOES, "w", encoding="utf-8") as f:
        for e in evolucoes:
            linha = "|".join([
                e.get("data", ""),
                str(e.get("peso", 0)),
                str(e.get("altura", 0)),
                str(e.get("gordura", 0))
            ])
            f.write(linha + "\n")


# ──────────────────────────────────────────
# ROTAS
#
# Rota é um endereço que o Flask "escuta".
# Quando o navegador acessa aquele endereço com o método correto,
# o Flask chama a função correspondente.
#
# O @app.route(...) é um decorator — ele registra a função como
# responsável por um endereço + método específico.
#
# Métodos HTTP:
#   GET    → buscar dados (o navegador quer receber algo)
#   POST   → enviar dados (o navegador quer salvar algo)
#   PUT    → atualizar dados (o navegador quer editar algo)
#   DELETE → deletar dados (o navegador quer remover algo)
# ──────────────────────────────────────────


# ── ROTAS DE TREINOS ──

# Rota: GET /treinos
# Chamada quando o front quer listar todos os treinos
# O front chama: fetch('/treinos') → Flask responde com a lista em JSON
@app.route("/treinos", methods=["GET"])
def get_treinos():
    # Lê os treinos do arquivo e converte para JSON automaticamente com jsonify()
    return jsonify(carregar_treinos())


# Rota: POST /treinos
# Chamada quando o usuário preenche o formulário e clica em "Salvar treino"
# O front manda: fetch('/treinos', { method: 'POST', body: JSON.stringify({nome, tipo, ...}) })
@app.route("/treinos", methods=["POST"])
def add_treino():
    # request.json lê o dicionário JSON que o navegador mandou no corpo da requisição
    # É o equivalente ao que o usuário preencheu no formulário
    dados = request.json

    # Valida que o campo 'nome' foi preenchido antes de salvar
    # .get("nome") retorna None se a chave não existir — e None é considerado falso pelo Python
    if not dados.get("nome"):
        # Retorna erro com código 400 (Bad Request = o cliente mandou algo inválido)
        return jsonify({"erro": "Nome obrigatório"}), 400

    # Carrega os treinos existentes, adiciona o novo e salva tudo
    treinos = carregar_treinos()
    treinos.append({
        "nome":     dados.get("nome", ""),
        "tipo":     dados.get("tipo", ""),
        "data":     dados.get("data", ""),
        "duracao":  str(dados.get("duracao", "")),  # str() pois salvamos tudo como texto
        "objetivo": dados.get("objetivo", ""),
        "meta":     dados.get("meta", "")
    })
    salvar_treinos(treinos)

    # Retorna sucesso com código 201 (Created = recurso criado com sucesso)
    return jsonify({"ok": True}), 201


# Rota: PUT /treinos/<nome>
# Chamada quando o usuário edita um treino existente
# O <nome> entre <> é um parâmetro dinâmico — captura o que vier na URL
# Exemplo: PUT /treinos/Treino A → a variável 'nome' recebe "Treino A"
@app.route("/treinos/<nome>", methods=["PUT"])
def edit_treino(nome):
    dados = request.json
    treinos = carregar_treinos()

    # Percorre a lista procurando o treino com o nome informado na URL
    for t in treinos:
        if t["nome"] == nome:
            # Atualiza apenas os campos que foram enviados
            # Se o campo não foi enviado, mantém o valor atual com .get("campo", valor_atual)
            t["tipo"]     = dados.get("tipo",     t["tipo"])
            t["data"]     = dados.get("data",     t["data"])
            t["duracao"]  = str(dados.get("duracao", t["duracao"]))
            t["objetivo"] = dados.get("objetivo", t["objetivo"])
            t["meta"]     = dados.get("meta",     t["meta"])
            salvar_treinos(treinos)
            return jsonify({"ok": True})

    # Se chegou aqui, o treino não foi encontrado
    # Código 404 = Not Found (recurso não encontrado)
    return jsonify({"erro": "Treino não encontrado"}), 404


# Rota: DELETE /treinos/<nome>
# Chamada quando o usuário confirma a exclusão de um treino
@app.route("/treinos/<nome>", methods=["DELETE"])
def delete_treino(nome):
    treinos = carregar_treinos()

    # List comprehension: cria uma nova lista SEM o treino com o nome informado
    # É o equivalente a um filtro — mantém tudo exceto o que queremos deletar
    novos = [t for t in treinos if t["nome"] != nome]

    # Se o tamanho não mudou, o treino não existia
    if len(novos) == len(treinos):
        return jsonify({"erro": "Treino não encontrado"}), 404

    salvar_treinos(novos)

    # Remove também todos os exercícios vinculados a esse treino
    # Mesma lógica: filtra mantendo apenas exercícios de outros treinos
    exercicios = carregar_exercicios()
    salvar_exercicios([e for e in exercicios if e["treino"] != nome])

    return jsonify({"ok": True})


# ── ROTAS DE EXERCÍCIOS ──

# Rota: GET /exercicios
# Aceita um parâmetro opcional na URL: ?treino=NomeDoTreino
# Exemplo sem filtro:  GET /exercicios          → retorna todos
# Exemplo com filtro:  GET /exercicios?treino=Treino A → retorna só os do Treino A
@app.route("/exercicios", methods=["GET"])
def get_exercicios():
    # request.args lê parâmetros que vêm depois do ? na URL
    # request.args.get("treino") retorna None se o parâmetro não foi passado
    treino = request.args.get("treino")

    exercicios = carregar_exercicios()

    # Se um treino foi especificado, filtra a lista
    if treino:
        exercicios = [e for e in exercicios if e["treino"] == treino]

    return jsonify(exercicios)


# Rota: POST /exercicios
# Chamada quando o usuário adiciona um exercício pelo formulário
@app.route("/exercicios", methods=["POST"])
def add_exercicio():
    dados = request.json

    if not dados.get("nome"):
        return jsonify({"erro": "Nome obrigatório"}), 400

    exercicios = carregar_exercicios()
    exercicios.append({
        "nome":       dados.get("nome", ""),
        "treino":     dados.get("treino", ""),
        "modo":       dados.get("modo", "series"),
        "series":     str(dados.get("series", 0)),
        "repeticoes": str(dados.get("repeticoes", 0)),
        "tempo":      str(dados.get("tempo", 0)),
        "distancia":  str(dados.get("distancia", 0))
    })
    salvar_exercicios(exercicios)

    return jsonify({"ok": True}), 201


# Rota: DELETE /exercicios/<index>
# Deleta um exercício pela posição na lista
# O int: antes de index faz o Flask converter o valor da URL para inteiro automaticamente
# Exemplo: DELETE /exercicios/2 → deleta o exercício na posição 2
@app.route("/exercicios/<int:index>", methods=["DELETE"])
def delete_exercicio(index):
    exercicios = carregar_exercicios()

    # Verifica se o índice está dentro do intervalo válido da lista
    if index < 0 or index >= len(exercicios):
        return jsonify({"erro": "Exercício não encontrado"}), 404

    # .pop(index) remove e retorna o item na posição indicada
    exercicios.pop(index)
    salvar_exercicios(exercicios)

    return jsonify({"ok": True})


# ── ROTAS DE METAS ──

# Rota: GET /metas — retorna todas as metas
@app.route("/metas", methods=["GET"])
def get_metas():
    return jsonify(carregar_metas())


# Rota: POST /metas — adiciona uma nova meta
@app.route("/metas", methods=["POST"])
def add_meta():
    dados = request.json

    if not dados.get("descricao"):
        return jsonify({"erro": "Descrição obrigatória"}), 400

    metas = carregar_metas()
    metas.append({
        "descricao": dados.get("descricao", ""),
        "prazo":     dados.get("prazo", ""),
        "status":    dados.get("status", "Em andamento")
    })
    salvar_metas(metas)

    return jsonify({"ok": True}), 201


# Rota: PUT /metas/<index> — edita uma meta pela posição na lista
@app.route("/metas/<int:index>", methods=["PUT"])
def edit_meta(index):
    dados = request.json
    metas = carregar_metas()

    if index < 0 or index >= len(metas):
        return jsonify({"erro": "Meta não encontrada"}), 404

    # Atualiza cada campo, mantendo o valor atual se o campo não foi enviado
    metas[index]["descricao"] = dados.get("descricao", metas[index]["descricao"])
    metas[index]["prazo"]     = dados.get("prazo",     metas[index]["prazo"])
    metas[index]["status"]    = dados.get("status",    metas[index]["status"])

    salvar_metas(metas)

    return jsonify({"ok": True})


# Rota: DELETE /metas/<index> — remove uma meta pela posição
@app.route("/metas/<int:index>", methods=["DELETE"])
def delete_meta(index):
    metas = carregar_metas()

    if index < 0 or index >= len(metas):
        return jsonify({"erro": "Meta não encontrada"}), 404

    metas.pop(index)
    salvar_metas(metas)

    return jsonify({"ok": True})


# ── ROTAS DE EVOLUÇÕES ──

# Rota: GET /evolucoes — retorna todo o histórico de evolução
@app.route("/evolucoes", methods=["GET"])
def get_evolucoes():
    return jsonify(carregar_evolucoes())


# Rota: POST /evolucoes — registra uma nova medição
@app.route("/evolucoes", methods=["POST"])
def add_evolucao():
    dados = request.json
    evolucoes = carregar_evolucoes()
    evolucoes.append({
        "data":    dados.get("data", ""),
        "peso":    str(dados.get("peso", 0)),
        "altura":  str(dados.get("altura", 0)),
        "gordura": str(dados.get("gordura", 0))
    })
    salvar_evolucoes(evolucoes)

    return jsonify({"ok": True}), 201


# Rota: DELETE /evolucoes/<index> — remove um registro pelo índice
@app.route("/evolucoes/<int:index>", methods=["DELETE"])
def delete_evolucao(index):
    evolucoes = carregar_evolucoes()

    if index < 0 or index >= len(evolucoes):
        return jsonify({"erro": "Registro não encontrado"}), 404

    evolucoes.pop(index)
    salvar_evolucoes(evolucoes)

    return jsonify({"ok": True})


# ── ROTAS DE SUGESTÕES ──

# Dicionário fixo com sugestões por tipo de treino
# Não salva em arquivo pois são dados estáticos que não mudam
SUGESTOES = {
    "musculacao": {
        "exercicios":  ["Agachamento", "Supino reto", "Levantamento terra", "Rosca direta",
                        "Tríceps corda", "Leg press", "Remada curvada", "Desenvolvimento com halteres"],
        "divisao":     "Sugestão de divisão: Segunda (peito/tríceps), Quarta (costas/bíceps), Sexta (pernas/ombros)",
        "descanso":    "Descanse 60 a 90 segundos entre séries. Durma pelo menos 8 horas para recuperação muscular.",
        "alimentacao": "Priorize proteínas (frango, ovo, atum). Consuma carboidratos antes do treino e proteína depois."
    },
    "cardio": {
        "exercicios":  ["Corrida leve 20min", "Bicicleta ergométrica", "Pular corda", "Jumping jack",
                        "Polichinelo", "Elíptico", "Natação", "Caminhada rápida"],
        "divisao":     "Sugestão de divisão: 3 a 5 vezes por semana, alternando intensidade (leve/moderado/intenso)",
        "descanso":    "Descanse 30 a 60 segundos entre exercícios. Um dia de descanso completo por semana é essencial.",
        "alimentacao": "Hidrate-se bem antes, durante e após o treino. Evite refeições pesadas 1h antes de treinar."
    },
    "funcional": {
        "exercicios":  ["Burpee", "Prancha", "Mountain climber", "Agachamento com salto",
                        "Flexão", "Abdominal bicicleta", "Superman", "Corrida estacionária"],
        "divisao":     "Sugestão de divisão: 3 vezes por semana com pelo menos 1 dia de descanso entre sessões",
        "descanso":    "Descanse 45 segundos entre circuitos. O funcional exige bastante do sistema nervoso central.",
        "alimentacao": "Consuma carboidratos de qualidade (aveia, batata-doce) para ter energia nos circuitos."
    },
    "corrida": {
        "exercicios":  ["Corrida leve 3km", "Tiro de 100m", "Corrida em subida", "Fartlek 5km",
                        "Corrida com variação de ritmo", "Caminhada ativa", "Corrida 10km leve"],
        "divisao":     "Sugestão de divisão: 3 corridas por semana (leve, moderada e longa), com 1 dia de descanso entre cada",
        "descanso":    "Após corridas longas, descanse 48h antes de treinar novamente. Alongue sempre após o treino.",
        "alimentacao": "Carboidratos são combustível para corrida. Consuma banana ou gel energético antes de treinos longos."
    }
}

# Lista de dicas gerais que aparecem aleatoriamente
DICAS_GERAIS = [
    "Beba pelo menos 2 litros de água por dia.",
    "Durma entre 7 e 9 horas para recuperação.",
    "Não pule o aquecimento — 5 minutos já fazem diferença.",
    "Anote seus treinos para acompanhar a evolução.",
    "Respeite os dias de descanso, eles fazem parte do treino.",
    "Prefira alimentos naturais a ultraprocessados.",
    "Consistência é mais importante que intensidade.",
    "Consulte um profissional de educação física para um treino personalizado."
]


# Rota: GET /sugestoes?tipo=musculacao
# Retorna sugestões aleatórias baseadas no tipo de treino passado na URL
@app.route("/sugestoes", methods=["GET"])
def get_sugestoes():
    # Lê o parâmetro ?tipo= da URL. Se não passar, usa "musculacao" como padrão
    tipo = request.args.get("tipo", "musculacao")

    # Busca as sugestões do tipo solicitado
    # Se o tipo não existir no dicionário, cai no padrão musculacao
    sugestao = SUGESTOES.get(tipo, SUGESTOES["musculacao"])

    return jsonify({
        "tipo": tipo,
        # random.sample(lista, n) sorteia n itens sem repetição
        # min(4, len(...)) garante que não tente sortear mais itens do que existem
        "exercicios":  random.sample(sugestao["exercicios"], min(4, len(sugestao["exercicios"]))),
        "divisao":     sugestao["divisao"],
        "descanso":    sugestao["descanso"],
        "alimentacao": sugestao["alimentacao"],
        # random.choice(lista) sorteia um único item aleatório
        "dica_geral":  random.choice(DICAS_GERAIS)
    })


# ──────────────────────────────────────────
# SERVIR O FRONT-END
#
# Quando você acessa http://127.0.0.1:5000 sem nenhum caminho,
# o Flask cai nessa rota e serve o index.html direto pro navegador
# ──────────────────────────────────────────

@app.route("/")
def index():
    # send_from_directory serve o arquivo a partir do diretório do projeto.
    # É a forma correta no Flask: funciona independente de onde o servidor foi iniciado,
    # define o Content-Type correto e lida com cache do navegador adequadamente.
    # os.path.dirname(os.path.abspath(__file__)) retorna a pasta onde app.py está.
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")


# ──────────────────────────────────────────
# INICIAR O SERVIDOR
# ──────────────────────────────────────────

# 'if __name__ == "__main__"' garante que o servidor só sobe quando você
# roda o arquivo diretamente com "python3 app.py"
# Se outro arquivo importar app.py, essa parte não executa
if __name__ == "__main__":
    # debug=True faz o servidor reiniciar sozinho toda vez que você salva o arquivo
    # Muito útil durante o desenvolvimento — em produção tiraria o debug=True
    app.run(debug=True, port=5001)