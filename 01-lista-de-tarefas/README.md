# Lista de tarefas em Python

Aplicação de terminal para cadastrar, listar e concluir tarefas. Os dados ficam em um arquivo JSON e continuam disponíveis depois que o programa fecha.

**Nível:** iniciante. **Tecnologias:** Python 3.10+, `argparse`, `json`, `pathlib` e `unittest`.

## Como executar

Abra o terminal nesta pasta. Se estiver na pasta que reúne os três projetos, execute primeiro `cd 01-lista-de-tarefas`.

```console
python tarefas.py adicionar "Estudar funções em Python"
python tarefas.py adicionar "Fazer meu primeiro commit"
python tarefas.py listar
python tarefas.py concluir 1
python tarefas.py listar
```

Na última listagem, considerando um cadastro inicialmente vazio:

```text
[x] 1: Estudar funções em Python
[ ] 2: Fazer meu primeiro commit
```

O arquivo `tarefas.json` é criado ao lado do programa na primeira gravação. Ele está no `.gitignore` para que suas tarefas pessoais não entrem no repositório.

Para listar apenas tarefas pendentes ou concluídas:

```console
python tarefas.py listar --status pendentes
python tarefas.py listar --status concluidas
```

Use `concluidas` sem acento no comando. Sem `--status`, a listagem continua mostrando todas as tarefas. O filtro apenas seleciona o que aparece no terminal, sem remover tarefas do arquivo.

Para usar outro arquivo, informe a opção antes do comando. A pasta de destino deve existir:

```console
python tarefas.py --arquivo estudo.json adicionar "Praticar listas"
python tarefas.py --arquivo estudo.json listar
python tarefas.py --help
```

## Como o código funciona

O fluxo é: **ler o comando → carregar o JSON → executar a operação → salvar se houve alteração**.

- `carregar()` transforma o JSON em uma lista de dicionários. Se o arquivo ainda não existe, retorna uma lista vazia. Se estiver inválido, interrompe a operação.
- `adicionar()` remove espaços nas pontas do título, valida o texto e calcula o próximo ID. `append()` coloca a nova tarefa no final da lista.
- `concluir()` percorre a lista procurando o ID informado. Quando encontra, muda `concluida` para `True`.
- `filtrar()` fica antes de `main()` e recebe a lista e o status desejado. Para `todas`, retorna uma cópia da lista. Para `pendentes` ou `concluidas`, percorre as tarefas e coloca as correspondentes em uma nova lista. A comparação `status == "concluidas"` produz `True` para concluídas e `False` para pendentes.
- `salvar()` escreve um arquivo temporário e depois substitui o JSON. Assim, uma falha durante a escrita do temporário não deixa o arquivo original pela metade.
- `main()` usa `argparse` para entender os comandos e apresentar o resultado. Listar tarefas não grava o arquivo.

Cada tarefa tem esta estrutura:

```json
{"id": 1, "titulo": "Estudar Python", "concluida": false}
```

Um **dicionário** agrupa os campos de uma tarefa. Uma **lista** reúne várias tarefas. O **JSON** representa esses dados em texto no disco.

O bloco `if __name__ == "__main__":` executa `main()` quando você abre o programa pelo terminal, mas permite importar as funções nos testes sem iniciar a aplicação.

## Testes

```console
python -m unittest discover -v
```

Os testes verificam o ciclo de cadastro, conclusão e persistência, além de título vazio, ID inexistente e arquivos inválidos. Usam pastas temporárias e não alteram suas tarefas.

## Limites e próximos passos

O projeto é local, para uma pessoa, sem edição ou remoção de tarefas. Ele não coordena gravações de dois processos simultâneos.

Desafios para praticar:

1. Adicionar uma busca por palavra no título, combinando-a com o filtro de situação.
2. Criar o comando `reabrir` e um teste para ele.
3. Incluir uma data de criação e exibi-la na listagem.

## Como explicar numa entrevista

“O programa recebe comandos pelo terminal, mantém as tarefas em uma lista de dicionários e salva os dados em JSON. Separei as operações da interface para poder testá-las. Valido o arquivo antes de usá-lo e salvo por meio de um temporário.”

Experimente responder também: por que um arquivo JSON é suficiente aqui? O que mudaria se várias pessoas usassem o programa ao mesmo tempo?
