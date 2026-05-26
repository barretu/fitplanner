# 🏋️ FitPlanner

Sistema de gerenciamento de rotina fitness via terminal. Permite cadastrar treinos, registrar exercícios e manter um histórico salvo em arquivo local.

---

## 📋 Funcionalidades

- Adicionar, visualizar, editar e excluir treinos
- Cadastrar exercícios vinculados a cada treino
- Suporte a três modos de medição: séries/repetições, tempo e distância
- Dados salvos automaticamente em arquivos `.txt`
- Ao excluir um treino, todos os exercícios vinculados são removidos junto

---

## 🚀 Como rodar o projeto

**Pré-requisitos:** Python 3 instalado.

```bash
python fitplanner.py
```

Não é necessário instalar nenhuma biblioteca externa.

---

## 🗂️ Estrutura do projeto

```
fitplanner/
├── fitplanner.py     # código principal
├── .gitignore        # ignora a pasta dados/
└── dados/            # criada automaticamente ao rodar
    ├── treinos.txt
    └── exercicios.txt
```

> A pasta `dados/` é gerada automaticamente pelo programa. Não precisa criar manualmente e não deve ser commitada.

---

## 📖 Como usar

### Menu principal

Ao rodar o programa, você verá:

```
========================================
        BEM-VINDO AO FITPLANNER
========================================
1 - Gerenciar Treinos
2 - Gerenciar Exercícios
0 - Sair
```

### Gerenciar Treinos

| Opção | Ação |
|-------|------|
| 1 | Adicionar treino |
| 2 | Visualizar todos os treinos |
| 3 | Editar um treino existente |
| 4 | Excluir treino ou exercício |
| 0 | Voltar ao menu principal |

Campos de um treino:
- **Nome** — identificador único do treino
- **Tipo** — deve ser um dos seguintes: `musculacao`, `cardio`, `funcional`, `corrida`
- **Data** — formato `DD/MM/AAAA`
- **Duração** — em minutos, número inteiro maior que zero
- **Objetivo** — descrição livre

### Gerenciar Exercícios

| Opção | Ação |
|-------|------|
| 1 | Cadastrar exercício |
| 2 | Listar todos os exercícios |
| 3 | Editar um exercício |
| 0 | Voltar ao menu principal |

Ao cadastrar um exercício, você escolhe o modo de medição:

| Modo | Campos |
|------|--------|
| Séries e repetições | Número de séries + repetições por série |
| Tempo | Duração em segundos |
| Distância | Distância em metros |

### Editar

Em qualquer tela de edição, deixar o campo em branco mantém o valor atual.

### Excluir

Toda exclusão pede confirmação (`sim/não`) antes de remover.  
Ao excluir um treino, todos os exercícios vinculados a ele são excluídos automaticamente.

---

## ⚠️ Restrições

- O tipo do treino deve ser exatamente um dos quatro aceitos: `musculacao`, `cardio`, `funcional`, `corrida`
- Datas devem estar no formato `DD/MM/AAAA`
- Duração e valores numéricos devem ser inteiros maiores que zero
- Não é possível ter dois treinos com o mesmo nome
- É necessário ter pelo menos um treino cadastrado para cadastrar exercícios

---

## 👥 Equipe
1° Período de Ciência da Computação CESAR School, turma B, 2026.1

Kauã Cardoso,
Letícia Almeida,
Letícia Dornas,
Maria Monalysa,
Maria Paula,
Thony Barreto.