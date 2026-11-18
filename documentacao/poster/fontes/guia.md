# Preparação para discutir o pôster COPASA

Sessão 5 do CMAS

Este guia acompanha o pôster corrente, conferido em 18 de novembro de 2026, e prepara a discussão sobre a comparação de AERMOD e CALPUFF. As duas estações permanecem identificadas como WWTP 1 e WWTP 2. Os resultados descrevem os cenários executados. As análises estatísticas não corrigem nem recalibram as concentrações dos modelos.

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

## Extended technical discussion in English

### What is the atmospheric boundary layer

The atmospheric boundary layer is the lower part of the atmosphere whose behaviour is strongly influenced by exchanges with the surface. During daytime surface heating can generate convective motions. During clear nights surface cooling often creates stable stratification, although wind shear can maintain turbulence. Sunset is not an automatic switch to a completely stagnant layer, and nighttime is not always stable. Cloud cover, wind, terrain and the preceding thermal history all matter.

For a low-level diffuse release, a shallow layer with weak turbulent exchange can keep a similar emitted mass within a smaller effective dilution volume. This can raise near-ground concentration without increasing the emission rate. The study must test this interpretation with the actual meteorological fields and measurements. Surface-layer similarity and a single mixing height do not resolve every intermittent or terrain-driven nocturnal circulation. [EPA model formulation](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_mfd.pdf).

### Monin Obukhov length and its physical meaning

The Monin-Obukhov length, L, has units of metres and describes the relative importance of buoyancy and mechanical shear in surface-layer turbulence. Under the usual sign convention, positive L indicates stable stratification and negative L indicates convective conditions. Near-neutral conditions correspond to a small magnitude of inverse L, rather than L close to zero. The ratio of height to L helps identify how strongly stability modifies a profile at that height.

L is not the depth of the boundary layer, the length of a plume, a receptor distance or a wind speed. Its magnitude should be interpreted together with height, friction velocity and the heat flux. Comparing the absolute L values in two processors without their sign, units and underlying surface treatment can be misleading. When heat flux approaches zero, L can become very large, so inverse L or a properly defined near-neutral category is often easier to diagnose.

