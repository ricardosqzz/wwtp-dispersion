# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/mod/AERMOD/H2S/H2S_TOTAL.ADI | src.read_bytes.
# Campos/chaves em audit: source_sha256.
# Saída: E:/copasa_map/output/entradas_corrigidas/correcao_postfile/H2S_TOTAL_POSTFILE_corrigido.ADI | target.write_bytes.
# Saída: E:/copasa_map/output/entradas_corrigidas/correcao_postfile/Bloco_OU_corrigido.txt | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/correcao_postfile/Verificacao_POSTFILE.json | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/correcao_postfile/Alteracoes.diff | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/correcao_postfile/LEIA_PRIMEIRO.md | .write_text.
# CÓDIGO DO PROCESSAMENTO

"""Corrige somente o conflito POSTFILE de animação, preservando a entrada recebida."""
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
from collections import Counter
import json,hashlib,difflib
R=Path(_cp_texto('', 'posix'));src=R/'mod/AERMOD/H2S/H2S_TOTAL.ADI';out=R/'output/entradas_corrigidas/correcao_postfile';out.mkdir(parents=True,exist_ok=True)
raw=src.read_bytes();text=raw.decode('cp1252');lines=text.splitlines(keepends=True)
# Post
def post(line):
    q=line.upper().split()
    if q and q[0]=='OU':q=q[1:]
    return q if len(q)>=5 and q[0]=='POSTFILE' else None
posts=[(i+1,post(line)) for i,line in enumerate(lines) if post(line)]
plot_keys={(q[1],q[2]) for n,q in posts if q[3]=='PLOT'}
remove={n for n,q in posts if q[3]=='UNFORM' and (q[1],q[2]) in plot_keys}
assert remove=={126,127,128},sorted(remove)
fixed=''.join(line for i,line in enumerate(lines,1) if i not in remove and '1-Hour Binary POSTFILE(s) for the Plume Animation' not in line)
remaining=[post(line) for line in fixed.splitlines() if post(line)]
keys=[(q[1],q[2]) for q in remaining]
assert len(keys)==len(set(keys))==9
before_ou=text.split('OU STARTING')[0];after_ou=fixed.split('OU STARTING')[0]
assert before_ou==after_ou
assert fixed.split('OU FINISHED',1)[1]==text.split('OU FINISHED',1)[1]
assert [l for l in lines if l.strip().startswith('PLOTFILE')]==[l for l in fixed.splitlines(keepends=True) if l.strip().startswith('PLOTFILE')]
target=out/'H2S_TOTAL_POSTFILE_corrigido.ADI';target.write_bytes(fixed.encode('cp1252'))
ou=fixed.split('OU STARTING',1)[1].split('OU FINISHED',1)[0]
(out/'Bloco_OU_corrigido.txt').write_text('OU STARTING'+ou+'OU FINISHED\n',encoding='ascii')
audit=dict(source=str(src),corrected=str(target),source_sha256=hashlib.sha256(raw).hexdigest(),removed_postfile_lines=sorted(remove),remaining_postfiles=len(keys),duplicate_period_group_pairs=0,source_receptor_meteorology_unchanged=True,plotfile_requests_unchanged=True,native_model_execution=False,reason='1h PLOT plus 1h UNFORM for the same ALL/WWTP2/WWTP1 pairs; the latter are generated for Plume Animation',references=['https://www.weblakes.com/Newsletter/2025/Dec2025.html','https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_userguide.pdf'])
(out/'Verificacao_POSTFILE.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
(out/'Alteracoes.diff').write_text(''.join(difflib.unified_diff(text.splitlines(keepends=True),fixed.splitlines(keepends=True),fromfile='H2S_TOTAL.ADI',tofile=target.name)),encoding='utf8')
(out/'LEIA_PRIMEIRO.md').write_text(_cp_adaptar('''# Correção E211 POSTFILE

O arquivo original foi preservado. A cópia corrigida retira somente as três linhas de POSTFILE 1h UNFORM criadas para Plume Animation, que repetem os pares 1h/ALL, 1h/WWTP2 e 1h/WWTP1 já solicitados como PLOT. O comentário do bloco de animação foi retirado. Permanecem nove POSTFILE PLOT, para 1h, 24h e anual dos três grupos, e todos os PLOTFILE existentes. Fontes, taxas, receptores, meteorologia e demais parâmetros permanecem iguais.

## Correção permanente no AERMOD View

Em Output Pathway > Lakes Tools > Plume Animation, desativar a geração dos POSTFILE de animação para ALL, WWTP1 e WWTP2. Manter as séries horárias já configuradas em Post-Processing Files. Gerar a entrada novamente e conferir que há somente um POSTFILE por combinação de período e grupo. PLOTFILE é outra opção e deve ser mantido.

## Execução pelo Batcher

H2S_TOTAL_POSTFILE_corrigido.ADI conserva os caminhos relativos originais. Antes de executar, copiar a cópia corrigida para E:/copasa_map/mod/AERMOD/H2S e selecioná-la no Batcher, mantendo essa pasta como diretório de execução. Não é necessário sobrescrever o ADI original. O ROU, os arquivos meteorológicos e a pasta de saída H2S_TOTAL.AD devem continuar acessíveis pelos caminhos originais. Se o View recriar o ADI, é preciso desativar a opção na interface; editar somente o texto gerado não persiste a configuração do projeto.

E901 indica a interrupção dos processos MPI em consequência do erro de configuração. Este E211 não é uma colisão FUNIT. Trocar nomes de arquivo ou unidades Fortran não remove o par período/grupo repetido. O ADO é saída de diagnóstico e não deve ser editado para corrigir a entrada.

A verificação da cópia foi textual/estrutural, sem nova execução do modelo. Esta correção se limita ao erro E211 e não confirma que os demais parâmetros desta entrada estejam harmonizados com a auditoria anterior.
'''),encoding='utf8')
assert hashlib.sha256(src.read_bytes()).hexdigest()==audit['source_sha256']
print(json.dumps(audit))
