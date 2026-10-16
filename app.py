# =====================================================================================
# Variáveis Globais - Usadas em várias partes do programa
# =====================================================================================

continuar1 = "s"         # Variável de controle para o loop principal do programa. Enquanto for "s", o programa continua rodando.
cod = 0                  # Variável para armazenar temporariamente um código de produto. Inicializada com 0.
cod_ind = []             # Lista para armazenar apenas os códigos dos produtos, usada para validar a escolha do usuário ao alterar/excluir.
lista_prod = []          # Lista principal que armazena os dados do cardápio lidos do arquivo (cada item é uma lista: [código, descrição, valor]).
lista_pedido = []        # Lista para armazenar um pedido. 
temp = []                # Lista temporária usada na função `codBruto` para manipular os códigos lidos do arquivo.
temp_cod = []            # Lista temporária usada na função `codBruto` para armazenar códigos faltantes na sequência.

# =====================================================================================
# Funções - Blocos de código reutilizáveis
# =====================================================================================
def comeco():# Função INICIAL: Mostra o primeiro menu para escolher o tipo de usuário.
    print("1 - Administrador")      # Exibe a opção para entrar como Administrador.
    print("2 - Operador")           # Exibe a opção para entrar como Operador.
    print("0 - Sair")               # Exibe a opção para fechar o programa.
    entrada = input("Escolha uma Opção:\n ") # Pede ao usuário para digitar sua escolha e armazena na variável 'entrada'.

    # Loop de validação: continua pedindo uma opção até que o usuário digite "1", "2" ou "0".
    while entrada != "1" and entrada != "2" and entrada != "0":
        print("Opção inválida! Tente novamente.") # Informa ao usuário que a opção digitada não é válida.
        entrada = input("Escolha uma Opção:\n ") # Pede a entrada novamente.

    if entrada == "1":
        # 'a+' abre o arquivo para adicionar ('append') e ler ('+'). Se o arquivo não existir, ele é criado.
        arquivo = open('cardapio.txt', 'a+', encoding='UTF-8') # Garante que o arquivo do cardápio exista.
        arquivo.close()             # Fecha o arquivo imediatamente, pois a intenção era apenas garantir sua existência.
        print("ENTROU COMO: 'ADM'") # Confirma que o usuário entrou no modo Administrador.
    elif entrada == "2":
        print("ENTROU COMO: 'Operador'") # Confirma que o usuário entrou no modo Operador.
    elif entrada == "0":
        print("Saiu")               # Informa que o programa está sendo encerrado.

    return entrada                  # Retorna a escolha válida do usuário ("1", "2" ou "0").

# Função MENU ADM: Mostra as opções disponíveis para o Administrador.
def menuADM():
    print("\nTABELA DE COMANDOS")    # Imprime um título para o menu.
    print("1 - Cadastrar produto")  # Opção para adicionar um novo produto.
    print("2 - Listar produto")     # Opção para ver todos os produtos cadastrados.
    print("3 - Alterar produto")    # Opção para modificar um produto existente.
    print("4 - Apagar produto")     # Opção para remover um produto.
    print("0 - sair")               # Opção para voltar ao menu principal.
    opEntrada = input ("Escolha uma opção:\n" ) # Pede ao ADM para escolher uma ação.
    
    # Loop de validação: continua se a entrada for vazia ou se não for uma das opções válidas.
    while( opEntrada == "" or (opEntrada != "1" and opEntrada != "2" and opEntrada != "3" and opEntrada != "4" and opEntrada != "0" )):
        print("opçao invalida")      # Informa que a opção é inválida.
        opEntrada = input("Escolha uma opção: ") # Pede a opção novamente.
    return opEntrada                 # Retorna a opção válida do ADM.
        
# Função MENU OPERADOR: Mostra as opções disponíveis para o Operador.
def menuOp():
    print("\nTABELA DE COMANDOS")    # Imprime um título para o menu.
    print("1 - fazer pedido")       # Opção para iniciar um novo pedido de cliente.
    print("0 - Sair")               # Opção para voltar ao menu principal.
    OpEntradaOp = input ("Escolha uma Opção:\n" ) # Pede ao Operador para escolher uma ação.
    
    # Loop de validação: continua se a entrada for vazia ou não for "1" ou "0". A verificação do "2" é um resquício de uma opção antiga.
    while( OpEntradaOp == "" or (OpEntradaOp != "1" and OpEntradaOp != "2" and OpEntradaOp != "0"  )):
        print("Opçao invalida")      # Informa que a opção é inválida.
        OpEntradaOp = input("Escolha uma Opção: ") # Pede a opção novamente.
        
    return OpEntradaOp               # Retorna a opção válida do Operador.

