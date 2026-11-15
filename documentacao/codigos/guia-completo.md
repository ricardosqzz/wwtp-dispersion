# Relatório dos códigos — COPASA

Edição de 14 de novembro de 2026. Fontes locais e resultados atuais, sem reexecução dos modelos de dispersão.

## Como usar este relatório

Este documento reúne uma explicação metodológica e fichas dos códigos existentes na pasta de trabalho. Cada ficha informa finalidade, dependências, entradas, campos, produtos e trechos reais do arquivo. O índice HTML ao lado deste PDF permite buscar um nome e abrir a ficha completa, com o código integral numerado. O inventário CSV/JSON registra as assinaturas dos arquivos. Bibliotecas de terceiros distribuídas com Quarto, Node e outros programas não são códigos autorais e ficaram fora desse inventário.

As fichas distinguem cálculo atual, apoio, teste, geração editorial e rotina histórica. A presença de um arquivo na pasta não significa que seja necessário executá-lo para atualizar todos os resultados. As etapas antigas de migração e os geradores dos seminários entregues permanecem para rastreabilidade e não devem ser executados como um lote indiscriminado.

As entradas explicitadas foram levantadas na sintaxe dos programas e conferidas nos módulos principais. Expressões como `{path}`, argumentos do chamador e nomes compostos em tempo de execução são interfaces, não arquivos faltantes. Nos cabeçalhos, “campos/chaves” inclui atributos de camadas, colunas de tabelas e chaves de configuração. O dicionário de campos do TECO mantém a descrição específica por camada. O código integral resolve eventuais ambiguidades de uma expressão dinâmica.

## Caminhos, ambiente e reprodução em outro computador

O arquivo `codigo/caminhos_projeto.json` concentra a raiz, remapeamentos de pastas, exceções de arquivos e dependências externas. Com `raiz_projeto` vazio, a pasta que contém `codigo` é a raiz adotada. Ao copiar toda a árvore do projeto e mantê-la organizada, não é necessário conservar a letra E do disco. Para usar dados fora dessa árvore, preencher `raiz_projeto` ou o item correspondente em `pastas`/`arquivos`. Os programas consultam esse arquivo pelos módulos `caminhos_<projeto>` de cada linguagem.

Exemplo de configuração a adaptar, sem alterar os campos e as equações do processamento:

```json
{"raiz_projeto":"D:/Pesquisa/Meu projeto",
 "pastas":{"output":"D:/Pesquisa/Resultados"},
 "arquivos":{},"externos":{},"ambiente":{}}
```

A raiz pode ser sobrescrita pelas variáveis de ambiente CONGONHAS_PROJECT_ROOT, TECO_PROJECT_ROOT ou COPASA_PROJECT_ROOT. Congonhas também preserva EMI_PROJECT_ROOT. Cada projeto tem seu próprio arquivo de configuração e não consulta o de outro projeto. Os itens em `externos` identificam arquivos fora da árvore, fontes tipográficas, modelos e executáveis. Eles devem ser revistos na máquina de destino. O JSON armazena caminhos, não instala os programas.

As ferramentas administrativas que geram e conferem esta documentação dos três projetos utilizam também a tabela PROJETOS, no início de documentar_portabilidade.py, para localizar cada árvore. Ao transferir essas ferramentas, ajustar essa tabela ou usar --projeto/--raiz no inventariador. Elas não são necessárias para executar a análise configurável entregue à colaboradora. Os cabeçalhos dessas rotinas identificam essa configuração adicional.

O ambiente geográfico usa NumPy, pandas, GeoPandas, Shapely, Rasterio, PyProj/Pyogrio e SciPy. Os recursos PyQGIS/GRASS devem ser executados no Python instalado com o QGIS. Gerar Word/PDF ou pôster pode exigir outro ambiente com python-docx, ReportLab, pypdf, Pillow, lxml, Microsoft Word e as bibliotecas de autoria de apresentações. Os módulos JavaScript que importam `@oai/artifact-tool` dependem desse pacote, fornecido pelo ambiente de autoria utilizado aqui; não basta instalar Node. Essa dependência não é necessária para recalcular os indicadores geográficos.

Os programas anteriores à edição dos caminhos foram arquivados em `descontinuado/20261114_portabilidade_codigo`, preservando sua localização relativa. A edição dos códigos não executou novamente os modelos de dispersão nem substituiu os mapas publicados ou os textos acadêmicos já entregues.

## Conceitos numéricos que atravessam os códigos

Uma normalização coloca variáveis em escalas comparáveis, sem criar informação. Na transformação logarítmica usa-se t=ln(1+x). No min-max, n=(t−mínimo)/(máximo−mínimo). Na padronização z, z=(t−média)/desvio-padrão. Colunas constantes usam denominador 1, para evitar divisão por zero. Lacuna não é automaticamente zero. A máscara de registros completos define quais observações podem entrar em determinado ajuste.

O índice ponderado do TECO é I=100×Σ(wj×nj)/Σwj. Os pesos exprimem hipóteses de importância relativa, não coeficientes obtidos pela medição de genes. No k-means minimiza-se Σi Σj wj×(nij−centrogrupo,j)². Por isso o código multiplica a matriz normalizada por √peso antes do ajuste. Usar o peso diretamente nessa matriz elevaria a influência ao quadrado. A implementação utiliza scipy.cluster.vq.kmeans2, não uma chamada ao k-means do QGIS ou do scikit-learn. Inicializações repetidas e sementes explícitas reduzem a dependência de uma única solução inicial. [Documentação SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html).

