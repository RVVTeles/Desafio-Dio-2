import textwrap


def menu():
    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [n] Nova conta
    [l] Listar contas
    [u] Novo usuário
    [q] Sair
    => """

    return input(textwrap.dedent(menu))

def deposito(saldo, extrato, valor, /): 

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Operação feita com sucesso! Saldo atual: R${saldo:.2f}\n")    
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def saque(*, saldo, limite, extrato, numero_saques, LIMITE_SAQUES, valor):

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print(f"Operação falhou! Você não tem saldo suficiente. Seu saldo atual é de R${saldo:.2f}")
    
    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite de R${limite:.2f}.")
    
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R${valor:.2f}\n"
        numero_saques += 1
        print(f"Operação feita com sucesso! Saldo atual: R${saldo:.2f}\n")

    else:
        print("Operação falhou! O valor informado é inválido")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n===================== EXTRATO =====================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R${saldo:.2f}.")
    print("===================================================")

def criar_conta(agencia, numero_conta,usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuário não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência: {conta["agencia"]}
            Número da conta: {conta["numero_conta"]}
            Titular: {conta["usuario"]["nome"]}
        """
        print ("=" * 100)
        print(textwrap.dedent(linha))

def novo_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (lougadouro, número - bairro - cidade/Sigla estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None



def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:

        opcao = menu()
        
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(saldo, extrato, valor)
            
        elif opcao == "s":
            print(f"Saldo disponível: R${saldo:.2f}\n")
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = saque(saldo=saldo, limite=limite, extrato=extrato, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES, valor=valor) 

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "n":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "l":
            print(listar_contas(contas))

        elif opcao == "u":
            novo_usuario(usuarios)
            
        elif opcao == "q":
            print("")
            break
            
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()