# Função OPERADOR: Lógica para registrar o pedido de um cliente.
def operador():
    pedido_cliente = []             # Cria uma lista vazia para armazenar os itens do pedido do cliente atual.

    arquivo = open("cardapio.txt", "r", encoding="utf-8") # Abre o arquivo do cardápio em modo de leitura ('r').
    linhas = arquivo.readlines()    # Lê todas as linhas do arquivo e as armazena na lista 'linhas'.
    arquivo.close()                 # Fecha o arquivo.

    print("\nBoa noite caro cliente! O que deseja comprar?\n\nCardápio:\n") # Mensagem de boas-vindas.
    for linha in linhas:            # Loop para exibir o cardápio.
        print(linha.strip())        # Imprime cada linha do cardápio, removendo espaços e quebras de linha do início/fim.

    continuar = "s"                 # Variável de controle para adicionar mais itens ao mesmo pedido.
    while continuar == "s":         # Loop continua enquanto o cliente quiser adicionar itens.
        pedido_valido = False       # Flag (bandeira) para verificar se o código digitado corresponde a um produto.
        pedido = input("\nInsira aqui o código do seu pedido: ").strip() # Pede o código do produto e remove espaços extras.

        i = 0                       # Inicializa um contador para percorrer as linhas do cardápio com um loop 'while'.
        while i < len(linhas):      # Loop 'while' que percorre todas as linhas lidas do arquivo.
            linha_limpa = linhas[i].strip() # Pega a linha atual e remove espaços/quebras de linha.

            if ";" in linha_limpa:  # Verifica se a linha usa o separador ';'.
                partes = linha_limpa.split(";") # Divide a linha em partes usando ';' como separador.
            else:
                partes = linha_limpa.split() # Se não, divide por espaços (menos ideal).

            if len(partes) > 0:     # Garante que a linha não estava vazia.
                codigo = partes[0].strip() # Pega a primeira parte (o código) e remove espaços.

                if pedido == codigo:# Compara o código digitado pelo cliente com o código do produto atual.
                    pedido_cliente.append(linha_limpa) # Adiciona a linha inteira do produto ao pedido do cliente.
                    print("\nProduto adicionado ao pedido:", linha_limpa) # Confirma a adição.
                    pedido_valido = True # Define a flag como True, pois o código foi encontrado.

            i += 1                  # Incrementa o contador para ir para a próxima linha do cardápio.

        if not pedido_valido:       # Após verificar todo o cardápio, se a flag ainda for False
            print("Código inválido. Por favor, tente novamente.") # informa que o código não foi encontrado.

        continuar = input("\nVocê deseja fazer outro pedido? (s/n): ").strip().lower() # Pergunta se o cliente quer adicionar mais itens.

    print("\nPedidos do cliente:")  # Imprime um cabeçalho para o resumo do pedido.
    for item in pedido_cliente:     # Loop que percorre todos os itens no pedido final.
        print("•", item)            # Imprime cada item do pedido.

    print("\nObrigado pela preferência!") # Mensagem de agradecimento.


# Função BACK-END: Gera um código de produto único.
def codBruto():  
    codigo = 0                      # Inicializa a variável que guardará o código final.
    arquivo = open('cardapio.txt', 'r', encoding='utf-8') # Abre o arquivo para leitura.
    dados_do_arquivo = arquivo.readlines() # Lê todas as linhas.
    arquivo.close()                 # Fecha o arquivo.
    if dados_do_arquivo == []:      # Se o arquivo estiver vazio
        codigo = 100                # o primeiro código será 100.
    else:                           # Se o arquivo já tiver produtos
        for linha in range(len(dados_do_arquivo)): # Loop para processar cada linha.
            dados_do_arquivo[linha] = dados_do_arquivo[linha].strip('\n') # Remove a quebra de linha ('\n') do final.
            dados_do_arquivo[linha] = dados_do_arquivo[linha].split(';')  # Divide a linha em uma lista de strings usando ';' como separador.
            temp.append(dados_do_arquivo[linha][0]) # Adiciona apenas o código (primeiro elemento) à lista temporária 'temp'.
 
        for linha in range(len(temp)): # Loop para converter os códigos de string para número.
            temp[linha] = int(temp[linha]) # Converte cada código (string) para inteiro.
        numeros = set(temp)         # Converte a lista de códigos em um conjunto (set) para operações eficientes.
        esperado = set(range(100, max(numeros) + 1)) # Cria um conjunto de todos os números que deveriam existir, de 100 até o maior código atual.
        faltantes = sorted(esperado - set(numeros)) # Encontra os números que faltam na sequência (os "buracos").
        
        if faltantes == []:         # Se não houver "buracos"
            codigo = str(max(numeros) + 1) # o novo código é o maior existente + 1.
        else:                       # Se houver "buracos"
            for numero in faltantes: # Loop pelos números faltantes.
                temp_cod.append(numero) # Adiciona os números faltantes a outra lista temporária.
            codigo = str(temp_cod[0]) # o novo código será o primeiro "buraco" encontrado na sequência.
    return codigo                   # Retorna o código gerado como uma string.

