# WWTP | Comparação AERMOD–CALPUFF

[Visualizador online](https://ricardosqzz.github.io/wwtp-dispersion/) · [Códigos e cálculos](https://ricardosqzz.github.io/wwtp-dispersion/codigos/)

## Organização

- `codigo/`: rotinas atuais e dependências locais.
- `config/`: parâmetros de análise, quando aplicáveis.
- `dados/`: derivados mínimos e estatísticas consolidadas.
- `docs/`: visualizador e prévias para navegação.
- `documentacao/codigos/`: documentação por rotina.

As bases brutas, ambientes de programação, arquivos horários volumosos, cópias descontinuadas e documentos temporários não são duplicados. Ajuste `codigo/caminhos_projeto.json` e instale `codigo/requirements-calculo.txt` para usar outra árvore de dados. Rotinas de geração completa exigem as fontes documentadas nos cabeçalhos.

## Comparação dos modelos

Os resultados são comparação entre modelos, não validação observacional. Os arquivos horários completos devem ser fornecidos nos caminhos indicados para regenerar todos os indicadores. As unidades são identificadas somente como WWTP 1 e WWTP 2 nos produtos públicos.
