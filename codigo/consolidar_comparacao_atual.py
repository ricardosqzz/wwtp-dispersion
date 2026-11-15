# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json | p.read_text.
# Entrada: E:/copasa_map/output/comparacao_modelos/CALPUFF_horario_validado.json | .read_text.
# Entrada: {path} | path.read_bytes.
# Saída: E:/copasa_map/output/comparacao_modelos/Comparacao_consolidada.json | p.write_text.
# Saída: E:/copasa_map/descontinuado/2026_11_10_novos_resultados/manifesto_nova_rodada.json | .write_text.
# CÓDIGO DO PROCESSAMENTO

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
import json,csv,hashlib,shutil
R=Path(_cp_texto('', 'posix'));O=R/'output/comparacao_modelos';A=R/'descontinuado/2026_11_10_novos_resultados'
p=O/'Comparacao_consolidada.json';d=json.loads(p.read_text(encoding='utf8'));cal=json.loads((O/'CALPUFF_horario_validado.json').read_text(encoding='utf8'))
d.update(quality_CALPUFF=cal,annual_CALPUFF_status='Derived from current hourly CONC, highest calendar-year mean at each receptor. 2024 complete; 2025 99.680365% available. No 8760h RANK substitution.',hourly_CALPUFF_status='Decoded current CONC files and reproduced native RANK fields within printed precision. Embedded input matches supplied INP. Normal end confirmed in current LST.',AERMET_time_zone='LOCATION 0 is a time adjustment, not proof of UTC. Supplied SAMSON header declares zone 0; original interval/clock convention needs confirmation against CALMET UTC-3. Each model is conditioned on its own executed meteorology. One-hour label offset is documented as a diagnostic, not imposed.',publication='Current poster and gallery use CMAS/AERMOD and CMAS/CALPUFF new outputs supplied on 10 November 2026')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
manifest=[]
for stem in ['Comparacao_24h_pre_harmonizacao','Comparacao_anual_8760h_pre_harmonizacao','Cenarios_24h_eventos_coerentes']:
    for path in (R/'output/cmas_poster/figuras').glob(stem+'*'):
        if not path.is_file():continue
        target=A/'figuras_historicas'/path.name;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():continue
        manifest.append(dict(source=str(path),archived=str(target),reason='Historical output superseded by current CMAS model run',sha256=hashlib.sha256(path.read_bytes()).hexdigest()));shutil.move(str(path),str(target))
for name in ['Resultados_historicos.json','Validacao_Poster_Anual.json']:
    path=R/('output/cmas_poster/figuras/'+name if name.startswith('Resultados') else 'output/auditoria/'+name)
    if path.exists():
        target=A/path.name
        if not target.exists():shutil.move(str(path),str(target));manifest.append(dict(source=str(path),archived=str(target),reason='Superseded generated status, not current analysis'))
(A/'manifesto_nova_rodada.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Current analysis consolidated; obsolete generated outputs archived:',len(manifest))
