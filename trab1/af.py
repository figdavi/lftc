import json
from typing import Any
from pathlib import Path


# ============================================================
# CLASSE PRINCIPAL: Representação de um autômato finito (AFND)
# ============================================================


class Automato:
    def __init__(
        self,
        estados: set[int],
        alfabeto: set[str],
        inicial: int,
        finais: set[int],
        transicoes: set[tuple[int, str, int]],
    ):
        self.estados = estados
        self.alfabeto = alfabeto
        self.inicial = inicial
        self.finais = finais
        self.transicoes = transicoes  # conjunto de tuplas (origem, símbolo, destino)

    def __str__(self) -> str:
        """Retorna a representação textual do autômato."""
        s = (
            f"\nEstados: {self.estados}"
            f"\nAlfabeto: {self.alfabeto}"
            f"\nInicial: {self.inicial}"
            f"\nFinais: {self.finais}"
            f"\nTransições:"
        )
        for origem, simbolo, destino in sorted(self.transicoes):
            s += f"\n\tδ({origem}, '{simbolo}') → {destino}"
        return s

    def to_dict(self) -> dict[str, Any]:
        """
        Converte o autômato para um dicionário compatível com JSON.
        (Como JSON não suporta set(), convertemos tudo em list().)
        """
        return {
            "estados": list(self.estados),
            "alfabeto": list(self.alfabeto),
            "inicial": self.inicial,
            "finais": list(self.finais),
            "transicoes": [list(t) for t in self.transicoes],
        }


# ============================================================
# FUNÇÃO 1: Cálculo do ε-fecho de um estado
# ============================================================


def calcular_e_fecho(A: Automato, estado: int) -> set[int]:
    """
    Retorna o ε-fecho do estado fornecido, ou seja, todos os estados
    alcançáveis a partir dele usando exclusivamente transições ε.

    Exemplo:
        δ(1, ε) → 2
        δ(2, ε) → 3
        Então: ε(1) = {1, 2, 3}
    """

    fecho = {estado}
    pilha = [estado]

    # Percorre estados conectados por transições ε
    while pilha:
        atual = pilha.pop()
        for origem, simbolo, destino in A.transicoes:
            if origem == atual and simbolo == "ε" and destino not in fecho:
                fecho.add(destino)
                pilha.append(destino)

    return fecho


# ============================================================
# FUNÇÃO 2: Eliminação das transições ε de um AFND-ε
# ============================================================


def eliminar_epsilon(A: Automato) -> Automato:
    """
    Retorna um novo autômato sem transições ε, seguindo rigorosamente:
      1. Se existe δ(p, ε*) = q e δ(q, a) = r, adiciona δ(p, a) = r.
      2. Se existe δ(p, ε*) = f (com f ∈ F), então p vira final.
    """

    EPS = "ε"

    # Cálculo do ε-fecho de cada estado
    fecho = {estado: calcular_e_fecho(A, estado) for estado in A.estados}

    # Remove o símbolo ε do alfabeto original
    alfabeto_sem_e = set(A.alfabeto) - {EPS}

    # Gera novas transições
    novas_transicoes = set()
    for p in A.estados:
        for simbolo in alfabeto_sem_e:
            destinos = set()
            # percorre cada q alcançável por ε a partir de p
            for q in fecho[p]:
                # pega apenas as transições reais por 'simbolo'
                for origem, s, destino in A.transicoes:
                    if origem == q and s == simbolo:
                        destinos.add(destino)
            # os destinos não precisam de fecho extra, basta conectar direto
            for r in destinos:
                novas_transicoes.add((p, simbolo, r))

    # Atualiza estados finais
    novos_finais = {p for p in A.estados for q in fecho[p] if q in A.finais}

    return Automato(
        estados=A.estados,
        alfabeto=alfabeto_sem_e,
        inicial=A.inicial,
        finais=novos_finais,
        transicoes=novas_transicoes,
    )


# ============================================================
# FUNÇÕES 3 e 4: Leitura e Escrita de Arquivos JSON
# ============================================================


def ler_automatos(nome_arquivo: Path) -> dict[str, Automato]:
    """
    Lê autômatos de um arquivo JSON e retorna um dicionário {nome: Automato}.
    """
    with open(nome_arquivo, "r", encoding="utf-8") as arq:
        dados = json.load(arq)

    return {
        nome: Automato(
            estados=set(a["estados"]),
            alfabeto=set(a["alfabeto"]),
            inicial=a["inicial"],
            finais=set(a["finais"]),
            transicoes={tuple(t) for t in a["transicoes"]},
        )
        for nome, a in dados.items()
    }


def escrever_automatos(nome_arquivo: Path, automatos: dict[str, Automato]) -> None:
    """
    Escreve um ou mais autômatos em formato JSON.
    """
    with open(nome_arquivo, "w", encoding="utf-8") as arq:
        automatos_dict = {nome: A.to_dict() for nome, A in automatos.items()}
        json.dump(automatos_dict, arq, indent=4, ensure_ascii=False)


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================


def main() -> None:
    # Caminhos relativos ao diretório do script atual
    cur_dir = Path(__file__).resolve().parent
    input_file = cur_dir / "automato.json"
    output_file = cur_dir / "automato_sem_e.json"

    # Leitura dos autômatos de entrada
    automatos: dict[str, Automato] = ler_automatos(input_file)
    automatos_sem_e: dict[str, Automato] = {}

    # Processa cada autômato
    for nome, A in automatos.items():
        B = eliminar_epsilon(A)
        automatos_sem_e[nome] = B

        print(f"\n=== Autômato '{nome}' antes da remoção de ε ===")
        print(A)
        print(f"\n=== Autômato '{nome}' depois da remoção de ε ===")
        print(B)
        print("\n--------------------------------------------\n")

    # Salva os novos autômatos em arquivo
    escrever_automatos(output_file, automatos_sem_e)


if __name__ == "__main__":
    main()