A silhouette de cada observação é s=(b−a)/máximo(a,b), em que a mede distância média ao próprio grupo e b à alternativa mais próxima. A média resume separação interna e pode comparar valores de k na mesma matriz. Não é um p-valor, nem porcentagem de acerto, nem comprovação de que o grupo corresponde a uma fonte real. Classes por quintis são cortes ordenados em uma variável. K-means é um agrupamento multivariado por semelhança. A estabilidade compara resultados depois de variar pesos, suporte ou amostras e não se confunde com nenhum dos dois. [Rousseeuw, 1987](https://doi.org/10.1016/0377-0427%2887%2990125-7).

Moran global relaciona os desvios padronizados de cada local aos de seus vizinhos. Com pesos de vizinhança padronizados por linha, o código usa I=(zᵀWz)/(zᵀz). O Moran local usa Ii=zi×(Wz)i. A significância é obtida por permutação, com p=(1+contagem de resultados tão extremos quanto o observado)/(1+número de permutações). O ajuste Benjamini-Hochberg controla a taxa de falsas descobertas da família declarada. HH e LL significam valor alto/baixo cercado de valores semelhantes; HL/LH são contrastes locais. NS indica ausência de evidência com o critério adotado, não ausência de pressão. ISO identifica isolamento topológico quando previsto. Associação espacial não demonstra uma rota hidrológica ou causal.

Uma junção por chave preserva identificadores e exige unicidade. Uma interseção espacial recorta as geometrias. Na média ponderada por área, x̄=Σ(xj×área de interseçãoj)/Σárea válida. Ratear população por área pressupõe distribuição uniforme dentro da parcela original quando não há uma base dasimétrica melhor. Uma reprojeção transforma coordenadas; atribuir um código EPSG sem transformar o dado não corrige uma coordenada errada. [GeoPandas overlay](https://geopandas.org/en/stable/docs/reference/api/geopandas.overlay.html).

## Ampliação controlada das variáveis

TECO e Congonhas receberam `config/analise_extensivel.json` e `codigo/reproduzir_analise_configuravel.py`. O cenário padrão reproduz a matriz publicada a partir dos produtos consolidados, com saída separada. Para acrescentar uma variável, declarar nome, origem, arquivo, camada/campo, unidade, transformação e agregação; depois informar o peso em cada cenário. A origem pode ser uma coluna da base, tabela, camada vetorial ou raster. Os métodos disponíveis são junção por chave, média ponderada pela área, soma de pontos e média dos pixels válidos. Outro tipo de dado requer acrescentar sua regra na função anexar_variavel. O programa interrompe a execução se houver campo ausente, chave duplicada ou agregação desconhecida.

Na expansão, justificar o sinal da variável e evitar contar duas vezes a mesma pressão. Revisar cobertura, ano, universo e lacunas. Transformações e pesos devem ser fixados antes de comparar cenários. No TECO, a agregação espacial usa os círculos de cálculo, enquanto a geometria final de apresentação continua sendo o suporte sem sobreposição. O exemplo de extensão demonstra uma interface técnica; escolher uma nova variável continua sendo uma decisão metodológica. Um peso não informado assume zero, portanto precisa ser conferido antes de interpretar o cenário.
## Fluxo específico da COPASA

O objetivo do pôster é comparar o comportamento de AERMOD e CALPUFF em dois sistemas de tratamento, publicamente identificados como WWTP 1 e WWTP 2. O fluxo atual lê as entradas e as novas saídas CMAS, confere as emissões, organiza receptores coincidentes e produz campos de dispersão e estatísticas por distância. As três rotinas map_copasa*.py da raiz pertencem à etapa inicial e não devem ser usadas como atalho para atualizar o pôster final.

As taxas são conferidas por processo e superfície efetivamente medida. Quando um processo possui vários reatores, sua massa deve ser distribuída entre eles de modo que a soma recupere o processo. Fluxo superficial = massa do processo/área emissora, com unidades consistentes. A altura de liberação é um parâmetro diferente da cota de terreno. Os totais mostrados no pôster são 0,05728 g/s na WWTP 1 e 0,06866 g/s na WWTP 2. UASB responde por 72% na primeira e filtros percoladores por 73% na segunda.

A grade combinada registra 1.790 identificadores e 1.789 posições únicas. Um par de identificadores compartilha coordenadas e é preservado para rastreabilidade, mas a posição não é duplicada nas estatísticas espaciais. A comparação usa pares nativos com tolerância de coordenadas de 0,75 m. Na análise até 1.800 m da superfície emissora mais próxima, há 562 pares na WWTP 1 e 556 na WWTP 2. Distância à fonte significa distância geométrica à superfície, não à borda do mapa ou a um centro arbitrário da unidade.

POST/POS do AERMOD e CONC.DAT do CALPUFF preservam séries temporais nos receptores. RANK é um produto de extremos ordenados, útil para máximos, mas não substitui a série completa de todas as horas. Por isso as estatísticas horárias e anuais atuais utilizam as saídas completas fornecidas. A leitura binária CALPUFF depende da estrutura dos registros, tipos, ordem de bytes e cabeçalho; os decodificadores conferem tamanho e calendário antes de interpretar concentrações.

O campo de 24 h representa o máximo diário nativo em cada receptor, não um único dia simultâneo de toda a pluma. O anual representa a maior média de ano-calendário disponível naquele receptor, entre 2024 e 2025. Não é máximo móvel de 8.760 horas nem média de todo o período. O CALPUFF contém 8.784 horas em 2024 e 8.732 em 2025; este último tem 99,68% das 8.760 horas esperadas. A comparação e os gráficos mantêm essa cobertura explícita.

Os boxplots não reúnem diretamente todas as horas de todos os pontos. Primeiro se calcula o P95 horário de 2024 em cada receptor para cada modelo. Depois a distribuição desses P95 entre receptores é mostrada nas faixas 0-100, 100-500 e 500-1.800 m. A caixa representa P25-P75, a linha central é a mediana e os bigodes usam 1,5×IQR. Omissão visual de pontos extremos não significa exclusão dos dados no cálculo. A diferença entre modelos é espacialmente variável e não se resume ao pico máximo do mapa.

Os perfis usam seis faixas, 0-50, 50-100, 100-200, 200-300, 300-500 e 500-1.800 m. Os pontos mostram medianas do P95, as faixas mostram quartis. A curva PCHIP é apenas uma ligação visual entre esses resumos. As faixas têm larguras físicas diferentes, embora apareçam como categorias com espaçamento gráfico igual. O quadro ampliado conserva os valores menores em unidade normal. A linha Δ representa mediana CALPUFF menos mediana AERMOD de cada faixa, que não é necessariamente a mediana das diferenças pareadas. [SciPy PCHIP](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html).

Spearman avalia se os receptores de maior concentração em um modelo tendem a ser os de maior concentração no outro. O fator 2 avalia a parcela de pares com 0,5×AERMOD ≤ CALPUFF ≤ 2×AERMOD. No universo principal, ρ=0,574 e 35,9% dentro do fator 2 na WWTP 1; ρ=0,626 e 24,8% na WWTP 2. Correlação moderada de ordenação pode coexistir com diferenças grandes de magnitude. Não se publica um p ingênuo tratando todos os receptores espacialmente dependentes como observações independentes. [SciPy Spearman](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html).

Essa comparação é entre modelos, não validação frente a medições ambientais. As entradas recebidas ainda guardam diferenças de altura e dispersão inicial, documentadas na auditoria técnica. O pôster não as discute por decisão de escopo, mas o relatório de código mantém essa ressalva para que as diferenças não sejam atribuídas exclusivamente ao algoritmo de dispersão ou à meteorologia. Uma análise causal do efeito do modelo exigirá entradas harmonizadas e relógios confirmados. As 8.496 horas válidas nativas do AERMOD em 2024 não foram tratadas automaticamente como as mesmas 8.784 horas válidas do CALPUFF.

As cores lineares dos mapas são compartilhadas entre os quatro painéis da mesma duração. A indicação em ppb é conversão do mesmo eixo, usando 1 ppb=1,40 µg/m³ nas condições de referência declaradas no produto. Não são duas simulações. A faixa cinza abaixo de 0,7 µg/m³ é referência visual e não um limiar universal de detecção de odor. Os topos abertos da escala não apagam os valores máximos auditados. As figuras preservam nomes genéricos e a composição cartográfica sem imagem de satélite.

A conferência atual do pôster verificou 80 itens, incluindo reprodução de médias nativas, cobertura, quartis, amostra, escala física, geometrias editáveis e imagens. Todos foram aprovados. Isso confirma consistência dos produtos e cálculos apresentados; não comprova desempenho ambiental do modelo. O AERMOD é descrito pela documentação da EPA e o CALPUFF pelo manual do sistema, mantendo a distinção entre modelo estacionário e sistema não estacionário de puffs. [EPA/SCRAM](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models), [manual CALPUFF](https://www.src.com/calpuff/download/CALPUFF_Version6_UserInstructions.pdf).

## Catálogo de rotinas

46 arquivos autorais foram documentados. O índice HTML apresenta a ficha integral e o código numerado de cada um. As fichas seguintes preservam os pontos de cálculo, os campos e os trechos citados.

## codigo/atualizar_cartografia_cmas.py

Produtos cartográficos da execução recebida em 10/11/2026.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\atualizar_cartografia_cmas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_e_preparar | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_copasa | Módulo autoral local; sua ficha está neste relatório. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.cm | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patheffects | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- c.F/Cartografia_metadados.json — chamada .read_text, linha 47.
- c.R/output/comparacao_modelos/Campos_nativos.npz — chamada np.load, linha 79.

**Saídas.**

- plt.figure(figsize=(wc / 2.54, hc / 2.54)) — chamada c.save, linha 125.
- c.F/Cartografia_metadados.json — chamada .write_text, linha 126.
- c.F/Faixas_concentracao_poster.json — chamada .write_text, linha 126.
- c.O/index.html — chamada .write_text, linha 141.

**Campos e chaves lidos.**

- c.META: Fontes_privacidade.

**Campos e chaves gerados.**

- v: process.
- c.D: sources_aermod.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main(only_methods=False) | 42-133 | lê dados; grava produtos |
| gallery() | 135-141 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_cartografia_cmas.py, linhas 79-85.

```python
    fields=np.load(A/'Campos_nativos.npz');records=[]
    span,scale=1000,8500;side=span/scale*100;left,right,bottom,top=1.35,4.0,1.15,1.1;gaps=[.5,1.0,.5];wc=left+4*side+sum(gaps)+right;hc=bottom+side+top
    cmap=LinearSegmentedColormap.from_list('copasa_linear',['#cee9fa','#7cc2db','#72bc8c','#d4d96b','#f9df64','#f5a54b','#df503a','#b8182c']);cmap.set_under('#f2f4f4');cmap.set_over('#ae1325')
    for period,stem,vmin,vmax,ticks in [('24h','Comparacao_24h_faixa',.7,50,[.7,10,20,30,40,50]),('annual_calendar_max','Comparacao_anual_faixa',.7,10,[.7,2,4,6,8,10]),('annual_2024','Comparacao_anual_2024',.7,10,[.7,2,4,6,8,10])]:
        fig=plt.figure(figsize=(wc/2.54,hc/2.54));axes=[]
        for i,(unit,model) in enumerate([('VM','AERMOD'),('VM','CALPUFF'),('NC','AERMOD'),('NC','CALPUFF')]):
            ax=fig.add_axes([(left+i*side+sum(gaps[:i]))/wc,bottom/hc,side/wc,side/hc]);axes.append(ax);x0,y0,x1,y1=c.frame(ax,unit,span,scale)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_calmet_dat.py

Inspeciona registros Fortran sem carregar o CALMET inteiro na memória.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\copasa_map\codigo\auditar_calmet_dat.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

- E:/copasa_map/in/CALMET.DAT — chamada p.open, linha 26.

**Saídas.**

- E:/copasa_map/output/auditoria/CALMET_DAT_verificado.json — chamada .write_text, linha 47.

**Campos e chaves lidos.**

- header: hours.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_calmet_dat.py, linhas 25-33.

```python
count=0;hours=[];header=None;lines=None
with p.open('rb') as f:
    while True:
        marker=f.read(4)
        if not marker:break
        assert len(marker)==4,'Marcador incompleto'
        n=struct.unpack('<i',marker)[0];assert 0<=n<10000000,(f.tell(),n)
        take=min(n,160 if count<1200 else 12);v=f.read(take);f.seek(n-take,1)
        tail=f.read(4);assert len(tail)==4 and struct.unpack('<i',tail)[0]==n,(count,f.tell())
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_e_preparar.py

Lê entradas dos modelos, confere unidades e massas por processo, organiza as geometrias das fontes e exporta entradas e grades corrigidas para importação.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\copasa_map\codigo\auditar_e_preparar.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| statistics | Estatísticas descritivas da biblioteca padrão. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {p} — chamada p.read_text, linha 88.
- E:/copasa_map/in/CALMET.INP — chamada .read_text, linha 108.
- E:/copasa_map/in/CALMET.LST — chamada .read_text, linha 108.
- E:/copasa_map/AERMET_COP.SFC — chamada .read_text, linha 114.
- E:/copasa_map/output/entradas_corrigidas/CALPUFF-VM_corrigido.INP — chamada .read_text, linha 216.
- E:/copasa_map/output/entradas_corrigidas/CALPUFF-NC_corrigido.INP — chamada .read_text, linha 217.
- E:/copasa_map/temp/fontes_NC_xls_leitura.sha256 — chamada sha.read_text, linha 235.
- E:/copasa_map/in/H2S_Grid_Sources-NC.xls — chamada oldxls.read_bytes, linha 235.
- E:/copasa_map/temp/fontes_NC_xls_leitura.json — chamada cache.read_text, linha 240.
- proc(n) — chamada p.read_bytes, linha 256.

**Saídas.**

- {p} — chamada p.write_text, linha 54.
- {p} — chamada p.open, linha 57.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_Comum.ROU — chamada .write_text, linha 156.
- E:/copasa_map/output/entradas_corrigidas/{name} — chamada .write_text, linha 174.
- E:/copasa_map/output/entradas_corrigidas/CALPUFF-{k}_corrigido.INP — chamada .write_text, linha 214.
- E:/copasa_map/output/entradas_corrigidas/CALPUFF-CMAS_TOTAL_corrigido.INP — chamada .write_text, linha 229.

**Campos e chaves lidos.**

- d: area, base, elev, flux, height, hill, index, mass, old_flux, origin, params, type, x, xy, xyinc, y.
- w: Comportamento, Entrada.
- s: B29, B31, B4, B54, B56, B58, B6, E13, K33, N17, N19, N20, N22, N23, N24.
- actual: NC, VM.
- cal: NC, VM.
- window: end, hours, start.
- z: Diam, Num_Coords, Type.

**Campos e chaves gerados.**

- : area, params, xy, xyinc.
- d: area, height, old_flux, receptor_id.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| dump(p, d) | 54-54 | grava produtos |
| csvout(p, rows) | 56-58 | Chamadas efetivas: p.open, csv.DictWriter, w.writeheader, w.writerows, list |
| nums(s) | 60-60 | Chamadas efetivas: float, re.findall, s.replace Retorno: [float(x) for x in re.findall('[-+]?\\d*\\.?\\d+(?:[EeDd][-+]?\\d+)?', s.replace('D', 'E'))]. |
| parse_cal(p) | 62-71 | lê dados Retorno: (t, out). |
| parse_aer(p) | 73-84 | lê dados Retorno: (t, out). |
| parse_rou(p) | 86-103 | lê dados Retorno: rows. |
| main() | 105-259 | lê dados; grava produtos Retorno: '\n'.join(lines) + '\n', (start, t.index('---------------', start + 25)). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_e_preparar.py, linhas 125-131.

```python
    dump(A/'Geometria_UASB_WWTP2.json',geometry_revision)
    actual={'VM':sum(d['area'] for n,d in aer.items() if n.startswith('VM_UASB')),'NC':sum(d['area'] for n,d in aer.items() if n.startswith('NC_UASB'))}
    process={'VM_PRE':s['N17'].value,'VM_UASB':s['B29'].value*actual['VM']*s['B31'].value+s['K33'].value,'VM_CALHA':s['N19'].value,'NC_PRE':s['N20'].value,'NC_UASB':s['B54'].value*actual['NC']*s['B56'].value*s['B58'].value,'NC_FB':s['N22'].value,'TRANSFER_A':s['N23'].value,'TRANSFER_B':s['N24'].value}
    def proc(n):
        for p in sorted(process,key=len,reverse=True):
            if n.startswith(p):return p
        raise ValueError(n)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/avaliacao_espacial_meteorologica.py

Gráficos científicos e descritores condicionais dos dois modelos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\avaliacao_espacial_meteorologica.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_copasa | Módulo autoral local; sua ficha está neste relatório. |
| comparar_modelos_cmas | Módulo autoral local; sua ficha está neste relatório. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {O}/Comparacao_consolidada.json — chamada .read_text, linha 64.
- {O}/Campos_nativos.npz — chamada np.load, linha 64.
- {O}/Entradas_executadas_fontes.csv — chamada .open, linha 64.
- {O}/Meteorologia_AERMET.csv — chamada pd.read_csv, linha 65.
- {O}/Meteorologia_CALMET.csv — chamada pd.read_csv, linha 65.
- {C}/AERMOD_{k}_1h.npy — chamada np.load, linha 67.
- {C}/AERMOD_{k}_1h.json — chamada .read_text, linha 67.
- {C}/CALPUFF_{k}_1h.npy — chamada np.load, linha 70.
- {C}/CALPUFF_{k}_1h.json — chamada .read_text, linha 70.
- E:/copasa_map/CMAS/CALPUFF/CALPUFF-{k}.LST — chamada .read_text, linha 76.
- {O}/Pares_nativos_{k}_24h.csv — chamada pd.read_csv, linha 141.

**Saídas.**

- E:/copasa_map/output/cmas_poster/figuras/{stem}.{ext} — chamada fig.savefig, linha 60.
- E:/copasa_map/output/cmas_poster/figuras/{stem}.png — chamada fig.savefig, linha 61.
- E:/copasa_map/output/cmas_poster/figuras/{stem}_previa.png — chamada fig.savefig, linha 61.
- {C}/CALPUFF_{k}_executado.INP — chamada embedded.write_text, linha 72.
- {fig} — chamada savefig, linha 142.

**Campos e chaves lidos.**

- meta: codes, xy.
- met: calm, missing, time_end.
- cmeta: embedded_input, end_times, start_times, xy.
- p: AERMOD, CALPUFF, distance_m, x, y.
- cm: unit.
- weather: clock.
- aa: calm, direction, missing, speed.
- bb: direction, speed.
- df: category, distance_min_m, model, unit.
- s: mean.
- v: max_distance_m, min_distance_m.

**Campos e chaves gerados.**

- met: clock.
- own: clock.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| savefig(fig, stem) | 59-61 | grava produtos |
| main() | 63-143 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/avaliacao_espacial_meteorologica.py, linhas 83-89.

```python
            month=clocks.dt.month.to_numpy() if hasattr(clocks,'dt') else clocks.month.to_numpy()
            meteorological.append(dict(unit=k,model=model,hours=int(ok.sum()),median_wind_m_s=float(np.median(ws[ok])),mean_wind_m_s=float(np.mean(ws[ok])),low_wind_below_1_percent=float(100*np.mean(ws[ok]<1)),wind_p90_m_s=float(np.quantile(ws[ok],.9))))
            for lo,hi in [(0,100),(100,500),(500,1800)]:
                pick=(p.distance_m>=lo)&(p.distance_m<hi);ix=indices[pick]
                if not len(ix):continue
                response=np.mean(arr[:,ix],axis=1)
                for category,cat in [('speed',np.digitize(ws,[1,2,4,6])),('direction',np.floor((wd+22.5)%360/45).astype(int)),('hour',clockhour),('month',month)]:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Associa valores a intervalos definidos pelos cortes do código, inclusive classes de relevo ou faixas de distância.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- digitize: Associa valores a intervalos definidos pelos cortes do código, inclusive classes de relevo ou faixas de distância.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_copasa.mjs

Caminhos copasa. Configuração compartilhada. A organização passa por settings, raizProjeto, caminho, callback, externo, adaptarTexto, callback, adaptarRuntime.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\copasa_map\codigo\caminhos_copasa.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| node:fs | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:path | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:url | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |


**Entradas.**

- process.env[envKey+'_CONFIG'] /  / path.join(code,'caminhos_projeto.json') — chamada fs.readFileSync, linha 14.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_copasa.mjs, linhas 14-22.

```javascript
const settings=()=>JSON.parse(fs.readFileSync(process.env[envKey+'_CONFIG']||path.join(code,'caminhos_projeto.json'),'utf8').replace(/^\uFEFF/,''));

// Configuração e raiz
export function raizProjeto(style='posix'){
 const c=settings();let r=process.env[envKey]||(project==='congonhas'?process.env.EMI_PROJECT_ROOT:'')||c.raiz_projeto||path.dirname(code);
 r=path.isAbsolute(r)?r:path.resolve(code,r);return style==='posix'?r.replaceAll('\\','/'):r;
}

// Pastas e arquivos
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_copasa.ps1

Caminhos copasa. Configuração compartilhada. A organização passa por Get, Get, Get, Get, Convert.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\copasa_map\codigo\caminhos_copasa.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_copasa.ps1, linhas 12-20.

```text
function Get-PortableSettings { Get-Content -LiteralPath $script:PortableConfig -Raw -Encoding UTF8 | ConvertFrom-Json }
function Get-PortableRoot {
 $c=Get-PortableSettings
 $name="COPASA_PROJECT_ROOT"
 $value=[Environment]::GetEnvironmentVariable($name)
 if(-not $value -and "copasa" -eq 'congonhas'){$value=$env:EMI_PROJECT_ROOT}
 if(-not $value){$value=$c.raiz_projeto}
 if(-not $value){return (Split-Path $script:PortableCode -Parent)}
 if([System.IO.Path]::IsPathRooted($value)){return $value}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_copasa.py

Caminhos copasa. Configuração compartilhada. A organização passa por configuracao, raiz_projeto, caminho, texto_caminho, externo, adaptar_texto.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\copasa_map\codigo\caminhos_copasa.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(override).expanduser() if override else CONFIG_FILE — chamada path.read_text, linha 24.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- entry: chave, original.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| configuracao() | 21-24 | lê dados Retorno: json.loads(path.read_text('utf-8-sig')) if path.exists() else {}. |
| raiz_projeto() | 26-35 | Chamadas efetivas: configuracao, cfg.get, .strip, .expanduser, p.is_absolute, .resolve, os.environ.get, Path Retorno: BASE_CODIGO.parent, p if p.is_absolute() else (BASE_CODIGO / p).resolve(). |
| caminho(relativo='') | 38-47 | Chamadas efetivas: configuracao, raiz_projeto, .strip, sorted, cfg.get, .replace, rel.startswith, .expanduser Retorno: root / rel if rel else root, base / suffix if suffix else base. |
| texto_caminho(relativo='', estilo='posix') | 49-51 | Chamadas efetivas: caminho, p.as_posix, str Retorno: p.as_posix() if estilo == 'posix' else str(p). |
| externo(chave) | 54-68 | Chamadas efetivas: configuracao, .get, .expanduser, KeyError, isinstance, entry.get, str, ValueError Retorno: p.as_posix() if '/' in text and '\\' not in text else str(p). |
| adaptar_texto(texto) | 71-89 | Chamadas efetivas: configuracao, cfg.get, .values, re.compile, pattern.sub, original.replace, texto_caminho, .join Retorno: pattern.sub(lambda m: pairs[m[0]], str(texto)), texto. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_copasa.py, linhas 26-34.

```python
def raiz_projeto():
    cfg=configuracao()
    explicit=os.environ.get(ENV_RAIZ,'').strip() or (os.environ.get('EMI_PROJECT_ROOT','').strip() if PROJETO=='congonhas' else '') or cfg.get('raiz_projeto','')
    if explicit:
        p=Path(explicit).expanduser()
        return p if p.is_absolute() else (BASE_CODIGO/p).resolve()
    if cfg.get('modo_entrega'):
        for p in BASE_CODIGO.parents:
            if (p/'01_entradas').is_dir() and (p/'02_saidas').is_dir():return p
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/cartografia_copasa.py

Gera mapas comparáveis de fontes, receptores e dispersão, com geometrias sem identificação das unidades, escala física e barras de concentração comuns.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\cartografia_copasa.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| atualizar_cartografia_cmas | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| contexto_ete | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.cm | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.text | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .read_text, linha 56.
- {path} — chamada path.read_text, linha 132.
- E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json — chamada .read_text, linha 152.
- selected['csv'] — chamada np.loadtxt, linha 159.
- E:/copasa_map/output/cmas_poster/figuras/Faixas_concentracao_poster.json — chamada .read_text, linha 205.

**Saídas.**

- E:/copasa_map/output/cmas_poster/figuras/{name}.{ext} — chamada fig.savefig, linha 115.
- E:/copasa_map/output/cmas_poster/figuras/{name}.png — chamada fig.savefig, linha 116.
- E:/copasa_map/output/cmas_poster/figuras/{name}_previa.png — chamada fig.savefig, linha 116.
- E:/copasa_map/output/cmas_poster/figuras/{name}_poster.{ext} — chamada fig.savefig, linha 126.
- E:/copasa_map/output/cmas_poster/figuras/{name}_poster.png — chamada fig.savefig, linha 127.
- plt.figure(figsize=(wc / 2.54, hc / 2.54)) — chamada save, linha 281.
- E:/copasa_map/output/cmas_poster/figuras/Faixas_concentracao_poster.json — chamada .write_text, linha 250.
- E:/copasa_map/output/cmas_poster/index.html — chamada .write_text, linha 262.
- E:/copasa_map/output/cmas_poster/figuras/Resultados_historicos.json — chamada .write_text, linha 283.
- E:/copasa_map/output/cmas_poster/figuras/Cartografia_metadados.json — chamada .write_text, linha 283.

**Campos e chaves lidos.**

- D: grid, sources_aermod.
- s: params, process, type, x, xy, y.
- event: period_end, period_start.
- v: color, finite_coverage, label, model, style, unit, width, x, y.
- selected: csv, period_end, period_start.

**Campos e chaves gerados.**

- record: poster_figure_cm, poster_scale.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| centre(k) | 62-64 | Chamadas efetivas: limite Retorno: ((x0 + x1) / 2, (y0 + y1) / 2). |
| bounds(k, span) | 66-68 | Chamadas efetivas: TO_GEO.transform, centre, GEOD.fwd Retorno: (GEOD.fwd(lon, lat, 270, span / 2)[0], GEOD.fwd(lon, lat, 180, span / 2)[1], GEOD.fwd(lon, lat, 90, span / 2)[0], GEOD.fwd(lon, lat, 0, span / 2)[1]). |
| frame(ax, k, span, scale) | 70-87 | Chamadas efetivas: bounds, ax.set_xlim, ax.set_ylim, ax.set_aspect, ax.set_facecolor, ax.set_xlabel, ax.set_ylabel, ax.set_xticks Retorno: (x0, y0, x1, y1). |
| sources(ax, k, filled=True) | 89-96 | Chamadas efetivas: .items, np.column_stack, ax.add_patch, n.startswith, np.linspace, TO_GEO.transform, Polygon, np.asarray |
| physical_layout(rows, span, scale, bottom_override=None) | 98-107 | Chamadas efetivas: plt.figure, range, axs.append, np.array, row.append, fig.add_axes Retorno: (fig, np.array(axs), wc, hc). |
| save(fig, name, poster_scale=None) | 109-128 | grava produtos |
| read_field(path, km=False) | 130-139 | lê dados Retorno: a[idx]. |
| event_title(event) | 141-145 | Chamadas efetivas: datetime.fromisoformat, start.strftime, end.strftime Retorno: f'{start.day:02d}–{end.day:02d} ' + end.strftime('%b %Y') + f' · {start:%H:%M}–{end:%H:%M}', start.strftime('%d %b %Y') + ' · 00:00–24:00'. |
| plume_pair(period='24', event=False) | 148-184 | lê dados; grava produtos |
| context_handles() | 186-187 | Chamadas efetivas: Patch, Line2D, ROAD_STYLES.values Retorno: [Line2D([], [], color='#122f40', linewidth=1.8, label='WWTP boundary')] + [Line2D([], [], color=v['color'], linewidth=v['width'], linestyle=v['style'], label=v['label']) for v in ROAD_STYLES.values()]. |
| context_legend(fig, y) | 189-190 | Chamadas efetivas: fig.legend, context_handles |
| credit(fig, y) | 192-193 | Chamadas efetivas: fig.text |
| poster_concentration_rows(only_annual=False) | 196-250 | lê dados; grava produtos |
| gallery() | 252-262 | grava produtos |
| main() | 264-283 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/cartografia_copasa.py, linhas 168-174.

```python
            lo,la=TO_GEO.transform(xx,yy);inside=(lo>=x0)&(lo<=x1)&(la>=y0)&(la<=y1)
            coverage=float(np.isfinite(zz[inside]).mean());assert coverage>.999,(path,coverage)
            m=ax.contourf(lo,la,np.maximum(zz,1e-12),levels=levels,cmap=cmap,norm=norm,extend='both',zorder=2);m.set_edgecolor('face');m.set_linewidth(.1)
            ax.contour(lo,la,zz,levels=[v for v in [1,10,100,1000] if v<vmax],colors='#24445b',alpha=.20,linewidths=.35,zorder=4)
            draw_context(ax,k,TO_GEO,True);sources(ax,k,False)
            label=model
            if period!='24':label+=' · annual mean' if i==0 else ' · max. 8,760 h mean'
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/cartografia_copasa.py, linhas 226-232.

```python
                lon,lat=TO_GEO.transform(xx,yy);inside=(lon>=x0)&(lon<=x1)&(lat>=y0)&(lat<=y1)
                coverage=float(np.isfinite(z[inside]).mean());assert coverage==1
                norm=LogNorm(.1,1200)
                m=ax.contourf(lon,lat,np.maximum(z,1e-12),levels=np.geomspace(.1,1200,65),cmap=cmap,norm=norm,extend='both',zorder=2)
                m.set_edgecolor('face');m.set_linewidth(.1)
                ax.contour(lon,lat,z,levels=[1,10,100,1000],colors='#24445b',alpha=.20,linewidths=.35,zorder=4)
                nl,nt=TO_GEO.transform(a[:,0],a[:,1]);visible=(nl>=x0)&(nl<=x1)&(nt>=y0)&(nt<=y1)
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/comparar_modelos_cmas.py

Lê saídas horárias AERMOD, interpreta os registros de concentração CALPUFF e organiza séries, coordenadas, códigos temporais, campos diários e anuais para comparação.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\comparar_modelos_cmas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_e_preparar | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_copasa | Módulo autoral local; sua ficha está neste relatório. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

- E:/copasa_map/in/CALMET.DAT — chamada p.open, linha 141.
- E:/copasa_map/temp/cache_nova_modelagem/CALMET_extracao.json — chamada meta.read_text, linha 133.
- E:/copasa_map/temp/cache_nova_modelagem/AERMOD_{unit}_1h.npy — chamada np.load, linha 108.
- E:/copasa_map/CMAS/AERMOD/H2S_TOTAL.ADO — chamada p.read_bytes, linha 114.
- E:/copasa_map/mod/AERMOD/H2S/H2S_TOTAL.ADO — chamada .read_bytes, linha 114.
- E:/copasa_map/mod/AERMOD/H2S/H2S_TOTAL.err — chamada err.read_text, linha 116.
- E:/copasa_map/in/AERMOD/AERMET/AERMET_COP.SFC — chamada path.read_text, linha 121.
- E:/copasa_map/output/comparacao_modelos/Meteorologia_CALMET.csv — chamada cache.open, linha 133.
- E:/copasa_map/output/auditoria/CALMET_DAT_verificado.json — chamada .read_text, linha 135.
- E:/copasa_map/CMAS/CALPUFF/RANK({k})_ODOR_{token}HR_CONC_C.DAT — chamada np.loadtxt, linha 215.

**Saídas.**

- {p} — chamada p.write_text, linha 56.
- {p} — chamada p.open, linha 60.

**Campos e chaves lidos.**

- m: codes, nx, ny, origin_x_m, origin_y_m, source, spacing_m, xy.
- mm: c, code, x, y.
- v: area, height, ix0, iy0, mass_g_s, max_distance_m, min_distance_m, model, old_flux, params, sigma, type, u, unit, v, x, xy, y.
- totals: AERMOD, CALPUFF.
- r: code, direction, speed.
- hmeta: last_end, start_end.
- all_fields: 24h, AERMOD, CALPUFF.
- result: elapsed_seconds.

**Campos e chaves gerados.**

- v: direction, speed.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| dump(p, v) | 56-56 | grava produtos |
| csvout(p, rows) | 58-61 | Chamadas efetivas: p.open, csv.DictWriter, w.writeheader, w.writerows, list |
| ident(p) | 63-63 | Chamadas efetivas: dict, str, p.stat Retorno: dict(path=str(p), bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns). |
| stamp(code) | 65-66 | Chamadas efetivas: int, dt.datetime.strptime, dt.timedelta, str Retorno: dt.datetime.strptime(str(code // 100), '%y%m%d') + dt.timedelta(hours=h). |
| native(p) | 68-75 | Chamadas efetivas: p.open, np.array, l.split, rows.append, codes.append, .startswith, header.append, list Retorno: (np.array(rows), np.array(codes), header). |
| hourly(unit) | 77-108 | lê dados; grava produtos Retorno: (np.load(cache, mmap_mode='r'), xy, codes, m), (np.load(cache, mmap_mode='r'), np.array(m['xy']), np.array(m['codes']), m). |
| met_aermet() | 111-127 | lê dados Retorno: (rows, missing, calm). |
| met_calmet() | 130-168 | lê dados; grava produtos Retorno: (rows, metaobj), (list(csv.DictReader(f)), json.loads(meta.read_text())). |
| main() | 171-238 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/comparar_modelos_cmas.py, linhas 208-214.

```python
            series=np.mean(h[:,si],axis=1)
            for typ,cat in [('speed',np.digitize(ws,[1,2,4,6])),('direction',(np.floor((wd+22.5)%360/45)).astype(int)),('hour',hr)]:
                for v in np.unique(cat[valid]):
                    z=series[valid&(cat==v)];conditional.append(dict(unit=k,model='AERMOD',distance_min_m=lo,distance_max_m=hi,category=typ,bin=int(v),hours=len(z),receptors=len(si),median=float(np.median(z)),p90=float(np.quantile(z,.9)),mean=float(z.mean())))
        for per,values in vals.items():
            npz[f'{k}_AERMOD_{per}']=values;all_fields[k,'AERMOD',per]=(xy,values)
        for per,token in [('1h','1'),('24h','24'),('rank8760_max','8760'),('period_mean','17517')]:
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Associa valores a intervalos definidos pelos cortes do código, inclusive classes de relevo ou faixas de distância.

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- digitize: Associa valores a intervalos definidos pelos cortes do código, inclusive classes de relevo ou faixas de distância.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/complementar_metricas_p95.py

Compara o P95 horário de cada receptor entre modelos, com pares de coordenadas válidos e estatísticas de associação e concordância de magnitude.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\complementar_metricas_p95.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| grafico_concordancia_p95 | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| perfis_comparacao_modelos | Módulo autoral local; sua ficha está neste relatório. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/comparacao_modelos/Estatistica_horaria_por_receptor.csv — chamada pd.read_csv, linha 38.

**Saídas.**

- E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json — chamada .write_text, linha 55.
- E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.csv — chamada .to_csv, linha 56.
- E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv — chamada .to_csv, linha 57.

**Campos e chaves lidos.**

- data: distance_m, unit.
- near: AERMOD_P95, CALPUFF_P95, P95_within_factor_2, WWTP, distance_m, receptor_id, unit, x, y.
- r: distance_max_m, distance_min_m.

**Campos e chaves gerados.**

- near: P95_within_factor_2.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 37-63 | lê dados; grava produtos; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. Retorno: payload. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/complementar_metricas_p95.py, linhas 47-53.

```python
            within=(b>=.5*a)&(b<=2*a)
            rho=float(spearmanr(a,b).statistic) if len(s)>1 and np.ptp(a)>0 and np.ptp(b)>0 else None
            results.append(dict(unit=unit,WWTP=1 if unit=='VM' else 2,distance_min_m=lo,distance_max_m=hi,n=len(s),within_factor_2_count=int(within.sum()),within_factor_2_percent=float(100*within.mean()),Spearman_rho_P95=rho,both_zero=int(((a==0)&(b==0)).sum()),one_zero=int(((a==0)^(b==0)).sum())))
        near['P95_within_factor_2']=(near.CALPUFF_P95>=.5*near.AERMOD_P95)&(near.CALPUFF_P95<=2*near.AERMOD_P95)
        selected=near[(near.AERMOD_P95>=.7)|(near.CALPUFF_P95>=.7)]
        sensitivity.append(dict(unit=unit,n=len(selected),selection='At least one model P95 >= 0.7 ug/m3',within_factor_2_percent=float(100*selected.P95_within_factor_2.mean()),Spearman_rho_P95=float(spearmanr(selected.AERMOD_P95,selected.CALPUFF_P95).statistic)))
        pairs.append(near[['unit','WWTP','receptor_id','x','y','distance_m','AERMOD_P95','CALPUFF_P95','P95_within_factor_2']])
```

Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_comparacao_atual.py

Integra as saídas da rodada nova, preserva seus critérios temporais e confere a reprodução dos indicadores nativos e os campos finais usados no pôster.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\consolidar_comparacao_atual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json — chamada p.read_text, linha 26.
- E:/copasa_map/output/comparacao_modelos/CALPUFF_horario_validado.json — chamada .read_text, linha 26.
- {path} — chamada path.read_bytes, linha 35.

**Saídas.**

- E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json — chamada p.write_text, linha 28.
- E:/copasa_map/descontinuado/2026_11_10_novos_resultados/manifesto_nova_rodada.json — chamada .write_text, linha 41.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_comparacao_atual.py, linhas 25-33.

```python
R=Path(_cp_texto('', 'posix'));O=R/'output/comparacao_modelos';A=R/'descontinuado/2026_11_10_novos_resultados'
p=O/'Comparacao_consolidada.json';d=json.loads(p.read_text(encoding='utf8'));cal=json.loads((O/'CALPUFF_horario_validado.json').read_text(encoding='utf8'))
d.update(quality_CALPUFF=cal,annual_CALPUFF_status='Derived from current hourly CONC, highest calendar-year mean at each receptor. 2024 complete; 2025 99.680365% available. No 8760h RANK substitution.',hourly_CALPUFF_status='Decoded current CONC files and reproduced native RANK fields within printed precision. Embedded input matches supplied INP. Normal end confirmed in current LST.',AERMET_time_zone='LOCATION 0 is a time adjustment, not proof of UTC. Supplied SAMSON header declares zone 0; original interval/clock convention needs confirmation against CALMET UTC-3. Each model is conditioned on its own executed meteorology. One-hour label offset is documented as a diagnostic, not imposed.',publication='Current poster and gallery use CMAS/AERMOD and CMAS/CALPUFF new outputs supplied on 10 November 2026')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
manifest=[]
for stem in ['Comparacao_24h_pre_harmonizacao','Comparacao_anual_8760h_pre_harmonizacao','Cenarios_24h_eventos_coerentes']:
    for path in (R/'output/cmas_poster/figuras').glob(stem+'*'):
        if not path.is_file():continue
        target=A/'figuras_historicas'/path.name;target.parent.mkdir(parents=True,exist_ok=True)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/contexto_ete.py

Contexto vetorial sem rótulos: vias/edificações externas e limite fornecido.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\contexto_ete.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.collections | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/in/cartografia_contexto/OSM_{k}.json — chamada p.read_text, linha 53.
- E:/copasa_map/CMAS/vias/malha_viaria.shp — chamada gpd.read_file, linha 75.

**Saídas.**

- E:/copasa_map/output/auditoria/Contexto_cartografico.json — chamada .write_text, linha 137.

**Campos e chaves lidos.**

- data: elements.
- v: lat, lon.
- tags: highway.
- st: color, style, width.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| road_class(kind) | 42-46 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: 'other', 'primary'. |
| layers(k) | 48-98 | lê dados Retorno: CACHE[k], CACHE[k]. |
| line_parts(g) | 100-104 | Chamadas efetivas: hasattr, line_parts |
| draw(ax, k, to_geo, plume=False) | 106-131 | Chamadas efetivas: layers, line_parts, ax.add_collection, ax.set_xlim, ax.set_ylim, ax.get_xlim, ax.get_ylim, b.append |
| export_metadata() | 133-138 | grava produtos Retorno: result. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/contexto_ete.py, linhas 135-138.

```python
    for k in ['VM','NC']:
        b,r,h=layers(k);result[k]=dict(boundary_file='v_maria/vm_limite.kmz' if k=='VM' else 'n_contagem/nc_limite.kmz',boundary_area_m2=b.area,road_features=len(r),road_classes={c:sum(road_class(t)==c for g,t in r) for c in ROAD_STYLES},classification='Provided hier_legal: arterial/rodovia primary and secondary; coletora principal/vicinal collector. Municipal or missing hierarchy remains local/unclassified. OSM highway fills uncovered context.',building_features=len(h),names_drawn=False,source='Provided CMAS/vias/malha_viaria.shp (EPSG:31983), reprojected to EPSG:32723; © OpenStreetMap contributors',cartographic_matching_tolerance_m=10,license='OSM complement: ODbL; supplied road dataset provenance retained as received',url='https://www.openstreetmap.org/copyright')
    (R/'output/auditoria/Contexto_cartografico.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    return result
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/converter_receptores_calpuff.ps1

Converter receptores calpuff. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\converter_receptores_calpuff.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/converter_receptores_calpuff.ps1, linhas 10-18.

```text
. (Join-Path $PSScriptRoot 'caminhos_copasa.ps1')
$ErrorActionPreference = 'Stop'
$projectRoot = (Get-PortablePath '')
$targetFolder = Join-Path $projectRoot 'output\entradas_corrigidas\CALPUFF'
New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null
$excelApp = New-Object -ComObject Excel.Application
$excelApp.Visible = $false
$excelApp.DisplayAlerts = $false
try {
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/corrigir_postfile_duplicado.py

Corrige somente o conflito POSTFILE de animação, preservando a entrada recebida.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\corrigir_postfile_duplicado.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| difflib | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/mod/AERMOD/H2S/H2S_TOTAL.ADI — chamada src.read_bytes, linha 70.

**Saídas.**

- E:/copasa_map/output/entradas_corrigidas/correcao_postfile/H2S_TOTAL_POSTFILE_corrigido.ADI — chamada target.write_bytes, linha 48.
- E:/copasa_map/output/entradas_corrigidas/correcao_postfile/Bloco_OU_corrigido.txt — chamada .write_text, linha 50.
- E:/copasa_map/output/entradas_corrigidas/correcao_postfile/Verificacao_POSTFILE.json — chamada .write_text, linha 52.
- E:/copasa_map/output/entradas_corrigidas/correcao_postfile/Alteracoes.diff — chamada .write_text, linha 53.
- E:/copasa_map/output/entradas_corrigidas/correcao_postfile/LEIA_PRIMEIRO.md — chamada .write_text, linha 54.

**Campos e chaves lidos.**

- audit: source_sha256.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| post(line) | 32-35 | Chamadas efetivas: .split, line.upper, len Retorno: q if len(q) >= 5 and q[0] == 'POSTFILE' else None. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/corrigir_postfile_duplicado.py, linhas 32-40.

```python
def post(line):
    q=line.upper().split()
    if q and q[0]=='OU':q=q[1:]
    return q if len(q)>=5 and q[0]=='POSTFILE' else None
posts=[(i+1,post(line)) for i,line in enumerate(lines) if post(line)]
plot_keys={(q[1],q[2]) for n,q in posts if q[3]=='PLOT'}
remove={n for n,q in posts if q[3]=='UNFORM' and (q[1],q[2]) in plot_keys}
assert remove=={126,127,128},sorted(remove)
fixed=''.join(line for i,line in enumerate(lines,1) if i not in remove and '1-Hour Binary POSTFILE(s) for the Plume Animation' not in line)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/diagnosticar_medias.py

Diagnosticar medias. Auditoria/diagnóstico. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\copasa_map\codigo\diagnosticar_medias.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| comparar_modelos_cmas | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/diagnosticar_medias.py, linhas 29-33.

```python
print(list(zip(codes[s].tolist(),h[s,j].tolist(),valid[s].tolist())))
print('Ratios',native24[i,j]/h[s,j].sum(),h[s,j].sum()/native24[i,j]);print('First native',a[:2],dc[:2]);print('Other errors',np.quantile(abs(native24-q),[0,.5,.9,.99,1]))
print('headers',hd[:8])
for y in [24,25]:
    a,ac,ah=native(R/'CMAS/AERMOD/AN_GWWTP1.POS');z=a[:,2].reshape(2,len(xy));s=codes//1000000==y;v=np.asarray(h[s],dtype='float64').sum(axis=0)/valid[s].sum();print('annual',y,np.max(abs(v-z[y-24])),valid[s].sum(),v.max(),z[y-24].max())
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/estatistica_horaria_avancada.py

Calcula estatísticas horárias em cada receptor e compõe distribuições espaciais por faixas de distância, separando o percentil temporal do boxplot entre receptores.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\estatistica_horaria_avancada.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_e_preparar | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| comparar_modelos_cmas | Módulo autoral local; sua ficha está neste relatório. |
| complementar_metricas_p95 | Módulo autoral local; sua ficha está neste relatório. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.backends.backend_pdf | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- files[j] — chamada np.loadtxt, linha 98.
- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .read_text, linha 104.
- E:/copasa_map/temp/cache_nova_modelagem/AERMOD_{k}_1h.json — chamada .read_text, linha 112.
- E:/copasa_map/temp/cache_nova_modelagem/CALPUFF_{k}_1h.json — chamada .read_text, linha 112.
- E:/copasa_map/temp/cache_nova_modelagem/AERMOD_{k}_1h.npy — chamada np.load, linha 112.
- E:/copasa_map/temp/cache_nova_modelagem/CALPUFF_{k}_1h.npy — chamada np.load, linha 112.
- E:/copasa_map/output/comparacao_modelos/Pares_nativos_{k}_24h.csv — chamada pd.read_csv, linha 114.
- E:/copasa_map/output/comparacao_modelos/Meteorologia_AERMET.csv — chamada pd.read_csv, linha 115.
- E:/copasa_map/output/comparacao_modelos/Estatistica_horaria_por_receptor.csv — chamada pd.read_csv, linha 189.
- E:/copasa_map/output/comparacao_modelos/Estatistica_avancada.json — chamada .read_text, linha 191.

**Saídas.**

- E:/copasa_map/output/cmas_poster/figuras/{name}.{ext} — chamada fig.savefig, linha 78.
- E:/copasa_map/output/cmas_poster/figuras/{name}.png — chamada fig.savefig, linha 79.
- E:/copasa_map/output/cmas_poster/figuras/{name}_previa.png — chamada fig.savefig, linha 79.
- {fig} — chamada save, linha 172.
- {fig} — chamada pdf.savefig, linha 184.

**Campos e chaves lidos.**

- art: boxes, medians.
- meta: source, start_times, xy.
- D: grid.
- a: area, base, boxes, height, medians, old_flux, params.
- v: area, base, height, old_flux, sigma, x, y.
- p: distance_m, x, y.
- hm: codes, xy.
- cm: start_times, xy.
- met: calm, missing.
- g: x, y.
- row: AERMOD_P95, AERMOD_mean, CALPUFF_P95, CALPUFF_mean.
- u: boxplot_eligible, distance_m, monitoring_location, screen_active.
- active: x, y.
- ax.spines: bottom, left.
- r: distance_m, receptor_id, unit.
- d: model, values.
- data: boxplot_eligible, unit.

**Campos e chaves gerados.**

- row: boxplot_eligible.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save(fig, name) | 77-79 | grava produtos |
| statsbox(row, model, label='') | 81-82 | Chamadas efetivas: dict, float Retorno: dict(label=label, whislo=float(row[f'{model}_P05']), q1=float(row[f'{model}_P25']), med=float(row[f'{model}_P50']), q3=float(row[f'{model}_P75']), whishi=float(row[f'{model}_P95']), fliers=[]). |
| add_boxes(ax, stats, pos, color, width=0.3) | 84-90 | Chamadas efetivas: ax.bxp, z.set Retorno: art. |
| validate_exports(k, arr, meta) | 92-101 | lê dados Retorno: dict(available_files=len(files), sampled=out, complete_series_source=meta['source']['path'], all_hours_from_binary=True), dict(available_files=0, sampled=[]). |
| main() | 103-148 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| render_monitor(u, k) | 151-158 | grava produtos |
| render_comparison_and_atlas(poster, atlas) | 161-185 | grava produtos |
| render_cached() | 188-192 | lê dados |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/estatistica_horaria_avancada.py, linhas 116-122.

```python
        assert A.shape[0]==8496 and B.shape[0]==8784
        quantiles=[.05,.1,.25,.5,.75,.9,.95,.98,.99];aq=np.quantile(A,quantiles,axis=0);bq=np.quantile(B,quantiles,axis=0)
        near_monitor=[]
        for v in monitor:
            dist,ind=cKDTree(xy).query([v['x'],v['y']])
            if dist<=.01:near_monitor.append((ind,str(v.get('id',v.get('receptor_id',v.get('ID',''))))))
        ids={}
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/extrair_calpuff_novo.py

Decodifica a nova saída CALPUFF recebida, preservando o cabeçalho, as espécies, os receptores e a sequência temporal para a comparação com o AERMOD.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\copasa_map\codigo\extrair_calpuff_novo.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| comparar_modelos_cmas | Módulo autoral local; sua ficha está neste relatório. |
| extrair_eventos_24h | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {C}/CALPUFF_{unit}_1h.json — chamada meta.read_text, linha 36.
- {C}/CALPUFF_{unit}_1h.npy — chamada np.load, linha 55.
- E:/copasa_map/CMAS/CALPUFF/RANK({unit})_ODOR_1HR_CONC_C.DAT — chamada np.loadtxt, linha 37.
- E:/copasa_map/CMAS/CALPUFF/CONC-{unit}.DAT — chamada path.open, linha 39.
- {O}/Campos_nativos.npz — chamada np.load, linha 58.
- E:/copasa_map/CMAS/CALPUFF/RANK({k})_ODOR_{token}HR_CONC_C.DAT — chamada np.loadtxt, linha 61.

**Saídas.**

- {C}/CALPUFF_{k}_24h.npy — chamada np.save, linha 76.

**Campos e chaves lidos.**

- m: embedded_input, end_times, start_times, xy.
- v: max_abs_error, passed.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| caltime(b) | 31-32 | Chamadas efetivas: map, dt.datetime, dt.timedelta Retorno: dt.datetime(y, 1, 1) + dt.timedelta(days=j - 1, hours=h, seconds=s). |
| extract(unit) | 34-55 | lê dados; grava produtos Retorno: (np.load(cache, mmap_mode='r'), m), (np.load(cache, mmap_mode='r'), json.loads(meta.read_text())). |
| main() | 57-80 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/extrair_calpuff_novo.py, linhas 65-71.

```python
        for offset in [0,1]:
            size=(len(h)-offset)//24;d=np.asarray(h[offset:offset+24*size],dtype='float64').reshape(size,24,n).mean(axis=1);env=d.max(axis=0);ref=rank('24')
            er=float(abs(env-ref).max());passed=bool(np.allclose(env,ref,rtol=6e-5,atol=1e-6));choices.append(dict(offset=offset,max_abs_error=er,passed=passed))
        ok=[v for v in choices if v['passed']];assert ok,(k,choices);offset=min(ok,key=lambda v:v['max_abs_error'])['offset'];size=(len(h)-offset)//24
        daily=np.asarray(h[offset:offset+size*24],dtype='float64').reshape(size,24,n).mean(axis=1);dstarts=[starts[offset+i*24] for i in range(size)]
        mean=np.mean(h,axis=0,dtype='float64');ref=rank('17517');ermean=float(abs(mean-ref).max());assert np.allclose(mean,ref,rtol=6e-5,atol=1e-6),(k,ermean)
        yrs=np.array([t.year for t in starts]);annual=[];yrmeta=[]
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/extrair_eventos_24h.py

Campos simultâneos de 24 h, extraídos de saídas horárias já executadas.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\copasa_map\codigo\extrair_eventos_24h.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {p} — chamada p.read_text, linha 38.
- E:/copasa_map/in/CONC-{k}.DAT — chamada p.open, linha 89.
- E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json — chamada manifest.read_text, linha 128.

**Saídas.**

- E:/copasa_map/output/cmas_poster/dados_cenarios24h/CALPUFF_{k}_auditoria_janelas.json — chamada .write_text, linha 120.
- E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json — chamada manifest.write_text, linha 134.

**Campos e chaves lidos.**

- mm: average, c, code, lead, tail.
- d: comparison_passed, csv, hourly_source, max_abs_error.
- chosen: offset.
- old: events.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| table(p, km=False) | 36-44 | lê dados Retorno: (np.array(rows), codes). |
| identity(p) | 46-46 | Chamadas efetivas: dict, str, p.stat Retorno: dict(path=str(p), bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns). |
| write(model, k, xy, values, meta) | 48-52 | Chamadas efetivas: np.savetxt, meta.update, np.column_stack, str, len, float, values.max, values.min Retorno: meta. |
| aermod(k, sg, pl) | 54-66 | Chamadas efetivas: table, len, int, np.dtype, np.memmap, np.flatnonzero, np.all, .mean Retorno: write('AERMOD', k, native[:, :2], field, dict(period_start=date.isoformat(), period_end=(date + dt.timedelta(days=1)).isoformat(), hours=24, selection='Date of the highest native 1ST HIGH 24h receptor. |
| unpack_record(f) | 68-73 | Chamadas efetivas: f.read, struct.unpack, len Retorno: b, None. |
| decode(b) | 75-79 | Chamadas efetivas: np.frombuffer, .astype, np.zeros, np.cumsum, counts.sum, np.where, np.trunc Retorno: values * 1000000.0. |
| stamp(values) | 81-83 | Chamadas efetivas: map, dt.datetime, dt.timedelta Retorno: dt.datetime(year, 1, 1) + dt.timedelta(days=day - 1, hours=hour, seconds=second). |
| calpuff(k, suffix) | 85-123 | grava produtos Retorno: write('CALPUFF', k, native[:, :2], a[i], dict(period_start=start.isoformat(), period_end=end.isoformat(), hours=24, selection='Complete 24h averaging block with the highest receptor concentration; mat. |
| main() | 125-135 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/extrair_eventos_24h.py, linhas 61-67.

```python
    assert np.all(mm['average'][select]==1)
    field=mm['c'][select].mean(axis=0);err=float(abs(field[j]-native[j,2]));assert err<1e-5,(k,err)
    same_date=np.array([int(c)//100==day for c in codes]);same_date_error=float(np.max(abs(field[same_date]-native[same_date,2])))
    assert same_date_error<1e-5,(k,same_date_error)
    date=dt.datetime.strptime(str(day),'%y%m%d')
    return write('AERMOD',k,native[:,:2],field,dict(period_start=date.isoformat(),period_end=(date+dt.timedelta(days=1)).isoformat(),hours=24,selection='Date of the highest native 1ST HIGH 24h receptor value; all receptors on the same day',native_rank_file=str(R/'CMAS'/pl),native_rank_peak=float(native[j,2]),peak_reproduction_error=err,same_date_peak_receptors=int(same_date.sum()),same_date_peak_max_error=same_date_error,hourly_source=identity(p),timezone='as executed by AERMET; preprocessor convention to confirm'))
# Unpack record
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_poster.py

Gera os mapas COPASA com o encarte geográfico consolidado.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\figuras_poster.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_copasa | Módulo autoral local; sua ficha está neste relatório. |
| extrair_eventos_24h | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_poster.py, linhas 8-16.

```python
"""Gera os mapas COPASA com o encarte geográfico consolidado."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_copasa.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_copasa.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/garantir_imagens_mapas.py

Incorpora PNGs científicos reais como fallback dos SVGs do PowerPoint.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\garantir_imagens_mapas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| posixpath | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- sys.argv[2] — chamada .read_text, linha 38.
- sys.argv[1] — chamada zipfile.ZipFile, linha 39.
- x['svg'] — chamada .read_bytes, linha 41.
- item['png'] — chamada .read_bytes, linha 46.
- io.BytesIO(raw) — chamada Image.open, linha 46.
- Argumento fornecido pelo chamador — chamada im.load, linha 54.
- io.BytesIO(v) — chamada Image.open, linha 54.

**Saídas.**

- sys.argv[1] — chamada zipfile.ZipFile, linha 51.
- Path(sys.argv[2]).with_name('imagens_verificadas.json') — chamada .write_text, linha 55.

**Campos e chaves lidos.**

- files: ppt/slides/_rels/slide1.xml.rels, ppt/slides/slide1.xml.
- x: svg.
- N: r.
- item: png, svg.

**Campos e chaves gerados.**

- files: ppt/slides/slide1.xml.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/garantir_imagens_mapas.py, linhas 37-45.

```python
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','s':'http://schemas.microsoft.com/office/drawing/2016/SVG/main'}
path=Path(sys.argv[1]);items=json.loads(Path(sys.argv[2]).read_text(encoding='utf8'))
with zipfile.ZipFile(path) as z:files={n:z.read(n) for n in z.namelist()}
root=E.fromstring(files['ppt/slides/slide1.xml']);rel={r.get('Id'):r.get('Target').lstrip('/') if r.get('Target').startswith('/') else posixpath.normpath('ppt/slides/'+r.get('Target')) for r in E.fromstring(files['ppt/slides/_rels/slide1.xml.rels'])}
lookup={hashlib.sha256(Path(x['svg']).read_bytes()).hexdigest():x for x in items};used=[]
for p in root.findall('.//p:pic',N):
    sv=p.find('.//s:svgBlip',N)
    if sv is None:continue
    target=rel[sv.get('{'+N['r']+'}embed')];item=lookup[hashlib.sha256(files[target]).hexdigest()]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/geometria_ete.py

Limites fornecidos e regularização geométrica autorizada dos UASB NC.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\geometria_ete.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/copasa_map/'v_maria/vm_limite.kmz' if k == 'VM' else 'n_contagem/nc_limite.kmz' — chamada zipfile.ZipFile, linha 36.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- cal: NC.
- d: area.
- record: sources.

**Campos e chaves gerados.**

- d: area, old_area, xy.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| limite(k) | 34-41 | Chamadas efetivas: r.findall, str, transform, zipfile.ZipFile, ET.fromstring, polygons.append, unary_union, z.read Retorno: transform(TO_UTM.transform, unary_union(polygons)). |
| regularizar(aer, cal) | 43-68 | Chamadas efetivas: np.array, centres.mean, np.linalg.svd, float, dict, limite, enumerate, Polygon Retorno: record. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/geometria_ete.py, linhas 45-51.

```python
    centres=np.array([[p.centroid.x,p.centroid.y] for p in old]);mid=centres.mean(axis=0)
    _,_,vh=np.linalg.svd(centres-mid);along=vh[0]
    if np.dot(along,centres[2]-centres[0])<0:along=-along
    across=np.array([-along[1],along[0]])

    widths=[]
    for p in old:
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Decomposição em valores singulares. Na PCA, a matriz centrada é decomposta em U, s e V; a proporção de variância é s²/Σs². É uma descrição da variação, não teste causal.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- svd: Decomposição em valores singulares. Na PCA, a matriz centrada é decomposta em U, s e V; a proporção de variância é s²/Σs². É uma descrição da variação, não teste causal.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_poster_copasa.mjs

Monta o pôster de duas colunas no modelo oficial e insere mapas e estatísticas auditadas; os boxplots e perfis do pôster são elementos editáveis.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\gerar_poster_copasa.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_copasa.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:fs | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:url | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:crypto | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:module | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |


**Entradas.**

- _cpPath("codigo/runtime_workspace.json") — chamada readFileSync, linha 32.
- await FileBlob.load(SRC) — chamada PresentationFile.importPptx, linha 44.
- SRC — chamada FileBlob.load, linha 44.
- O+'/figuras/Cartografia_metadados.json' — chamada readFileSync, linha 67.
- R+'/output/auditoria/Auditoria_consolidada.json' — chamada readFileSync, linha 69.
- R+'/output/comparacao_modelos/Comparacao_consolidada.json' — chamada readFileSync, linha 71.
- R+'/output/comparacao_modelos/Estatistica_avancada.json' — chamada readFileSync, linha 73.
- R+'/output/comparacao_modelos/Concordancia_espacial_P95.json' — chamada readFileSync, linha 75.
- O+'/figuras/Perfis_comparacao_modelos.json' — chamada readFileSync, linha 79.
- file — chamada readFileSync, linha 84.
- A+'/'+f — chamada readFileSync, linha 227.
- R+'/output/comparacao_modelos/Notas_poster_English.txt' — chamada readFileSync, linha 237.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- candidate — chamada (await PresentationFile.exportPptx(p)).save, linha 239.
- p — chamada PresentationFile.exportPptx, linha 239.
- O+'/figuras/Boxplots_editaveis_dados.json' — chamada fs.writeFile, linha 241.
- O+'/figuras/Perfis_editaveis_dados.json' — chamada fs.writeFile, linha 243.
- T+'/mapas_incorporados.json' — chamada fs.writeFile, linha 245.
- archive+'/manifesto.json' — chamada fs.writeFile, linha 251.
- {workspaceDir:R,candidatePath:candidate,finalPath:O+'/Poster_CMAS_Session05_WWTP.pptx',pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',lay — chamada finalizePresentation, linha 253.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_poster_copasa.mjs, linhas 48-56.

```javascript
const keep=['sh/jitg36dg','sh/9kby1g3i'];p.delete(rec.filter(r=>r.position&&r.position.top>=650&&!keep.includes(r.id)&&['shape','textbox','image','chart'].includes(r.kind)).map(r=>r.id));

const C={ink:'#173445',blue:'#287e96',muted:'#566772',gold:'#f6a72c'},L=70,RX=2320,CW=2110;

// text
function text(t,x,y,w,h,size=36,bold=false,align='left',color=C.ink){const z=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});z.text=t;z.text.style={typeface:'Arial',fontSize:size,bold,alignment:align,color,verticalAlignment:'top',insets:0,autoFit:'none',wrap:'square'};return z;}

// update
function update(id,t,size){const z=p.resolve(id);z.text=t;z.text.style={typeface:'Arial',fontSize:size,bold:true,color:'#FFFFFF',alignment:'left',insets:0,autoFit:'none'};}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/grade_importacao.mjs

Grade importacao. Processamento ou módulo de apoio. A organização passa por callback.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\grade_importacao.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_copasa.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:module | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:url | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:child_process | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |


**Entradas.**

- R+'/codigo/runtime_workspace.json' — chamada fs.readFile, linha 19.
- R+'/output/auditoria/Grades_por_unidade.json' — chamada fs.readFile, linha 22.
- R+'/codigo/recursos_receptores/CALPUFF_Discrete_Receptors_modelo.xlsx' — chamada FileBlob.load, linha 25.
- R+'/codigo/converter_receptores_calpuff.ps1' — chamada fs.readFile, linha 45.
- R+'/codigo/verificar_calpuff_xls.ps1' — chamada fs.readFile, linha 46.
- A+'/manifesto.json' — chamada fs.readFile, linha 59.

**Saídas.**

- T+'/'+unit+'_errors.ndjson' — chamada fs.writeFile, linha 36.
- T+'/'+unit+'_'+suffix+'.png' — chamada fs.writeFile, linha 38.
- T+'/Grade_Receptora_'+unit+'_CALPUFF.xlsx' — chamada (await SpreadsheetFile.exportXlsx(w)).save, linha 40.
- A+'/manifesto.json' — chamada fs.writeFile, linha 60.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/grade_importacao.mjs, linhas 30-38.

```javascript
 s.getRange('A15').write(grid.map(q=>[q.id,q.x,q.y,q.elev,0,q.sensitive?'Monitoring receptor':'Regular receptor grid']));
 s.getRange('A15:F'+(grid.length+14)).format.font={name:'Arial',size:10};
 s.getRange('B15:C'+(grid.length+14)).setNumberFormat('0.0000');
 s.getRange('D15:E'+(grid.length+14)).setNumberFormat('0.00');
 w.recalculate();
 const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},summary:'formula error scan'});
 await fs.writeFile(T+'/'+unit+'_errors.ndjson',errors.ndjson);
 for(const[range,suffix]of[['A1:F23','cabecalho'],['A'+(15+d.counts[unit].monitoring)+':F'+(23+d.counts[unit].monitoring),'grade']]){
  const png=await w.render({sheetName:s.name,range,scale:1.2,format:'png'});await fs.writeFile(T+'/'+unit+'_'+suffix+'.png',new Uint8Array(await png.arrayBuffer()));
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/grafico_concordancia_p95.py

Dispersão P95 em pares nativos, com ampliação e visão integral dos extremos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\grafico_concordancia_p95.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv — chamada pd.read_csv, linha 43.
- E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json — chamada .read_text, linha 43.
- E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv — chamada .read_bytes, linha 71.

**Saídas.**

- E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.{ext} — chamada fig.savefig, linha 69.
- E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.png — chamada fig.savefig, linha 70.
- E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores_previa.png — chamada fig.savefig, linha 70.
- E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.json — chamada .write_text, linha 71.

**Campos e chaves lidos.**

- d: unit.
- summary: rows.
- x: distance_max_m, distance_min_m, unit.
- score: Spearman_rho_P95, WWTP, within_factor_2_percent.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 42-72 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/grafico_concordancia_p95.py, linhas 62-68.

```python
        inset.set(xlim=(0,cap),ylim=(0,cap),xticks=[0,cap],yticks=[0,cap]);inset.tick_params(labelsize=8,pad=2,length=2);inset.set_title('Full range',fontsize=9,pad=5);inset.set_aspect('equal')
        visible=int(((a<=30)&(b<=30)).sum());ax.text(.5,-.20,f'Zoom: 0–30 µg/m³ ({visible}/{len(s)} receptors shown)',transform=ax.transAxes,ha='center',fontsize=10,color='#536b77')
        evidence.append(dict(unit=k,n=len(s),n_visible_main=visible,n_in_full_range=len(s),full_range_max=cap,stats_all_receptors=True,Spearman_rho=score['Spearman_rho_P95'],within_factor_2_percent=score['within_factor_2_percent']))
    fig.suptitle('Intermodel comparison at matched receptors · 2024',fontsize=19,fontweight='bold',color='#173445',y=.975)
    handles=[Line2D([],[],marker='o',ls='',color=col[0],label='Within factor 2'),Line2D([],[],marker='o',ls='',color=col[1],label='Outside factor 2'),Line2D([],[],ls='--',color='#526874',label='Equal concentration (1:1)'),Patch(facecolor='#e4eeea',label='Factor-of-two band')]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.92),ncol=4,frameon=False,fontsize=11)
    fig.text(.5,.035,'Each point is the hourly P95 at one receptor within 1,800 m. Insets retain the full range; all receptors enter the statistics.\nThe two native hourly distributions are compared descriptively. Neither model is treated as an ambient observation.',ha='center',fontsize=10,color='#536b77',linespacing=1.6)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/guia_grade_poster.py

Guia de importação e interpretação da revisão COPASA.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\guia_grade_poster.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| runpy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.sax.saxutils | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/copasa_map/output/auditoria/Guia_grade_e_poster_COPASA.md — chamada .write_text, linha 81.

**Campos e chaves lidos.**

- st: BodyCOP, Heading1, Title.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| p(t) | 35-35 | Chamadas efetivas: story.append, md.append, Paragraph, escape |
| h(t) | 37-37 | Chamadas efetivas: story.append, md.append, Paragraph, escape |
| table(data, widths) | 39-42 | Chamadas efetivas: Table, t.setStyle, story.extend, md.append, TableStyle, Spacer, Paragraph, .join |
| footer(c, doc) | 79-79 | Chamadas efetivas: c.setFont, c.setFillColor, c.drawString, c.drawRightString, colors.HexColor, str |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/guia_grade_poster.py, linhas 35-43.

```python
def p(t):story.append(Paragraph(escape(t),st['BodyCOP']));md.append(t+'\n')
# H
def h(t):story.append(Paragraph(escape(t),st['Heading1']));md.append('\n## '+t+'\n')
# Table
def table(data,widths):
    t=Table([[Paragraph(escape(str(c)),st['BodyCOP']) for c in row] for row in data],colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eff2')),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#78929e')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.extend([t,Spacer(1,10)])
    md.append('\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in [data[0],['---']*len(data[0])]+data[1:])+'\n')
story.append(Paragraph('Grade comum e interpretação do pôster',st['Title']));p('Projeto COPASA · 10/11/2026')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/inspecionar_conc_novo.py

Inspecionar conc novo. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\inspecionar_conc_novo.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/CMAS/CALPUFF/CONC-{k}.DAT — chamada .open, linha 25.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/inspecionar_conc_novo.py, linhas 24-32.

```python
    print(k)
    with (R/f'CMAS/CALPUFF/CONC-{k}.DAT').open('rb') as f:
        for i in range(20):
            n=struct.unpack('<i',f.read(4))[0];b=f.read(n);assert struct.unpack('<i',f.read(4))[0]==n
            print(i,n,repr(b[:100]))
            if i==1:nlines=struct.unpack('<i',b)[0];print('nlines',nlines)
        f.seek(0)
        for i in range(nlines+2+15):
            n=struct.unpack('<i',f.read(4))[0];b=f.read(n);assert struct.unpack('<i',f.read(4))[0]==n
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/inspecionar_nova_execucao.py

Inspecionar nova execucao. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\inspecionar_nova_execucao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_e_preparar | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {p} — chamada np.loadtxt, linha 38.
- E:/copasa_map/in/CALMET.DAT — chamada .open, linha 40.

**Saídas.**

- E:/copasa_map/temp/Inspecao_nova_execucao.json — chamada .write_text, linha 45.

**Campos e chaves lidos.**

- v: area, height, old_flux, sigma.
- out: CALMET_header_records, CALPUFF.

**Campos e chaves gerados.**

- out: CALMET_header_records.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/inspecionar_nova_execucao.py, linhas 37-45.

```python
    for p in (R/'CMAS/CALPUFF').glob(f'RANK({k})*'):
        z=np.loadtxt(p,skiprows=6);out.setdefault('RANK',{})[p.name]=dict(shape=list(z.shape),max=float(z[:,2].max()),xy_min=z[:,:2].min(axis=0).tolist(),xy_max=z[:,:2].max(axis=0).tolist())
out['CALMET_header_records']=[]
with (R/'in/CALMET.DAT').open('rb') as f:
    for i in range(1110):
        n=struct.unpack('<i',f.read(4))[0];b=f.read(n);assert struct.unpack('<i',f.read(4))[0]==n
        if i<3 or i>1053:
            out['CALMET_header_records'].append(dict(i=i,n=n,head=repr(b[:36]),floats=np.frombuffer(b[:min(len(b)//4*4,52)],dtype='<f4').tolist() if len(b)%4==0 else []))
(R/'temp/Inspecao_nova_execucao.json').write_text(json.dumps(out,indent=2),encoding='utf8')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/instrucoes_importacao_nativa.py

Instrucoes importacao nativa. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\instrucoes_importacao_nativa.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/copasa_map/output/auditoria/Grades_por_unidade.json — chamada .read_text, linha 36.
- E:/copasa_map/output/entradas_corrigidas/AERMOD/Grade_Receptora_{unit}_AERMOD.csv — chamada p.read_bytes, linha 38.
- E:/copasa_map/output/entradas_corrigidas/CALPUFF/Grade_Receptora_{unit}_CALPUFF.xls — chamada xls.read_bytes, linha 48.
- E:/copasa_map/output/auditoria/CALPUFF_XLS_verificado.json — chamada .read_text, linha 50.
- E:/copasa_map/output/entradas_corrigidas/CALPUFF/Grade_Receptora_{q['unit']}_CALPUFF.xls — chamada path.read_bytes, linha 55.

**Saídas.**

- E:/copasa_map/output/auditoria/Verificacao_Importacao_Nativa.json — chamada .write_text, linha 57.
- E:/copasa_map/output/entradas_corrigidas/LEIA_PRIMEIRO.md — chamada .write_text, linha 100.
- E:/copasa_map/output/entradas_corrigidas/consulta/LEIA_CONSULTA.md — chamada .write_text, linha 101.
- E:/copasa_map/output/Receptores_importacao_AERMOD_CALPUFF.zip — chamada zipfile.ZipFile, linha 102.
- E:/copasa_map/output/Entradas_corrigidas_COPASA.zip — chamada zipfile.ZipFile, linha 108.

**Campos e chaves lidos.**

- d: counts, grids.
- r: FLAG, GROUP, ID, SENSITIVE, X, Y.
- q: all_ids_verified, all_numeric_coordinates_verified, group, id, records, sensitive, sha256, unit, zero_coordinates.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/instrucoes_importacao_nativa.py, linhas 35-43.

```python
R=Path(_cp_texto('', 'posix'));O=R/'output/entradas_corrigidas';A=R/'output/auditoria'
d=json.loads((A/'Grades_por_unidade.json').read_text(encoding='utf8'));checks=[]
for unit,points in d['grids'].items():
    p=O/'AERMOD'/f'Grade_Receptora_{unit}_AERMOD.csv';raw=p.read_bytes()
    assert raw.isascii() and not raw.startswith(b'\xef\xbb\xbf')
    rows=list(csv.DictReader(raw.decode('ascii').splitlines()))
    assert list(rows[0])==['X','Y','ELEV','HILL','FLAG','GROUP','ID','SENSITIVE'] and len(rows)==len(points)
    for r,q in zip(rows,points):
        assert r['ID']==q['id'] and r['GROUP']==q['group'] and int(r['SENSITIVE'])==q['sensitive']
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/ler_xls_original.ps1

Ler xls original. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\ler_xls_original.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/ler_xls_original.ps1, linhas 10-18.

```text
. (Join-Path $PSScriptRoot 'caminhos_copasa.ps1')
$taskRoot=(Get-PortablePath '')
$sourceFile=Join-Path $taskRoot 'in\H2S_Grid_Sources-NC.xls'
$excelApp=New-Object -ComObject Excel.Application
$excelApp.Visible=$false
$excelApp.DisplayAlerts=$false
try {
    $book=$excelApp.Workbooks.Open($sourceFile,0,$true)
    try {
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/limpar_chart_data.py

Remove apenas caches de gráficos gerados dentro da raiz COPASA.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\limpar_chart_data.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| stat | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/copasa_map/output/cmas_poster/Poster_CMAS_Session05_WWTP.pptx — chamada zipfile.ZipFile, linha 25.
- E:/copasa_map/output/cmas_poster/Poster_CMAS_Session05_WWTP.pptx — chamada P.read_bytes, linha 40.

**Saídas.**

- E:/copasa_map/temp/chart_data_receipts/limpeza_chart_data.json — chamada .write_text, linha 40.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/limpar_chart_data.py, linhas 24-32.

```python
R=Path(_cp_texto('', 'posix')).resolve();P=R/'output/cmas_poster/Poster_CMAS_Session05_WWTP.pptx';O=R/'temp/chart_data_receipts';O.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(P) as z:
    assert z.testzip() is None
    assert any('/embeddings/' in name and name.endswith('.xlsx') for name in z.namelist()),'Chart data not yet embedded'
    for name in z.namelist():
        if name.endswith('.rels'):assert b'.chart-data-' not in z.read(name),'Final file still references a cache'
removed=[]
for p in R.glob('.chart-data-*'):
    target=p.resolve();assert p.name.startswith('.chart-data-') and target.parent==R and target!=R
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/nota_cenarios_24h.py

Explicação dos campos de 24 h, baseada no manifesto da extração.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\nota_cenarios_24h.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.sax.saxutils | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json — chamada .read_text, linha 33.

**Saídas.**

- E:/copasa_map/output/auditoria/Origem_cenarios_24h.md — chamada .write_text, linha 71.

**Campos e chaves lidos.**

- st: Body, Cell, Heading2, Title.
- D: events.
- e: aliases, maximum, model, period_end, period_start.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 36-71 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/nota_cenarios_24h.py, linhas 45-53.

```python
    def h(t):
        if t.startswith('3.'):story.append(PageBreak())
        story.append(Paragraph(escape(t),st['Heading2']));md.extend(['## '+t,''])
    def p(t):story.append(Paragraph(escape(t),st['Body']));md.extend([t,''])
    h('1. O que os mapas anteriores apresentavam')
    p('Os arquivos PLT de 24 h do AERMOD e RANK de 24 h do CALPOST contêm o maior valor de média de 24 h em cada receptor. Ao reuni-los em um mapa, obtém-se um envelope de máximos. Um ponto pode representar julho e outro abril. Portanto, esse envelope descreve os extremos calculados durante a série, mas não a distribuição espacial de um único episódio. Ele permanece no visualizador como complemento explicitamente identificado.')
    p('A interpolação anterior por inverso da distância acentuava superfícies arredondadas ao redor dos pontos. Ela foi substituída por triangulação linear, sem extrapolação e sem novos extremos por suavização. Os trechos ainda angulosos refletem a distância entre receptores da grade original. Uma aparência mais lisa não acrescentaria informação física à simulação.')
    h('2. O que o novo cenário de 24 h apresenta')
    p('Em cada painel, todos os receptores agora usam o mesmo intervalo completo de 24 horas. A seleção identifica o intervalo em que ocorreu a maior média de 24 h entre os receptores daquela combinação de unidade e modelo. O mapa mostra as médias desse intervalo em todos os demais pontos, e não os máximos individuais desses pontos. A data e o horário aparecem no título do painel.')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/obter_contexto_cartografico.py

Baixa apenas geometrias OSM; nenhum nome é usado nos mapas públicos.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\copasa_map\codigo\obter_contexto_cartografico.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| requests | Consultas e downloads HTTP; depende de internet e da disponibilidade do provedor. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/in/cartografia_contexto/OSM_{k}.json — chamada path.read_text, linha 36.

**Saídas.**

- E:/copasa_map/in/cartografia_contexto/OSM_{k}.json — chamada path.write_text, linha 42.
- E:/copasa_map/in/cartografia_contexto/OSM_{k}_origem.json — chamada .write_text, linha 43.

**Campos e chaves lidos.**

- data: elements.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| fetch(k) | 32-46 | lê dados; grava produtos Retorno: (k, 0, failures), (k, len(json.loads(path.read_text(encoding='utf8'))['elements']), 'cache'). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/obter_contexto_cartografico.py, linhas 32-40.

```python
def fetch(k):
    center=(614080,7834430) if k=='VM' else (589190,7805680)
    a,b=T.transform(center[0]-2100,center[1]-2100);c,d=T.transform(center[0]+2100,center[1]+2100)
    path=O/f'OSM_{k}.json'
    if path.exists():return k,len(json.loads(path.read_text(encoding='utf8'))['elements']),'cache'
    query=f'[out:json][timeout:45];(way["highway"]({b},{a},{d},{c});way["building"]({b},{a},{d},{c});relation["building"]({b},{a},{d},{c}););out geom;'
    failures=[]
    for endpoint in ['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter']:
        try:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/perfis_comparacao_modelos.py

Agrupa pares por distância à superfície emissora, resume mediana e quartis do P95 e interpola apenas as curvas gráficas entre as faixas.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\perfis_comparacao_modelos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv — chamada pd.read_csv, linha 51.
- E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv — chamada source.read_bytes, linha 70.

**Saídas.**

- E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos.json — chamada .write_text, linha 71.
- E:/copasa_map/output/comparacao_modelos/Perfis_P95_faixas_distancia.csv — chamada .to_csv, linha 76.
- E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos.{ext} — chamada fig.savefig, linha 104.
- E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos.png — chamada fig.savefig, linha 105.
- E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos_previa.png — chamada fig.savefig, linha 105.

**Campos e chaves lidos.**

- data: unit.
- b: AERMOD, CALPUFF, high_m, label, low_m, median_difference_CAL_minus_AER, n.
- yy: median, q1, q3.
- u: WWTP, bins, n, samples, unit.
- sample: median, model, q1, q3, x.

**Campos e chaves gerados.**

- b: median_difference_CAL_minus_AER.
- yy: q1, q3.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 50-106 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.; Interpolação cúbica que preserva a forma local. Nos perfis COPASA suaviza a apresentação entre estatísticas já calculadas. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/perfis_comparacao_modelos.py, linhas 58-64.

```python
            for model in COL:
                q=z[model+'_P95'].quantile([.25,.5,.75]).to_numpy()
                b[model]=dict(q1=float(q[0]),median=float(q[1]),q3=float(q[2]))
            b['median_difference_CAL_minus_AER']=b['CALPUFF']['median']-b['AERMOD']['median'];bins.append(b)
        assert sum(b['n'] for b in bins)==len(s)
        samples=[];xs=np.linspace(0,5,181)
        for model in COL:
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/perfis_comparacao_modelos.py, linhas 65-71.

```python

            yy={stat:PchipInterpolator(np.arange(6),[b[model][stat] for b in bins])(xs) for stat in ['q1','median','q3']}
            yy['q1']=np.minimum(yy['q1'],yy['median']);yy['q3']=np.maximum(yy['q3'],yy['median'])
            samples.append(dict(model=model,x=xs.tolist(),q1=yy['q1'].tolist(),median=yy['median'].tolist(),q3=yy['q3'].tolist()))
        out.append(dict(unit=unit,WWTP=1 if unit=='VM' else 2,n=len(s),bins=bins,samples=samples))
    payload=dict(reference_year=2024,statistic='Hourly P95 per receptor, then spatial median and quartiles within distance bands',distance='Distance to closest emitting footprint',scope='All unique paired receptors within 1800 m; no concentration filter',band_axes='Categorical; equal display width does not imply equal distance width',ribbons='Spatial interquartile range, not confidence intervals',interpolation='Shape-preserving PCHIP for display only, no interpolation of model concentrations',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),units=out)
    (F/'Perfis_comparacao_modelos.json').write_text(json.dumps(payload,indent=2),encoding='utf8')
```

Interpolação cúbica que preserva a forma local. Nos perfis COPASA suaviza a apresentação entre estatísticas já calculadas.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- PchipInterpolator: Interpolação cúbica que preserva a forma local. Nos perfis COPASA suaviza a apresentação entre estatísticas já calculadas.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/planilhas_corrigidas.mjs

Planilhas corrigidas. Processamento ou módulo de apoio. A organização passa por load, save, preview, callback, callback, set, callback, callback, set, callback.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\planilhas_corrigidas.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_copasa.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| @oai/artifact-tool | Biblioteca de autoria do ambiente de apresentações/planilhas; precisa ser disponibilizada na máquina de autoria. |


**Entradas.**

- R+'/output/auditoria/Auditoria_consolidada.json' — chamada fs.readFile, linha 22.
- p — chamada FileBlob.load, linha 23.
- R+'/in/Resumo_MOD.xlsx' — chamada load, linha 26.
- R+'/in/H2S_TOTAL_Sources-AERMOD.xlsx' — chamada load, linha 47.
- R+'/in/H2S_Grid_Sources-VM.xlsx' — chamada load, linha 59.

**Saídas.**

- O+'/'+n — chamada (await SpreadsheetFile.exportXlsx(w)).save, linha 24.
- T+'/'+n — chamada fs.writeFile, linha 25.
- w — chamada save, linha 44.
- w — chamada save, linha 56.
- w — chamada save, linha 62.
- w — chamada save, linha 71.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/planilhas_corrigidas.mjs, linhas 23-31.

```javascript
async function load(p){return SpreadsheetFile.importXlsx(await FileBlob.load(p));}
async function save(w,n){w.recalculate();await(await SpreadsheetFile.exportXlsx(w)).save(O+'/'+n);}
async function preview(w,s,range,n){await fs.writeFile(T+'/'+n,new Uint8Array(await(await w.render({sheetName:s,range,scale:1.4,format:'png'})).arrayBuffer()));}
let w=await load(R+'/in/Resumo_MOD.xlsx');
await preview(w,'Entrada','A17:L39','Resumo_MOD_antes.png');
const s=w.worksheets.getItem('Entrada'),p=w.worksheets.getItem('Comportamento');
s.getRange('B28').formulas=[['=2*PI()*6^2']];
s.getRange('B53').formulas=[['=SUM(F57:F59)']];

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_grade_importacao.py

Preserva receptores sensíveis e gera a mesma sequência nativa nos dois modelos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\preparar_grade_importacao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .read_text, linha 48.
- E:/copasa_map/output/auditoria/Grade_base_1789.json — chamada bp.read_text, linha 52.
- E:/copasa_map/mod/AERMOD/receptors_part.csv — chamada src.open, linha 55.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_NC_VM_CALPUFF_17b.txt — chamada .read_text, linha 106.
- {p} — chamada p.read_text, linha 121.
- E:/copasa_map/mod/AERMOD/receptors_part.csv — chamada src.read_bytes, linha 133.

**Saídas.**

- E:/copasa_map/output/auditoria/Grade_base_1789.json — chamada bp.write_text, linha 53.
- E:/copasa_map/output/entradas_corrigidas/AERMOD/Grade_Receptora_{unit}_AERMOD.csv — chamada .open, linha 100.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_{unit}.ROU — chamada .write_text, linha 103.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_{unit}_CALPUFF_17b.txt — chamada .write_text, linha 105.
- {p} — chamada p.write_text, linha 123.
- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .write_text, linha 126.
- E:/copasa_map/output/auditoria/Grades_por_unidade.json — chamada .write_text, linha 128.
- E:/copasa_map/output/auditoria/Correspondencia_Receptores_Grades.csv — chamada .open, linha 129.
- E:/copasa_map/output/auditoria/Grade_importacao_validada.json — chamada .write_text, linha 135.

**Campos e chaves lidos.**

- d: grid, grid_revision.
- row: ID, SENSITIVE.
- q: elev, group, hill, id, joint_id, origin, sensitive, x, y.
- v: distance_m.

**Campos e chaves gerados.**

- row: receptor_id.
- q: id, joint_id, receptor_id.
- sets: NC_VM.
- d: grid, grid_count, grid_revision, grid_unique_locations.
- audit: sets.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| number(s) | 58-58 | Chamadas efetivas: float, s.replace Retorno: float(s.replace(',', '.')). |
| dec(v) | 96-96 | Chamadas efetivas: .replace, .rstrip Retorno: f'{v:.8f}'.rstrip('0').rstrip('.').replace('.', ','). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_grade_importacao.py, linhas 126-132.

```python
(A/'Auditoria_consolidada.json').write_text(json.dumps(d,indent=2),encoding='utf8')
counts={unit:dict(total=len(selected),monitoring=sum(q['sensitive'] for q in selected),grid=sum(not q['sensitive'] for q in selected),unique_positions=len({(q['x'],q['y']) for q in selected})) for unit,selected in sets.items()}
(A/'Grades_por_unidade.json').write_text(json.dumps(dict(counts=counts,grids=sets,method=d['grid_revision']),indent=2),encoding='utf8')
with (A/'Correspondencia_Receptores_Grades.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['GRADE','INDICE_MODELO','ID','ID_NC_VM','X_m','Y_m','TIPO'])
    for unit,selected in sets.items():
        for i,q in enumerate(selected,1):w.writerow([unit,i,q['id'],q['joint_id'],dec(q['x']),dec(q['y']),q['group']])
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_auditoria.py

Relatorio auditoria. Documentação/apoio. A organização passa por main, h, p, table, footer.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\copasa_map\codigo\relatorio_auditoria.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.sax.saxutils | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .read_text, linha 36.
- E:/copasa_map/{fn} — chamada p.read_text, linha 41.
- E:/copasa_map/{fn} — chamada p.read_bytes, linha 43.
- E:/copasa_map/output/auditoria/CALMET_DAT_verificado.json — chamada metfile.read_text, linha 75.

**Saídas.**

- E:/copasa_map/{fn} — chamada p.write_text, linha 43.
- E:/copasa_map/descontinuado/2026_11_09_caminhos_antigos/manifesto.json — chamada .write_text, linha 44.
- E:/copasa_map/output/auditoria/Relatorio_Auditoria_COPASA.md — chamada .write_text, linha 108.

**Campos e chaves lidos.**

- s: alias, new_process_total, old_aermod_total, old_calpuff_total, old_process_total.
- D: process, profile_mean_old, summary.
- cm: fortran_records_checked.
- st: Heading1, Texto, Title.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 38-122 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_auditoria.py, linhas 47-55.

```python
    def h(t):sec.append(('h',t))
    def p(t):sec.append(('p',t))
    def table(t):sec.append(('table',t))
    h('1. Síntese da decisão e alcance da auditoria')
    p(_cp_adaptar('Foram conferidas a memória de cálculo Resumo_MOD, as planilhas de importação, os arquivos AERMOD ADI e os arquivos CALPUFF INP/LST. As cópias corrigidas ficam em E:/copasa_map/output/entradas_corrigidas. Os arquivos-base recebidos foram preservados. As taxas corrigidas conservam a massa de cada processo entre os modelos. Nenhum modelo de dispersão foi executado nesta revisão.'))
    p('A orientação do autor foi utilizar as áreas das unidades. Para a WWTP 1, foram mantidos dois círculos UASB de raio 6 m, totalizando 226,1947 m². Os três UASB da WWTP 2 foram regularizados como retângulos congruentes de 436,3333 m², preservando os 1.309 m² totais das geometrias recebidas. Cada unidade tem largura de 21,3942 m e profundidade de 20,3949 m, com alinhamento comum e centros espaçados em 27,4975 m. Trata-se de regularização das coordenadas existentes, autorizada pelo autor, sem novo levantamento de campo. IDs, massas totais, alturas e demais características foram preservados. As correções estão no ADI, nas planilhas AERMOD/CALPUFF, nos INP e na memória Resumo_MOD. A coluna Diam das planilhas originais contém 6 e 8,5, enquanto o ADI as interpreta como raios de AREACIRC. Deve-se preservar esse significado ao importar.')
    p('No tratamento preliminar, foram mantidas as áreas líquidas de 15 m² e 30 m² documentadas na memória de cálculo. Os polígonos externos, de aproximadamente 209 m² e 375 m², definem a distribuição espacial da emissão e não comprovam que toda essa superfície externa seja líquida e emissora. A área ativa participa do cálculo físico; a área do polígono modelado participa da distribuição do fluxo superficial.')
    table([['Unidade','Memória antiga\ng/s','ADI antigo\ng/s','INP antigo\ng/s','Corrigido\ng/s']]+[[s['alias'],f"{s['old_process_total']:.6f}",f"{s['old_aermod_total']:.6f}",f"{s['old_calpuff_total']:.6f}",f"{s['new_process_total']:.6f}"] for s in D['summary']])
    p('Os valores antigos do ADI e do INP acima são as somas dos fluxos multiplicados pelas áreas de suas respectivas fontes, antes dos fatores horários. A diferença entre eles impede atribuir a discrepância das plumas antigas exclusivamente à formulação dos modelos.')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_comparacao_modelos.py

Relatório de interpretação da rodada atual, sem alterar entradas executadas.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\copasa_map\codigo\relatorio_comparacao_modelos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.enums | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.utils | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfgen | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/codigo/runtime_workspace.json — chamada .read_text, linha 36.
- E:/copasa_map/output/comparacao_modelos/{n} — chamada .open, linha 48.
- E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json — chamada .read_text, linha 51.
- E:/copasa_map/output/comparacao_modelos/CALPUFF_horario_validado.json — chamada .read_text, linha 51.
- E:/copasa_map/output/comparacao_modelos/Estatistica_avancada.json — chamada .read_text, linha 51.
- E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json — chamada .read_text, linha 141.

**Saídas.**

- E:/copasa_map/output/comparacao_modelos/Comparacao_AERMOD_CALPUFF.md — chamada .write_text, linha 160.
- E:/copasa_map/output/comparacao_modelos/Notas_poster_English.txt — chamada .write_text, linha 186.

**Campos e chaves lidos.**

- d: paired.
- styles: CellA, CellB, SmallA.
- q: max_distance_m, min_distance_m, period, unit.
- v: median_AERMOD, median_CALPUFF, median_CALPUFF_over_AERMOD, n.
- spatial: rows, sensitivity_P95_ge_0_7.
- r: Spearman_rho_P95, WWTP, distance_max_m, distance_min_m, n, within_factor_2_count, within_factor_2_percent.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| readcsv(n) | 48-48 | Chamadas efetivas: list, csv.DictReader, .open Retorno: list(csv.DictReader((O / n).open(encoding='utf-8-sig'))). |
| main() | 50-186 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_comparacao_modelos.py, linhas 48-56.

```python
def readcsv(n):return list(csv.DictReader((O/n).open(encoding='utf-8-sig')))
# Main
def main():
    d=json.loads((O/'Comparacao_consolidada.json').read_text(encoding='utf8'));cal=json.loads((O/'CALPUFF_horario_validado.json').read_text());paired=d['paired'];met=readcsv('Descritores_meteorologia.csv');annual=readcsv('Comparacao_anual_pares.csv');sources=readcsv('Entradas_executadas_fontes.csv');advanced=json.loads((O/'Estatistica_avancada.json').read_text(encoding='utf8'))
    pdfmetrics.registerFont(TTFont('Arial',_cp_externo('arial_ttf_41a7a4d')));pdfmetrics.registerFont(TTFont('Arial-Bold',_cp_externo('arialbd_ttf_7dff968')));pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold')
    styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyA',fontName='Arial',fontSize=10.3,leading=15,spaceAfter=9,textColor=colors.HexColor('#263d4b')));styles.add(ParagraphStyle(name='TitleA',fontName='Arial-Bold',fontSize=23,leading=29,spaceAfter=18,textColor=colors.HexColor('#173445')));styles.add(ParagraphStyle(name='HeadA',fontName='Arial-Bold',fontSize=15,leading=20,spaceBefore=13,spaceAfter=11,textColor=colors.HexColor('#196c83')));styles.add(ParagraphStyle(name='SmallA',fontName='Arial',fontSize=8.5,leading=12,spaceAfter=7));styles.add(ParagraphStyle(name='CellA',fontName='Arial',fontSize=8.3,leading=11));styles.add(ParagraphStyle(name='CellB',parent=styles['CellA'],fontName='Arial-Bold',textColor=colors.white))
    story=[];md=[]
    def p(t,style='BodyA'):
        story.append(Paragraph(t,styles[style]));md.append(t.replace('<b>','**').replace('</b>','**').replace('<br/>','\n'))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/transparencia_logos.py

Transparencia logos. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\copasa_map\codigo\transparencia_logos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| posixpath | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/copasa_map/codigo/recursos_poster/assets/{n} — chamada .read_bytes, linha 29.
- sys.argv[1] — chamada zipfile.ZipFile, linha 30.

**Saídas.**

- sys.argv[1] — chamada zipfile.ZipFile, linha 38.

**Campos e chaves lidos.**

- files: ppt/slides/_rels/slide1.xml.rels, ppt/slides/slide1.xml.
- N: a, r.

**Campos e chaves gerados.**

- files: ppt/slides/slide1.xml.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/transparencia_logos.py, linhas 28-36.

```python
p=Path(sys.argv[1]);A=Path(_cp_texto('codigo/recursos_poster/assets', 'posix'))
hashes={hashlib.sha256((A/n).read_bytes()).hexdigest() for n in ['logo_gpama.png','logo_smarh_original.png']}
with zipfile.ZipFile(p) as z:files={n:z.read(n) for n in z.namelist()}
root=E.fromstring(files['ppt/slides/slide1.xml']);rels={r.get('Id'):r.get('Target').lstrip('/') if r.get('Target').startswith('/') else posixpath.normpath('ppt/slides/'+r.get('Target')) for r in E.fromstring(files['ppt/slides/_rels/slide1.xml.rels'])};count=0
for b in root.findall('.//p:pic/p:blipFill/a:blip',N):
    dest=rels[b.get('{'+N['r']+'}embed')]
    if dest not in files or hashlib.sha256(files[dest]).hexdigest() not in hashes:continue
    effect=E.SubElement(b,'{'+N['a']+'}clrChange',useA='1');a=E.SubElement(effect,'{'+N['a']+'}clrFrom');E.SubElement(a,'{'+N['a']+'}srgbClr',val='FFFFFF');a=E.SubElement(effect,'{'+N['a']+'}clrTo');a=E.SubElement(a,'{'+N['a']+'}srgbClr',val='FFFFFF');E.SubElement(a,'{'+N['a']+'}alpha',val='0');count+=1
assert count==2,count
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_cmas_atual.py

Conferência da nova rodada e dos valores publicados no pôster.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\copasa_map\codigo\validar_cmas_atual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| math | Funções matemáticas escalares. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pypdf | Leitura, montagem e inspeção de PDFs; não substitui a conferência visual das páginas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/copasa_map/output/cmas_poster/figuras/Cartografia_metadados.json — chamada .read_text, linha 58.
- E:/copasa_map/output/cmas_poster/figuras/Faixas_concentracao_poster.json — chamada .read_text, linha 58.
- E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json — chamada .read_text, linha 58.
- E:/copasa_map/output/comparacao_modelos/Estatistica_horaria_por_receptor.csv — chamada .open, linha 65.
- E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json — chamada .read_text, linha 66.
- E:/copasa_map/output/cmas_poster/Poster_CMAS_Session05_WWTP.pptx — chamada zipfile.ZipFile, linha 78.
- E:/copasa_map/output/cmas_poster/figuras/Boxplots_editaveis_dados.json — chamada .read_text, linha 96.
- E:/copasa_map/output/comparacao_modelos/Estatistica_avancada.json — chamada .read_text, linha 103.
- E:/copasa_map/output/cmas_poster/figuras/Perfis_editaveis_dados.json — chamada .read_text, linha 109.
- E:/copasa_map/codigo/recursos_poster/assets/{logo} — chamada .read_bytes, linha 119.
- io.BytesIO(z.read(name)) — chamada Image.open, linha 122.
- Argumento fornecido pelo chamador — chamada im.load, linha 122.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/copasa_map/output/auditoria/Validacao_Poster_Anual.json — chamada .write_text, linha 129.

**Campos e chaves lidos.**

- v: annual, annual_native_max_abs_error_ug_m3, current_run, daily_native_max_abs_error_ug_m3, finite_coverage, mass_difference_percent, maximum_displayed, maximum_native_in_frame, native_node_max_error.
- fields: current_fields.
- m: color_norm, colorbar_end_shape, colorbar_map_gap_cm, colorbar_orientation, colorbar_text_clearance_cm, colorbar_thickness_cm, context_legend, measured_scale, panels, placeholder, poster_scale, primary_ticks_ug_m3, secondary_ticks_ppb, secondary_unit, ug_m3_per_ppb.
- p: AERMOD_P95, CALPUFF_P95, Spearman_rho_P95, distance_m, distance_max_m, distance_min_m, unit, within_factor_2_percent.
- spatial: rows.
- summary: n, within_factor_2_count, within_factor_2_percent.
- meta: Fontes_privacidade.
- data: execution_inputs, quality_AERMOD, quality_CALPUFF.
- b: axis_max, axis_min, axis_offset_below_zero_px, distance_min, high_m, index, low_m, median, model, n, plot_bounds, q1, q3, unit, y_unit_top.
- adv: poster_distributions.
- q: distance_min, model.
- series: values.
- pb: h, w, x, y.
- u: axis_max, axis_min, bins, n, unit.
- scatter: units.
- r: n, n_in_full_range, n_visible_main, stats_all_receptors.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| check(name, ok) | 57-57 | Chamadas efetivas: checks.append, dict, bool |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_cmas_atual.py, linhas 69-75.

```python
    summary=next(p for p in spatial['rows'] if p['unit']==unit and p['distance_min_m']==0 and p['distance_max_m']==1800)
    count=sum(.5*float(p['AERMOD_P95'])<=float(p['CALPUFF_P95'])<=2*float(p['AERMOD_P95']) for p in pairs)
    check(unit+' factor-two agreement reproduces source receptor table',summary['n']==len(pairs) and summary['within_factor_2_count']==count and abs(summary['within_factor_2_percent']-count/len(pairs)*100)<1e-12)
check('Source-map physical scale recalculated to 1:2500',meta['Fontes_privacidade']['poster_scale']==2500 and all(abs(m['measured_scale']-2500)<.01 for m in meta['Fontes_privacidade']['maps']))
check('Larger grouped method legend clear of map and complete facilities',meta['Fontes_privacidade']['legend_position']=='right' and meta['Fontes_privacidade']['legend_fontsize_poster_pt']==25 and meta['Fontes_privacidade']['legend_context_fontsize_pt']==22 and meta['Fontes_privacidade']['legend_grouped'] and meta['Fontes_privacidade']['facility_boundaries_complete'] and meta['Fontes_privacidade']['legend_map_clearance_cm']>0)
check('Hourly AERMOD reproduces daily and annual native data',all(v['daily_native_max_abs_error_ug_m3']<1e-5 and v['annual_native_max_abs_error_ug_m3']<1e-5 for v in data['quality_AERMOD']))
check('Annual CALPUFF derived from hourly CONC with audited coverage',all(v['annual'][0]['hours']==8784 and v['annual'][1]['hours']==8732 for v in data['quality_CALPUFF']))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/validar_cmas_atual.py, linhas 109-115.

```python
    profile=json.loads((F/'Perfis_editaveis_dados.json').read_text(encoding='utf8'));names=root.xpath('//p:cNvPr/@name',namespaces=N)
    check('Twelve editable profile ribbons and curves retained',sum(n.startswith(('perfil_faixa_','perfil_mediana_','perfil_zoom_')) for n in names)==12)
    for u in profile:
        raw=[p for p in stats if p['unit']==u['unit'] and float(p['distance_m'])<1800]
        check(u['unit']+' profile conserves full paired sample',sum(b['n'] for b in u['bins'])==u['n']==len(raw) and u['axis_min']==0 and u['axis_max']==80)
        for b in u['bins']:
            selected=[p for p in raw if b['low_m']<=float(p['distance_m'])<b['high_m']]
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_entrega.py

Validar entrega. Conferência/teste. A organização passa por check.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\copasa_map\codigo\validar_entrega.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_e_preparar | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| geometria_ete | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| statistics | Estatísticas descritivas da biblioteca padrão. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .read_text, linha 34.
- item['path'] — chamada .read_bytes, linha 39.

**Saídas.**

- E:/copasa_map/output/auditoria/Validacao_Entrega.json — chamada .write_text, linha 93.

**Campos e chaves lidos.**

- D: common_window, grid, inputs, process, sources_aermod, sources_calpuff.
- item: path, sha256.
- w: Comportamento, Entrada.
- r: Diam, Emission_Rate, ID, Length_X, ODOR, elev, x, y.
- s: area, old_flux.
- e: flux, params, type.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| check(name, condition, detail=None) | 37-38 | Chamadas efetivas: checks.append, dict, bool |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_entrega.py, linhas 48-54.

```python
for c,k in [('N17','VM_PRE'),('N18','VM_UASB'),('N19','VM_CALHA'),('N20','NC_PRE'),('N21','NC_UASB'),('N22','NC_FB'),('N23','TRANSFER_A'),('N24','TRANSFER_B')]:check('Memoria recalculada '+k,abs(w['Entrada'][c].value-D['process'][k])<1e-12)
check('Perfil da planilha media 1',abs(statistics.mean(w['Comportamento'].cell(i,3).value for i in range(3,27))-1)<1e-12)
gt=D['grid'];target=[(r['x'],r['y'],r['elev']) for r in gt]
for name in ['H2S_CMAS_corrigido.ADI','H2S_COMPLETO_corrigido.ADI']:
    text,src=parse_aer(O/name)
    if D['common_window']:check(name+' janela comum','STARTEND 2024 1 1 1 2025 12 30 20' in text)
    for n,s in src.items():check(name+' massa '+n,abs(s['old_flux']*s['area']-D['sources_aermod'][n]['mass'])<1e-10)
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/validar_entrega.py, linhas 56-62.

```python
    check(name+' UASB areas iguais',max(p.area for p in polys)-min(p.area for p in polys)<1e-5)
    check(name+' area acumulada preservada',abs(sum(p.area for p in polys)-1309)<1e-5)
    check(name+' UASB contidos na ETE',all(limite('NC').covers(p) for p in polys))
    centers=[p.centroid for p in polys];check(name+' espacamento uniforme',abs(centers[0].distance(centers[1])-centers[1].distance(centers[2]))<1e-5)
    first=next(iter(src));fac=[]
    for m in re.finditer(rf'EMISFACT {first}\s+HROFDY ([^\n]+)',text):fac+=nums(m[1])
    check(name+' 24 fatores',len(fac)==24 and abs(statistics.mean(fac)-1)<1e-9)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_poster_anual.py

Validar poster anual. Conferência/teste. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\copasa_map\codigo\validar_poster_anual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| validar_cmas_atual | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_poster_anual.py, linhas 11-19.

```python
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_copasa.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_copasa.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_copasa import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_revisao_grade_poster.py

Conferências de leitura dos produtos finais, sem executar os modelos.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\copasa_map\codigo\validar_revisao_grade_poster.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pypdf | Leitura, montagem e inspeção de PDFs; não substitui a conferência visual das páginas. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/copasa_map/output/auditoria/Auditoria_consolidada.json — chamada .read_text, linha 48.
- E:/copasa_map/mod/AERMOD/receptors_part.csv — chamada .open, linha 53.
- E:/copasa_map/output/auditoria/Grades_por_unidade.json — chamada .read_text, linha 67.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_{unit}.ROU — chamada .read_text, linha 79.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_{unit}_CALPUFF_17b.txt — chamada .read_text, linha 80.
- E:/copasa_map/output/entradas_corrigidas/AERMOD/Grade_Receptora_NC_VM_AERMOD.csv — chamada .open, linha 86.
- E:/copasa_map/output/auditoria/CALPUFF_XLS_verificado.json — chamada .read_text, linha 89.
- E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_NC_VM.ROU — chamada .read_text, linha 91.
- {path} — chamada path.read_text, linha 94.
- E:/copasa_map/output/cmas_poster/figuras/Resultados_historicos.json — chamada .read_text, linha 97.
- E:/copasa_map/output/cmas_poster/figuras/Cartografia_metadados.json — chamada .read_text, linha 102.
- E:/copasa_map/output/cmas_poster/Poster_CMAS_Session05_WWTP.pptx — chamada zipfile.ZipFile, linha 105.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/copasa_map/output/auditoria/Validacao_Grade_Poster.json — chamada .write_text, linha 117.
- E:/copasa_map/output/auditoria/Validacao_Mapas_24h.json — chamada .write_text, linha 118.
- E:/copasa_map/output/Entradas_corrigidas_COPASA.zip — chamada zipfile.ZipFile, linha 125.

**Campos e chaves lidos.**

- d: grid.
- w: AERMOD, CALPUFF_km.
- q: ID, elev, finite_coverage, group, hill, id, maximum_displayed, maximum_native_in_frame, native_node_max_error, sensitive, source, statistic, x, y.
- sets: grids.
- book: AERMOD, CALPUFF_km, Grade, Monitoramento.
- v: all_ids_verified, all_numeric_coordinates_verified, zero_coordinates.
- meta: Comparacao_24h_pre_harmonizacao, Fontes_privacidade.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| check(name, value) | 50-52 | Chamadas efetivas: checks.append, dict |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_revisao_grade_poster.py, linhas 50-58.

```python
def check(name,value):
    assert value,name
    checks.append(dict(name=name,passed=True))
with (R/'mod/AERMOD/receptors_part.csv').open(encoding='utf-8-sig',newline='') as f:original=[{k.strip():v.strip() for k,v in r.items()} for r in csv.DictReader(f,delimiter=';')]
w=openpyxl.load_workbook(I/'consulta/Consulta_Receptores_NC_VM.xlsx',data_only=True)
check('Workbook separates complete imports and monitoring/grid subsets',w.sheetnames==['AERMOD','CALPUFF_km','Monitoramento','Grade'])
check('1790 workbook records per model',all(w[s].max_row==1791 for s in ['AERMOD','CALPUFF_km']))
check('AERMOD headers match provided schema',[c.value for c in w['AERMOD'][1]]==['X','Y','ELEV','HILL','GROUP','ID','SENSITIVE'])
for i,q in enumerate(g,2):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/verificar_calpuff_xls.ps1

Verificar calpuff xls. Conferência/teste. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\copasa_map\codigo\verificar_calpuff_xls.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/verificar_calpuff_xls.ps1, linhas 10-18.

```text
. (Join-Path $PSScriptRoot 'caminhos_copasa.ps1')
$ErrorActionPreference = 'Stop'
$projectRoot=(Get-PortablePath '')
$data=Get-Content -LiteralPath (Join-Path $projectRoot 'output\auditoria\Grades_por_unidade.json') -Raw | ConvertFrom-Json
$excelApp=New-Object -ComObject Excel.Application
$excelApp.Visible=$false
$excelApp.DisplayAlerts=$false
$results=@()
try {
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## map_copasa.py

Rotina histórica do projeto inicial, com estrutura e unidades anteriores. Não é o gerador do pôster atual e pode conter representação que não atende à anonimização atual.

**Papel.** Histórico: etapa anterior à rodada CMAS atual. **Fonte inspecionada.** E:\copasa_map\map_copasa.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| adjustText | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| calendar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| contextily | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| glob | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| locale | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| logging | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| math | Funções matemáticas escalares. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.dates | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patheffects | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib_scalebar.scalebar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| seaborn | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |
| windrose | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {filepath} — chamada gpd.read_file, linha 346.
- {filepath} — chamada zipfile.ZipFile, linha 355.
- os.path.join(temp_dir, kml_list[0]) — chamada gpd.read_file, linha 359.
- {filepath} — chamada open, linha 1192.
- {filepath} — chamada pd.read_csv, linha 568.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada pd.read_csv, linha 1651.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada pd.read_excel, linha 1646.
- os.path.join(BASE_DIR, 'AERMET_COP.SFC') — chamada open, linha 1757.
- os.path.join(root, nome) — chamada pd.read_excel, linha 2267.

**Saídas.**

- {filepath} — chamada fig.savefig, linha 233.
- filepath.replace('.png', '_backup.png') — chamada fig.savefig, linha 238.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada df.to_csv, linha 1362.

**Campos e chaves lidos.**

- gdf: MINLEVEL.
- df_shp_valores: MINLEVEL.
- df: ANO, DATA, HORA, conc, datetime, timedelta, x_km, y_km.
- row: hora_int.
- df.loc: HORA.
- dados: csv, kmz, nome.
- gdf_data: MINLEVEL, conc.
- df_plot: _conc_plot, conc, conc_media_ugm3, dir_media_o, hora, vel_media_vetorial_ms.
- gdfs: 24, anual.
- info: nome, pasta, shp_suffix.
- d: conc.
- df_hr: conc.
- gdf_temp: conc.
- df_meteo: VVr_ms, datetime.
- df_model_unit: datetime.
- df_m: DV_o, PP_mm, VV_ms, datetime, y_quiver.
- df_mod_cut: AERMOD_ppb, CALPUFF_ppb, datetime.
- df_camp: datetime.
- df_c_cut: concentracao_ppb, datetime.
- day_data: datetime.
- dados_u: nome.
- paths: clp, manifest, pasta, resumo_metrica, serie, vento.
- out: ANO, DIA, HORA, MÊS, clp_m, datetime.
- df_clp: datetime.
- g: dir_media_o, u_medio, v_medio.
- df_clp_hora: clp_media_m, hora.
- df_clp_plot: clp_media_m, hora.
- ax_clp.spines: bottom, left, right, top.
- df_vento_hora: n_horas, vel_media_vetorial_ms.
- paths_cache: resumo_base.
- subset: DV_o, MÊS, VVr_ms.
- mes_data: DV_o, VVr_ms.
- mensal: MÊS, PP_mm.

**Campos e chaves gerados.**

- gdf_kml: MINLEVEL, area.
- df: HORA, _u, _v, datetime, hora, hora_int, x_m, y_m.
- df_hourly: concentracao_ppb.
- df_plot: _conc_plot, conc.
- df_m: y_quiver.
- paths: resumo_metrica.
- out: clp_m, datetime.
- df_clp: hora.
- g: dir_cardinal, dir_media_o, vel_media_vetorial_ms.
- df_clp_plot: clp_media_m, hora.
- mensal: Nome_Mês.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| salvar_figura_segura(fig, filepath, dpi_padrao=600) | 231-240 | grava produtos |
| convert_ug_to_ppb(x) | 243-243 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: x * FATOR_UG_TO_PPB. |
| convert_ppb_to_ug(x) | 245-245 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: x / FATOR_UG_TO_PPB. |
| direcao_cardinal(graus) | 248-254 | Chamadas efetivas: pd.isna, int, float Retorno: setores[int((float(graus) + 11.25) // 22.5) % 16], ''. |
| obter_escala_visual_conc(valores, vmin_base=0.1) | 257-276 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (vmin_base, vmax_visual, vmax_abs), (vmin_base, max(vmin_base * 10, 1.0), 0.0). |
| format_lon(x, pos) | 279-281 | Chamadas efetivas: transformer_axes.transform Retorno: f'{lon:.3f}°'. |
| format_lat(y, pos) | 284-286 | Chamadas efetivas: transformer_axes.transform Retorno: f'{lat:.3f}°'. |
| parse_coordinates_string(coords_str) | 289-298 | Chamadas efetivas: .replace, coords_str.split, c.split, len, lista_coords.append, coords_str.strip, float Retorno: lista_coords, []. |
| ler_kml_xml_geometry_only(filepath) | 301-318 | Chamadas efetivas: os.path.exists, ET.parse, tree.getroot, root.iter, gpd.GeoDataFrame, gdf.to_crs, tag.split, strip_ns Retorno: None, gdf.to_crs(CRS_WEB). |
| obter_valores_do_shp(filepath) | 321-327 | lê dados Retorno: None, None. |
| combinar_kml_shp(gdf_kml, df_shp_valores) | 330-340 | Chamadas efetivas: .reset_index, len, np.linspace, gdf_kml.sort_values, .sort_values, .min, .max Retorno: gdf_kml, None. |
| ler_shp_aermod(filepath) | 343-349 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_kmz_limite_poligono(filepath) | 352-369 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_csv_pontos(filepath) | 372-390 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_arquivo_dat_calpost(filepath) | 393-412 | Chamadas efetivas: os.path.exists, pd.DataFrame, open, .split, len, line.strip, float, data_rows.append Retorno: None, df. |
| parse_dat_filename(filename) | 415-470 | Chamadas efetivas: .strip, os.path.splitext, os.path.basename, re.search, match.groups, int, pd.Timestamp, str Retorno: None, dt + pd.Timedelta(hours=hour, minutes=minute). |
| listar_arquivos_calpuff_horarios(path_dir, recursive=True) | 473-510 | Chamadas efetivas: sorted, os.walk, set, os.path.exists, os.path.join, .lower, os.path.isfile, parse_dat_filename Retorno: sorted(set(arquivos)), []. |
| ler_concentracao_campanha(filepath, data_referencia_inicio) | 513-561 | lê dados Retorno: None, df_hourly. |
| ler_concentracao_modelo(filepath) | 564-581 | lê dados Retorno: None, df.dropna(subset=['datetime']). |
| encontrar_arquivo_campanha(sigla_unidade, campanha_key) | 584-595 | Chamadas efetivas: os.path.join, os.path.exists, campanha_key.split, int Retorno: (None, None), (path, f'Medido (Campanha {campanha_key})'). |
| gerar_mapa_duplo_calpuff_24h_anual() | 598-698 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, plt.subplots, .set, fig.suptitle |
| plotar_disp(ax, current_fig, gdf_data, gdf_limite, bounds, nome_soft, show_model_label=True) | 701-769 | Chamadas efetivas: ax.xaxis.set_major_formatter, ax.xaxis.set_major_locator, ax.set_xlabel, ax.yaxis.set_major_formatter, ax.yaxis.set_major_locator, ax.set_ylabel, ax.tick_params, plt.setp Retorno: sm. |
| gerar_mapas_dispersao() | 772-853 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, PERIODOS.items, ler_shp_aermod, dados.get |
| gerar_mapa_pontos_amostragem() | 856-924 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ler_csv_pontos, ZOOM_BUFFER_PONTOS.get, plt.subplots, ax.set_title |
| gerar_grid_plumas_24h() | 927-1037 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| plotar_completo_campanha(df_meteo, df_model_unit, arquivo_medido_info, nome_unidade, id_campanha, datas, output_path) | 1040-1122 | Chamadas efetivas: pd.to_datetime, .copy, pd.DataFrame, plt.subplots, ax_top.twinx, ax_precip.bar, ax_precip.set_ylabel, ax_precip.set_ylim |
| processar_campanhas_completas(df_meteo) | 1125-1136 | Chamadas efetivas: CAMPANHAS_HISTORICAS.items, os.path.join, ler_concentracao_modelo, dados_u.get, models.get, info_hist.items, plotar_completo_campanha, encontrar_arquivo_campanha |
| encontrar_pasta_calpuff_horaria(dados) | 1139-1182 | Chamadas efetivas: dados.get, .lower, print, add_candidato, os.path.exists, str, candidatos.append, os.path.join Retorno: None, pasta. |
| estatisticas_dat_calpuff(filepath) | 1185-1225 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: {'conc_max_ugm3': float(np.max(arr)), 'conc_media_grade_ugm3': media_pos, 'conc_p95_grade_ugm3': p95_pos, 'n_celulas': int(arr.size)}, None. |
| construir_serie_calpuff_horaria(path_dir, anos=None) | 1228-1274 | Chamadas efetivas: listar_arquivos_calpuff_horarios, set, sorted, .sort_values, .agg, parse_dat_filename, estatisticas_dat_calpuff, row.update Retorno: df, pd.DataFrame(). |
| calcular_concentracao_media_por_hora(df_serie, metrica='max') | 1277-1302 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: out, pd.DataFrame(). |
| anos_para_texto(anos) | 1305-1311 | Chamadas efetivas: .join, str, int Retorno: 'todos', '-'.join((str(int(a)) for a in anos)). |
| garantir_pasta(path) | 1314-1318 | Chamadas efetivas: os.makedirs |
| caminhos_cache_calpuff(key_unidade, metrica=None) | 1321-1336 | Chamadas efetivas: os.path.join, garantir_pasta Retorno: paths. |
| caminhos_cache_vento() | 1339-1346 | Chamadas efetivas: os.path.join, garantir_pasta, anos_para_texto Retorno: {'pasta': pasta, 'vento': os.path.join(pasta, f'vento_horario_vetorial_{anos_txt}.csv')}. |
| caminhos_cache_clp() | 1349-1356 | Chamadas efetivas: os.path.join, garantir_pasta, anos_para_texto Retorno: {'pasta': pasta, 'clp': os.path.join(pasta, f'clp_horaria_{anos_txt}.csv')}. |
| salvar_csv_cache(df, path) | 1359-1366 | grava produtos Retorno: True, False. |
| ler_csv_cache(path, parse_datetime_cols=None) | 1369-1381 | lê dados Retorno: pd.DataFrame(), df. |
| assinatura_arquivos_calpuff(path_dir, anos=None) | 1384-1423 | Chamadas efetivas: listar_arquivos_calpuff_horarios, parse_dat_filename, arquivos.append, datas.append, os.path.abspath, anos_para_texto, int, sorted Retorno: (assinatura, sorted(arquivos)). |
| salvar_manifest_cache(path_manifest, assinatura) | 1426-1431 | Chamadas efetivas: pd.DataFrame, salvar_csv_cache, print |
| cache_serie_calpuff_valido(path_manifest, assinatura_atual) | 1434-1458 | Chamadas efetivas: ler_csv_cache, .to_dict, os.path.exists, assinatura_atual.get, row.get, int, str Retorno: True, True. |
| construir_serie_calpuff_horaria_de_arquivos(arquivos, anos=None) | 1461-1505 | Chamadas efetivas: enumerate, .sort_values, .agg, sorted, parse_dat_filename, estatisticas_dat_calpuff, row.update, rows.append Retorno: df, pd.DataFrame(). |
| obter_serie_calpuff_horaria_cacheada(key_unidade, path_dir, anos=None) | 1508-1553 | Chamadas efetivas: caminhos_cache_calpuff, assinatura_arquivos_calpuff, print, construir_serie_calpuff_horaria_de_arquivos, pd.DataFrame, os.path.exists, cache_serie_calpuff_valido, ler_csv_cache Retorno: df_serie, pd.DataFrame(). |
| obter_resumo_concentracao_horario_cacheado(key_unidade, df_serie, metrica) | 1556-1575 | Chamadas efetivas: caminhos_cache_calpuff, calcular_concentracao_media_por_hora, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols_necessarias.issubset, set Retorno: df_resumo, df_resumo. |
| obter_vento_horario_cacheado(df_meteo) | 1578-1597 | Chamadas efetivas: caminhos_cache_vento, calcular_vento_horario_vetorial, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols.issubset, set Retorno: df_vento, df_cache. |
| detectar_coluna_clp(df) | 1600-1620 | Chamadas efetivas: list, .upper, any, .strip, str Retorno: None, None. |
| ler_arquivo_clp_auxiliar() | 1623-1656 | lê dados Retorno: pd.DataFrame(), df. |
| preparar_dataframe_clp(df) | 1659-1686 | Chamadas efetivas: df.copy, detectar_coluna_clp, pd.to_numeric, out.dropna, pd.DataFrame, .strip, next, pd.to_datetime Retorno: out[['datetime', 'clp_m']], pd.DataFrame(). |
| _safe_float_sfc(valor) | 1689-1694 | Chamadas efetivas: float, .replace, .strip, str Retorno: float(str(valor).strip().replace('D', 'E').replace('d', 'e')), np.nan. |
| _ano_aermet_para_quatro_digitos(ano) | 1697-1706 | Chamadas efetivas: int, float Retorno: 2000 + ano_int if ano_int < 50 else 1900 + ano_int, ano_int. |
| _limpar_clp_valor(valor) | 1709-1717 | Chamadas efetivas: _safe_float_sfc, np.isfinite, abs Retorno: v, np.nan. |
| _combinar_zic_zim(zic, zim) | 1720-1737 | Chamadas efetivas: .lower, max, .strip, np.isfinite, str Retorno: max(vals), np.nan. |
| ler_aermet_sfc_clp(path=None) | 1740-1831 | Chamadas efetivas: pd.DataFrame, .sort_values, .agg, print, os.path.exists, open, df.dropna, df.groupby Retorno: df, pd.DataFrame(). |
| calcular_clp_horario(df_meteo, anos=None) | 1834-1869 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: resumo, pd.DataFrame(). |
| obter_clp_horario_cacheado(df_meteo) | 1872-1891 | Chamadas efetivas: caminhos_cache_clp, calcular_clp_horario, pd.DataFrame, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols.issubset Retorno: df_clp, pd.DataFrame(). |
| calcular_vento_horario_vetorial(df_meteo, anos=None) | 1894-1943 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: g, pd.DataFrame(). |
| carregar_dados_meteo_from_df(df) | 1946-1964 | Chamadas efetivas: df.copy, pd.to_numeric, pd.to_datetime, .astype, hora.where, pd.to_timedelta, hora_corr.fillna Retorno: out. |
| plotar_diagnostico_horario_vento_conc(df_vento_hora, df_conc_hora, nome_unidade, output_path, metrica, df_clp_hora=None) | 1967-2123 | Chamadas efetivas: .sort_values, df_plot.dropna, .to_numpy, max, plt.subplots, fig.subplots_adjust, mcolors.Normalize, plt.cm.viridis |
| gerar_diagnosticos_horarios_calpuff(df_meteo) | 2126-2170 | Chamadas efetivas: print, garantir_pasta, obter_vento_horario_cacheado, obter_clp_horario_cacheado, UNIDADES.items, encontrar_pasta_calpuff_horaria, obter_serie_calpuff_horaria_cacheada, obter_resumo_concentracao_horario_cacheado |
| plotar_rosa_ventos_anual(df, ano, vmax_global) | 2173-2189 | Chamadas efetivas: plt.figure, WindroseAxes.from_ax, ax.bar, ax.tick_params, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_rosa_ventos_dupla_anual(df, anos, vmax_global) | 2192-2217 | Chamadas efetivas: plt.figure, fig.add_subplot, zip, fig.suptitle, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_rosa_ventos_mensal(df, ano, vmax_global) | 2220-2243 | Chamadas efetivas: plt.figure, sorted, enumerate, fig.suptitle, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_precipitacao_mensal_comparativa(df) | 2246-2262 | Chamadas efetivas: .reset_index, .map, plt.subplots, sns.barplot, .max, ax.set_ylim, ax.set_xlabel, ax.tick_params |
| carregar_dados_meteo(caminho) | 2265-2273 | lê dados Retorno: df, None. |
| main() | 2276-2300 | Chamadas efetivas: gerar_mapas_dispersao, gerar_mapa_duplo_calpuff_24h_anual, gerar_mapa_pontos_amostragem, gerar_grid_plumas_24h, carregar_dados_meteo, print, os.path.exists, os.makedirs |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de map_copasa.py, linhas 265-271.

```python
    if PLUMA_ESCALA_ROBUSTA:
        vmax_visual = float(serie_pos.quantile(PLUMA_QUANTIL_VISUAL))
        if not np.isfinite(vmax_visual) or vmax_visual <= vmin_base:
            vmax_visual = vmax_abs
        vmax_visual = min(vmax_visual, vmax_abs)
    else:
        vmax_visual = vmax_abs
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Trecho de map_copasa.py, linhas 961-967.

```python
        if not valid_conc.empty:
            vmax_visual = valid_conc.quantile(0.95)
        else:
            vmax_visual = max_abs

        if vmax_visual <= 0.1: vmax_visual = 1.0
        vmin = 0.1
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- nanmean: Média ignorando valores não finitos representados por NaN. A cobertura precisa ser examinada, pois ignorar lacunas não as preenche.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## map_copasa_bilingue.py

Versão histórica bilíngue do processamento inicial. Seus produtos e entradas não devem substituir a rodada CMAS atual.

**Papel.** Histórico: etapa anterior à rodada CMAS atual. **Fonte inspecionada.** E:\copasa_map\map_copasa_bilingue.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| adjustText | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| calendar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| contextily | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| glob | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| locale | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| logging | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| math | Funções matemáticas escalares. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.dates | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patheffects | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.text | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib_scalebar.scalebar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| seaborn | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |
| windrose | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {filepath} — chamada gpd.read_file, linha 445.
- {filepath} — chamada zipfile.ZipFile, linha 454.
- os.path.join(temp_dir, kml_list[0]) — chamada gpd.read_file, linha 458.
- {filepath} — chamada open, linha 1291.
- {filepath} — chamada pd.read_csv, linha 667.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada pd.read_csv, linha 1750.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada pd.read_excel, linha 1745.
- os.path.join(BASE_DIR, 'AERMET_COP.SFC') — chamada open, linha 1856.
- os.path.join(root, nome) — chamada pd.read_excel, linha 2366.

**Saídas.**

- {filepath} — chamada fig.savefig, linha 289.
- filepath.replace('.png', '_backup.png') — chamada fig.savefig, linha 295.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada df.to_csv, linha 1461.

**Campos e chaves lidos.**

- gdf: MINLEVEL.
- df_shp_valores: MINLEVEL.
- df: ANO, DATA, HORA, conc, datetime, timedelta, x_km, y_km.
- row: hora_int.
- df.loc: HORA.
- dados: csv, kmz, nome.
- gdf_data: MINLEVEL, conc.
- df_plot: _conc_plot, conc, conc_media_ugm3, dir_media_o, hora, vel_media_vetorial_ms.
- gdfs: 24, anual.
- info: nome, pasta, shp_suffix.
- d: conc.
- df_hr: conc.
- gdf_temp: conc.
- df_meteo: VVr_ms, datetime.
- df_model_unit: datetime.
- df_m: DV_o, PP_mm, VV_ms, datetime, y_quiver.
- df_mod_cut: AERMOD_ppb, CALPUFF_ppb, datetime.
- df_camp: datetime.
- df_c_cut: concentracao_ppb, datetime.
- day_data: datetime.
- dados_u: nome.
- paths: clp, manifest, pasta, resumo_metrica, serie, vento.
- out: ANO, DIA, HORA, MÊS, clp_m, datetime.
- df_clp: datetime.
- g: dir_media_o, u_medio, v_medio.
- df_clp_hora: clp_media_m, hora.
- df_clp_plot: clp_media_m, hora.
- ax_clp.spines: bottom, left, right, top.
- df_vento_hora: n_horas, vel_media_vetorial_ms.
- paths_cache: resumo_base.
- subset: DV_o, MÊS, VVr_ms.
- mes_data: DV_o, VVr_ms.
- mensal: MÊS, PP_mm.

**Campos e chaves gerados.**

- gdf_kml: MINLEVEL, area.
- df: HORA, _u, _v, datetime, hora, hora_int, x_m, y_m.
- df_hourly: concentracao_ppb.
- df_plot: _conc_plot, conc.
- df_m: y_quiver.
- paths: resumo_metrica.
- out: clp_m, datetime.
- df_clp: hora.
- g: dir_cardinal, dir_media_o, vel_media_vetorial_ms.
- df_clp_plot: clp_media_m, hora.
- mensal: Nome_Mês.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _traduzir_texto_figura(texto) | 273-283 | Chamadas efetivas: str, _TRANSLATION_EXACT.items, s.replace, re.sub, re.escape Retorno: s, texto. |
| _salvar_png_com_fallback(fig, filepath, dpi_padrao) | 286-298 | grava produtos Retorno: filepath, fallback_path. |
| _salvar_versao_ingles(fig, filepath, dpi_padrao) | 301-333 | Chamadas efetivas: os.path.dirname, os.path.join, os.makedirs, os.path.splitext, _salvar_png_com_fallback, fig.canvas.draw, os.path.basename, fig.findobj |
| salvar_figura_segura(fig, filepath, dpi_padrao=600) | 336-339 | Chamadas efetivas: _salvar_png_com_fallback, _salvar_versao_ingles |
| convert_ug_to_ppb(x) | 342-342 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: x * FATOR_UG_TO_PPB. |
| convert_ppb_to_ug(x) | 344-344 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: x / FATOR_UG_TO_PPB. |
| direcao_cardinal(graus) | 347-353 | Chamadas efetivas: pd.isna, int, float Retorno: setores[int((float(graus) + 11.25) // 22.5) % 16], ''. |
| obter_escala_visual_conc(valores, vmin_base=0.1) | 356-375 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (vmin_base, vmax_visual, vmax_abs), (vmin_base, max(vmin_base * 10, 1.0), 0.0). |
| format_lon(x, pos) | 378-380 | Chamadas efetivas: transformer_axes.transform Retorno: f'{lon:.3f}°'. |
| format_lat(y, pos) | 383-385 | Chamadas efetivas: transformer_axes.transform Retorno: f'{lat:.3f}°'. |
| parse_coordinates_string(coords_str) | 388-397 | Chamadas efetivas: .replace, coords_str.split, c.split, len, lista_coords.append, coords_str.strip, float Retorno: lista_coords, []. |
| ler_kml_xml_geometry_only(filepath) | 400-417 | Chamadas efetivas: os.path.exists, ET.parse, tree.getroot, root.iter, gpd.GeoDataFrame, gdf.to_crs, tag.split, strip_ns Retorno: None, gdf.to_crs(CRS_WEB). |
| obter_valores_do_shp(filepath) | 420-426 | lê dados Retorno: None, None. |
| combinar_kml_shp(gdf_kml, df_shp_valores) | 429-439 | Chamadas efetivas: .reset_index, len, np.linspace, gdf_kml.sort_values, .sort_values, .min, .max Retorno: gdf_kml, None. |
| ler_shp_aermod(filepath) | 442-448 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_kmz_limite_poligono(filepath) | 451-468 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_csv_pontos(filepath) | 471-489 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_arquivo_dat_calpost(filepath) | 492-511 | Chamadas efetivas: os.path.exists, pd.DataFrame, open, .split, len, line.strip, float, data_rows.append Retorno: None, df. |
| parse_dat_filename(filename) | 514-569 | Chamadas efetivas: .strip, os.path.splitext, os.path.basename, re.search, match.groups, int, pd.Timestamp, str Retorno: None, dt + pd.Timedelta(hours=hour, minutes=minute). |
| listar_arquivos_calpuff_horarios(path_dir, recursive=True) | 572-609 | Chamadas efetivas: sorted, os.walk, set, os.path.exists, os.path.join, .lower, os.path.isfile, parse_dat_filename Retorno: sorted(set(arquivos)), []. |
| ler_concentracao_campanha(filepath, data_referencia_inicio) | 612-660 | lê dados Retorno: None, df_hourly. |
| ler_concentracao_modelo(filepath) | 663-680 | lê dados Retorno: None, df.dropna(subset=['datetime']). |
| encontrar_arquivo_campanha(sigla_unidade, campanha_key) | 683-694 | Chamadas efetivas: os.path.join, os.path.exists, campanha_key.split, int Retorno: (None, None), (path, f'Medido (Campanha {campanha_key})'). |
| gerar_mapa_duplo_calpuff_24h_anual() | 697-797 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, plt.subplots, .set, fig.suptitle |
| plotar_disp(ax, current_fig, gdf_data, gdf_limite, bounds, nome_soft, show_model_label=True) | 800-868 | Chamadas efetivas: ax.xaxis.set_major_formatter, ax.xaxis.set_major_locator, ax.set_xlabel, ax.yaxis.set_major_formatter, ax.yaxis.set_major_locator, ax.set_ylabel, ax.tick_params, plt.setp Retorno: sm. |
| gerar_mapas_dispersao() | 871-952 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, PERIODOS.items, ler_shp_aermod, dados.get |
| gerar_mapa_pontos_amostragem() | 955-1023 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ler_csv_pontos, ZOOM_BUFFER_PONTOS.get, plt.subplots, ax.set_title |
| gerar_grid_plumas_24h() | 1026-1136 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| plotar_completo_campanha(df_meteo, df_model_unit, arquivo_medido_info, nome_unidade, id_campanha, datas, output_path) | 1139-1221 | Chamadas efetivas: pd.to_datetime, .copy, pd.DataFrame, plt.subplots, ax_top.twinx, ax_precip.bar, ax_precip.set_ylabel, ax_precip.set_ylim |
| processar_campanhas_completas(df_meteo) | 1224-1235 | Chamadas efetivas: CAMPANHAS_HISTORICAS.items, os.path.join, ler_concentracao_modelo, dados_u.get, models.get, info_hist.items, plotar_completo_campanha, encontrar_arquivo_campanha |
| encontrar_pasta_calpuff_horaria(dados) | 1238-1281 | Chamadas efetivas: dados.get, .lower, print, add_candidato, os.path.exists, str, candidatos.append, os.path.join Retorno: None, pasta. |
| estatisticas_dat_calpuff(filepath) | 1284-1324 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: {'conc_max_ugm3': float(np.max(arr)), 'conc_media_grade_ugm3': media_pos, 'conc_p95_grade_ugm3': p95_pos, 'n_celulas': int(arr.size)}, None. |
| construir_serie_calpuff_horaria(path_dir, anos=None) | 1327-1373 | Chamadas efetivas: listar_arquivos_calpuff_horarios, set, sorted, .sort_values, .agg, parse_dat_filename, estatisticas_dat_calpuff, row.update Retorno: df, pd.DataFrame(). |
| calcular_concentracao_media_por_hora(df_serie, metrica='max') | 1376-1401 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: out, pd.DataFrame(). |
| anos_para_texto(anos) | 1404-1410 | Chamadas efetivas: .join, str, int Retorno: 'todos', '-'.join((str(int(a)) for a in anos)). |
| garantir_pasta(path) | 1413-1417 | Chamadas efetivas: os.makedirs |
| caminhos_cache_calpuff(key_unidade, metrica=None) | 1420-1435 | Chamadas efetivas: os.path.join, garantir_pasta Retorno: paths. |
| caminhos_cache_vento() | 1438-1445 | Chamadas efetivas: os.path.join, garantir_pasta, anos_para_texto Retorno: {'pasta': pasta, 'vento': os.path.join(pasta, f'vento_horario_vetorial_{anos_txt}.csv')}. |
| caminhos_cache_clp() | 1448-1455 | Chamadas efetivas: os.path.join, garantir_pasta, anos_para_texto Retorno: {'pasta': pasta, 'clp': os.path.join(pasta, f'clp_horaria_{anos_txt}.csv')}. |
| salvar_csv_cache(df, path) | 1458-1465 | grava produtos Retorno: True, False. |
| ler_csv_cache(path, parse_datetime_cols=None) | 1468-1480 | lê dados Retorno: pd.DataFrame(), df. |
| assinatura_arquivos_calpuff(path_dir, anos=None) | 1483-1522 | Chamadas efetivas: listar_arquivos_calpuff_horarios, parse_dat_filename, arquivos.append, datas.append, os.path.abspath, anos_para_texto, int, sorted Retorno: (assinatura, sorted(arquivos)). |
| salvar_manifest_cache(path_manifest, assinatura) | 1525-1530 | Chamadas efetivas: pd.DataFrame, salvar_csv_cache, print |
| cache_serie_calpuff_valido(path_manifest, assinatura_atual) | 1533-1557 | Chamadas efetivas: ler_csv_cache, .to_dict, os.path.exists, assinatura_atual.get, row.get, int, str Retorno: True, True. |
| construir_serie_calpuff_horaria_de_arquivos(arquivos, anos=None) | 1560-1604 | Chamadas efetivas: enumerate, .sort_values, .agg, sorted, parse_dat_filename, estatisticas_dat_calpuff, row.update, rows.append Retorno: df, pd.DataFrame(). |
| obter_serie_calpuff_horaria_cacheada(key_unidade, path_dir, anos=None) | 1607-1652 | Chamadas efetivas: caminhos_cache_calpuff, assinatura_arquivos_calpuff, print, construir_serie_calpuff_horaria_de_arquivos, pd.DataFrame, os.path.exists, cache_serie_calpuff_valido, ler_csv_cache Retorno: df_serie, pd.DataFrame(). |
| obter_resumo_concentracao_horario_cacheado(key_unidade, df_serie, metrica) | 1655-1674 | Chamadas efetivas: caminhos_cache_calpuff, calcular_concentracao_media_por_hora, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols_necessarias.issubset, set Retorno: df_resumo, df_resumo. |
| obter_vento_horario_cacheado(df_meteo) | 1677-1696 | Chamadas efetivas: caminhos_cache_vento, calcular_vento_horario_vetorial, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols.issubset, set Retorno: df_vento, df_cache. |
| detectar_coluna_clp(df) | 1699-1719 | Chamadas efetivas: list, .upper, any, .strip, str Retorno: None, None. |
| ler_arquivo_clp_auxiliar() | 1722-1755 | lê dados Retorno: pd.DataFrame(), df. |
| preparar_dataframe_clp(df) | 1758-1785 | Chamadas efetivas: df.copy, detectar_coluna_clp, pd.to_numeric, out.dropna, pd.DataFrame, .strip, next, pd.to_datetime Retorno: out[['datetime', 'clp_m']], pd.DataFrame(). |
| _safe_float_sfc(valor) | 1788-1793 | Chamadas efetivas: float, .replace, .strip, str Retorno: float(str(valor).strip().replace('D', 'E').replace('d', 'e')), np.nan. |
| _ano_aermet_para_quatro_digitos(ano) | 1796-1805 | Chamadas efetivas: int, float Retorno: 2000 + ano_int if ano_int < 50 else 1900 + ano_int, ano_int. |
| _limpar_clp_valor(valor) | 1808-1816 | Chamadas efetivas: _safe_float_sfc, np.isfinite, abs Retorno: v, np.nan. |
| _combinar_zic_zim(zic, zim) | 1819-1836 | Chamadas efetivas: .lower, max, .strip, np.isfinite, str Retorno: max(vals), np.nan. |
| ler_aermet_sfc_clp(path=None) | 1839-1930 | Chamadas efetivas: pd.DataFrame, .sort_values, .agg, print, os.path.exists, open, df.dropna, df.groupby Retorno: df, pd.DataFrame(). |
| calcular_clp_horario(df_meteo, anos=None) | 1933-1968 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: resumo, pd.DataFrame(). |
| obter_clp_horario_cacheado(df_meteo) | 1971-1990 | Chamadas efetivas: caminhos_cache_clp, calcular_clp_horario, pd.DataFrame, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols.issubset Retorno: df_clp, pd.DataFrame(). |
| calcular_vento_horario_vetorial(df_meteo, anos=None) | 1993-2042 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: g, pd.DataFrame(). |
| carregar_dados_meteo_from_df(df) | 2045-2063 | Chamadas efetivas: df.copy, pd.to_numeric, pd.to_datetime, .astype, hora.where, pd.to_timedelta, hora_corr.fillna Retorno: out. |
| plotar_diagnostico_horario_vento_conc(df_vento_hora, df_conc_hora, nome_unidade, output_path, metrica, df_clp_hora=None) | 2066-2222 | Chamadas efetivas: .sort_values, df_plot.dropna, .to_numpy, max, plt.subplots, fig.subplots_adjust, mcolors.Normalize, plt.cm.viridis |
| gerar_diagnosticos_horarios_calpuff(df_meteo) | 2225-2269 | Chamadas efetivas: print, garantir_pasta, obter_vento_horario_cacheado, obter_clp_horario_cacheado, UNIDADES.items, encontrar_pasta_calpuff_horaria, obter_serie_calpuff_horaria_cacheada, obter_resumo_concentracao_horario_cacheado |
| plotar_rosa_ventos_anual(df, ano, vmax_global) | 2272-2288 | Chamadas efetivas: plt.figure, WindroseAxes.from_ax, ax.bar, ax.tick_params, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_rosa_ventos_dupla_anual(df, anos, vmax_global) | 2291-2316 | Chamadas efetivas: plt.figure, fig.add_subplot, zip, fig.suptitle, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_rosa_ventos_mensal(df, ano, vmax_global) | 2319-2342 | Chamadas efetivas: plt.figure, sorted, enumerate, fig.suptitle, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_precipitacao_mensal_comparativa(df) | 2345-2361 | Chamadas efetivas: .reset_index, .map, plt.subplots, sns.barplot, .max, ax.set_ylim, ax.set_xlabel, ax.tick_params |
| carregar_dados_meteo(caminho) | 2364-2372 | lê dados Retorno: df, None. |
| main() | 2375-2399 | Chamadas efetivas: gerar_mapas_dispersao, gerar_mapa_duplo_calpuff_24h_anual, gerar_mapa_pontos_amostragem, gerar_grid_plumas_24h, carregar_dados_meteo, print, os.path.exists, os.makedirs |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de map_copasa_bilingue.py, linhas 364-370.

```python
    if PLUMA_ESCALA_ROBUSTA:
        vmax_visual = float(serie_pos.quantile(PLUMA_QUANTIL_VISUAL))
        if not np.isfinite(vmax_visual) or vmax_visual <= vmin_base:
            vmax_visual = vmax_abs
        vmax_visual = min(vmax_visual, vmax_abs)
    else:
        vmax_visual = vmax_abs
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Trecho de map_copasa_bilingue.py, linhas 1060-1066.

```python
        if not valid_conc.empty:
            vmax_visual = valid_conc.quantile(0.95)
        else:
            vmax_visual = max_abs

        if vmax_visual <= 0.1: vmax_visual = 1.0
        vmin = 0.1
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- nanmean: Média ignorando valores não finitos representados por NaN. A cobertura precisa ser examinada, pois ignorar lacunas não as preenche.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## map_copasa_resumo_expandido.py

Gerador histórico associado ao resumo expandido inicial; mantém utilidade como rastreabilidade, mas não representa sozinho os cálculos e figuras atuais.

**Papel.** Histórico: etapa anterior à rodada CMAS atual. **Fonte inspecionada.** E:\copasa_map\map_copasa_resumo_expandido.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| adjustText | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| calendar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_copasa | Configuração local dos caminhos, independente dos cálculos. |
| contextily | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| gc | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| glob | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| locale | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| logging | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| math | Funções matemáticas escalares. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.dates | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patheffects | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.tri | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib_scalebar.scalebar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| scipy.ndimage | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| seaborn | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |
| windrose | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- os.path.abspath(os.path.normpath(filepath)) — chamada gpd.read_file, linha 547.
- os.path.abspath(os.path.normpath(filepath)) — chamada zipfile.ZipFile, linha 556.
- os.path.join(temp_dir, kml_list[0]) — chamada gpd.read_file, linha 560.
- os.path.abspath(os.path.normpath(filepath)) — chamada open, linha 1873.
- os.path.abspath(os.path.normpath(filepath)) — chamada pd.read_csv, linha 829.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada pd.read_csv, linha 2332.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada pd.read_excel, linha 2327.
- os.path.join(BASE_DIR, 'AERMET_COP.SFC') — chamada open, linha 2438.
- os.path.join(root, nome) — chamada pd.read_excel, linha 2948.

**Saídas.**

- os.path.abspath(os.path.normpath(filepath)) — chamada fig.savefig, linha 261.
- os.path.join(CONCENTRACAO_DIR, filename) — chamada df.to_csv, linha 2043.

**Campos e chaves lidos.**

- gdf: MINLEVEL, conc.
- df_shp_valores: MINLEVEL.
- df: ANO, DATA, HORA, conc, datetime, timedelta, x_km, y_km.
- row: hora_int.
- df.loc: HORA.
- dados: csv, kmz, nome.
- gdf_data: MINLEVEL, conc.
- df_plot: _conc_plot, conc, conc_media_ugm3, dir_media_o, hora, vel_media_vetorial_ms.
- gdfs: 24, anual.
- info: nome, pasta, shp_suffix.
- ds: aermod, bounds, calpuff, limite, nome.
- ax.spines: bottom, left.
- d: conc.
- df_hr: conc.
- gdf_temp: conc.
- df_meteo: VVr_ms, datetime.
- df_model_unit: datetime.
- df_m: DV_o, PP_mm, VV_ms, datetime, y_quiver.
- df_mod_cut: AERMOD_ppb, CALPUFF_ppb, datetime.
- df_camp: datetime.
- df_c_cut: concentracao_ppb, datetime.
- day_data: datetime.
- dados_u: nome.
- paths: clp, manifest, pasta, resumo_metrica, serie, vento.
- out: ANO, DIA, HORA, MÊS, clp_m, datetime.
- df_clp: datetime.
- g: dir_media_o, u_medio, v_medio.
- df_clp_hora: clp_media_m, hora.
- df_clp_plot: clp_media_m, hora.
- ax_clp.spines: bottom, left, right, top.
- df_vento_hora: n_horas, vel_media_vetorial_ms.
- paths_cache: resumo_base.
- subset: DV_o, MÊS, VVr_ms.
- mes_data: DV_o, VVr_ms.
- mensal: MÊS, PP_mm.

**Campos e chaves gerados.**

- gdf_kml: MINLEVEL, area.
- df: HORA, MINLEVEL, _u, _v, datetime, hora, hora_int, x_m, y_m.
- df_hourly: concentracao_ppb.
- df_plot: _conc_plot, conc.
- gdf: MINLEVEL, conc.
- df_m: y_quiver.
- paths: resumo_metrica.
- out: clp_m, datetime.
- df_clp: hora.
- g: dir_cardinal, dir_media_o, vel_media_vetorial_ms.
- df_clp_plot: clp_media_m, hora.
- mensal: Nome_Mês.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| salvar_figura_segura(fig, filepath, dpi_padrao=600) | 246-276 | grava produtos |
| convert_ug_to_ppb(x) | 279-279 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: x * FATOR_UG_TO_PPB. |
| convert_ppb_to_ug(x) | 281-281 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: x / FATOR_UG_TO_PPB. |
| fmt_plain_number(x) | 284-298 | Chamadas efetivas: abs, .rstrip, float, str Retorno: f'{x:.3f}'.rstrip('0').rstrip('.'), f'{x:.0f}'. |
| add_basemap_publication(ax) | 301-321 | Chamadas efetivas: ctx.add_basemap Retorno: True, True. |
| _adjust_bounds_to_ratio(bounds, target_ratio=2.0) | 324-338 | Chamadas efetivas: map, max Retorno: [cx - width / 2.0, cy - height / 2.0, cx + width / 2.0, cy + height / 2.0], None. |
| _nice_scale_length(max_len) | 341-344 | Chamadas efetivas: np.array, len, float, validos.max Retorno: float(validos.max()) if len(validos) else float(max_len). |
| draw_simple_north(ax) | 347-357 | Chamadas efetivas: ax.annotate, ax.text, dict, pe.withStroke |
| draw_simple_scalebar(ax) | 360-395 | Chamadas efetivas: ax.get_xlim, ax.get_ylim, _nice_scale_length, ax.add_patch, ax.text, mpatches.FancyBboxPatch, mpatches.Rectangle, ax.plot |
| render_plume_surface(ax, gdf, value_col, norm, levels, cmap) | 398-446 | Chamadas efetivas: pd.to_numeric, np.isfinite, np.clip, ax.get_xlim, ax.get_ylim, np.linspace, np.meshgrid, m.sum |
| direcao_cardinal(graus) | 449-455 | Chamadas efetivas: pd.isna, int, float Retorno: setores[int((float(graus) + 11.25) // 22.5) % 16], ''. |
| obter_escala_visual_conc(valores, vmin_base=0.1) | 458-477 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (vmin_base, vmax_visual, vmax_abs), (vmin_base, max(vmin_base * 10, 1.0), 0.0). |
| format_lon(x, pos) | 480-482 | Chamadas efetivas: transformer_axes.transform Retorno: f'{lon:.3f}°'. |
| format_lat(y, pos) | 485-487 | Chamadas efetivas: transformer_axes.transform Retorno: f'{lat:.3f}°'. |
| parse_coordinates_string(coords_str) | 490-499 | Chamadas efetivas: .replace, coords_str.split, c.split, len, lista_coords.append, coords_str.strip, float Retorno: lista_coords, []. |
| ler_kml_xml_geometry_only(filepath) | 502-519 | Chamadas efetivas: os.path.exists, ET.parse, tree.getroot, root.iter, gpd.GeoDataFrame, gdf.to_crs, tag.split, strip_ns Retorno: None, gdf.to_crs(CRS_WEB). |
| obter_valores_do_shp(filepath) | 522-528 | lê dados Retorno: None, None. |
| combinar_kml_shp(gdf_kml, df_shp_valores) | 531-541 | Chamadas efetivas: .reset_index, len, np.linspace, gdf_kml.sort_values, .sort_values, .min, .max Retorno: gdf_kml, None. |
| ler_shp_aermod(filepath) | 544-550 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_kmz_limite_poligono(filepath) | 553-570 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_csv_pontos(filepath) | 573-591 | lê dados Retorno: None, gdf.to_crs(CRS_WEB). |
| ler_arquivo_dat_calpost(filepath) | 594-613 | Chamadas efetivas: os.path.exists, pd.DataFrame, open, .split, len, line.strip, float, data_rows.append Retorno: None, df. |
| ler_arquivo_plt_aermod(filepath) | 616-642 | Chamadas efetivas: os.path.exists, pd.DataFrame, open, line.split, line.startswith, len, float, rows.append Retorno: None, df. |
| _resolver_arquivo_cmas(key_unidade, key_periodo, modelo) | 645-673 | Chamadas efetivas: next, os.path.join, os.path.exists Retorno: None, next((f for f in candidatos if os.path.exists(f)), candidatos[0]). |
| parse_dat_filename(filename) | 676-731 | Chamadas efetivas: .strip, os.path.splitext, os.path.basename, re.search, match.groups, int, pd.Timestamp, str Retorno: None, dt + pd.Timedelta(hours=hour, minutes=minute). |
| listar_arquivos_calpuff_horarios(path_dir, recursive=True) | 734-771 | Chamadas efetivas: sorted, os.walk, set, os.path.exists, os.path.join, .lower, os.path.isfile, parse_dat_filename Retorno: sorted(set(arquivos)), []. |
| ler_concentracao_campanha(filepath, data_referencia_inicio) | 774-822 | lê dados Retorno: None, df_hourly. |
| ler_concentracao_modelo(filepath) | 825-842 | lê dados Retorno: None, df.dropna(subset=['datetime']). |
| encontrar_arquivo_campanha(sigla_unidade, campanha_key) | 845-856 | Chamadas efetivas: os.path.join, os.path.exists, campanha_key.split, int Retorno: (None, None), (path, f'Medido (Campanha {campanha_key})'). |
| gerar_mapa_duplo_calpuff_24h_anual() | 859-959 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, plt.subplots, .set, fig.suptitle |
| plotar_disp(ax, current_fig, gdf_data, gdf_limite, bounds, nome_soft, show_model_label=True) | 962-1030 | Chamadas efetivas: ax.xaxis.set_major_formatter, ax.xaxis.set_major_locator, ax.set_xlabel, ax.yaxis.set_major_formatter, ax.yaxis.set_major_locator, ax.set_ylabel, ax.tick_params, plt.setp Retorno: sm. |
| gerar_mapas_dispersao() | 1033-1114 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, PERIODOS.items, ler_shp_aermod, dados.get |
| _carregar_dispersao_resumo_expandido(key_unidade, key_periodo, target_ratio=2.0) | 1117-1157 | Chamadas efetivas: os.path.join, ler_kmz_limite_poligono, ZOOM_BUFFER_DISPERSAO.get, max, _adjust_bounds_to_ratio, _resolver_arquivo_cmas, int, os.path.exists Retorno: {'key': key_unidade, 'nome': dados['nome'], 'limite': gdf_limite, 'bounds': bounds, 'aermod': gdf_aermod, 'calpuff': gdf_calpuff}. |
| _serie_positiva_resumo(gdf, coluna) | 1160-1165 | Chamadas efetivas: pd.to_numeric, .dropna, pd.Series, serie.replace Retorno: serie[serie > 0], pd.Series(dtype=float). |
| _escala_comum_resumo_expandido(datasets) | 1168-1209 | Chamadas efetivas: pd.concat, float, min, max, _serie_positiva_resumo, todos.max, valores_aermod.append, valores_todos.append Retorno: (vmin, vmax), (0.1, 1.0). |
| _escala_por_ete_resumo(ds) | 1212-1229 | Chamadas efetivas: _serie_positiva_resumo, max, ds.get, float, pd.concat, aer.max, s.max, aer.min Retorno: (vmin, vmax), (0.1, 1.0). |
| _plotar_painel_resumo_expandido(ax, ds, modelo, norm, levels, panel_label, mostrar_x=False, y_side='left', show_north=False, show_scalebar=False, panel_ratio=2.0, panel_label_fs=None, tick_fs=None) | 1232-1331 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| _gerar_figura_comparativa_resumo_periodo(key_periodo, output_dir, panel_ratio=2.0, filename_suffix='') | 1334-1438 | Chamadas efetivas: _escala_comum_resumo_expandido, mcolors.LogNorm, np.geomspace, np.array, enumerate, .get_position, fig.text, fig.add_axes |
| gerar_figura1_contribuicao_fontes(output_dir) | 1441-1503 | Chamadas efetivas: plt.subplots, zip, ax.set_xlim, ax.set_ylim, ax.set_yticks, ax.set_yticklabels, ax.set_xlabel, ax.tick_params |
| gerar_mapas_resumo_expandido() | 1506-1534 | Chamadas efetivas: print, os.path.join, os.makedirs, gerar_figura1_contribuicao_fontes, _gerar_figura_comparativa_resumo_periodo, os.path.exists, os.remove |
| gerar_mapa_pontos_amostragem() | 1537-1605 | Chamadas efetivas: print, UNIDADES.items, os.path.join, ler_kmz_limite_poligono, ler_csv_pontos, ZOOM_BUFFER_PONTOS.get, plt.subplots, ax.set_title |
| gerar_grid_plumas_24h() | 1608-1718 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| plotar_completo_campanha(df_meteo, df_model_unit, arquivo_medido_info, nome_unidade, id_campanha, datas, output_path) | 1721-1803 | Chamadas efetivas: pd.to_datetime, .copy, pd.DataFrame, plt.subplots, ax_top.twinx, ax_precip.bar, ax_precip.set_ylabel, ax_precip.set_ylim |
| processar_campanhas_completas(df_meteo) | 1806-1817 | Chamadas efetivas: CAMPANHAS_HISTORICAS.items, os.path.join, ler_concentracao_modelo, dados_u.get, models.get, info_hist.items, plotar_completo_campanha, encontrar_arquivo_campanha |
| encontrar_pasta_calpuff_horaria(dados) | 1820-1863 | Chamadas efetivas: dados.get, .lower, print, add_candidato, os.path.exists, str, candidatos.append, os.path.join Retorno: None, pasta. |
| estatisticas_dat_calpuff(filepath) | 1866-1906 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: {'conc_max_ugm3': float(np.max(arr)), 'conc_media_grade_ugm3': media_pos, 'conc_p95_grade_ugm3': p95_pos, 'n_celulas': int(arr.size)}, None. |
| construir_serie_calpuff_horaria(path_dir, anos=None) | 1909-1955 | Chamadas efetivas: listar_arquivos_calpuff_horarios, set, sorted, .sort_values, .agg, parse_dat_filename, estatisticas_dat_calpuff, row.update Retorno: df, pd.DataFrame(). |
| calcular_concentracao_media_por_hora(df_serie, metrica='max') | 1958-1983 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: out, pd.DataFrame(). |
| anos_para_texto(anos) | 1986-1992 | Chamadas efetivas: .join, str, int Retorno: 'todos', '-'.join((str(int(a)) for a in anos)). |
| garantir_pasta(path) | 1995-1999 | Chamadas efetivas: os.makedirs |
| caminhos_cache_calpuff(key_unidade, metrica=None) | 2002-2017 | Chamadas efetivas: os.path.join, garantir_pasta Retorno: paths. |
| caminhos_cache_vento() | 2020-2027 | Chamadas efetivas: os.path.join, garantir_pasta, anos_para_texto Retorno: {'pasta': pasta, 'vento': os.path.join(pasta, f'vento_horario_vetorial_{anos_txt}.csv')}. |
| caminhos_cache_clp() | 2030-2037 | Chamadas efetivas: os.path.join, garantir_pasta, anos_para_texto Retorno: {'pasta': pasta, 'clp': os.path.join(pasta, f'clp_horaria_{anos_txt}.csv')}. |
| salvar_csv_cache(df, path) | 2040-2047 | grava produtos Retorno: True, False. |
| ler_csv_cache(path, parse_datetime_cols=None) | 2050-2062 | lê dados Retorno: pd.DataFrame(), df. |
| assinatura_arquivos_calpuff(path_dir, anos=None) | 2065-2104 | Chamadas efetivas: listar_arquivos_calpuff_horarios, parse_dat_filename, arquivos.append, datas.append, os.path.abspath, anos_para_texto, int, sorted Retorno: (assinatura, sorted(arquivos)). |
| salvar_manifest_cache(path_manifest, assinatura) | 2107-2112 | Chamadas efetivas: pd.DataFrame, salvar_csv_cache, print |
| cache_serie_calpuff_valido(path_manifest, assinatura_atual) | 2115-2139 | Chamadas efetivas: ler_csv_cache, .to_dict, os.path.exists, assinatura_atual.get, row.get, int, str Retorno: True, True. |
| construir_serie_calpuff_horaria_de_arquivos(arquivos, anos=None) | 2142-2186 | Chamadas efetivas: enumerate, .sort_values, .agg, sorted, parse_dat_filename, estatisticas_dat_calpuff, row.update, rows.append Retorno: df, pd.DataFrame(). |
| obter_serie_calpuff_horaria_cacheada(key_unidade, path_dir, anos=None) | 2189-2234 | Chamadas efetivas: caminhos_cache_calpuff, assinatura_arquivos_calpuff, print, construir_serie_calpuff_horaria_de_arquivos, pd.DataFrame, os.path.exists, cache_serie_calpuff_valido, ler_csv_cache Retorno: df_serie, pd.DataFrame(). |
| obter_resumo_concentracao_horario_cacheado(key_unidade, df_serie, metrica) | 2237-2256 | Chamadas efetivas: caminhos_cache_calpuff, calcular_concentracao_media_por_hora, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols_necessarias.issubset, set Retorno: df_resumo, df_resumo. |
| obter_vento_horario_cacheado(df_meteo) | 2259-2278 | Chamadas efetivas: caminhos_cache_vento, calcular_vento_horario_vetorial, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols.issubset, set Retorno: df_vento, df_cache. |
| detectar_coluna_clp(df) | 2281-2301 | Chamadas efetivas: list, .upper, any, .strip, str Retorno: None, None. |
| ler_arquivo_clp_auxiliar() | 2304-2337 | lê dados Retorno: pd.DataFrame(), df. |
| preparar_dataframe_clp(df) | 2340-2367 | Chamadas efetivas: df.copy, detectar_coluna_clp, pd.to_numeric, out.dropna, pd.DataFrame, .strip, next, pd.to_datetime Retorno: out[['datetime', 'clp_m']], pd.DataFrame(). |
| _safe_float_sfc(valor) | 2370-2375 | Chamadas efetivas: float, .replace, .strip, str Retorno: float(str(valor).strip().replace('D', 'E').replace('d', 'e')), np.nan. |
| _ano_aermet_para_quatro_digitos(ano) | 2378-2387 | Chamadas efetivas: int, float Retorno: 2000 + ano_int if ano_int < 50 else 1900 + ano_int, ano_int. |
| _limpar_clp_valor(valor) | 2390-2398 | Chamadas efetivas: _safe_float_sfc, np.isfinite, abs Retorno: v, np.nan. |
| _combinar_zic_zim(zic, zim) | 2401-2418 | Chamadas efetivas: .lower, max, .strip, np.isfinite, str Retorno: max(vals), np.nan. |
| ler_aermet_sfc_clp(path=None) | 2421-2512 | Chamadas efetivas: pd.DataFrame, .sort_values, .agg, print, os.path.exists, open, df.dropna, df.groupby Retorno: df, pd.DataFrame(). |
| calcular_clp_horario(df_meteo, anos=None) | 2515-2550 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: resumo, pd.DataFrame(). |
| obter_clp_horario_cacheado(df_meteo) | 2553-2572 | Chamadas efetivas: caminhos_cache_clp, calcular_clp_horario, pd.DataFrame, os.path.exists, ler_csv_cache, salvar_csv_cache, print, cols.issubset Retorno: df_clp, pd.DataFrame(). |
| calcular_vento_horario_vetorial(df_meteo, anos=None) | 2575-2624 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: g, pd.DataFrame(). |
| carregar_dados_meteo_from_df(df) | 2627-2645 | Chamadas efetivas: df.copy, pd.to_numeric, pd.to_datetime, .astype, hora.where, pd.to_timedelta, hora_corr.fillna Retorno: out. |
| plotar_diagnostico_horario_vento_conc(df_vento_hora, df_conc_hora, nome_unidade, output_path, metrica, df_clp_hora=None) | 2648-2804 | Chamadas efetivas: .sort_values, df_plot.dropna, .to_numpy, max, plt.subplots, fig.subplots_adjust, mcolors.Normalize, plt.cm.viridis |
| gerar_diagnosticos_horarios_calpuff(df_meteo) | 2807-2851 | Chamadas efetivas: print, garantir_pasta, obter_vento_horario_cacheado, obter_clp_horario_cacheado, UNIDADES.items, encontrar_pasta_calpuff_horaria, obter_serie_calpuff_horaria_cacheada, obter_resumo_concentracao_horario_cacheado |
| plotar_rosa_ventos_anual(df, ano, vmax_global) | 2854-2870 | Chamadas efetivas: plt.figure, WindroseAxes.from_ax, ax.bar, ax.tick_params, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_rosa_ventos_dupla_anual(df, anos, vmax_global) | 2873-2898 | Chamadas efetivas: plt.figure, fig.add_subplot, zip, fig.suptitle, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_rosa_ventos_mensal(df, ano, vmax_global) | 2901-2924 | Chamadas efetivas: plt.figure, sorted, enumerate, fig.suptitle, plt.cm.ScalarMappable, fig.colorbar, cb.set_label, cb.ax.tick_params |
| plotar_precipitacao_mensal_comparativa(df) | 2927-2943 | Chamadas efetivas: .reset_index, .map, plt.subplots, sns.barplot, .max, ax.set_ylim, ax.set_xlabel, ax.tick_params |
| carregar_dados_meteo(caminho) | 2946-2954 | lê dados Retorno: df, None. |
| main() | 2957-2987 | Chamadas efetivas: gerar_mapas_dispersao, gerar_mapas_resumo_expandido, gerar_mapa_duplo_calpuff_24h_anual, gerar_mapa_pontos_amostragem, gerar_grid_plumas_24h, carregar_dados_meteo, print, os.path.exists |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de map_copasa_resumo_expandido.py, linhas 466-472.

```python
    if PLUMA_ESCALA_ROBUSTA:
        vmax_visual = float(serie_pos.quantile(PLUMA_QUANTIL_VISUAL))
        if not np.isfinite(vmax_visual) or vmax_visual <= vmin_base:
            vmax_visual = vmax_abs
        vmax_visual = min(vmax_visual, vmax_abs)
    else:
        vmax_visual = vmax_abs
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Trecho de map_copasa_resumo_expandido.py, linhas 1262-1268.

```python
            if not gdf.empty:
                thr = max(norm.vmin, float(gdf['MINLEVEL'].quantile(0.35)), float(gdf['MINLEVEL'].max()) * 0.08)
                render_plume_surface(ax, gdf[gdf['MINLEVEL'] >= thr], 'MINLEVEL', norm, levels, cmap)
    else:
        gdf = ds['calpuff']
        if gdf is not None and not gdf.empty and 'conc' in gdf.columns:
            gdf = gdf.copy()
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- nanmean: Média ignorando valores não finitos representados por NaN. A cobertura precisa ser examinada, pois ignorar lacunas não as preenche.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.
