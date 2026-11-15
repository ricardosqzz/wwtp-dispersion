# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/cmas_poster/figuras/Cartografia_metadados.json | .read_text.
# Entrada: E:/copasa_map/output/cmas_poster/figuras/Faixas_concentracao_poster.json | .read_text.
# Entrada: E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json | .read_text.
# Entrada: E:/copasa_map/output/comparacao_modelos/Estatistica_horaria_por_receptor.csv | .open.
# Entrada: E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json | .read_text.
# Entrada: E:/copasa_map/output/cmas_poster/Poster_CMAS_Session05_WWTP.pptx | zipfile.ZipFile.
# Entrada: E:/copasa_map/output/cmas_poster/figuras/Boxplots_editaveis_dados.json | .read_text.
# Entrada: E:/copasa_map/output/comparacao_modelos/Estatistica_avancada.json | .read_text.
# Entrada: E:/copasa_map/output/cmas_poster/figuras/Perfis_editaveis_dados.json | .read_text.
# Entrada: E:/copasa_map/codigo/recursos_poster/assets/{logo} | .read_bytes.
# Entrada: io.BytesIO(z.read(name)) | Image.open.
# Entrada: Argumento fornecido pelo chamador | im.load.
# Entrada: E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.json | .read_text.
# Campos/chaves em v: annual, annual_native_max_abs_error_ug_m3, current_run, daily_native_max_abs_error_ug_m3, finite_coverage, mass_difference_percent, maximum_displayed, maximum_native_in_frame, native_node_max_error.
# Campos/chaves em fields: current_fields.
# Campos/chaves em m: color_norm, colorbar_end_shape, colorbar_map_gap_cm, colorbar_orientation, colorbar_text_clearance_cm, colorbar_thickness_cm, context_legend, measured_scale, panels, placeholder, poster_scale, primary_ticks_ug_m3, secondary_ticks_ppb, secondary_unit, ug_m3_per_ppb.
# Campos/chaves em p: AERMOD_P95, CALPUFF_P95, Spearman_rho_P95, distance_m, distance_max_m, distance_min_m, unit, within_factor_2_percent.
# Campos/chaves em spatial: rows.
# Campos/chaves em summary: n, within_factor_2_count, within_factor_2_percent.
# Campos/chaves em meta: Fontes_privacidade.
# Campos/chaves em data: execution_inputs, quality_AERMOD, quality_CALPUFF.
# Campos/chaves em b: axis_max, axis_min, axis_offset_below_zero_px, distance_min, high_m, index, low_m, median, model, n, plot_bounds, q1, q3, unit, y_unit_top.
# Campos/chaves em adv: poster_distributions.
# Campos/chaves em q: distance_min, model.
# Campos/chaves em series: values.
# Campos/chaves em pb: h, w, x, y.
# Campos/chaves em u: axis_max, axis_min, bins, n, unit.
# Campos/chaves em scatter: units.
# Campos/chaves em r: n, n_in_full_range, n_visible_main, stats_all_receptors.
# Saída: E:/copasa_map/output/auditoria/Validacao_Poster_Anual.json | .write_text.
# CÓDIGO DO PROCESSAMENTO

