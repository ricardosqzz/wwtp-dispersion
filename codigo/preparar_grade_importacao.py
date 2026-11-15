# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/auditoria/Auditoria_consolidada.json | .read_text.
# Entrada: E:/copasa_map/output/auditoria/Grade_base_1789.json | bp.read_text.
# Entrada: E:/copasa_map/mod/AERMOD/receptors_part.csv | src.open.
# Entrada: E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_NC_VM_CALPUFF_17b.txt | .read_text.
# Entrada: {p} | p.read_text.
# Entrada: E:/copasa_map/mod/AERMOD/receptors_part.csv | src.read_bytes.
# Campos/chaves em d: grid, grid_revision.
# Campos/chaves em row: ID, SENSITIVE.
# Campos/chaves em q: elev, group, hill, id, joint_id, origin, sensitive, x, y.
# Campos/chaves em v: distance_m.
# Saída: E:/copasa_map/output/auditoria/Grade_base_1789.json | bp.write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/AERMOD/Grade_Receptora_{unit}_AERMOD.csv | .open.
# Saída: E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_{unit}.ROU | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_{unit}_CALPUFF_17b.txt | .write_text.
# Saída: {p} | p.write_text.
# Saída: E:/copasa_map/output/auditoria/Auditoria_consolidada.json | .write_text.
# Saída: E:/copasa_map/output/auditoria/Grades_por_unidade.json | .write_text.
# Saída: E:/copasa_map/output/auditoria/Correspondencia_Receptores_Grades.csv | .open.
# Saída: E:/copasa_map/output/auditoria/Grade_importacao_validada.json | .write_text.
# Campos/chaves gerados em row: receptor_id.
# Campos/chaves gerados em q: id, joint_id, receptor_id.
# Campos/chaves gerados em sets: NC_VM.
# Campos/chaves gerados em d: grid, grid_count, grid_revision, grid_unique_locations.
# Campos/chaves gerados em audit: sets.
# receptor_id: identificador do receptor.
# CÓDIGO DO PROCESSAMENTO

"""Preserva receptores sensíveis e gera a mesma sequência nativa nos dois modelos."""
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
import csv,json,math,re,hashlib
R=Path(_cp_texto('', 'posix'));O=R/'output/entradas_corrigidas';A=R/'output/auditoria'
src=R/'mod/AERMOD/receptors_part.csv'
d=json.loads((A/'Auditoria_consolidada.json').read_text(encoding='utf8'))
base=[v for v in d['grid'] if not v.get('sensitive')]

bp=A/'Grade_base_1789.json'
if bp.exists():base=json.loads(bp.read_text(encoding='utf8'))
else:bp.write_text(json.dumps(d['grid'],indent=2),encoding='utf8');base=d['grid']
assert len(base)==1789
with src.open(encoding='utf-8-sig',newline='') as f:
    original=[{k.strip():v.strip() for k,v in row.items()} for row in csv.DictReader(f,delimiter=';')]
# Number
def number(s):return float(s.replace(',','.'))
matched=set();rows=[];matches=[]
for row in original:
    q={k.lower():number(row[k]) for k in ['X','Y','ELEV','HILL']}
    q.update(id=row['ID'],group='MONITOR',sensitive=int(row['SENSITIVE']),origin='receptors_part.csv')
    idx=min(range(len(base)),key=lambda i:math.hypot(base[i]['x']-q['x'],base[i]['y']-q['y']))
    dist=math.hypot(base[idx]['x']-q['x'],base[idx]['y']-q['y'])
    assert dist<.01,(q['id'],dist)
    assert q['elev']==base[idx]['elev'] and q['hill']==base[idx]['hill']
    assert q['hill']>=q['elev']
    matches.append(dict(id=q['id'],base_index=idx+1,distance_m=dist))
    matched.add(idx);rows.append(q)
regular_index=0
for i,q in enumerate(base):
    if i in matched:continue
    regular_index+=1
    rows.append(dict(x=q['x'],y=q['y'],elev=q['elev'],hill=q['hill'],id=f'R{regular_index:04d}',group='GRADE',sensitive=0,origin=q['origin']))
for i,row in enumerate(rows):row['receptor_id']=i+1
assert len(original)==40 and len(matched)==39 and len(rows)==1790
coords={}
for q in rows:coords.setdefault((q['x'],q['y']),[]).append(q['id'])
duplicates=[dict(x=k[0],y=k[1],ids=v) for k,v in coords.items() if len(v)>1]
assert len(coords)==1789 and len(duplicates)==1 and set(duplicates[0]['ids'])=={'NC_6','NC_BAG'}

centres={'NC':(589190,7805680),'VM':(614080,7834430)}
sets={}
for unit,centre in centres.items():
    selected=[dict(q) for q in rows if (q['sensitive'] and q['id'].startswith(unit+'_')) or (not q['sensitive'] and (q['origin']=='UCART4' or math.hypot(q['x']-centre[0],q['y']-centre[1])<=1800))]
    counter=0
    for i,q in enumerate(selected):
        q['joint_id']=q['id'];q['receptor_id']=i+1
        if not q['sensitive']:counter+=1;q['id']=f'R{counter:04d}'
    sets[unit]=selected
