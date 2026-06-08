# 🏋️ FitPlanner

Sistema de gerenciamento de rotina fitness. Disponível em duas versões: **terminal** e **web** (com front-end e back-end Flask).

---

## 📋 Funcionalidades

- Adicionar, visualizar, editar e excluir treinos
- Cadastrar exercícios vinculados a cada treino, com suporte a séries/repetições, tempo e distância
- Controle de metas com prazo e status
- Acompanhamento de evolução física (peso, altura, % de gordura, IMC)
- Sugestões personalizadas de exercícios, divisão semanal, descanso e alimentação por tipo de treino
- ⏱️ **Timer de intervalo** — cronômetro para descanso entre séries, com histórico dos tempos registrados
- ⚙️ **Configurações** — alternância entre tema escuro/claro e suporte a dois idiomas (PT/EN)
- Dados salvos automaticamente em arquivos `.txt`
- Ao excluir um treino, todos os exercícios vinculados são removidos automaticamente

---

## 🗂️ Estrutura do projeto

```
fitplanner/
├── fitplanner.py     # versão terminal
├── app.py            # back-end Flask (versão web)
├── index.html        # front-end (versão web)
├── README.md
├── .gitignore        # ignora a pasta dados/
└── dados/            # criada automaticamente ao rodar
    ├── treinos.txt
    ├── exercicios.txt
    ├── metas.txt
    └── evolucoes.txt
```

> A pasta `dados/` é gerada automaticamente pelo programa. Não precisa criar manualmente e não deve ser commitada.

---

## 🖥️ Versão Terminal

**Pré-requisitos:** Python 3 instalado. Sem bibliotecas externas.

```bash
python3 fitplanner.py
```

### Menu principal

```
--- FitPlanner ---
1 - Adicionar treino
2 - Visualizar treinos
3 - Editar treino
4 - Excluir treino
5 - Adicionar meta
6 - Visualizar metas
7 - Editar meta
8 - Excluir meta
9 - Vincular meta a treino
10 - Registrar evolução física
11 - Visualizar evoluções
12 - Parar
```

---

## 🌐 Versão Web (Flask)

**Pré-requisitos:** Python 3 e Flask instalados.

```bash
pip3 install flask
python3 app.py
```

Depois abra o navegador em:
```
http://127.0.0.1:5000
```

Deixe o terminal aberto enquanto estiver usando. Para parar o servidor: `CTRL+C`.

### Páginas disponíveis

| Página | Funcionalidade |
|--------|---------------|
| Treinos | Adicionar, visualizar e excluir treinos. Clique num treino para ver os exercícios vinculados |
| Exercícios | Listar e cadastrar exercícios por treino |
| Metas | Cadastrar e acompanhar metas com prazo e status |
| Evolução | Registrar peso, altura e % de gordura. IMC calculado automaticamente |
| Sugestões | Sugestões de exercícios, divisão semanal, descanso e alimentação por tipo de treino |
| ⏱️ Timer | Cronômetro de intervalo entre séries com histórico da sessão |
| ⚙️ Configurações | Tema claro/escuro e idioma da interface (Português / English) |

---

## 📖 Como usar — Treinos

Campos de um treino:
- **Nome** — identificador único
- **Tipo** — deve ser um dos seguintes: `musculacao`, `cardio`, `funcional`, `corrida`
- **Data** — formato `DD/MM/AAAA`
- **Duração** — em minutos, número inteiro maior que zero
- **Objetivo** — descrição livre

## 📖 Como usar — Exercícios

Ao cadastrar um exercício, escolha o modo de medição:

| Modo | Campos |
|------|--------|
| Séries e repetições | Número de séries + repetições por série |
| Tempo | Duração em segundos |
| Distância | Distância em metros |

## 📖 Como usar — Timer ⏱️

1. Acesse a página **Timer** no menu lateral
2. Configure o tempo de descanso desejado (ex: 60 segundos)
3. Clique em **Iniciar** ao começar o intervalo
4. O timer faz uma contagem regressiva e emite um alerta ao terminar
5. Cada intervalo é salvo automaticamente no histórico da sessão

---

## ⚠️ Restrições

- O tipo do treino deve ser exatamente um dos quatro aceitos: `musculacao`, `cardio`, `funcional`, `corrida`
- Datas devem estar no formato `DD/MM/AAAA`
- Duração e valores numéricos devem ser inteiros maiores que zero
- Não é possível ter dois treinos com o mesmo nome
- É necessário ter pelo menos um treino cadastrado para cadastrar exercícios
- O histórico do timer é da sessão atual — não é salvo ao fechar o navegador
- As preferências de **tema** e **idioma** são salvas automaticamente no navegador (`localStorage`) e persistem entre sessões

---

## 👥 Equipe

1° Período de Ciência da Computação CESAR School, turma B, 2026.1

Kauã Cardoso, Letícia Almeida, Letícia Dornas, Maria Monalysa, Maria Paula, Thony Barreto.