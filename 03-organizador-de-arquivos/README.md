# Organizador de arquivos em Python

Automação que separa os arquivos de uma pasta em subpastas de imagens, documentos, planilhas, código, compactados e outros. Por padrão, apenas mostra o plano de organização.

**Nível:** iniciante a intermediário. **Tecnologias:** Python 3.10+, `pathlib`, `shutil`, `argparse` e `unittest`.

## Como experimentar

Abra o terminal nesta pasta. Se estiver na pasta que reúne os projetos, execute primeiro `cd 03-organizador-de-arquivos`.

Crie uma pasta de exemplo vazia e um arquivo para praticar:

```console
mkdir exemplo
python -c "from pathlib import Path; Path('exemplo/nota.txt').write_text('Arquivo para praticar', encoding='utf-8')"
python organizar.py exemplo
```

Resultado:

```text
Simulação: nenhum arquivo será movido.
  nota.txt -> documentos/nota.txt
Para executar, repita o comando incluindo --aplicar.
```

Para executar o plano:

```console
python organizar.py exemplo --aplicar
```

O arquivo ficará em `exemplo/documentos/nota.txt`. Você também pode passar outro caminho entre aspas se ele contiver espaços.

## Como o código funciona

O fluxo é: **examinar a pasta → classificar cada arquivo → escolher destinos disponíveis → mostrar o plano → aplicar se solicitado**.

- `EXTENSOES` associa cada categoria a um conjunto de extensões. Para incluir outro formato, acrescente sua extensão nesse dicionário.
- `categoria()` consulta `Path.suffix`, que retorna a última extensão. `lower()` permite tratar `.JPG` e `.jpg` da mesma forma. Extensões desconhecidas vão para `outros`.
- `planejar()` examina apenas os arquivos diretamente dentro da pasta. Ignora subpastas, links simbólicos e nomes começando com ponto. Não modifica nada.
- Se um nome de destino já existir, o planejamento acrescenta um número, como `nota_1.txt`. O conjunto `reservados` também impede dois itens do mesmo plano de receberem o mesmo destino.
- `mover_sem_sobrescrever()` abre o novo arquivo no modo `xb`: escrita binária com criação exclusiva. Esse modo falha se alguém tiver criado o destino depois do planejamento. A função copia o conteúdo e só então remove a origem.
- `main()` mostra o plano e só chama a movimentação quando recebe `--aplicar`.

### Por que separar planejamento e execução?

Essa separação permite conferir o resultado antes de modificar os arquivos e testar a classificação sem realizar movimentações. A mesma ideia pode ser usada em automações que renomeiam arquivos em lote.

## Testes

```console
python -m unittest discover -v
```

Os testes usam arquivos fictícios em pastas temporárias. Verificam a simulação, os conflitos de nomes, a preservação da origem quando a cópia falha e um destino criado depois do planejamento.

## Limites e próximos passos

O programa não entra em subpastas e não possui comando de desfazer. A movimentação preserva o conteúdo, mas não promete preservar metadados como datas e permissões originais. Como faz uma cópia antes de remover a origem, precisa de espaço livre para o arquivo copiado.

Se uma movimentação falhar, o programa para; os arquivos já organizados continuam no destino. Se apenas a remoção da origem falhar, as duas cópias permanecem. Use uma pasta sem arquivos sendo alterados por outro programa durante a execução.

Desafios para praticar:

1. Adicionar categorias para áudio e vídeo.
2. Mostrar a quantidade de arquivos por categoria na simulação.
3. Gravar um registro das movimentações para implementar um comando de desfazer.

## Como explicar numa entrevista

“Criei uma automação que classifica arquivos por extensão. Separei o planejamento da execução para permitir uma simulação, resolvi conflitos de nomes e só removo a origem depois de terminar a cópia.”

Pergunta para praticar: por que verificar se o destino existe durante o planejamento não basta para impedir uma sobrescrita depois?
