# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {p} | p.read_text.
# Entrada: E:/copasa_map/in/CONC-{k}.DAT | p.open.
# Entrada: E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json | manifest.read_text.
# Campos/chaves em mm: average, c, code, lead, tail.
# Campos/chaves em d: comparison_passed, csv, hourly_source, max_abs_error.
# Campos/chaves em chosen: offset.
# Campos/chaves em old: events.
# Saída: E:/copasa_map/output/cmas_poster/dados_cenarios24h/CALPUFF_{k}_auditoria_janelas.json | .write_text.
# Saída: E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json | manifest.write_text.
# CÓDIGO DO PROCESSAMENTO

"""Campos simultâneos de 24 h, extraídos de saídas horárias já executadas.

Nenhuma simulação, ajuste de emissão ou interpolação espacial neste módulo.
"""
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
import datetime as dt,json,struct,csv
import numpy as np
R=Path(_cp_texto('', 'posix'));O=R/'output/cmas_poster/dados_cenarios24h';O.mkdir(parents=True,exist_ok=True)
# Table
def table(p,km=False):
    rows=[];codes=[]
    for l in p.read_text(encoding='cp1252').splitlines():
        q=l.split()
        if len(q)<3 or l.startswith('*'):continue
        try:x,y,c=map(float,q[:3])
        except ValueError:continue
        rows.append([x*1000 if km else x,y*1000 if km else y,c]);codes.append(q[-1])
    return np.array(rows),codes
# Identity
def identity(p):return dict(path=str(p),bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns)
# Write
def write(model,k,xy,values,meta):
    path=O/f'{model}_{k}_evento24h.csv'
    np.savetxt(path,np.column_stack([xy,values]),delimiter=',',header='X,Y,CONC',comments='',fmt=['%.8f','%.8f','%.12g'])
    meta.update(csv=str(path),model=model,unit=k,aliases='WWTP 1' if k=='VM' else 'WWTP 2',receptors=len(values),maximum=float(values.max()),minimum=float(values.min()),simultaneous=True,emission_corrections_applied=False)
    return meta
