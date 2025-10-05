import json
from typing import Any


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
        self.transicoes = transicoes  # conjunto de tupla (origem, simbolo, destino)

    def __str__(self) -> str:
        s = f"""
    Estados: {self.estados}
    Alfabeto: {self.alfabeto}
    Inicial: {self.inicial}
    Finais: {self.finais}
    Transições:"""
        for origem, simbolo, destino in self.transicoes:
            s += f"\n\tδ({origem}, '{simbolo}') → {destino}"
        return s

    def to_dict(self) -> dict[str, Any]:
        # Como json não suporta set(), é necessário transformar tudo em list()
        return {
            "estados": list(self.estados),
            "alfabeto": list(self.alfabeto),
            "inicial": self.inicial,
            "finais": list(self.finais),
            "transicoes": [list(t) for t in self.transicoes],
        }


def calcular_e_fecho(A: Automato, estado: int) -> set[int]:
    """
    Calcula o E(estado) do automato A
    """

    # The ε-closure of a state s is the set of states you can reach from s using only (0 or more) ε-transitions.

    # Ex:
    # δ(1, ε) -> 2
    # δ(2, ε) -> 3
    #
    # ε(1) = 1, 2, 3

    fecho = {estado}
    pilha = [estado]

    while pilha:
        # estado
        atual = pilha.pop()
        for origem, simbolo, destino in A.transicoes:
            # Se origem da transição é a partir do estado atual, utiliza epsilon e destino ainda não foi visitado:
            if origem == atual and simbolo == "ε" and destino not in fecho:
                fecho.add(destino)
                pilha.append(destino)
    return fecho


def eliminar_epsilon(A: Automato) -> Automato:
    """
    Retorna um novo Automato() A' sem ε-transições
    """

    # Obs: Os passos irão alterar apenas transições e finais.

    # Calcular E(q)
    #
    # Ex:
    # E({1}) = {1, 2, 3}
    # E({2}) = {2, 3}
    #
    # fecho_total = {1: {1, 2, 3}, 2: {2, 3}}
    fecho_total: dict[int, set[int]] = {
        estado: calcular_e_fecho(A, estado) for estado in A.estados
    }

    # Calcular novos finais
    # (Passo 2): Se δ(p, ε) = q e q ∈ F, acrescentamos p a F
    novos_finais: set[int] = set()

    for p in A.estados:
        for q in fecho_total[p]:
            if q in A.finais:
                novos_finais.add(p)

    # Alfabeto sem 'E'
    alfabeto_sem_e: set[str] = {s for (_, s, _) in A.transicoes if s != "ε"}

    # Calcular novas transições (sem ε)
    # (Passo 1): Se 'a' ∈ Σ, δ(q₁, ε) = q₂ e δ(q₂, 'a') = q₃ , acrescentaremos uma transição de q₁ para q₃  com 'a';
    novas_transicoes: set[tuple[int, str, int]] = set()
    for p in A.estados:
        for char in alfabeto_sem_e:
            destinos: set[int] = set()
            # Para cada estado em E(p):
            for q in fecho_total[p]:
                for origem, simbolo, destino in A.transicoes:
                    if origem == q and simbolo == char:
                        destinos.add(destino)

            for destino in destinos:
                novas_transicoes.add((p, char, destino))

    return Automato(
        A.estados, alfabeto_sem_e, A.inicial, novos_finais, novas_transicoes
    )


def ler_automatos(nome_arquivo: str) -> list[Automato]:
    """
    Lê dos autômatos em json para um conjunto de Automato()
    """
    with open(nome_arquivo, "r") as arq:
        dados = json.load(arq)

    automatos: list[Automato] = [
        # json: [[1, "0", 2], [2, "1", 1]] -> python: {(1, "0", 2), (2, "1", 1)}
        Automato(
            a["estados"],
            a["alfabeto"],
            a["inicial"],
            a["finais"],
            {tuple(transicao) for transicao in a["transicoes"]},
        )
        for a in dados
    ]

    return automatos


def escrever_automatos(nome_arquivo: str, automatos: list[Automato]):
    """
    Escreve uma lista de Automato() em um arquivo json
    """
    with open(nome_arquivo, "w") as arq:
        automatos_dict = [A.to_dict() for A in automatos]
        json.dump(automatos_dict, arq, indent=4, ensure_ascii=False)


def main():
    automatos: list[Automato] = ler_automatos("automato.json")
    automatos_sem_e: list[Automato] = []

    for A in automatos:
        B = eliminar_epsilon(A)
        automatos_sem_e.append(B)

        print(f"Autômato antes: {A}\n")
        print(f"Autômato depois: {B}")

        print("\n---\n")

    escrever_automatos("automato_sem_e.json", automatos_sem_e)


if __name__ == "__main__":
    main()
