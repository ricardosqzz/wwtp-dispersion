# ENTRADAS: output/cmas_poster/preparacao_apresentacao/*.md; CMAS/AERMOD/H2S_TOTAL.ADI, ADO; CALPUFF-VM/NC.INP; in/CALMET.INP e AERMET_COP.INP.
# EVIDÊNCIAS: output/comparacao_modelos, P95 por receptor, meteorologia e configurações já auditadas; nenhuma concentração é recalculada.
# SAÍDAS: Roteiro_Session05_PT_EN.md e Guia_preparacao_Session05_PT_EN.md; versões anteriores em descontinuado.
# CAMINHOS: COPASA_PROJECT_ROOT ou codigo/caminhos_projeto.json; a formatação Word/PDF é uma etapa separada.
from pathlib import Path
import datetime,shutil,json,re
from caminhos_copasa import raiz_projeto
R=raiz_projeto();D=R/'output/cmas_poster/preparacao_apresentacao';STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Roteiro ampliado em inglês
FULL_EN='''## Full presentation in English

### Purpose and research question

Good morning. This study compares hydrogen sulphide dispersion predicted by AERMOD and CALPUFF at two wastewater treatment plants, identified here as WWTP 1 and WWTP 2. Hydrogen sulphide can be generated during anaerobic wastewater treatment and released when dissolved sulphide is transferred from water to the atmosphere. The point where sulphide is produced is therefore not necessarily the point where most of it is emitted.

Our question is how the two modelling systems distribute the predicted concentrations around the same treatment processes, and how their differences change with distance. We are comparing model responses, rather than assuming that one model provides the correct answer. Ambient observations will be used in a subsequent evaluation. This distinction is important because a model-to-model comparison can reveal sensitivity, but it cannot establish which prediction is more accurate in the real environment.

### Sources and emission inventory

Please look first at the source-characterisation maps. We represented the emitting surfaces using circular or polygonal area sources, including UASB reactors, preliminary treatment and the relevant downstream units. UASB stands for upflow anaerobic sludge blanket. These are diffuse releases from treatment surfaces, rather than conventional hot exhaust stacks.

The inventory is based on process mass balances. The mass assigned to a process is calculated once and distributed among its corresponding surfaces. Total mean emission rates are approximately 0.05728 grams per second at WWTP 1 and 0.06866 grams per second at WWTP 2. In this inventory, UASB reactors account for about 72 percent of the first plant's emission, while trickling filters account for about 73 percent at the second plant. These percentages describe the adopted inventory and should not be treated as universal emission shares for wastewater treatment plants.

For an area source, surface flux and total emission rate are different quantities. Surface flux is expressed per square metre, whereas the total rate is obtained by integrating that flux over the source area. This distinction matters when comparing a circular representation with a polygonal approximation. The present simulations use constant source rates. We have not imposed an observed hourly emission profile or established that the plants emit more hydrogen sulphide at night.

### Meteorological processing and model formulation

AERMOD represents a plume under the meteorological conditions assigned to each hour. It uses boundary-layer parameters and vertical profiles supplied by AERMET, together with source geometry and terrain information. The executed model was AERMOD version 26135, using meteorological files produced by AERMET version 24142. The run used the default concentration options with elevated terrain and the rural dispersion treatment. Here, rural is a model option; it does not mean that the surrounding region has no urban development.

AERMET processed the supplied surface time series and upper-air soundings. Its outputs describe wind, temperature and boundary-layer properties such as friction velocity, sensible heat flux, the Monin-Obukhov length and mixing heights. These variables determine how readily the atmosphere can dilute a release. They are not extra emission rates. We used the resulting surface and profile files as inputs to the dispersion calculation.

CALMET and CALPUFF were both version 5.8.5 in this execution. CALMET generated a three-dimensional diagnostic meteorological field using the supplied observations, terrain and land-surface information. The configured grid contains forty by forty cells, with a horizontal spacing of 1.5 kilometres and ten vertical layers. This is the meteorological grid, which is different from the finer receptor network used to sample concentrations. A dense receptor grid does not itself increase the resolution of the meteorological information.

The submitted CALMET configuration has one surface station, one upper-air station and no prognostic three-dimensional input. We therefore do not describe this run as a WRF-driven, high-resolution reconstruction of every local circulation. CALPUFF transports and disperses puffs through the CALMET field, retaining their evolution over time. An important execution detail is that MDISP was set to three. This uses the configured Pasquill-Gifford or McElroy-Pooler dispersion relationships, rather than the alternative option based directly on internally calculated turbulence standard deviations. Chemical transformation, wet removal and dry deposition were disabled in the CALPUFF input. These details define the scope of the current comparison.

### Receptors and comparison strategy

The AERMOD network contains 1,790 receptor records at 1,789 unique positions. Two cadastral identifiers share a location, and that location is not counted twice in the spatial statistics. We matched native receptor coordinates between the two systems, using the documented 0.75-metre tolerance, rather than interpolating concentrations to manufacture pairs.

Within 1,800 metres of the nearest emitting surface, the comparison includes 562 receptor pairs at WWTP 1 and 556 at WWTP 2. Distance is measured to the union of the emitting surfaces, not to the plant centre. A receptor inside a source polygon therefore has a geometric distance of zero. The receptor percentages discussed here are not percentages of exposed population or of municipal area.

### How to read the boxplots and distance profiles

For the distributional analysis, we used the leap year 2024. At each receptor and for each model, we calculated the ninety-fifth percentile of the valid hourly concentrations. We then compared these receptor-level percentiles across distance bands. Each value in a boxplot is therefore one receptor's hourly P95, rather than an individual hourly observation. The boxes show spatial variation in upper-tail temporal indicators.

AERMOD contributed 8,496 valid hours in this analysis, while CALPUFF contributed 8,784. We preserved native validity rules and did not fill missing hours. These distributions are consequently not a set of synchronised hourly prediction errors. A controlled temporal comparison requires a common clock and a common valid-hour mask, which are part of the next refinement.

The distance profiles summarise six bands from the source boundary to 1,800 metres. The central line is the median of receptor P95 values within a band, and the shaded interval extends from the first to the third quartile. This is spatial interquartile variability, not a confidence interval. The interpolation between the six summaries is only a display aid; it does not change any modelled concentration. The lower strip shows the difference between the two medians, CALPUFF minus AERMOD, which is not necessarily the median of the paired differences.

### How to read the dispersion maps

The 24-hour maps show the highest daily mean at each receptor. The peaks need not occur on the same day, so each map is a receptor-specific envelope of maxima, not a single simultaneous pollution episode. For the annual maps, we selected the larger calendar-year mean from 2024 and 2025 at each point. CALPUFF has complete coverage in 2024 and 99.68 percent coverage in 2025, so the latter is a nearly complete year and is identified as such.

The hourly CALPUFF concentration outputs provide the temporal information needed for this calculation. The RANK files alone do not contain a complete hourly series at every receptor. AERMOD hourly POST files and CALPUFF hourly fields were checked against their native summaries. This numerical consistency check supports the extraction and aggregation procedure; it does not validate the atmospheric predictions against measurements.

The colour bar shows the same hydrogen sulphide concentration in micrograms per cubic metre and equivalent parts per billion. The conversion uses a conventional temperature of 25 degrees Celsius and a pressure of one atmosphere. The daily and annual maps are useful for comparing model behaviour, but they should not be interpreted directly as the frequency of short odour events.

### Main results and their interpretation

AERMOD generally produces higher concentrations very close to the emitting surfaces in this comparison, while the contrast changes with distance and plant. Spatial Spearman correlations of receptor P95 are approximately 0.57 at WWTP 1 and 0.63 at WWTP 2. However, only 35.9 and 24.8 percent of receptor pairs, respectively, are within a factor of two. A partially similar ranking of receptors can therefore coexist with substantial differences in concentration magnitude. Neither statistic is an accuracy score against observed concentrations.

We are still refining the model representation, particularly under nocturnal boundary-layer conditions. The diagnostic hourly summaries show higher AERMOD concentrations during the nominal overnight and early-morning part of its model clock. Constant source rates continue to supply pollutant while weaker mixing, shallow mixing layers and low effective wind speeds can limit dilution. These are physically plausible explanations to investigate, rather than a demonstrated attribution of the model difference to one mechanism. Clock conventions must also be resolved before a detailed local day-night comparison.

It would therefore be premature to say that actual emissions are higher at night, that the model has already been corrected, or that either system is overpredicting the real concentrations. We will compare the predictions with measurements at compatible locations, averaging periods and times. Sensitivity scenarios will separately examine emission timing, source representation and the meteorological treatment, preserving the appropriate total mass when the mean emission is unchanged.

### Conclusion and next steps

The contribution of this work is to combine extreme concentration maps, temporal distributions and spatial distance profiles, rather than choosing a model on the basis of a single maximum. This helps identify where the two systems disagree and where additional monitoring can most effectively test the assumptions. The present poster reports a comparison of executed scenarios. Boundary-layer refinement and independent observed-model evaluation are continuing work for the article. We acknowledge the ARSAE-MG and COPASA research programme, CNPq, CAPES and FAPEMIG.

'''