sets['NC_VM']=[dict(q,joint_id=q['id']) for q in rows]
joint_coords={(q['x'],q['y']) for q in rows}
assert {(q['x'],q['y']) for unit in ['NC','VM'] for q in sets[unit]}==joint_coords

# Dec
def dec(v):return f'{v:.8f}'.rstrip('0').rstrip('.').replace('.',',')
(O/'AERMOD').mkdir(parents=True,exist_ok=True)
for unit,selected in sets.items():
    stem='Grade_Receptora_'+unit
    with (O/'AERMOD'/(stem+'_AERMOD.csv')).open('w',encoding='ascii',newline='') as f:
        w=csv.writer(f,delimiter=',');w.writerow(['X','Y','ELEV','HILL','FLAG','GROUP','ID','SENSITIVE'])
        for q in selected:w.writerow([f"{q['x']:.8f}".rstrip('0').rstrip('.'),f"{q['y']:.8f}".rstrip('0').rstrip('.'),q['elev'],q['hill'],0,q['group'],q['id'],q['sensitive']])
    (O/(stem+'.ROU')).write_text('RE ELEVUNIT METERS\n'+''.join(f" DISCCART {q['x']:.8f} {q['y']:.8f} {q['elev']:.3f} {q['hill']:.3f}\n" for q in selected),encoding='ascii')
    native=''.join(f" {i+1} ! X = {q['x']/1000:.11f}, {q['y']/1000:.11f}, {q['elev']:.3f}, 0.0 ! !END!\n" for i,q in enumerate(selected))
    (O/(stem+'_CALPUFF_17b.txt')).write_text(native,encoding='ascii')
native=(O/'Grade_Receptora_NC_VM_CALPUFF_17b.txt').read_text(encoding='ascii')
patched=[]
for p in sorted(O.glob('CALPUFF-*_corrigido.INP')):
    t=p.read_text(encoding='cp1252');at=t.index('Subgroup (17b)');head,tail=t[:at],t[at:]
    m=re.search(r'(?m)^\s*1\s*!\s*X\s*=',tail);assert m
    end=tail.rindex('!END!')+len('!END!')
    new=head+tail[:m.start()]+native+tail[end:]
    new=re.sub(r'(!\s*NREC\s*=\s*)\d+',lambda m:m[1]+str(len(rows)),new)
    assert len(re.findall(r'(?m)^\s*\d+\s*!\s*X\s*=',new[new.index('Subgroup (17b)'):]))==len(rows)

    before=re.sub(r'(!\s*NREC\s*=\s*)\d+',r'\g<1>N',head)
    after=re.sub(r'(!\s*NREC\s*=\s*)\d+',r'\g<1>N',new[:new.index('Subgroup (17b)')])
    assert before==after
    p.write_text(new,encoding='cp1252');patched.append(p.name)
for p in O.glob('H2S_*_corrigido.ADI'):
    t=p.read_text(encoding='ascii').replace('INCLUDED Grade_Receptora_Comum.ROU','INCLUDED Grade_Receptora_NC_VM.ROU')
    assert 'INCLUDED Grade_Receptora_NC_VM.ROU' in t
    p.write_text(t,encoding='ascii')
d['grid']=rows;d['grid_count']=len(rows);d['grid_unique_locations']=len(coords)
d['grid_revision']=dict(source=str(src),sensitive_records=40,unique_sensitive_locations=39,original_duplicate=duplicates,order='Monitoring IDs preserved first; regular grid uses R0001 onward, restarted within each file',unit_selection='Original UCART4 regional network in each unit, plus existing detailed receptors within 1800 m of original reference centres',reference_centres=centres,new_terrain_points=0)
(A/'Auditoria_consolidada.json').write_text(json.dumps(d,indent=2),encoding='utf8')
counts={unit:dict(total=len(selected),monitoring=sum(q['sensitive'] for q in selected),grid=sum(not q['sensitive'] for q in selected),unique_positions=len({(q['x'],q['y']) for q in selected})) for unit,selected in sets.items()}
(A/'Grades_por_unidade.json').write_text(json.dumps(dict(counts=counts,grids=sets,method=d['grid_revision']),indent=2),encoding='utf8')
with (A/'Correspondencia_Receptores_Grades.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['GRADE','INDICE_MODELO','ID','ID_NC_VM','X_m','Y_m','TIPO'])
    for unit,selected in sets.items():
        for i,q in enumerate(selected,1):w.writerow([unit,i,q['id'],q['joint_id'],dec(q['x']),dec(q['y']),q['group']])
audit=dict(records=len(rows),unique_locations=len(coords),sensitive_records=40,regular_records=len(rows)-40,duplicates=duplicates,matches=matches,maximum_matching_distance_m=max(v['distance_m'] for v in matches),crs='WGS 84 / UTM zone 23S (EPSG:32723)',calpuff_units='X/Y km; ground elevation m; receptor height above ground 0 m',files_patched=patched,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source_inputs_changed=False)
audit['sets']=counts
(A/'Grade_importacao_validada.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in audit.items() if k!='matches'}))
