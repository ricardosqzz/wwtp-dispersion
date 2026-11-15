# Preparação para discutir o pôster COPASA

Sessão 5 do CMAS

Este guia acompanha o pôster corrente, conferido em 14 de novembro de 2026, e prepara a discussão sobre a comparação de AERMOD e CALPUFF. As duas estações permanecem identificadas como WWTP 1 e WWTP 2. Os resultados descrevem os cenários executados. As análises estatísticas não corrigem nem recalibram as concentrações dos modelos.

## A pergunta que organiza o estudo

Uma comparação baseada apenas no maior valor previsto pode esconder diferenças relevantes entre modelos. Dois campos podem apresentar uma ordenação espacial parcialmente parecida, mas divergir na magnitude das concentrações. Também podem discordar principalmente perto das fontes e aproximar-se em distâncias maiores. O estudo combina mapas de máximos, indicadores anuais, distribuições horárias e resumos por distância para examinar essas diferenças.

Essa estrutura é útil para planejar monitoramento. Se os modelos divergem fortemente nos mesmos receptores próximos, esses locais ajudam a testar as hipóteses do cenário e a representação das fontes. Se o contraste muda ao longo da distância, uma campanha restrita ao ponto de máximo pode não representar o comportamento do entorno. A comparação oferece um diagnóstico para orientar essa avaliação, sem escolher automaticamente um modelo vencedor.

## O que cada modelo representa

O AERMOD é um modelo de pluma que trabalha com uma representação estacionária das condições de cada período meteorológico e conceitos da camada limite atmosférica. O CALPUFF representa o transporte de puffs em condições não estacionárias, com campos meteorológicos que podem variar no espaço e no tempo. Essas diferenças de formulação ajudam a motivar a comparação, mas não demonstram, isoladamente, a causa de toda diferença observada entre duas execuções.

O estudo utiliza os processamentos meteorológicos correspondentes a cada sistema. Uma afirmação causal sobre o efeito exclusivo da formulação exigiria cenários controlados, com harmonização das demais escolhas e dos relógios. A discussão principal do pôster permanece na resposta dos campos de concentração. O relatório técnico conserva as verificações das entradas e dos períodos, que devem ser consultadas se a pessoa perguntar sobre equivalência completa dos cenários.

## Inventário e significado das taxas

As taxas médias totais do inventário são aproximadamente 0,05728 g/s na WWTP 1 e 0,06866 g/s na WWTP 2. A massa de processo é calculada e depois distribuída entre as superfícies, evitando repetir a massa total em cada reator. Quando a geometria representada muda, o fluxo superficial deve ser ajustado para manter a taxa total correspondente.

Os reatores UASB correspondem a 72% da emissão da WWTP 1. Na WWTP 2, os filtros percoladores correspondem a 73%. UASB significa upflow anaerobic sludge blanket, um reator anaeróbio de manta de lodo e fluxo ascendente. A unidade em que o sulfeto é produzido e a etapa em que o gás é transferido para a atmosfera podem ser diferentes. Assim, uma unidade posterior pode concentrar a emissão estimada no inventário, sem que isso constitua uma regra geral para todas as estações de tratamento.

A leitura deve distinguir massa total, fluxo superficial, altura de liberação e cota de terreno. A cota posiciona a base da fonte, enquanto a altura de liberação descreve o ponto de emissão em relação a essa base. A utilização de modelos de terreno diferentes não torna esses parâmetros automaticamente equivalentes. Não acrescente ao pôster uma explicação causal que não tenha sido testada em cenários controlados.

## Receptores e distâncias

A grade AERMOD tem 1.790 registros em 1.789 posições únicas. Dois identificadores coincidem espacialmente e foram preservados como registros cadastrais, sem contar a mesma posição duas vezes nas estatísticas espaciais. A comparação utiliza pares de posições nativas coincidentes, com a tolerância documentada, sem interpolar concentrações para fabricar correspondências.

O recorte até 1.800 m reúne 562 pares na WWTP 1 e 556 na WWTP 2. A distância é calculada até a superfície emissora mais próxima, considerando a união das geometrias das fontes AERMOD. Ela não é distância ao centro da estação, ao prédio administrativo ou necessariamente ao limite geral da WWTP. Um receptor dentro de uma superfície tem distância geométrica zero.

Os percentuais calculados para esses pares descrevem receptores. Eles não são automaticamente frações da população exposta ou da área territorial, porque a grade é mais densa em alguns locais e a estatística não usa um peso populacional.

## O P95 horário em cada receptor

