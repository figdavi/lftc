# Trabalho de implementação 1

- Alunos: Davi Figueiredo e [Davi Coutinho](https://github.com/Davi394)

## Tema

Converter um autômato finito não-determinístico (AFND) com epsilon-transições para um AFND sem epsilon-transições.

## Solução

![alt text](images/Introdução%20à%20Teoria%20da%20Computação%20%20(Pág.%2057)%20-%20Michael%20Sipser.png)

- Ref: Introdução à Teoria da Computação, 3 ed. (Pág. 57) - Michael Sipser.

### Passos

1. Se 'a' ∈ Σ, δ(q₁, ε) = q₂ e δ(q₂, 'a') = q₃ , acrescentaremos uma transição de q₁ para q₃  com 'a';

![alt text](images/passo_1.png)


2. Se δ(q₁, ε) = q₂ e q₂ ∈ F, acrescentamos q₁ a F.

![alt text](images/passo_2.png)

### Representação do autômato

Automato: 5-tupla (Q: conjunto finito de estados, Σ: Alfabeto, δ: função de transição, q₀: estado inicial, F: conjunto de estados finais)

```json
{
    "Automato-1": {
        "estados": [1, 2, 3],
        "alfabeto": ["a", "b", "ε"],
        "inicial": 1,
        "finais": [2],
        "transicoes": [
            [1, "ε", 2],
            [1, "a", 2],
            [2, "a", 3],
            [3, "b", 2]
        ]
    }
}
```
