import json

# -----------------------------------------
# 1. Carregamento da Máquina de Turing
# -----------------------------------------

def carregar_maquina_de_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        configuracao_bruta = json.load(arquivo)

    simbolo_branco = configuracao_bruta["blank"]
    estado_inicial = configuracao_bruta["initial_state"]
    estados_finais = set(configuracao_bruta["final_states"])

    # monta o dicionário de transições a partir da lista do JSON
    transicoes = {}
    for t in configuracao_bruta["transitions"]:
        chave = (t["state"], t["read"])  # (estado_atual, símbolo_lido)
        valor = (t["next_state"], t["write"], t["move"])  # (próximo_estado, símbolo_escrito, movimento)
        transicoes[chave] = valor

    return {
        "branco": simbolo_branco,
        "estado_inicial": estado_inicial,
        "estados_finais": estados_finais,
        "transicoes": transicoes,
        "nome": configuracao_bruta.get("name", "")
    }


# -----------------------------------------
# 2. Exibição da configuração
# -----------------------------------------

def exibir_configuracao(fita, posicao_cabeca, estado_atual, simbolo_branco):
    # encontra o último símbolo não-branco
    ultimo_util = len(fita) - 1
    while ultimo_util >= 0 and fita[ultimo_util] == simbolo_branco:
        ultimo_util -= 1
    if ultimo_util < 0:
        ultimo_util = 0

    # garante que não vai cortar antes da cabeça
    limite = max(ultimo_util, posicao_cabeca)

    itens_para_imprimir = []
    for i in range(limite + 1):
        simbolo = fita[i]

        # posição da cabeça
        if i == posicao_cabeca:
            itens_para_imprimir.append(f"[{estado_atual} {simbolo}]")
        else:
            # se for blank e não estiver sob a cabeça - não imprime nada
            if simbolo == simbolo_branco:
                itens_para_imprimir.append("")
            else:
                itens_para_imprimir.append(simbolo)

    linha = " ".join(itens_para_imprimir)
    return linha.strip()


# -----------------------------------------
# 3. Execução da Máquina de Turing
# -----------------------------------------

def executar_maquina_turing(entrada, configuracao, nome_arquivo_saida="resultado_mt.json"):
    simbolo_branco = configuracao["branco"]
    estado_atual = configuracao["estado_inicial"]
    estados_finais = configuracao["estados_finais"]
    transicoes = configuracao["transicoes"]

    # descobre estados e alfabeto a partir das transições
    estados_usados = set()
    alfabeto_usado = set()

    for (estado, simbolo_lido), (novo_estado, simbolo_escrito, movimento) in transicoes.items():
        estados_usados.add(estado)
        estados_usados.add(novo_estado)

        alfabeto_usado.add(simbolo_lido)
        alfabeto_usado.add(simbolo_escrito)

    # garante que o branco também está no alfabeto
    alfabeto_usado.add(simbolo_branco)

    # fita com sobra 
    fita = list(entrada) + [simbolo_branco] * 10
    posicao_cabeca = 0

    passos = []  # armazena as configurações em ordem

    # registra a configuração inicial
    passos.append(exibir_configuracao(fita, posicao_cabeca, estado_atual, simbolo_branco))

    numero_de_passos = 0

    # executa enquanto não chegar em um estado final
    while estado_atual not in estados_finais:
        simbolo_lido = fita[posicao_cabeca]
        chave = (estado_atual, simbolo_lido)

        # se não existe transição definida, a MT "trava" e para
        if chave not in transicoes:
            passos.append(f"Sem transição definida para {chave}. Execução interrompida.")
            break

        novo_estado, simbolo_escrito, movimento = transicoes[chave]

        # escreve o símbolo na posição atual da cabeça
        fita[posicao_cabeca] = simbolo_escrito

        # move a cabeça
        if movimento == 'R':
            posicao_cabeca += 1
            if posicao_cabeca == len(fita):
                fita.append(simbolo_branco)

        elif movimento == 'L':
            if posicao_cabeca == 0:
                fita.insert(0, simbolo_branco)
                # cabeça continua em 0 (agora sobre o novo branco)
            else:
                posicao_cabeca -= 1
        else:
            passos.append(f"Movimento inválido: {movimento}. Execução interrompida.")
            break

        estado_atual = novo_estado
        numero_de_passos += 1

        # registra a nova configuração
        passos.append(exibir_configuracao(fita, posicao_cabeca, estado_atual, simbolo_branco))

    # remove brancos à direita e à esquerda
    fita_final = "".join(fita).strip(simbolo_branco)

    # monta o dicionário de saída para o json
    saida = {
        "maquina": configuracao.get("nome", ""),
        "entrada": entrada,
        "fita_final": fita_final,
        "states": sorted(estados_usados),
        "estado_final": estado_atual,
        "tape_alphabet": sorted(alfabeto_usado),
        "numero_de_passos": numero_de_passos,
        "passos": passos
    }

    with open(nome_arquivo_saida, "w", encoding="utf-8") as arquivo:
        json.dump(saida, arquivo, ensure_ascii=False, indent=2)

    print(f"Execução concluída. {numero_de_passos} passos salvos em '{nome_arquivo_saida}'.")

    return fita_final


# -----------------------------------------
# 4. Main de entrada
# -----------------------------------------

if __name__ == "__main__":
    configuracao_mt = carregar_maquina_de_arquivo("mt_soma.json")
    print("Máquina carregada:", configuracao_mt["nome"])
    print()

    entrada_inicial = "111$11111@_____"

    resultado = executar_maquina_turing(entrada_inicial, configuracao_mt, "resultado_mt.json")
    print("Resultado final na fita:", resultado)