# Função COMANDO 1 (ADM): Cadastra um novo produto.
def cadastrar():
    print("|-------CADASTRO-------|\n") # Exibe o título da seção.
    cont_cad = 1                    # Variável de controle para o loop de cadastro.
    
    while cont_cad != 2:            # O loop roda uma vez.
        
        arquivo = open('cardapio.txt', 'a+', encoding='utf-8') # Abre o arquivo para garantir que ele exista.
        
        cod = codBruto()            # Chama a função para gerar um novo código de produto.
        print("Digite o codigo do seu produto: %s \n" %(cod)) # Mostra o código gerado.
        
        desc = input("Nome do seu produto:\n") # Pede o nome (descrição) do produto.
        while desc == "":           # Validação: não permite nome vazio.
            print("Insira um nome válido")
            desc = input('Digite o nome que deseja inserir para o código %s\n' %(cod)) # Pede novamente.
            
        valor = input('Digite o valor para o(a) %s\n' %(desc)) # Pede o valor do produto.
        while (valor == "" or valor.isalpha()): # Validação: não permite valor vazio ou com letras.
            print("Insira um valor válido\n")  
            valor = input('Digite o valor para o(a) %s\n' %(desc)) # Pede novamente.
            
        # Pede a confirmação final do usuário.
        cadastro = input('Deseja confirmar o cadastro?\nDigite 1 para SIM\nDigite 2 para NÃO\n\n')
        while (cadastro != "1" and cadastro != "2"): # Validação: só aceita "1" ou "2".
            print("Insira uma opção válida\n")
            cadastro = input('Deseja confirmar o cadastro?\nDigite 1 para SIM\nDigite 2 para NÃO\n')
            
        if cadastro == "1":         # Se o usuário confirmou
            arquivo = open('cardapio.txt', 'r', encoding='utf-8') # Abre o arquivo para ler o conteúdo atual.
            dados_do_arquivo = arquivo.readlines() # Lê todas as linhas existentes.
            arquivo.close()         # Fecha o arquivo.
           
            arquivo = open('cardapio.txt', 'a+', encoding='utf-8') # Abre novamente para adicionar.
            if dados_do_arquivo == []: # Se o arquivo estava vazio
                arquivo.write(str(cod) + ';' + desc + ';' + valor + '\n') # escreve o novo produto diretamente.
                arquivo.close()     # Fecha o arquivo.
            else:                   # Se o arquivo já tinha conteúdo
                for i in range(len(dados_do_arquivo)): # Loop para processar os dados existentes.
                    dados_do_arquivo[i] = dados_do_arquivo[i].strip('\n').split(';') # Limpa e divide cada linha.
                dados_do_arquivo.append([cod, desc, valor]) # Adiciona o novo produto à lista em memória.
                lista_cad = sorted(dados_do_arquivo, key=lambda x: int(x[0])) # Ordena a lista completa pelo código do produto.
                
                arquivo = open('cardapio.txt', 'w', encoding='utf-8') # Abre o arquivo em modo 'w' (escrita), que APAGA o conteúdo antigo.
                
                for i in range(len(lista_cad)): # Loop pela lista ordenada.
                    # Reescreve cada produto no arquivo, agora na ordem correta.
                    arquivo.write(str(lista_cad[i][0]) + ";" + str(lista_cad[i][1]) + ";" + str(lista_cad[i][2]) + "\n")
                arquivo.close()     # Fecha o arquivo, salvando as alterações.
                
            lista_prod.append(dados_do_arquivo) # Adiciona os dados à variável global (pode criar lista aninhada).
            print("Item cadastrado com sucesso!!\n") # Mensagem de sucesso.
            cont_cad = 2            # Altera a variável para sair do loop de cadastro.
        elif cadastro == "2":       # Se o usuário cancelou
            print("Cadastro cancelado\n") # informa o cancelamento.
            cont_cad = 2            # e sai do loop de cadastro.

