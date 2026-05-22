metas = []

def adicionar_meta(descricao, categoria):
    nova_meta = {
        "descricao": descricao,
        "categoria": categoria,
        "status": "Pendente"
    }
    metas.append(nova_meta)
    print(f"\nMeta '{descricao}' registrada com sucesso!")

def listar_metas():
    if not metas:
        print("\nNenhuma meta registrada no momento.")
        return

    print("\n--- Suas Metas ---")
    for i in range(len(metas)):
        meta = metas[i]
        print(f"{i}. [{meta['status']}] {meta['descricao']} (Categoria: {meta['categoria']})")

def atualizar_status(indice, novo_status):
    if 0 <= indice < len(metas):
        metas[indice]["status"] = novo_status
        print("\nStatus da meta atualizado com sucesso!")
    else:
        print("\nÍndice de meta inválido.")

def menu():
    while True:
        print("\n--- Controle de Metas ---")
        print("1. Registrar nova meta")
        print("2. Listar metas")
        print("3. Atualizar status de uma meta")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            desc = input("Descrição da meta (ex: Chegar aos 70kg): ")
            cat = input("Categoria (ex: Perder peso, Ganhar massa, Condicionamento): ")
            adicionar_meta(desc, cat)
        
        elif opcao == '2':
            listar_metas()
            
        elif opcao == '3':
            listar_metas()
            if metas:
                try:
                    ind = int(input("Digite o número da meta que deseja atualizar: "))
                    status = input("Novo status (ex: Concluída, Em andamento): ")
                    atualizar_status(ind, status)
                except ValueError:
                    print("\nPor favor, digite um número válido.")
                    
        elif opcao == '4':
            print("\nSaindo do controle de metas...")
            break
            
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