# Aermod
def aermod(k,sg,pl):
    native,codes=table(R/'CMAS'/pl);n=len(native);j=int(native[:,2].argmax());day=int(codes[j])//100
    p=R/f'in/AERMOD/H2S/H2S_TOTAL.AD/1HG{sg}UN_PA.POS'
    dtype=np.dtype([('lead','<i4'),('code','<i4'),('average','<i4'),('group','S8'),('c','<f8',(n,)),('tail','<i4')]);assert p.stat().st_size%dtype.itemsize==0
    mm=np.memmap(p,dtype=dtype,mode='r');select=np.flatnonzero(mm['code']//100==day)
    assert len(select)==24 and np.array_equal(mm['code'][select]%100,np.arange(1,25))
    assert np.all(mm['lead'][select]==16+8*n) and np.all(mm['tail'][select]==16+8*n)
    assert np.all(mm['average'][select]==1)
    field=mm['c'][select].mean(axis=0);err=float(abs(field[j]-native[j,2]));assert err<1e-5,(k,err)
    same_date=np.array([int(c)//100==day for c in codes]);same_date_error=float(np.max(abs(field[same_date]-native[same_date,2])))
    assert same_date_error<1e-5,(k,same_date_error)
    date=dt.datetime.strptime(str(day),'%y%m%d')
    return write('AERMOD',k,native[:,:2],field,dict(period_start=date.isoformat(),period_end=(date+dt.timedelta(days=1)).isoformat(),hours=24,selection='Date of the highest native 1ST HIGH 24h receptor value; all receptors on the same day',native_rank_file=str(R/'CMAS'/pl),native_rank_peak=float(native[j,2]),peak_reproduction_error=err,same_date_peak_receptors=int(same_date.sum()),same_date_peak_max_error=same_date_error,hourly_source=identity(p),timezone='as executed by AERMET; preprocessor convention to confirm'))
# Unpack record
def unpack_record(f):
    a=f.read(4)
    if not a:return None
    n=struct.unpack('<i',a)[0];assert 0<=n<10000000
    b=f.read(n);end=f.read(4);assert len(b)==n and len(end)==4 and struct.unpack('<i',end)[0]==n
    return b
# Decode
def decode(b):
    assert b[:4]==b'ODOR';z=np.frombuffer(b[15:],dtype='<f4');neg=z<0
    counts=np.where(neg,-np.trunc(z),1).astype(int);indices=np.cumsum(counts)-counts
    values=np.zeros(counts.sum(),dtype='float64');values[indices[~neg]]=z[~neg]
    return values*1e6
# Stamp
def stamp(values):
    year,day,hour,second=map(int,values)
    return dt.datetime(year,1,1)+dt.timedelta(days=day-1,hours=hour,seconds=second)
# Calpuff
def calpuff(k,suffix):
    p=R/f'in/CONC-{k}.DAT';native,_=table(R/f'CMAS/RANK(ALL)_ODOR_24HR_CONC_C_{suffix}.DAT',True)
    first=next((R/f'calpuff_horario/{k.lower()}').glob('2023_M12_D31_2300*'));coord,_=table(first,True);assert len(coord)==len(native) and np.allclose(coord[:,:2],native[:,:2],atol=.001)
    acc=[np.zeros(len(native)),np.zeros(len(native))];days=[[],[]];periods=[[],[]];starts=[None,None]
    with p.open('rb') as f:
        assert unpack_record(f).startswith(b'CONC.DAT');nlines=struct.unpack('<i',unpack_record(f))[0]
        for _ in range(nlines):unpack_record(f)
        for _ in range(5):unpack_record(f)
        count=0;previous_end=None
        while True:
            b=unpack_record(f)
            if b is None:break
            assert len(b)==32;btime=struct.unpack('<8i',b);start,end=stamp(btime[:4]),stamp(btime[4:]);assert end-start==dt.timedelta(hours=1)
            assert previous_end is None or start==previous_end
            previous_end=end
            meta=unpack_record(f);assert meta[8:13]==b'TOTAL'
            chunks=[]
            for _ in range(2):
                pack=struct.unpack('<i',unpack_record(f))[0];b=unpack_record(f);assert (len(b)-15)//4==pack;chunks.append(decode(b))
            c=np.concatenate(chunks);assert len(c)==len(native) and np.isfinite(c).all() and (c>=0).all()
            for offset in [0,1]:
                if count<offset:continue
                j=(count-offset)%24
                if j==0:starts[offset]=start
                acc[offset]+=c
                if j==23:
                    days[offset].append(acc[offset]/24);periods[offset].append((starts[offset],end));acc[offset]=np.zeros(len(native))
            count+=1
    assert count==17517
    candidates=[]
    for offset in [0,1]:
        a=np.asarray(days[offset]);env=a.max(axis=0);error=float(np.max(abs(env-native[:,2])));relative=float(np.max(abs(env-native[:,2])/np.maximum(native[:,2],1e-6)))
        passed=bool(np.allclose(env,native[:,2],rtol=1e-4,atol=1e-6));candidates.append(dict(offset=offset,comparison_passed=passed,max_abs_error=error,max_relative_error=relative))
    choices=[d for d in candidates if d['comparison_passed']]
    if not choices:
        (O/f'CALPUFF_{k}_auditoria_janelas.json').write_text(json.dumps(candidates,indent=2),encoding='utf8');raise ValueError((k,'24h averaging windows do not reproduce native CALPOST ranking',candidates))
    chosen=min(choices,key=lambda d:d['max_abs_error']);offset=chosen['offset'];a=np.asarray(days[offset]);i,j=np.unravel_index(a.argmax(),a.shape);start,end=periods[offset][i]
    assert end-start==dt.timedelta(hours=24)
    return write('CALPUFF',k,native[:,:2],a[i],dict(period_start=start.isoformat(),period_end=end.isoformat(),hours=24,selection='Complete 24h averaging block with the highest receptor concentration; matched to native CALPOST RANK',native_rank_peak=float(native[:,2].max()),native_envelope_validation=candidates,selected_offset=offset,hourly_source=identity(p),timezone='UTC-03:00, as recorded in the model',decoded_records=count))
# Main
def main():
    manifest=O/'Cenarios24h_manifesto.json'
    if manifest.exists():
        old=json.loads(manifest.read_text(encoding='utf8'))
        if old.get('extraction_version')==2 and all(identity(Path(d['hourly_source']['path']))==d['hourly_source'] and Path(d['csv']).exists() for d in old['events']):print('Event cache current');return
    events=[]
    for k,sg,pl,suffix in [('VM','V-Maria','24H1G001_V-MARIA.PLT','V-MARIA'),('NC','N-Cont','24H1G002_N-CONT.PLT','N-CONT')]:
        events.append(aermod(k,sg,pl));print('AERMOD',k,events[-1]['period_start'],events[-1]['maximum'],flush=True)
        events.append(calpuff(k,suffix));print('CALPUFF',k,events[-1]['period_start'],events[-1]['maximum'],flush=True)
    manifest.write_text(json.dumps(dict(events=events,simulation_run=False,interpolation_used=False,extraction_version=2),indent=2),encoding='utf8')
    print(json.dumps(events))
if __name__=='__main__':main()