# Função auxiliar: Carrega os produtos do arquivo para a 'lista_prod' global.
def carregar_lista_prod():
    lista_prod.clear()              # Limpa a lista para evitar duplicatas ao chamar a função várias vezes.
    arquivo = open('cardapio.txt', 'r', encoding='utf-8') # Abre o arquivo para leitura.
    for linha in arquivo:           # Lê o arquivo linha por linha.
        partes = linha.strip().split(";") # Limpa e divide a linha em partes.
        if len(partes) == 3:        # Se a linha tiver 3 partes (código, desc, valor)
            lista_prod.append(partes) # adiciona à 'lista_prod'.
    arquivo.close()                 # Fecha o arquivo.

# Função COMANDO 2 (ADM): Lista todos os produtos cadastrados.
def listar():
    loop = 1                        # Variável de controle do loop.
    while (loop != 2):              # O loop executa uma vez.
        arquivo = open('cardapio.txt', 'r', encoding='utf-8') # Abre para leitura.
        info = arquivo.readlines()  # Lê todas as linhas para a lista 'info'.
        arquivo.close()             # Fecha o arquivo.

        if (info == []):            # Se a lista 'info' estiver vazia (arquivo vazio)
            print("\nSEM DADOS EXISTENTE !!") # informa que não há produtos.
            loop = 2                # Sai do loop.
        else:                       # Se houver produtos
            for lista in info:      # percorre cada linha/produto.
                print("|-------LISTA-------|") # Imprime um cabeçalho.
                print(lista.strip())# Imprime o produto, removendo espaços/quebras de linha.
            loop = 2                # Sai do loop.

# Função COMANDO 3 (ADM): Altera um produto existente.
def alterar():
    carregar_lista_prod()           # Garante que 'lista_prod' está atualizada com os dados do arquivo.
    print("|-------ALTERAÇÃO DE PRODUTOS CADASTRADOS-------|") # Título da seção.
    listar()                        # Mostra a lista de produtos para o usuário saber o que pode alterar.
    if lista_prod == []:            # Se a lista estiver vazia, não há o que alterar.
        print("")                   # Não faz nada (poderia ter uma mensagem).
    else:                           # Se houver produtos
        indice_coluna = buscar_indice(lista_prod) # Chama a função para o usuário escolher um produto e obter seu índice.
        print("Você está alterando o produto %s\n" % (lista_prod[indice_coluna][1])) # Informa qual produto será alterado.
        conf_alterar = input("Deseja confirmar a alteração ?\nDigite 1 para Sim\nDigite 2 para Não\n\n") # Pede confirmação.
        
        if conf_alterar == "1":     # Se o usuário confirmar
            novo_valor = input("Digite o novo valor para este produto:\n") # Pede o novo valor.
            lista_prod[indice_coluna][2] = novo_valor  # Atualiza o valor (terceiro item, índice 2) na lista.
            novo_desc = input("Digite o novo nome para este produto:\n") # Pede o novo nome.
            lista_prod[indice_coluna][1] = novo_desc   # Atualiza a descrição (segundo item, índice 1) na lista.
            
            gravar_txt(lista_prod)  # Salva a 'lista_prod' (agora modificada) de volta no arquivo.
            print("Produto alterado com sucesso") # Mensagem de sucesso.
        elif conf_alterar == "2":   # Se o usuário cancelar
            print("Alteração cancelada") # informa o cancelamento.
        
# Função auxiliar: Pede ao usuário um código e retorna o índice correspondente na lista.
def buscar_indice(Lista_prod):
    # prod = [Cod; Desc; Valor_u]
    for percorre_todas_linhas in range(len(Lista_prod)): # Loop por todos os produtos.
        cod_ind.append(Lista_prod[percorre_todas_linhas][0]) # Adiciona apenas os códigos à lista 'cod_ind'.
    op = input('Escolha o código do produto desejado:\n') # Pede ao usuário para escolher um código.
    
    while op not in cod_ind:        # Validação: enquanto o código digitado não estiver na lista de códigos válidos
        listar()                    # mostra a lista novamente para ajudar.
        op = input('Escolha um código válido\n') # pede um código válido.
    codigo = cod_ind.index(op)      # Encontra o índice (posição) do código escolhido.
    return codigo                   # Retorna esse índice.
   