# Fundamento técnico e respostas em inglês
TECHNICAL='''## Extended technical discussion in English

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
'''

# Atualização preservando as versões anteriores
def main():
 for stem in ['Roteiro_Session05_PT_EN','Guia_preparacao_Session05_PT_EN']:
  for ext in ['md','docx','pdf']:
   p=D/(stem+'.'+ext)
   if p.exists():
    dest=R/'descontinuado'/STAMP/'preparacao_cmas'/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 p=D/'Roteiro_Session05_PT_EN.md';s=p.read_text('utf8');s=s.replace('conferido em 14 de novembro de 2026','conferido em 18 de novembro de 2026');s=s.replace('## Full presentation in English\n', '## Full presentation in English\n',1)
 start=s.index('## Full presentation in English');end=s.index('## Frases úteis',start);s=s[:start]+FULL_EN+s[end:]
 s=s.replace('outra de aproximadamente cinco minutos','outra ampliada, para adaptar à duração da conversa');s=s.replace('de aproximadamente cinco minutos','ampliada de aproximadamente dez a doze minutos, com leitura seletiva conforme o interesse do público')
 s=s.replace('## Frases úteis para a conversa em inglês','## Frases úteis para a conversa em inglês\n\n“We are still refining the nocturnal boundary-layer representation, and comparison with compatible observations is the next step.”\n\n“The source rates are constant; higher modelled nighttime concentrations do not demonstrate higher actual nighttime emissions.”\n\n“MDISP was set to three in the executed CALPUFF input; we have not yet run the alternative turbulence-based option.”\n')
 p.write_text(s,encoding='utf8');p=D/'Guia_preparacao_Session05_PT_EN.md';s=p.read_text('utf8').replace('conferido em 14 de novembro de 2026','conferido em 18 de novembro de 2026')
 if '## Extended technical discussion in English' in s:s=s.split('## Extended technical discussion in English')[0]
 p.write_text(s+'\n'+TECHNICAL+'\n',encoding='utf8')
 (D/'Atualizacao_20261118.json').write_text(json.dumps({'date':'2026-11-18','new_simulation':False,'observational_validation_performed':False,'AERMOD_version':'26135','AERMET_version':'24142','CALMET_CALPUFF_version':'5.8.5','MDISP':3,'constant_emission':True,'topics':['boundary layer','Monin-Obukhov','turbulence and plume sigmas','source representation','nocturnal interpretation','observed-model evaluation plan']},indent=2),encoding='utf8');print('Roteiro e guia ampliados',flush=True)
if __name__=='__main__':main()