"""Conferência da nova rodada e dos valores publicados no pôster."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_copasa.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_copasa.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_copasa import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

from pathlib import Path
import zipfile,json,io
from PIL import Image
from lxml import etree as E
from pypdf import PdfReader
R=Path(_cp_texto('', 'posix'));O=R/'output/cmas_poster';F=O/'figuras';A=R/'output/comparacao_modelos'
checks=[]
# Check
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)));assert ok,name
meta=json.loads((F/'Cartografia_metadados.json').read_text());fields=json.loads((F/'Faixas_concentracao_poster.json').read_text());data=json.loads((A/'Comparacao_consolidada.json').read_text())
check('Current maps preserve native maxima and full frame coverage',all(v['finite_coverage']==1 and v['native_node_max_error']<1e-4 and abs(v['maximum_displayed']-v['maximum_native_in_frame'])<1e-5 and v['current_run'] for v in fields['current_fields']))
for stem in ['Comparacao_24h_faixa','Comparacao_anual_faixa']:
    m=meta[stem];check(stem+' linear colours, vertical flat bar, no contextual legend',m['panels']==4 and m['poster_scale']==8500 and m['colorbar_orientation']=='vertical' and m['colorbar_end_shape']=='flat' and m['colorbar_thickness_cm']==.58 and m['color_norm']=='linear' and not m['context_legend'] and not m['placeholder'])
    check(stem+' colourbar labels separated from last map',m['colorbar_map_gap_cm']>=1.65 and m['colorbar_text_clearance_cm']>.2)
    check(stem+' ppb axis is a conversion of the same concentrations',m['secondary_unit']=='ppb' and m['ug_m3_per_ppb']==1.40 and all(abs(a/1.40-b)<1e-12 for a,b in zip(m['primary_ticks_ug_m3'],m['secondary_ticks_ppb'])))
import csv,math
stats=list(csv.DictReader((A/'Estatistica_horaria_por_receptor.csv').open(encoding='utf-8-sig')))
spatial=json.loads((A/'Concordancia_espacial_P95.json').read_text(encoding='utf8'))
for unit in ['VM','NC']:
    pairs=[p for p in stats if p['unit']==unit and float(p['distance_m'])<1800]
    summary=next(p for p in spatial['rows'] if p['unit']==unit and p['distance_min_m']==0 and p['distance_max_m']==1800)
    count=sum(.5*float(p['AERMOD_P95'])<=float(p['CALPUFF_P95'])<=2*float(p['AERMOD_P95']) for p in pairs)
    check(unit+' factor-two agreement reproduces source receptor table',summary['n']==len(pairs) and summary['within_factor_2_count']==count and abs(summary['within_factor_2_percent']-count/len(pairs)*100)<1e-12)
check('Source-map physical scale recalculated to 1:2500',meta['Fontes_privacidade']['poster_scale']==2500 and all(abs(m['measured_scale']-2500)<.01 for m in meta['Fontes_privacidade']['maps']))
check('Larger grouped method legend clear of map and complete facilities',meta['Fontes_privacidade']['legend_position']=='right' and meta['Fontes_privacidade']['legend_fontsize_poster_pt']==25 and meta['Fontes_privacidade']['legend_context_fontsize_pt']==22 and meta['Fontes_privacidade']['legend_grouped'] and meta['Fontes_privacidade']['facility_boundaries_complete'] and meta['Fontes_privacidade']['legend_map_clearance_cm']>0)
check('Hourly AERMOD reproduces daily and annual native data',all(v['daily_native_max_abs_error_ug_m3']<1e-5 and v['annual_native_max_abs_error_ug_m3']<1e-5 for v in data['quality_AERMOD']))
check('Annual CALPUFF derived from hourly CONC with audited coverage',all(v['annual'][0]['hours']==8784 and v['annual'][1]['hours']==8732 for v in data['quality_CALPUFF']))
check('Mass difference below 0.02 percent',all(abs(v['mass_difference_percent'])<.02 for v in data['execution_inputs'].values()))
N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with zipfile.ZipFile(O/'Poster_CMAS_Session05_WWTP.pptx') as z:
    text=' '.join(E.fromstring(z.read('ppt/slides/slide1.xml')).xpath('//a:t/text()',namespaces=N));charts=sorted(n for n in z.namelist() if '/charts/chart' in n and n.endswith('.xml'))
    check('Editable emission chart retained; profiles are native quantitative shapes',len(charts)==1);caches=[]
    for name in charts:
        series=E.fromstring(z.read(name)).xpath('//c:ser',namespaces=N);caches.append((name,series));check(name+' series complete',len(series) in [1,2,4] and all(s.xpath('.//c:val//c:pt/c:v/text()',namespaces=N) for s in series))
    emission=next(ss for name,ss in caches if len(ss)==4);cat=emission[0].xpath('.//c:cat//c:pt/c:v/text()',namespaces=N);check('WWTP categories correct reversed native bar order',cat==['WWTP 2','WWTP 1'])
    scores=[next(p for p in spatial['rows'] if p['unit']==unit and p['distance_min_m']==0 and p['distance_max_m']==1800) for unit in ['NC','VM']]
    for name,ss in caches:
        if len(ss)==4:continue
        actual=[[float(v) for v in s.xpath('.//c:val//c:pt/c:v/text()',namespaces=N)] for s in ss]
        expected=[[p['Spearman_rho_P95'] for p in scores]] if len(ss)==1 else [[p['within_factor_2_percent']/100 for p in scores],[1-p['within_factor_2_percent']/100 for p in scores]]
        check(name+' statistics agree with full receptor analysis',all(abs(x-y)<1e-9 for a,b in zip(actual,expected) for x,y in zip(a,b)))
        if len(ss)==2:check('Factor-two chart labels show percentages',any('0.0%' in v for s in ss for v in s.xpath('.//c:dLbls/c:numFmt/@formatCode',namespaces=N)))
    check('No historical or pending result claim in poster',not any(s in text for s in ['Historical PLT','results are pending','Annual results pending']))
    check('Coverage documented; input differences excluded from poster','99.68%' in text and 'Terrain elevations' not in text and 'input inconsistencies' not in text and 'release heights' not in text)
    check('P95 spatial profiles and conventional ppb conversion included',all(t in text for t in ['MODEL CONTRAST ACROSS DISTANCE BANDS','1.40','ppb','ρ = 0.57','ρ = 0.63']))
    check('Full new institutional acknowledgements',all(v in text for v in ['Regulatory Research, Development, and Innovation Program','ARSAE-MG','COPASA','CNPq','CAPES','FAPEMIG','Finance Code 001']))
    check('Hourly distribution boxes and physical concentration units labelled','receptor-level hourly P95 (2024)' in text and 'µg/m³' in text and 'logarithmic concentration scale' not in text)
    boxes=json.loads((F/'Boxplots_editaveis_dados.json').read_text());check('Twelve editable P95 comparison boxes',len(boxes)==12)
    check('Nonnegative boxplot axis with space below zero and separate unit',all(b['axis_min']==0 and b['axis_offset_below_zero_px']==20 and b['plot_bounds']['y']-b['y_unit_top']>=58 for b in boxes))
    root=E.fromstring(z.read('ppt/slides/slide1.xml'));rects=[]
    for sp in root.xpath('//p:sp',namespaces=N):
        if not sp.xpath('./p:spPr/a:prstGeom[@prst="rect"]',namespaces=N):continue
        off=sp.find('p:spPr/a:xfrm/a:off',N);ext=sp.find('p:spPr/a:xfrm/a:ext',N)
        if off is not None and ext is not None:rects.append([int(off.get('x'))/9525,int(off.get('y'))/9525,int(ext.get('cx'))/9525,int(ext.get('cy'))/9525])
    adv=json.loads((A/'Estatistica_avancada.json').read_text())
    def quant(v,q):
        a=sorted(v);t=(len(a)-1)*q;i=int(t);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(t-i)
    for b in boxes:
        series=next(q for q in adv['poster_distributions'][b['unit']] if q['model']==b['model'] and q['distance_min']==b['distance_min']);check('Box quartiles '+b['unit']+b['model']+str(b['distance_min']),all(abs(x-y)<1e-9 for x,y in [(b['q1'],quant(series['values'],.25)),(b['median'],quant(series['values'],.5)),(b['q3'],quant(series['values'],.75))]))
        pb=b['plot_bounds'];band=0 if b['distance_min']==0 else 1 if b['distance_min']==100 else 2;cx=pb['x']+(band+.5)*pb['w']/3+(-48 if b['model']=='AERMOD' else 48);expected=[cx-35,pb['y']+pb['h']-b['q3']/b['axis_max']*pb['h'],70,max(.01,(b['q3']-b['q1'])/b['axis_max']*pb['h'])];check('Native editable IQR geometry '+b['unit']+b['model']+str(b['distance_min']),any(all(abs(x-y)<.02 for x,y in zip(actual,expected)) for actual in rects))
    profile=json.loads((F/'Perfis_editaveis_dados.json').read_text(encoding='utf8'));names=root.xpath('//p:cNvPr/@name',namespaces=N)
    check('Twelve editable profile ribbons and curves retained',sum(n.startswith(('perfil_faixa_','perfil_mediana_','perfil_zoom_')) for n in names)==12)
    for u in profile:
        raw=[p for p in stats if p['unit']==u['unit'] and float(p['distance_m'])<1800]
        check(u['unit']+' profile conserves full paired sample',sum(b['n'] for b in u['bins'])==u['n']==len(raw) and u['axis_min']==0 and u['axis_max']==80)
        for b in u['bins']:
            selected=[p for p in raw if b['low_m']<=float(p['distance_m'])<b['high_m']]
            check(u['unit']+' profile band '+str(b['index'])+' sample and quartiles',len(selected)==b['n'] and all(abs(b[model][stat]-quant([float(p[model+'_P95']) for p in selected],q))<1e-9 for model in ['AERMOD','CALPUFF'] for stat,q in [('q1',.25),('median',.5),('q3',.75)]))
    import hashlib
    hashes={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('ppt/media/') and n.endswith('.png')}
    for logo in ['logo_copasa.png','logo_cretes.png','logo_smarh_novo.png']:check('Supplied logo unchanged '+logo,hashlib.sha256((R/'codigo/recursos_poster/assets'/logo).read_bytes()).hexdigest() in hashes)
    for name in z.namelist():
        if name.startswith('ppt/media/') and name.endswith('.png'):
            im=Image.open(io.BytesIO(z.read(name)));im.load();check(name+' valid image fallback',im.width>1 and im.height>1)
pdf=PdfReader(O/'Poster_CMAS_Session05_WWTP.pdf');check('Native PDF one page 120 x 90 cm',len(pdf.pages)==1 and abs(float(pdf.pages[0].mediabox.width)/72*2.54-120)<.1 and abs(float(pdf.pages[0].mediabox.height)/72*2.54-90)<.1)
report=PdfReader(A/'Comparacao_AERMOD_CALPUFF.pdf');check('Complete interpretation report',len(report.pages)>=8)
check('Generated chart-data folders removed',not list(R.glob('.chart-data-*')))
scatter=json.loads((F/'Concordancia_P95_receptores.json').read_text())
check('Companion scatter retains full range and full statistical sample',len(scatter['units'])==2 and all(r['stats_all_receptors'] and r['n_in_full_range']==r['n'] and r['n_visible_main']<=r['n'] for r in scatter['units']) and [r['n'] for r in scatter['units']]==[562,556])
result=dict(passed=True,checks=checks,publication='New CMAS run supplied 10 November 2026',native_powerpoint_pdf_export=True,annual_data_status='Actual hourly-derived annual fields',annual_coverage_CALPUFF={'2024':100,'2025':99.68036529680366},limitations=['Different source heights and initial spread at WWTP 2','Native 24h block alignment differs','Original meteorological clock convention requires confirmation','No ambient-observation validation performed'])
(R/'output/auditoria/Validacao_Poster_Anual.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(dict(passed=True,checks=len(checks),report_pages=len(report.pages))))