# Função COMANDO 4 (ADM): Exclui um produto cadastrado.
def excluir():
    print(" |--------EXCLUSÃO DE PRODUTOS CADASTRADOS--------|\n") # Título da seção.
    listar()                        # Mostra a lista de produtos.
    if lista_prod == []:            # Se a lista estiver vazia
        print("")                   # não faz nada.
    else:                           # Se houver produtos
        indice_ex = buscar_indice(lista_prod) # Pede ao usuário para escolher um produto e obtém seu índice.
        print("Você está excluindo o produto:%s\n" %(lista_prod[indice_ex][1])) # Confirma qual produto será excluído.
        conf_apagar = input("Deseja confirmar a exclusão ?\nDigite 1 para Sim\nDigite 2 para Não\n\n") # Pede confirmação.
        if conf_apagar == "1":      # Se o usuário confirmar
            lista_prod.pop(indice_ex) # Remove o item da lista na posição 'indice_ex'.
            gravar_txt(lista_prod)  # Salva a lista (agora menor) de volta no arquivo.
            print("Arquivo deletado com sucesso") # Mensagem de sucesso.
        elif conf_apagar == "2":    # Se o usuário cancelar
            print("Exclusão cancelada") # informa o cancelamento.
    
# Função auxiliar: Salva a lista de produtos no arquivo de texto.
def gravar_txt(lista_prod):
    # prod = [Cod; Desc; Valor_u]
    arquivo = open('cardapio.txt', 'w', encoding='utf-8') # Abre o arquivo em modo 'w' (escrita), apagando o conteúdo antigo.
    for i in range(len(lista_prod)): # Loop por cada produto na lista.
        # Reescreve o produto no arquivo, juntando as partes com ';' e adicionando uma quebra de linha.
        arquivo.write(lista_prod[i][0] + ";" + lista_prod[i][1] + ";" + lista_prod[i][2] + "\n")
    arquivo.close()                 # Fecha o arquivo para salvar as alterações.


# =====================================================================================
# Main - Ponto de partida e controle principal do programa
# =====================================================================================

while (continuar1 == "s"):          # Loop principal. O programa roda enquanto esta variável for "s".
    entrada = comeco()              # Chama o menu inicial e armazena a escolha do usuário.
    print(entrada)                  # Imprime a escolha (útil para depuração).

    if entrada == "1":              # Se o usuário escolheu "Administrador".
        opEntrada = menuADM()       # Mostra o menu do ADM e pega a sua escolha.
        print(opEntrada)            # Imprime a escolha do ADM.

        while opEntrada != "0":     # Loop do menu ADM: continua até o ADM digitar "0" para sair.
            if opEntrada == "1":    # Se a escolha for "1"
                cadastrar()         # chama a função de cadastro.
            elif opEntrada == "2":  # Se a escolha for "2"
                 listar()           # chama a função de listagem.
            elif opEntrada == "3":  # Se a escolha for "3"
                alterar()           # chama a função de alteração.
            elif opEntrada == "4":  # Se a escolha for "4"
                excluir()           # chama a função de exclusão.
            else:                   # Se for qualquer outra coisa (não deveria acontecer devido à validação).
                print("Opção inválida.") # Mensagem de erro.
            
            opEntrada = menuADM()   # Após cada ação, mostra o menu ADM novamente para a próxima ação.
            print(opEntrada)        # Imprime a nova escolha.

        print("Saindo do menu Administrador") # Mensagem exibida quando o ADM digita "0".

    elif entrada == "2":            # Se o usuário escolheu "Operador".
        continuarOp = "s"           # Variável de controle para o loop do menu do Operador.
        while continuarOp == "s":   # Loop do menu do Operador.
            OpEntradaOp = menuOp()  # Mostra o menu do Operador e pega a sua escolha.
            if OpEntradaOp == "1":  # Se a escolha for "1" (fazer pedido)
                operador()          # chama a função principal do operador.
            elif OpEntradaOp == "2":# Se a escolha for "2"
                print("Função 'fazer pedido' ainda não implementada.") # informa que a função não existe.
            elif OpEntradaOp == "0":# Se a escolha for "0" (Sair)
                print("Saindo do menu Operador") # imprime a mensagem de saída.
                continuarOp = "n"   # altera a variável de controle para 'n', encerrando o loop do operador.
            else:                   # Se a opção for inválida.
                print("Opção inválida, tente novamente.") # informa o erro.