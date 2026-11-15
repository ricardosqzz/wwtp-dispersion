# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/comparacao_modelos/Estatistica_horaria_por_receptor.csv | pd.read_csv.
# Campos/chaves em data: distance_m, unit.
# Campos/chaves em near: AERMOD_P95, CALPUFF_P95, P95_within_factor_2, WWTP, distance_m, receptor_id, unit, x, y.
# Campos/chaves em r: distance_max_m, distance_min_m.
# Saída: E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json | .write_text.
# Saída: E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.csv | .to_csv.
# Saída: E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv | .to_csv.
# Campos/chaves gerados em near: P95_within_factor_2.
# receptor_id: identificador do receptor.
# CÓDIGO DO PROCESSAMENTO

"""Concordância espacial descritiva dos P95, sem validar contra observações."""
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
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

O=Path(_cp_texto('output/comparacao_modelos', 'posix'))

# Main
def main():
    data=pd.read_csv(O/'Estatistica_horaria_por_receptor.csv')
    results=[];pairs=[];sensitivity=[]
    for unit in ['VM','NC']:
        near=data[data.unit.eq(unit)&data.distance_m.lt(1800)].copy()
        for lo,hi in [(0,1800),(0,100),(100,500),(500,1800)]:
            s=near[near.distance_m.ge(lo)&near.distance_m.lt(hi)]
            a=s.AERMOD_P95.to_numpy();b=s.CALPUFF_P95.to_numpy()
            assert np.isfinite(a).all() and np.isfinite(b).all() and (a>=0).all() and (b>=0).all()

            within=(b>=.5*a)&(b<=2*a)
            rho=float(spearmanr(a,b).statistic) if len(s)>1 and np.ptp(a)>0 and np.ptp(b)>0 else None
            results.append(dict(unit=unit,WWTP=1 if unit=='VM' else 2,distance_min_m=lo,distance_max_m=hi,n=len(s),within_factor_2_count=int(within.sum()),within_factor_2_percent=float(100*within.mean()),Spearman_rho_P95=rho,both_zero=int(((a==0)&(b==0)).sum()),one_zero=int(((a==0)^(b==0)).sum())))
        near['P95_within_factor_2']=(near.CALPUFF_P95>=.5*near.AERMOD_P95)&(near.CALPUFF_P95<=2*near.AERMOD_P95)
        selected=near[(near.AERMOD_P95>=.7)|(near.CALPUFF_P95>=.7)]
        sensitivity.append(dict(unit=unit,n=len(selected),selection='At least one model P95 >= 0.7 ug/m3',within_factor_2_percent=float(100*selected.P95_within_factor_2.mean()),Spearman_rho_P95=float(spearmanr(selected.AERMOD_P95,selected.CALPUFF_P95).statistic)))
        pairs.append(near[['unit','WWTP','receptor_id','x','y','distance_m','AERMOD_P95','CALPUFF_P95','P95_within_factor_2']])
    payload=dict(reference_year=2024,metric='Spatial agreement of model-native hourly P95 at unique coincident receptors',scope='All unique coincident receptors within 1800 m; no low-concentration filtering',factor_2_definition='0.5*AERMOD_P95 <= CALPUFF_P95 <= 2*AERMOD_P95',zero_policy='Both zero agree; exactly one zero disagrees',inference='Descriptive, no spatially independent p values or pass/fail acceptance criterion; neither model is an observation',rows=results,sensitivity_P95_ge_0_7=sensitivity,sources=['https://www.cerc.co.uk/environmental-software/assets/data/doc_userguides/Model_Evaluation_Toolkit_User_Guide.pdf','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html'])
    (O/'Concordancia_espacial_P95.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf8')
    pd.DataFrame(results).to_csv(O/'Concordancia_espacial_P95.csv',index=False,encoding='utf-8-sig')
    pd.concat(pairs).to_csv(O/'Pares_concordancia_P95.csv',index=False,encoding='utf-8-sig')
    from grafico_concordancia_p95 import main as render_scatter
    render_scatter()
    from perfis_comparacao_modelos import main as render_profiles
    render_profiles()
    print(json.dumps([r for r in results if r['distance_max_m']==1800 and r['distance_min_m']==0],indent=2))
    return payload

if __name__=='__main__':main()