Para cada modelo e cada receptor, considera-se a distribuição das concentrações horárias válidas de 2024 e calcula-se o percentil 95. Esse indicador descreve a parte superior da distribuição temporal naquele ponto, sem ser seu máximo absoluto. Uma concentração acima do P95 corresponde à cauda superior da série, sujeita aos empates e ao método de cálculo do quantil.

As séries nativas preservam as regras de validade dos modelos. Em 2024, a comparação documentada utiliza 8.496 horas válidas do AERMOD e 8.784 do CALPUFF. Portanto, o conjunto principal compara distribuições nativas. Ele não é uma comparação de erros horários sincronizados entre dois modelos e uma estação observada. O relógio e a máscara de horas comuns precisam ser tratados explicitamente em uma futura comparação temporal controlada.

O uso do P95 não é uma correção da superestimação. É a escolha de um indicador de cauda. Se a série estiver enviesada, o quantil também pode estar. Não descarte os maiores valores com a justificativa de tornar os modelos mais parecidos.

## Como ler os boxplots

Primeiro há um P95 temporal por receptor. Os boxplots agrupam esses valores nas três faixas de distância mostradas no painel. Cada observação do boxplot é, portanto, um receptor. A caixa representa o primeiro e o terceiro quartil desse conjunto espacial, e a linha central representa a mediana. As hastes seguem a regra de 1,5 vezes o intervalo interquartil.

Os pontos extremos não são desenhados nesse painel para preservar a leitura. Eles não foram retirados das tabelas primárias ou dos indicadores que consideram todos os pares. Também é importante perceber que um boxplot com mediana baixa não significa que todas as horas de todos os receptores sejam baixas. Ele resume o conjunto de percentis temporais por posição.

Essas caixas são diferentes do atlas complementar que mostra uma distribuição temporal em cada ponto. Não use a explicação de uma representação para a outra. O título, a unidade estatística e a regra de agrupamento precisam acompanhar a leitura.

## Perfis por distância e diferença entre modelos

Os perfis detalhados utilizam seis faixas, de 0 a 50, 50 a 100, 100 a 200, 200 a 300, 300 a 500 e 500 a 1.800 m. Em cada faixa, o gráfico apresenta a mediana e o intervalo interquartil dos P95 dos receptores. O número de pares aparece na figura. As categorias ocupam larguras semelhantes na página, embora representem intervalos físicos de extensão diferente.

As curvas entre os seis resumos usam PCHIP, uma interpolação que preserva a forma para apresentação. Ela não interpola o campo de concentrações nem acrescenta horas ou receptores aos cálculos. As bandas são intervalos entre quartis espaciais, sem a interpretação de intervalo de confiança de uma média ou de uma curva física contínua.

Na primeira faixa da WWTP 1, a mediana do AERMOD é aproximadamente 38,47 µg/m³ e a do CALPUFF é aproximadamente 0,92 µg/m³, uma diferença de cerca de -37,55 µg/m³ quando se calcula CALPUFF menos AERMOD. A diferença diminui nas faixas seguintes e pode mudar de sinal em distâncias maiores. Na WWTP 2, o contraste também é negativo e maior perto das fontes, enquanto algumas faixas intermediárias apresentam sinal positivo.

O painel inferior calcula a diferença entre as duas medianas de cada faixa. Essa grandeza não é necessariamente igual à mediana das diferenças pareadas entre receptores. A ordem de cálculo importa, porque a mediana é uma operação não linear. Essa distinção deve ser mantida ao explicar os valores negativos e positivos.

## Correlação espacial e fator dois

A correlação de Spearman dos P95 é aproximadamente 0,574 na WWTP 1 e 0,626 na WWTP 2. Ela informa a associação entre as ordenações espaciais dos dois conjuntos. Um valor positivo indica que receptores relativamente mais altos em um modelo tendem a também ser relativamente mais altos no outro, com dispersão nessa relação.

A proporção dentro de um fator dois é 35,9% na WWTP 1 e 24,8% na WWTP 2. A regra verifica se a concentração de um modelo está entre a metade e o dobro da do outro. A implementação usa desigualdades multiplicativas e trata os zeros explicitamente, sem gerar divisões inválidas. Dois zeros concordam nessa regra. Um zero e um valor positivo não satisfazem o fator dois.

Os dois indicadores respondem a perguntas distintas. Um modelo pode ordenar os locais de maneira parcialmente semelhante e produzir concentrações sistematicamente mais altas. Por isso os valores de Spearman não compensam as proporções baixas dentro de fator dois. Nenhum dos dois indicadores informa qual modelo está mais próximo da atmosfera real na ausência de observações compatíveis.