In AERMET, L is supplied in the surface file. CALMET also estimates a spatially varying L field. However, the availability of L in CALMET does not mean that this CALPUFF run selected the same dispersion formulation as AERMOD. The submitted CALPUFF setting MDISP=3 is decisive here. The alternative MDISP=2 calculates dispersion from micrometeorological turbulence estimates. It remains a potential controlled sensitivity run, not a change already made. [AERMET guide](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/met/aermet/aermet_userguide.pdf) and [CALMET guide](https://www.calpuff.org/calpuff/download/CALMET_UsersGuide.pdf).

### Friction velocity convective velocity and mixing height

Friction velocity, written u-star, is a velocity scale associated with the turbulent transfer of momentum near the surface. It is expressed in metres per second. It is not simply the wind speed at ten metres, and it is not the velocity of the emitted gas. A small u-star can indicate weak mechanically generated turbulence, while a strong mean wind can coexist with different turbulence intensities depending on roughness and stability.

The convective velocity scale, w-star, characterises buoyancy-driven turbulent motions in a convective boundary layer. It is not the mean vertical wind and should not be interpreted as the plume rise speed. Sensible heat flux indicates the thermal exchange driving or suppressing that buoyant turbulence. AERMET estimates convective and mechanical mixing heights; they describe different production mechanisms and should not be confused with a direct observation of a sharply defined atmospheric lid.

CALMET supplies spatially varying wind and boundary-layer fields. Its configured minimum and maximum overland mixing heights are 50 and 3,000 metres in the supplied input. These are numerical modelling bounds, not measurements establishing that the real nocturnal layer is always at least fifty metres deep. A future sensitivity test must document any changed bounds and assess physical support, rather than selecting the values solely to reduce concentrations. [CALMET guide](https://www.calpuff.org/calpuff/download/CALMET_UsersGuide.pdf).

### The different meanings of sigma

Sigma-y and sigma-z describe the lateral and vertical spread of a concentration distribution and are expressed in metres. Sigma-v and sigma-w describe variability in turbulent velocity components and have units of metres per second. Sigma-theta describes wind-direction variability and is angular. None of these is a confidence interval around the prediction or a direct statement of the model's error.

AERMOD estimates plume dispersion using the vertical structure of wind and turbulence, with different treatments for stable and convective conditions. In the present AERMOD source file, the initial vertical dispersion parameter is 0.1 metre for the area sources. This is an initial release parameter, not the atmospheric sigma-w. It must not be adjusted merely to obtain a preferred concentration. CALPUFF also has source-specific initial spread parameters, in addition to atmospheric dispersion coefficients. Distinguishing initial geometry from subsequent turbulent growth is especially important near a source.

The submitted CALPUFF run uses MDISP=3. Its dispersion coefficients are based on the configured Pasquill-Gifford relationships in rural conditions and McElroy-Pooler relationships in urban conditions. The fact that MTURBVW and MCTURB appear elsewhere in an input template does not make them active in every configuration. Their documented activation conditions must be checked. The current run should not be described as using measured sigma-v and sigma-w to control puff growth. [CALPUFF user guide](https://www.calpuff.org/calpuff/download/CALPUFF_UsersGuide.pdf) and executed technical-option block.

### Stability classes and continuous boundary layer parameters

The Pasquill-Gifford convention groups dispersion conditions into classes commonly denoted A through F, from strongly unstable to strongly stable, with D near neutral. These categories condense meteorological information and should not be treated as measurements of a single turbulence variable. AERMOD's boundary-layer treatment uses continuous scaling parameters and profiles rather than relying solely on one categorical stability label.

This distinction does not by itself establish that one model must be more accurate at the study sites. The observed contrast also depends on source representation, wind fields, terrain, numerical options and temporal coverage. In a controlled experiment, one should hold other relevant assumptions fixed and alter a clearly defined meteorological or dispersion option. Otherwise, an apparent model effect can combine several changes.

### Plume rise and why a treatment surface is different from a stack

For a hot point-source release, plume rise can result from exit momentum and thermal buoyancy. Effective release height then depends on the physical stack height plus the rise of the emitted mixture. Stack diameter, exit velocity, exhaust temperature and ambient conditions are important for that calculation. A rise in the plume centre is different from an increase in its vertical spread.

The present AERMOD sources are AREACIRC and AREAPOLY. They are not hot point stacks, and no aircraft-type buoyant-area option was enabled. The ordinary area-source formulation does not provide the conventional point-stack momentum and thermal plume rise. The CALPUFF point-source count is zero, and the relevant releases are area sources. A general plume-rise switch in a template is not evidence that hot-stack rise governed these wastewater releases. Their height and initial vertical spread are the relevant declared near-source assumptions. [AERMOD user guide](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_userguide.pdf).

If measurements later demonstrate a warm, directed or strongly aerated exhaust, its source representation should be reconsidered using physical discharge information. A higher release height must not be introduced as an arbitrary substitute for plume rise. Similarly, the molecular weight of pure H2S does not justify describing these dilute ambient plumes as a validated dense-gas cloud. The mixture conditions, discharge and dilution need to be characterised.

### What AERMET and CALMET actually received

The supplied AERMET setup uses a SAMSON surface record, FSL upper-air data and a ten-metre wind reference. The surface-characteristic table contains twelve directional sectors but assigns the same annual albedo of 0.18, Bowen ratio of 1.15 and roughness length of 0.30 metre to every sector. Twelve sectors therefore do not mean twelve different observed surface regimes. Seasonal or directional refinement is a possible next step if supported by land-cover and moisture information.

The supplied CALMET setup has NOOBS=0, one surface station, one upper-air station, NM3D=0 and IPROG=0. It is a diagnostic field constrained by those inputs and the terrain and land-surface data. It is not a run driven by a full prognostic WRF field. Its 1.5-kilometre meteorological cells and first-layer faces at 0 and 20 metres should be distinguished from a receptor spacing of tens of metres. The near-source atmosphere is parameterised; it is not directly measured at each fine receptor.

The current meteorological inputs also require a clock audit. CALMET declares the UTC-minus-three convention, while the AERMET/SAMSON labels and processing settings require reconciliation. A nominal one-hour difference was diagnosed in earlier checks, but no shift was selected merely to maximise correlation. The correct solution is to trace each timestamp to the measurement interval and time-zone convention, then apply a reproducible alignment.

### A practical answer about the nocturnal results

If asked why the model still shows high nighttime concentrations, a defensible answer is: “We are still refining the representation of the atmospheric boundary layer. Constant source rates continue through the night, while weak mixing and lower effective transport can produce higher near-ground concentrations. This is a hypothesis supported by the model diagnostics, and we will test it with aligned meteorology and observations. We have not established that actual plant emissions increase at night.”

In the existing hourly summaries for receptors within 100 metres of the sources, AERMOD's mean response peaks around hour five and is lowest around hour fourteen in its native clock, for both plants. CALPUFF's corresponding peaks are around hours seven and eight. These summaries cover the available 2024-2025 simulation output and describe the hourly mean of a spatially averaged concentration. They are not the receptor-level 2024 P95 used in the boxplots, and the clocks have not yet been harmonised. They should not be presented as a measured local nocturnal cycle.

Several mechanisms should be examined separately. First, check whether the observed emission process varies with flow, temperature, sulphide availability and operating conditions. Second, examine wind, u-star, heat flux, stability and mixing height during the high-concentration hours. Third, test release height, initial spread and receptors very close to or inside emitting surfaces. Fourth, examine source and terrain representation. None of these checks can be replaced by simply reducing the emission factor until a figure looks more plausible.

### How an emission timing sensitivity should preserve the inventory

A candidate normalised hourly profile was prepared during an earlier input audit, but preparing a file is different from executing it. The ADI and embedded CALPUFF inputs associated with the results discussed here do not apply that variable profile. We therefore describe the current scenario as constant-rate emissions and retain the prepared profile as a sensitivity candidate, rather than presenting it as an already demonstrated correction.

If a base rate represents an annual mean, an hourly multiplier should be normalised to a mean of one over the defined reference period. The resulting sum of emitted mass should be checked explicitly. If real activity is unavailable, alternative profiles are assumptions and must be labelled as sensitivity scenarios. They are not calibrated emission measurements. It may be appropriate to use different profiles for different treatment processes, but that requires operational evidence.

A nighttime-only concentration reduction obtained by reducing all nighttime emissions would not prove that the boundary-layer treatment has improved. To separate the mechanisms, compare a constant-rate baseline, a mass-preserving timing scenario, a meteorological or dispersion scenario and, if justified, a combined scenario. Assess each against the same independent observations. Preserve a record of which parameters changed and what remained fixed.

### How observational evaluation will be performed

The next comparison needs collocated model receptors and measurements, a common time zone, the same averaging interval and an explicit valid-data mask. Instrument detection limits, calibration, missing data and response time must be documented. Background and unmodelled sources need consideration because a source-only simulation and a total ambient measurement do not necessarily represent the same quantity.

For hourly data, examine time series, diurnal and seasonal behaviour, paired scatter, bias, absolute error and correlation. Stratify the comparison by wind direction, speed, stability and distance where sample size allows it. Do not remove genuine peaks solely because they are inconvenient. Handle censored values and near-zero concentrations transparently. Use an independent period or a suitable blocked validation design when parameters are adjusted.

The present spatial Spearman values and factor-of-two proportions compare one model with another. They are not the observed-model performance metrics of the future evaluation. A factor-two fraction does not become an acceptance test unless an appropriate protocol, data support and application have been defined. Likewise, numerical reproduction of daily or annual native summaries confirms extraction consistency, not atmospheric accuracy.

### Questions that may arise during the discussion

**Why not choose CALPUFF because it uses three-dimensional meteorology?** A spatially varying diagnostic field can represent important processes, but its accuracy depends on the observations and assumptions used to construct it. With one surface station and a 1.5-kilometre grid, we cannot claim that all plant-scale flows are resolved. Independent observations are still needed.

**Why not choose AERMOD because its concentrations are higher?** A higher prediction is not automatically more accurate or more appropriate for every decision. We need to examine the relevant averaging time, receptor support, physical assumptions and observed behaviour. The objective is to understand model response, not to reward whichever system produces the largest maximum.

**Does a larger sigma always reduce every ground-level value?** Greater spread usually redistributes mass over a larger volume, but the response at a particular receptor also depends on release height, distance, reflection, terrain and whether spreading brings pollutant towards that receptor. It is unsafe to describe sigma as a universal concentration-reduction knob.

**Did you use an observed hourly H2S emission profile?** No. The current sources have constant rates. The hourly concentration cycle arises from the dispersion calculation and the meteorology under that emission assumption. A process-informed temporal profile will be tested separately.

**Were building outlines used to calculate downwash?** The map outlines are contextual. They do not demonstrate that building dimensions or a suitable downwash treatment were supplied for these diffuse area sources. No downwash effect should be inferred from the presence of buildings on a map.

**Was H2S chemistry simulated?** Chemical transformation, wet removal and dry deposition were switched off in the submitted CALPUFF input. The AERMOD setup requests concentration and does not supply a chemical-loss or deposition treatment for this comparison. The maps are not a validated account of all atmospheric H2S transformation or loss processes.

**Can the daily maps identify actual odour exceedances?** Not directly. Odour perception involves short fluctuations, individual sensitivity and other compounds. Daily and annual averages are much longer than a brief odour event. The display reference of 0.7 microgram per cubic metre is not a universal threshold to apply to every averaging period.

**Why do maximum maps not describe a single event?** Each receptor selects its own largest daily mean. Adjacent high colours can therefore combine different dates. A coherent event map must select one common date or hour and show every receptor for that same interval.

**Why is P95 not an adjustment that fixes high concentrations?** P95 selects a different feature of the same hourly distribution. It does not change an emission, a meteorological field or any hourly prediction. Reporting a percentile instead of a maximum is a change of indicator, not calibration.

**Are the spatial bands uncertainty intervals?** The bands in the distance profiles are the interquartile range across receptors within each distance class. They describe spatial heterogeneity. They are not confidence intervals for the mean and do not cover total modelling uncertainty.

**What is the strongest result we can defend now?** Under the executed scenarios, the systems show partly similar receptor rankings but substantial differences in magnitude and near-source behaviour. The combination of maps, native hourly distributions and distance profiles helps prioritise measurements and sensitivity tests. It does not yet establish which system best reproduces the real sites.

## Explicação em português dos pontos físicos essenciais

O comprimento de Monin-Obukhov é uma escala da estabilidade da camada superficial, e não a altura da camada limite. Seu sinal distingue condições estáveis e convectivas na convenção usual. Valores muito grandes em módulo podem representar aproximação da neutralidade. A interpretação melhora quando consideramos a razão entre a altura avaliada e L, juntamente com u-star e o fluxo de calor. Não faz sentido usar apenas o valor absoluto de L para dizer que uma estação dispersa melhor que outra.

U-star representa uma escala de turbulência mecânica ligada ao atrito na superfície. W-star é uma escala convectiva ligada ao aquecimento. Ambas são velocidades, mas nenhuma é a velocidade de saída do gás. A altura de mistura é outra variável, em metros. Uma camada menos profunda pode limitar a diluição de uma mesma massa emitida, mas isso não significa que toda noite seja estável ou que a emissão real aumente à noite.

Sigma-y e sigma-z descrevem dimensões da distribuição da pluma, em metros. Sigma-v e sigma-w descrevem flutuações de velocidade, em metros por segundo. O sigma-z inicial informado para uma fonte é ainda outra informação, ligada à representação da liberação. A classe de estabilidade A-F não é um desses sigmas. É importante saber qual opção do modelo transforma a informação meteorológica em dispersão: nesta execução, o CALPUFF usou MDISP=3, e não a opção MDISP=2 baseada diretamente em turbulência micrometeorológica calculada.

Também não devemos atribuir a essas fontes a ascensão típica de uma chaminé quente. O AERMOD recebeu superfícies circulares e poligonais, com alturas de liberação e dispersão inicial. Não recebeu temperatura e velocidade de exaustão de uma chaminé para essas fontes. Elevar a altura ou aumentar sigma-z sem caracterização física pode diminuir certos resultados, mas não demonstra melhoria do cenário.

Ao apresentar o noturno, prefira “concentrações modeladas mais elevadas” a “emissões mais elevadas”. As taxas usadas são constantes. A discussão técnica é que o regime constante interage com as condições de dispersão, sobretudo a mistura e o vento efetivo, e que esse comportamento ainda será comparado com medições. A auditoria do relógio e da validade deve anteceder uma conclusão fina sobre dia e noite locais.

## Configuração efetivamente encontrada nesta rodada

| Componente | Configuração conferida | Como explicar |
|---|---|---|
| AERMOD | Versão 26135; DFAULT, CONC, ELEV, RURAL | Pluma horária com tratamento de camada limite e terreno elevado. |
| AERMET | Versão 24142; superfície SAMSON e altitude FSL | O uso de documentação atual não significa que a meteorologia foi reprocessada na versão 26135. |
| Características de superfície | Albedo 0,18; Bowen 1,15; z0 0,30 m nos 12 setores anuais | A tabela tem 12 setores, mas seus parâmetros são iguais. |
| Fontes AERMOD | AREACIRC e AREAPOLY | Fluxo por área, altura de liberação e sigma-z inicial; sem ascensão convencional de chaminé. |
| CALMET | 5.8.5; uma estação de superfície e uma de altitude | Campo diagnóstico; NOOBS=0, NM3D=0, IPROG=0. |
| Grade meteorológica | 40 × 40; 1,5 km; dez camadas | É diferente da grade fina de receptores de concentração. |
| CALPUFF | 5.8.5; MDISP=3 | Relações de dispersão PG/MP; não atribuir à execução uma opção alternativa não ativada. |
| Remoção e transformação | MCHEM=0; MWET=0; MDRY=0 | Não foram simuladas química, remoção úmida e deposição seca no CALPUFF. |
| Temporalidade da emissão | Taxas constantes | Perfil variável e calibração observacional permanecem como trabalho futuro. |

## Plano de refinamento para discutir com o público

Primeiro, reconciliar os relógios e intervalos de medição e simulação. Em seguida, construir uma comparação observada-modelada com suporte espacial e temporal comum. Só então será possível quantificar viés em relação a observações. O contraste entre dois modelos não identifica, por si só, qual deles superestima o ambiente real.

Os testes devem separar o perfil temporal da emissão da representação atmosférica. Um perfil de emissão com média um conserva a massa associada à taxa média, enquanto um teste de estabilidade altera o tratamento meteorológico ou a dispersão mantendo o inventário. As opções devem ser justificadas fisicamente e avaliadas em período independente. Não foi executado um cenário novo para esta revisão do roteiro.

Para a discussão detalhada, a auditoria técnica já registra diferenças de algumas alturas de liberação e dispersão inicial entre os cenários. Elas permanecem como itens de harmonização para o artigo e não foram acrescentadas ao texto do pôster. Assim, não devemos afirmar que toda diferença atual representa exclusivamente a formulação matemática de AERMOD contra CALPUFF.

## Referências técnicas desta ampliação

- U.S. EPA. AERMOD User Guide, julho de 2026. [Guia oficial](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_userguide.pdf). Tipos de fonte e significado das entradas de liberação, especialmente seções de AREA, AREAPOLY e AREACIRC.
- U.S. EPA. AERMOD Model Formulation, julho de 2026. [Formulação oficial](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_mfd.pdf). Estrutura de camada limite e dispersão.
- U.S. EPA. AERMET User Guide, julho de 2026. [Guia oficial](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/met/aermet/aermet_userguide.pdf). Conceitos e formato de saídas; a rodada fornecida utiliza AERMET 24142.
- Scire e colaboradores. CALMET Version 5 User Guide. [Manual do sistema](https://www.calpuff.org/calpuff/download/CALMET_UsersGuide.pdf). Campo diagnóstico, parâmetros micrometeorológicos e altura de mistura.
- Scire e colaboradores. CALPUFF Version 5 User Guide. [Manual do sistema](https://www.calpuff.org/calpuff/download/CALPUFF_UsersGuide.pdf). Fontes, coeficientes de dispersão e opções MDISP.
- [Distribuição oficial do sistema CALPUFF](https://www.calpuff.org/calpuff/download/download.htm). Identificação das versões 5.8.5 e distinção das versões posteriores. A condição regulatória atual depende da jurisdição e da aplicação; a página do fornecedor não substitui essa verificação.
- Evidências locais: ADI/ADO da rodada de 10/11/2026; CALPUFF-VM/NC.INP e LST; CALMET.INP/LST; AERMET_COP.INP; Comparacao_consolidada.json; Concordancia_espacial_P95.json; Resposta_meteorologica_dois_modelos.csv. Nenhuma medição de H2S foi incorporada como validação nesta ampliação.

