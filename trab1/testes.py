from main import Automato, eliminar_epsilon


def test_automato_slide_7_pag_11():
    A = Automato(
        estados={1, 2, 3},
        alfabeto={"a", "b", "ε"},
        inicial=1,
        finais={2},
        transicoes={(1, "a", 2), (1, "ε", 3), (2, "a", 3), (3, "b", 2)},
    )

    B = eliminar_epsilon(A)

    assert B.estados == A.estados
    assert B.alfabeto == A.alfabeto - {"ε"}
    assert B.finais == A.finais
    assert B.transicoes == {(1, "a", 2), (1, "b", 2), (2, "a", 3), (3, "b", 2)}


def test_automato_slide_7_pag_16():
    A = Automato(
        estados={1, 2, 3, 4},
        alfabeto={"a", "b", "ε"},
        inicial=1,
        finais={4},
        transicoes={
            (1, "a", 2),
            (2, "b", 3),
            (3, "a", 3),
            (3, "ε", 4),
            (4, "b", 1),
        },
    )

    B = eliminar_epsilon(A)

    assert B.estados == A.estados
    assert B.alfabeto == A.alfabeto - {"ε"}
    assert B.finais == {3, 4}
    assert B.transicoes == {
        (1, "a", 2),
        (2, "b", 3),
        (3, "a", 3),
        (3, "b", 1),
        (4, "b", 1),
    }


def test_automato_prova():
    A = Automato(
        estados={1, 2, 3, 4, 5},
        alfabeto={"a", "b", "ε"},
        inicial=1,
        finais={4},
        transicoes={
            (1, "a", 2),
            (1, "b", 5),
            (2, "ε", 3),
            (3, "a", 4),
            (3, "b", 5),
            (4, "ε", 5),
            (5, "a", 1),
            (5, "b", 5),
        },
    )

    B = eliminar_epsilon(A)

    assert B.estados == A.estados
    assert B.alfabeto == A.alfabeto - {"ε"}
    assert B.finais == A.finais
    assert B.transicoes == {
        (1, "a", 2),
        (1, "b", 5),
        (2, "a", 4),
        (2, "b", 5),
        (3, "a", 4),
        (3, "b", 5),
        (4, "a", 1),
        (4, "b", 5),
        (5, "a", 1),
        (5, "b", 5),
    }
