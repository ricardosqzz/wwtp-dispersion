# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {C}/CALPUFF_{unit}_1h.json | meta.read_text.
# Entrada: {C}/CALPUFF_{unit}_1h.npy | np.load.
# Entrada: E:/copasa_map/CMAS/CALPUFF/RANK({unit})_ODOR_1HR_CONC_C.DAT | np.loadtxt.
# Entrada: E:/copasa_map/CMAS/CALPUFF/CONC-{unit}.DAT | path.open.
# Entrada: {O}/Campos_nativos.npz | np.load.
# Entrada: E:/copasa_map/CMAS/CALPUFF/RANK({k})_ODOR_{token}HR_CONC_C.DAT | np.loadtxt.
# Campos/chaves em m: embedded_input, end_times, start_times, xy.
# Campos/chaves em v: max_abs_error, passed.
# Saída: {C}/CALPUFF_{k}_24h.npy | np.save.
# CÓDIGO DO PROCESSAMENTO

"""Decodifica CONC.DAT atual e verifica cada campo contra RANK nativo."""
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

from comparar_modelos_cmas import *
from extrair_eventos_24h import unpack_record,decode
# Caltime
def caltime(b):
    y,j,h,s=map(int,b);return dt.datetime(y,1,1)+dt.timedelta(days=j-1,hours=h,seconds=s)
# Extract
def extract(unit):
    path=R/f'CMAS/CALPUFF/CONC-{unit}.DAT';cache=C/f'CALPUFF_{unit}_1h.npy';meta=C/f'CALPUFF_{unit}_1h.json'
    if cache.exists() and meta.exists() and json.loads(meta.read_text())['source']==ident(path):return np.load(cache,mmap_mode='r'),json.loads(meta.read_text())
    rank=np.loadtxt(R/f'CMAS/CALPUFF/RANK({unit})_ODOR_1HR_CONC_C.DAT',skiprows=6);n=len(rank);nt=17517
    arr=np.lib.format.open_memmap(cache,mode='w+',dtype='float32',shape=(nt,n));ends=[];starts=[]
    with path.open('rb') as f:
        assert unpack_record(f).startswith(b'CONC.DAT');nlines=struct.unpack('<i',unpack_record(f))[0]
        embedded=[]
        for _ in range(nlines):embedded.append(unpack_record(f).decode('cp1252').rstrip())
        control=unpack_record(f);title=unpack_record(f);species=unpack_record(f);elevation=unpack_record(f);names=unpack_record(f)
        i=0;previous=None
        while True:
            b=unpack_record(f)
            if b is None:break
            assert len(b)==32;st=struct.unpack('<8i',b);start,end=caltime(st[:4]),caltime(st[4:]);assert end-start==dt.timedelta(hours=1)
            assert previous is None or previous==start;previous=end
            assert unpack_record(f)[8:13]==b'TOTAL';chunks=[]
            for _ in range(2):
                pack=struct.unpack('<i',unpack_record(f))[0];b=unpack_record(f);assert (len(b)-15)//4==pack;chunks.append(decode(b))
            z=np.concatenate(chunks);assert len(z)==n and np.isfinite(z).all() and (z>=0).all();arr[i]=z;starts.append(start.isoformat());ends.append(end.isoformat());i+=1
    assert i==nt;arr.flush();m=dict(source=ident(path),xy=(rank[:,:2]*1000).tolist(),start_times=starts,end_times=ends,hours=i,receptors=n,units='ug/m3',timezone='UTC-03:00, XBTZ=3 in embedded control',embedded_input=embedded)
    dump(meta,m);print('CALPUFF decoded',unit,i,n,flush=True);return np.load(cache,mmap_mode='r'),m
# Main
def main():
    result={};fields=dict(np.load(O/'Campos_nativos.npz'));quality=[];summary=[]
    for k in ['VM','NC']:
        h,m=extract(k);starts=[dt.datetime.fromisoformat(s) for s in m['start_times']];ends=[dt.datetime.fromisoformat(s) for s in m['end_times']];n=h.shape[1];xy=np.array(m['xy']);prefix=f'{k}_CALPUFF'
        rank=lambda token:np.loadtxt(R/f'CMAS/CALPUFF/RANK({k})_ODOR_{token}HR_CONC_C.DAT',skiprows=6)[:,2]
        one=h.max(axis=0);err1=float(np.max(abs(one-rank('1'))));assert np.allclose(one,rank('1'),rtol=6e-5,atol=1e-6),(k,err1)

        choices=[]
        for offset in [0,1]:
            size=(len(h)-offset)//24;d=np.asarray(h[offset:offset+24*size],dtype='float64').reshape(size,24,n).mean(axis=1);env=d.max(axis=0);ref=rank('24')
            er=float(abs(env-ref).max());passed=bool(np.allclose(env,ref,rtol=6e-5,atol=1e-6));choices.append(dict(offset=offset,max_abs_error=er,passed=passed))
        ok=[v for v in choices if v['passed']];assert ok,(k,choices);offset=min(ok,key=lambda v:v['max_abs_error'])['offset'];size=(len(h)-offset)//24
        daily=np.asarray(h[offset:offset+size*24],dtype='float64').reshape(size,24,n).mean(axis=1);dstarts=[starts[offset+i*24] for i in range(size)]
        mean=np.mean(h,axis=0,dtype='float64');ref=rank('17517');ermean=float(abs(mean-ref).max());assert np.allclose(mean,ref,rtol=6e-5,atol=1e-6),(k,ermean)
        yrs=np.array([t.year for t in starts]);annual=[];yrmeta=[]
        for y in [2024,2025]:
            sel=yrs==y;expected=int((dt.datetime(y+1,1,1)-dt.datetime(y,1,1)).total_seconds()/3600);z=np.mean(h[sel],axis=0,dtype='float64');annual.append(z);fields[f'{prefix}_annual_{y}']=z
            yrmeta.append(dict(year=y,hours=int(sel.sum()),calendar_hours=expected,coverage_percent=100*int(sel.sum())/expected,period_first_start=min(t for t in starts if t.year==y).isoformat(),period_last_end=max(e for t,e in zip(starts,ends) if t.year==y).isoformat(),maximum=float(z.max())))
        a=np.asarray(annual);fields[f'{prefix}_annual_calendar_max']=a.max(axis=0)
        np.save(C/f'CALPUFF_{k}_24h.npy',daily);dump(C/f'CALPUFF_{k}_24h.json',dict(start_times=[d.isoformat() for d in dstarts],offset=offset,rank_validation=choices))

        quality.append(dict(unit=k,hours=len(h),receptors=n,start=starts[0].isoformat(),end=ends[-1].isoformat(),rank_1h_max_error=err1,rank_24h=choices,rank_period_mean_max_error=ermean,annual=yrmeta,annual_qualification='2025 is a near-complete calendar-year estimate, not a complete calendar year. No 8760h RANK substituted.',input_identity=ident(R/f'CMAS/CALPUFF/CALPUFF-{k}.INP'),embedded_source_count=int(re.search(r'!\s*NAR1\s*=\s*(\d+)','\n'.join(m['embedded_input']))[1])))
        for y,z in zip([2024,2025],a):summary.append(dict(unit=k,model='CALPUFF',year=y,maximum=float(z.max())))
    np.savez_compressed(O/'Campos_nativos.npz',**fields);dump(O/'CALPUFF_horario_validado.json',quality);csvout(O/'CALPUFF_medias_anuais.csv',summary);print(json.dumps(quality,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