Os receptores têm dependência espacial. Por esse motivo, o pôster não apresenta um valor p calculado como se todos fossem amostras independentes. Os resultados são descritivos no recorte analisado. Avaliações inferenciais precisam considerar a estrutura espacial e temporal e a pergunta estatística específica.

## Mapas de 24 horas e de longa duração

O mapa de 24 horas mostra o maior valor nativo de cada receptor. Um ponto pode atingir esse máximo em um dia e outro ponto em um dia diferente. O produto é um envelope espacial de máximos. Ele não representa necessariamente uma pluma que ocorreu inteira naquele formato em uma única data.

O anual corresponde à maior média de ano-calendário entre 2024 e 2025 em cada receptor. Não é uma média dos dois anos, nem um máximo móvel de 8.760 horas. O CALPUFF tem 8.784 horas em 2024, um ano bissexto, e 8.732 de 8.760 em 2025, equivalentes a 99,68% de cobertura. As horas faltantes não foram inventadas para completar o calendário. As médias nativas preservam seus denominadores próprios.

A análise de 2024 isolado está disponível como sensibilidade para examinar o papel do ano quase completo. A comparação controlada entre médias ainda exige atenção às janelas, aos relógios e às máscaras. A mesma cautela se aplica ao interpretar respostas condicionadas à meteorologia processada por cada sistema.

## Cores unidades e referência de exibição

As cores dos cenários usam uma escala linear compartilhada por duração. A classe cinza indica valores abaixo de 0,7 µg/m³, adotados como referência inferior de apresentação. Essa referência não é um limiar universal de percepção de odor e não transforma médias diárias ou anuais em critérios de incômodo. A ausência de cor intensa não demonstra ausência de efeito em qualquer escala temporal.

A escala superior em ppb expressa a mesma concentração de H2S. A conversão convencional do pôster considera 25 °C e 1 atm, com 1 ppb aproximadamente igual a 1,40 µg/m³. Ela depende da massa molar e das condições de temperatura e pressão. A conversão serve à comunicação dos mesmos resultados e não altera a modelagem. Não aplique esse fator ao material particulado do projeto Congonhas.

## Perguntas e respostas para a discussão

### Pergunta 1

**Qual dos modelos foi melhor?**

O estudo identifica diferenças entre previsões, sem uma referência observada suficiente para determinar superioridade ambiental. A comparação orienta onde medir e quais hipóteses testar. Um modelo mais complexo não é automaticamente mais preciso em todos os pontos ou condições.

**English answer.** We cannot determine the more accurate model without compatible observations. The comparison identifies where evaluation is most informative.

### Pergunta 2

**A análise estatística corrigiu o AERMOD?**

Não houve recalibração das concentrações. Foram calculados indicadores e preparados resumos visuais dos resultados executados. A suavização dos perfis também não modifica os dados dos modelos.

**English answer.** We summarised the executed predictions. No statistical recalibration of model concentrations was applied.

### Pergunta 3

**O P95 é calculado antes ou depois de reunir os receptores?**

O percentil é calculado na série horária de cada receptor. Só depois os valores são reunidos por faixa de distância para produzir o boxplot e o perfil espacial.

**English answer.** We calculate the hourly P95 at each receptor first, then summarise those values across distance bands.

### Pergunta 4

**Por que a correlação parece razoável e o fator dois é baixo?**

Spearman avalia ordenação. O fator dois avalia proximidade de magnitude. Os receptores podem manter parte de sua ordenação e ainda apresentar diferenças multiplicativas grandes entre os modelos.

**English answer.** Spatial ranking and agreement in magnitude are different properties. Partial rank agreement can coexist with large concentration differences.

### Pergunta 5

**As bandas são intervalos de confiança?**

As bandas representam o primeiro ao terceiro quartil entre receptores da faixa. Elas descrevem heterogeneidade espacial e não incerteza inferencial de uma média.

**English answer.** The shading is the spatial interquartile range, not a confidence interval.

### Pergunta 6

**A curva mostra um decaimento contínuo medido ao longo de uma linha?**

Os resumos vêm de faixas de distância com receptores em diferentes direções. A conexão entre seis pontos é visual. Não se trata de uma trajetória única medida ou de um perfil físico estimado continuamente.

**English answer.** The curve connects distance-band summaries from receptors in different directions. It is not a measured continuous transect.

### Pergunta 7

**Os mapas máximos ocorreram no mesmo dia?**

Não necessariamente. Cada receptor recebe seu próprio máximo, que pode ocorrer em outro dia. Para discutir um episódio específico, é necessário selecionar uma data comum e representar o campo correspondente.

**English answer.** The maps are receptor-specific maximum envelopes. An event map would require a common date.

### Pergunta 8

**Por que 2024 tem mais de 8.760 horas?**

