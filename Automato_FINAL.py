from tabulate import tabulate

NUMEROS = "0123456789"
LETRAS = "[ABCDEF]"
UPPER = "[ABCDEFGHIJKLMNOPQRSTUVWXYZ]"
LOWER = "[abcdefghijklmnopqrstuvwxyz]"
palavras_reservadas = {
    'rotina': 'TK_ROTINA', 'fim_rotina': 'TK_FIM_ROTINA', 'se': 'TK_SE', 'senao': 'TK_SENAO',
    'imprima': 'TK_IMPRIMA', 'leia': 'TK_LEIA', 'para': 'TK_PARA', 'enquanto': 'TK_ENQUANTO'
}
tokens = {}
errors = []
def save_errors(line, id_coluna, error_msg):
    global errors

    errors.append({"LINHA": line, "COLUNA": id_coluna, "ERRO": error_msg})

def errors_table(errors):
    table = []

    for error in errors:
        table.append([error["LINHA"], error["COLUNA"], error["ERRO"]])
    
    return tabulate (table, headers=["LIN", "COL", "ERRO"], tablefmt="grid")

def save_tokens(tokens, token, lexema):
    if token in tokens:
        tokens[token] += 1
    else:
        tokens[token] = 1

def tokens_table(tokens):
    tokens_tabela = [["TOKEN", "USOS"]]
    for token, uso in tokens.items(): 
        tokens_tabela.append([token, uso])  
    tokens_tabela.append(["Total", sum(tokens.values())])  
    return tabulate(tokens_tabela, headers="firstrow", tablefmt="grid")

def reseta_analisador_lexico(caractere):
    estado = 0
    lexema = ""

    if caractere != " ":
        lexema = caractere

    transicoes = {
        '"': 29, '+': 26, '-': 27, '*': 35, '%': 36, '|': 37, '~': 38, ':': 47, 
        '>': 40, '=': 41, '<': 46, '(': 48, ')': 49, '&': 65, '.': 68
    }

    if caractere in transicoes:
        estado = transicoes[caractere]
    if caractere in LOWER:
        estado = 32
    if caractere == '#':
        estado = 1
    if caractere in NUMEROS:
        estado = 6
    if caractere in LETRAS:
        estado = 25

    return estado, lexema


