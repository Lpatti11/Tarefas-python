# Analisador de gastos em CSV

Programa que lê uma planilha exportada como CSV, soma as despesas por categoria e permite filtrar um mês. Inclui dados fictícios para experimentar imediatamente.

**Nível:** iniciante a intermediário. **Tecnologias:** Python 3.10+, `csv`, `datetime`, `decimal`, `argparse` e `unittest`.

## Como executar

Abra o terminal nesta pasta. Se estiver na pasta que reúne os projetos, execute primeiro `cd 02-analisador-de-gastos`.

```console
python gastos.py exemplo.csv
python gastos.py exemplo.csv --mes 2026-09
```

Resultado do segundo comando:

```text
Despesas: 7
Total: R$ 363,30
  alimentacao: R$ 250,90
  educacao: R$ 60,00
  transporte: R$ 27,90
  lazer: R$ 24,50
```

## Formato do arquivo

Use texto em UTF-8, colunas nesta ordem e ponto e vírgula como separador:

```csv
data;descricao;categoria;valor
2026-09-01;Almoço;alimentacao;25,90
2026-09-02;Ônibus;transporte;6,00
```

- `data`: data no formato `AAAA-MM-DD`.
- `descricao`: texto identificando a despesa.
- `categoria`: grupo utilizado no resumo. Maiúsculas e espaços nas pontas são normalizados.
- `valor`: número positivo, até 999999999,99, com no máximo duas casas decimais. Aceita ponto ou vírgula decimal; não use separador de milhares nem `R$`.

Se quiser experimentar dados próprios, guarde-os em uma pasta chamada `dados-pessoais`, já incluída no `.gitignore`.

## Como o código funciona

O fluxo é: **abrir o CSV → validar as linhas → filtrar o mês → agrupar por categoria → exibir os totais**.

- `ler_gastos()` usa `csv.DictReader`: cada linha vira um dicionário com as chaves do cabeçalho. A função converte o texto da data e do valor para tipos apropriados e informa a linha quando encontra um problema.
- `resumir()` percorre as despesas, ignora meses fora do filtro e acumula os valores em um dicionário. `get(categoria, Decimal("0"))` começa em zero quando uma categoria aparece pela primeira vez.
- `moeda()` prepara o valor para exibição com duas casas decimais e vírgula.
- `main()` recebe as opções do terminal e ordena as categorias do maior total para o menor. Empates ficam em ordem alfabética.

### Por que usar Decimal?

`float` representa números em base binária, e alguns valores decimais não têm representação exata. Por exemplo, `0.1 + 0.2` pode resultar em `0.30000000000000004`. Ao construir `Decimal` diretamente a partir de texto, os centavos do CSV são preservados.

### Por que separar leitura e resumo?

A leitura cuida do formato do arquivo; o resumo cuida do cálculo. Essa separação permite testar a soma sem depender do terminal e reutilizá-la em outra interface.

## Testes

```console
python -m unittest discover -v
```

Os testes conferem a soma de centavos, a normalização de categorias, o filtro mensal, um mês sem despesas e a rejeição de linhas inválidas.

## Limites e próximos passos

O programa considera apenas despesas positivas em reais. Não trata receitas, estornos ou conversão de moedas. Se uma linha for inválida, interrompe o relatório para não apresentar uma soma parcial como se estivesse completa.

Desafios para praticar:

1. Mostrar o percentual do total de cada categoria.
2. Exportar o resumo para outro CSV.
3. Adicionar um filtro por categoria e seus testes.

## Como explicar numa entrevista

“Li um CSV com a biblioteca padrão, validei as linhas e agrupei despesas por categoria. Usei Decimal para preservar os centavos e separei a leitura do cálculo. O usuário pode filtrar um mês pelo terminal.”

Pergunta para praticar: o que acontece se você ignorar silenciosamente uma linha inválida em um relatório?