É um ano bissexto, com 366 dias e 8.784 horas. Não se deve eliminar um dia para impor a duração de um ano comum. O ano de 2025 é quase completo e sua cobertura está explicitada.

**English answer.** 2024 is a leap year with 8,784 hours. We retain the calendar rather than forcing an 8,760-hour year.

### Pergunta 9

**Valores abaixo de 0,7 significam ausência de odor?**

O valor é uma referência de exibição, sujeita à variabilidade das referências de percepção. A interpretação de odor depende também da duração, frequência, sensibilidade e do método de avaliação. O mapa anual não comprova ausência ou presença de incômodo em episódios curtos.

**English answer.** It is a display reference, not a universal odour threshold for daily or annual means.

### Pergunta 10

**O inventário é a mesma coisa que a concentração recebida?**

O inventário descreve a taxa de emissão das fontes. A concentração também depende da dispersão e da posição dos receptores. Uma unidade que domina a massa emitida não necessariamente domina todos os locais e durações de recepção na mesma proporção.

**English answer.** Emission rates describe the source. Received concentrations also depend on dispersion and receptor location.

### Pergunta 11

**As diferenças decorrem exclusivamente da formulação dos modelos?**

Essa conclusão exigiria uma comparação controlada com harmonização completa das demais escolhas. O pôster compara os cenários executados e seus resultados. O relatório técnico registra verificações adicionais das entradas, alturas, dispersão inicial e meteorologia, sem atribuir automaticamente todo contraste a um único mecanismo.

**English answer.** This is a comparison of the executed scenarios. Isolating model formulation would require fully controlled and harmonised sensitivity runs.

### Pergunta 12

**Existe alguma questão de horário na comparação?**

As distribuições principais são nativas de cada modelo e não exigem afirmar que as horas estão sincronizadas. Para análises condicionais ou erros pareados por hora, é necessário confirmar convenções de relógio e janelas comuns. O fuso ou deslocamento não deve ser escolhido para maximizar a correlação.

**English answer.** The main analysis compares native distributions. Hour-by-hour comparisons require verified clock conventions and common validity masks.

### Pergunta 13

**Por que não usar o RANK para toda a comparação temporal?**

Os arquivos RANK organizam extremos e outros resumos conforme o processamento. Eles não substituem necessariamente uma série completa de concentração em cada ponto e hora. As distribuições horárias e médias anuais foram obtidas dos arquivos de concentração e saídas horários correspondentes, com conferência dos resumos.

**English answer.** Ranked outputs do not replace complete hourly receptor series. Distribution statistics use the corresponding concentration outputs.

### Pergunta 14

**O número de receptores indica área afetada ou população?**

Não diretamente. A grade tem uma geometria de amostragem e pode ser mais densa perto de certas fontes. Para converter o resultado em área ou exposição populacional, seria necessário um suporte e uma ponderação específicos.

**English answer.** These percentages describe receptors, not population or territorial area.

### Pergunta 15

**Qual é o próximo teste mais útil?**

Priorizar medições em locais e períodos compatíveis, incluindo as regiões de maior discordância, e executar cenários controlados para investigar os mecanismos que influenciam o resultado. A comparação deve conservar a massa, documentar os parâmetros e separar efeito de formulação, meteorologia e escolhas da representação das fontes.

**English answer.** Compatible measurements and controlled sensitivity runs are the next steps for evaluating representativeness and separating mechanisms.

## Informações que devem ficar como apoio técnico

Se houver uma pergunta específica sobre equivalência das entradas, consulte a auditoria, em vez de responder apenas que as duas simulações usam o mesmo inventário. Existem verificações documentadas de alturas de liberação e dispersão inicial que precisam ser consideradas na comparação controlada. Cota de terreno e altura de emissão são parâmetros diferentes. Essa informação não altera os resultados exibidos nem deve ser ocultada quando for relevante para a interpretação.

Preserve a privacidade das unidades. Nos materiais públicos, utilize WWTP 1 e WWTP 2 e os elementos genéricos já apresentados. Não é necessário informar os nomes reais para explicar as taxas, geometrias ou estatísticas.

## Fontes para aprofundamento

Os números foram conferidos no PPTX da Sessão 5, em Perfis_comparacao_modelos.json, Concordancia_P95_receptores.json e nos relatórios da rodada atual. A descrição dos modelos pode ser aprofundada na documentação do [AERMOD da US EPA](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models) e nas [instruções oficiais do CALPUFF](https://www.src.com/calpuff/download/CALPUFF_Version6_UserInstructions.pdf). Os conceitos das ferramentas utilizadas constam na documentação de [Spearman no SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) e do [interpolador PCHIP](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html).