def analisador_lexico(ex01cic):
    estado_atual = 0
    lexeme = ""
    lexema_atual = ""
    resultados = []
    line = 1 
    id_coluna = 1 

    for caractere in ex01cic.strip() + "\n":
        #transição para casos básicos
        if caractere == "+" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 26
        elif estado_atual == 26:
            resultados.append(("TK_SOMA", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            
        elif caractere == "-" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 27
        elif estado_atual == 27:
            resultados.append(("TK_SUBTRAÇÃO", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "*" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 35
        elif estado_atual == 35:
            resultados.append(("TK_MULTIPLICAÇÃO", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "%" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 36
        elif estado_atual == 36:
            resultados.append(("TK_RESTO", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "|" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 37
        elif estado_atual == 37:
            resultados.append(("TK_OR", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "~" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 38
        elif estado_atual == 38:
            resultados.append(("TK_NEGAÇÃO", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == ":" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 47
        elif estado_atual == 47:
            resultados.append(("TK_OP", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "&" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 65
        elif estado_atual == 65:
            resultados.append(("TK_AND", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
        
        elif caractere == "(" and estado_atual == 0:
            estado_atual = 48
            id_coluna += 1
            lexema_atual += caractere
        elif estado_atual == 48:
            resultados.append(("TK_DELIMITA_ABERTURA", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            print("caractere", caractere)

        elif caractere == ")" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 49
        elif estado_atual == 49:
            resultados.append(("TK_DELIMITA FECHAMENTO", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == ">" and estado_atual == 0:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 40
        elif caractere == "=" and estado_atual == 40:
            id_coluna += 1
            lexema_atual += caractere
            estado_atual = 66
        elif estado_atual == 66:
            resultados.append(("TK_MENOR_IGUAL", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere not in [">", "="] and estado_atual == 40:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 63
        elif estado_atual == 63:
            resultados.append(("TK_MENOR", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "=" and estado_atual == 0:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 41
        elif caractere == "=" and estado_atual == 41:
            lexeme += caractere
            id_coluna += 1
            estado_atual = 44
        elif estado_atual == 44:
            resultados.append(("TK_COMPARA", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "<" and estado_atual == 0:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 46
        elif caractere == ">" and estado_atual == 46:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 39
        elif estado_atual == 39:
            resultados.append(("TK_DIFERENTE", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "=" and estado_atual == 46:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 60

        elif caractere == "=" and estado_atual == 60:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 61
        elif caractere != "=" and estado_atual == 60:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 62

        elif estado_atual == 61:
            resultados.append(("TK_ATRIBUIÇÃO", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual == 62:
            resultados.append(("TK_MAIOR_IGUAL", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual == 46 and caractere != "<":
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 58
        elif estado_atual == 58:
            resultados.append(("TK_MAIOR", lexema_atual, id_coluna-1))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            
        elif caractere == "<" and estado_atual == 46:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 43
        elif caractere == "<" and estado_atual == 43:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 3
        elif estado_atual == 3 and (caractere not in ["<", ">"] or caractere in ["\n"]):
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 3 
        elif estado_atual == 3 and caractere == ">":
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 5
        elif caractere == ">" and estado_atual == 5:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 28
        elif caractere == ">" and estado_atual == 28:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 42       
        elif caractere != "<" and estado_atual in [43]:
            save_errors(line, id_coluna, "ERRO: CADEIA NÃO ABERTA")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere != ">" and estado_atual in [5, 28]:
            save_errors(line, id_coluna, "ERRO: CADEIA NÃO FECHADA")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            id_coluna = 1

        elif estado_atual in [42]:
            resultados.append(("TK_BLOCO", lexema_atual, id_coluna-1))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        #comentário em linha
        elif caractere == "#" and estado_atual == 0:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 1
        elif caractere != '\n' and estado_atual == 1:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 1
        elif caractere == '\n' and estado_atual == 1:
            lexema_atual += caractere
            resultados.append(("TK_COMEN_LINHA", lexema_atual, id_coluna-1))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual in [2]:
            resultados.append(("TK_COMEN_LINHA", lexema_atual, id_coluna-1))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
        
            #transição para número inteiro
        elif caractere in NUMEROS and estado_atual == 0:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 6
    #transição para hexadecimal saindo do estado 0
        elif caractere in LETRAS and estado_atual == 0:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 25
        elif caractere == "x" and estado_atual == 25:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 23
        elif (caractere in LETRAS or caractere in NUMEROS) and estado_atual == 23:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 24 
        elif (caractere in LETRAS or caractere in NUMEROS) and estado_atual == 24:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 24 
        #continuação da transição int
        elif caractere in NUMEROS and estado_atual == 6:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 8
        #transição 2 hexadecimal saindo do estado 6
        elif caractere == "x" and estado_atual == 6:
            lexema_atual += caractere 
            id_coluna += 1
            estado_atual = 23
        elif (caractere in LETRAS or caractere in NUMEROS) and estado_atual == 23:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 24
        elif (caractere in LETRAS or caractere in NUMEROS) and estado_atual == 24:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 24
        elif caractere in NUMEROS and caractere not in ["/", "_", "."]and estado_atual == 8:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 22
        elif caractere in NUMEROS and estado_atual == 22:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 45
        elif caractere in NUMEROS and estado_atual == 45:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 45

        elif estado_atual in [8] and caractere in ["x"]:
            save_errors(line, id_coluna-1, "Número Invalido")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual in [23] and caractere not in NUMEROS + LETRAS:
            save_errors(line, id_coluna-1, "ERRO: Endereço Inválido")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual in [23, 24] and caractere in ["a","b","c","d","e","f","x"]:
            save_errors(line, id_coluna-1, "numero mal formado")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            
        elif estado_atual in [6, 8, 22] and caractere not in ["NUMEROS", ".", "/", "_"]:
            estado_atual = 54
            resultados.append(("TK_INT", lexema_atual, id_coluna-1))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual in [45] and caractere not in NUMEROS and caractere not in ["."]:
            estado_atual = 64
            resultados.append(("TK_INT", lexema_atual, id_coluna-1))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual == 45 and caractere == ".":
            print(estado_atual,lexema_atual, caractere)
            save_errors(line, id_coluna, "FLOAT mal formado")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            id_coluna = 1

        elif estado_atual in [24] and caractere not in NUMEROS + LETRAS: 
            estado_atual = 55
            resultados.append(("TK_END", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        #transição para tk_cadeia
        elif caractere == '"' and estado_atual == 0:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 29 
        elif caractere != '"' and caractere not in "\n" and estado_atual == 29:
            #print("estado 0", lexema_atual, caractere)
            lexema_atual += caractere 
            id_coluna += 1
        elif caractere == '"' and estado_atual == 29:
            #print(estado_atual, lexema_atual, caractere)
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 31

        elif estado_atual in [31]:
            #print(estado_atual, lexema_atual, caractere)
            resultados.append(("TK_CADEIA", lexema_atual, id_coluna))  # Adiciona o token "TK_CADEIA" ao resultado
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere not in ['"'] and estado_atual in [31]:
            save_errors(line, id_coluna-1, "ERRO: Cadeia Inválida - Aspas não fechadas")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        #transições para data   
        elif estado_atual == 8 and caractere == "/" and caractere not in ["NUMEROS", ".", "_"]:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 9
        elif estado_atual == 9 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 10
        elif estado_atual == 10 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 11
        elif estado_atual == 11 and caractere == "/" and caractere not in ["NUMEROS", ".", "_"]:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 13
        elif estado_atual == 13 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 14
        elif estado_atual == 14 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 15
        elif estado_atual == 15 and caractere in NUMEROS:
            lexema_atual += caractere
            estado_atual = 16
        elif estado_atual == 16 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 17
        elif estado_atual == 8 and caractere == "_" and caractere not in ["NUMEROS", ".", "/"]:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 12
        elif estado_atual == 12 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 18
        elif estado_atual == 18 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 19
        elif estado_atual == 19 and caractere == "_" and caractere not in ["NUMEROS", ".", "/"]:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 20
        elif estado_atual == 20 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 14 

        #erros para data
        elif estado_atual in [6, 22, 9, 10, 12, 18] and caractere in ["/", "_"]:
            save_errors(line, id_coluna, "ERRO: DATA INVÁLIDA")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
        elif estado_atual in [11, 19] and caractere in NUMEROS:
            save_errors(line, id_coluna, "ERRO: DATA INVÁLIDA")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
        elif caractere not in NUMEROS and estado_atual in [13,14,15,16]:
            save_errors(line, id_coluna, "ERRO: DATA INVÁLIDA")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
        elif caractere in NUMEROS and estado_atual in [17]:
            lexema_atual += caractere
            save_errors(line, id_coluna, "ERRO: DATA INVÁLIDA")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        #estado id
        elif estado_atual == 0 and caractere in LOWER: 
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 32
        elif estado_atual == 32 and caractere in UPPER:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 33
        elif caractere in LOWER and estado_atual == 33:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 34
        elif caractere in UPPER and estado_atual == 34:
            lexema_atual += caractere 
            id_coluna += 1
            estado_atual = 33 
        
        elif estado_atual in [32, 33, 34] and caractere in NUMEROS: 
            lexema_atual += caractere
            id_coluna += 1
            save_errors(line, id_coluna-1, "ERRO: ID INVÁLIDO")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        #palavras_reservadas
        elif estado_atual == 32 and caractere in LOWER:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 50
        elif estado_atual == 50: 
            if caractere in LOWER:
                estado_atual = 50
                lexema_atual += caractere
                id_coluna += 1
            elif caractere == "_":
                estado_atual = 59
                lexema_atual += caractere
                id_coluna += 1
            else:
                # Verifica se o lexema atual é uma palavra reservada
                if lexema_atual in palavras_reservadas:
                    resultados.append((palavras_reservadas[lexema_atual], lexema_atual))
                    estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
                else:
                    save_errors(line, id_coluna-1, "ERRO NA PALAVRA RESERVADA")
                    estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
                    id_coluna = 1
                # Reseta o estado e o lexema atual
                
        elif estado_atual == 59 and caractere in LOWER: 
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 50

        elif caractere in UPPER and estado_atual in [0, 25, 33]:
            lexema_atual += caractere
            id_coluna += 1
            save_errors(line, id_coluna-1, "ERRO: ENDEREÇO OU ID INVÁLIDO")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere not in UPPER and estado_atual == 34:
            resultados.append(("TK_ID", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual in [33, 34]:
            resultados.append(("TK_ID", lexema_atual, id_coluna))
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)
            print("lexema", lexema_atual, estado_atual)
            id_coluna = 1
                    
        #estados aceitação e erro para data
        elif estado_atual in [17]:
            resultados.append(("TK_DATA", lexema_atual, id_coluna-1))  # Adiciona o token "TK_CADEIA" ao resultado
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere) 
        elif estado_atual in [0, 6] and caractere in ["/", "_"]:
            save_errors(line, id_coluna-1, "ERRO: Formato DATA inválida")
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        #estados transição float
        
        elif estado_atual == 0 and caractere == ".":
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 68
        elif caractere in NUMEROS and estado_atual == 68:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 21
        elif caractere == "e" and estado_atual == 21:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 51
        elif caractere == "-" and estado_atual == 51:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 69
        elif caractere in NUMEROS and estado_atual == 69:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 52
        elif caractere in NUMEROS and estado_atual == 52:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 52
        elif caractere in NUMEROS and estado_atual == 51:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 52

        elif estado_atual in [6, 8, 22] and caractere == ".":
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 7
        elif estado_atual == 7 and caractere in NUMEROS:
            lexema_atual += caractere
            id_coluna += 1
            estado_atual = 21
        elif estado_atual == 21 and caractere in NUMEROS:
            lexema_atual += caractere 
            id_coluna += 1 
        elif estado_atual == 7 and caractere == "e":
            lexema_atual += caractere 
            estado_atual = 51
            id_coluna += 1


        elif estado_atual in [21, 52] and caractere not in NUMEROS + "e":
            estado_atual = 56
            resultados.append(("TK_FLOAT", lexema_atual, id_coluna-1))  # Adiciona o token "TK_FLOAT" ao resultado 
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif estado_atual in [7] and caractere not in NUMEROS + ".":
            resultados.append(("TK_FLOAT", lexema_atual, id_coluna-1))  # Adiciona o token "TK_FLOAT" ao resultado
            estado_atual, lexema_atual = reseta_analisador_lexico(caractere)

        elif caractere == "\n":
            line += 1
            id_coluna = 1
        elif caractere == "," or caractere == " ":
            id_coluna += 1
        elif estado_atual == 0 and caractere not in NUMEROS:
            id_coluna += 1

                                
    return resultados

def verificar_erro(lista_erros, num_linha):
    for erro in lista_erros:
        if erro['LINHA'] == num_linha:
            return erro
    return None

def print_errors(ex01cic, errors):
    try:
        with open(ex01cic, 'r') as arquivo:
            linhas = arquivo.readlines()

            # Itera sobre as linhas e imprime numeradas
            for num_linha, linha in enumerate(linhas, start=1):
                print(f"[{num_linha}] {linha.rstrip()}")  # rstrip() remove espaços em branco adicionais e quebras de linha
                teste = verificar_erro(errors, num_linha)
                if teste:
                    print('-'*(int(teste['COLUNA'])+3) + '^')
                    print(f'Erro linha {teste["LINHA"]} coluna {teste["COLUNA"]}: {teste["ERRO"]}')

    except FileNotFoundError:
        print(f"O arquivo '{ex01cic}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def main():
    global tokens, errors
    errors = []
    file = open('ex01cic.txt', 'r')
    analisador_lexico(file.read() + '\n')

    linhas_tokens_lexemas, tokens = get_tokens_lexemas('ex01cic.txt')
    tabela_tokens_lexemas = tabulate(linhas_tokens_lexemas, headers=["LINHA", "TOKEN", "LEXEMA"], tablefmt="grid")
    tabela_tokens = tokens_table(tokens)
    tabela_erros = errors_table(errors)
    
    print("\nTabela de TOKENS e Lexemas:\n", tabela_tokens_lexemas)
    print("\nTabela de TOKENS e suas quantidades:\n", tabela_tokens)
    print("\nTabela de erros:\n", tabela_erros)

    if len(errors) != 0:
        print("\nCódigo com erros:\n")
        print_errors('ex01cic.txt', errors)

def get_tokens_lexemas(ex01cic):
    linhas_tabela = []
    tokens = {}

    try:
        with open(ex01cic, "r") as ex01cic:
            for num_linha, linha in enumerate(ex01cic, start=1):
                resultados = analisador_lexico(linha)
                for resultado in resultados:
                    token = resultado[0]
                    lexema = resultado[1]
                    linhas_tabela.append([num_linha, token, lexema])
                    save_tokens(tokens, token, lexema)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{ex01cic}' não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo '{ex01cic}': {e}")

    return linhas_tabela, tokens

    
main()
