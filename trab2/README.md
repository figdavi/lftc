# Trabalho de implementação 2

- Alunos: [Davi Figueiredo](https://github.com/figdavi)
  e [Davi Coutinho](https://github.com/Davi394)

## Tema

Simulador de Máquina de Turing.

## Solução

1. Carrega a máquina a partir do arquivo JSON (transições, estado inicial, estados finais e símbolo branco).
2. Prepara a fita inicial com a entrada fornecida.
3. Move a cabeça de leitura/escrita conforme as transições definidas.
4. Registra cada passo contendo:
   - Estado atual
   - Conteúdo da fita
   - Posição da cabeça
5. Encerra quando atinge um estado final ou quando não existe transição válida.
6. Gera um arquivo `resultado_mt.json` contendo:
   - Fita final sem brancos
   - Estados utilizados
   - Alfabeto da fita
   - Número de passos
   - Todas as configurações do processamento (campo `"passos"`)

## Estrutura do Projeto

```bash
.
├── main.py              # Código principal (simulador)
├── mt_soma.json         # Configuração da Máquina de Turing para soma
├── mt_divisao.json         # Configuração da Máquina de Turing para divisão
...
├── resultado_mt.json    # Resultado gerado após a execução
└── README.md
```

## Representação da Máquina:

```json
{
  "name": "MT_soma",
  "blank": "_",
  "initial_state": "q1",
  "final_states": ["q4"],
  "transitions": [
    {
      "state": "q1",
      "read": "1",
      "next_state": "q2",
      "write": "X",
      "move": "R"
    },
    {
      "state": "q1",
      "read": "$",
      "next_state": "q1",
      "write": "$",
      "move": "R"
    },
    {
      "state": "q1",
      "read": "@",
      "next_state": "q4",
      "write": "@",
      "move": "L"
    },

    {
      "state": "q2",
      "read": "1",
      "next_state": "q2",
      "write": "1",
      "move": "R"
    },
    {
      "state": "q2",
      "read": "$",
      "next_state": "q2",
      "write": "$",
      "move": "R"
    },
    {
      "state": "q2",
      "read": "@",
      "next_state": "q2",
      "write": "@",
      "move": "R"
    },
    {
      "state": "q2",
      "read": "_",
      "next_state": "q3",
      "write": "1",
      "move": "L"
    },

    {
      "state": "q3",
      "read": "1",
      "next_state": "q3",
      "write": "1",
      "move": "L"
    },
    {
      "state": "q3",
      "read": "@",
      "next_state": "q3",
      "write": "@",
      "move": "L"
    },
    {
      "state": "q3",
      "read": "$",
      "next_state": "q3",
      "write": "$",
      "move": "L"
    },
    {
      "state": "q3",
      "read": "X",
      "next_state": "q1",
      "write": "X",
      "move": "R"
    }
  ]
}
```

## Execução

Para executar o código é necessário ter **Python 3.9+** ([Download](https://www.python.org/downloads/))

1. Clone o repositório e vá para pasta `lftc/trab1`

```bash
git clone https://github.com/figdavi/lftc.git
cd lftc/trab2
```

2. Na parte da função main em `MT.py`, altere o arquivo da máquina de Turing de entrada e a entrada inicial.

3. Rode o programa

```bash
python MT.py
```

- Use `python3 main.py` se `python main.py` não funcionar

4. O resultado será impresso no cmd/terminal e escrito em `resultado_mt.json`
