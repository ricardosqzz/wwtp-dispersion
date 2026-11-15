# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/in/CALMET.DAT | p.open.
# Entrada: E:/copasa_map/temp/cache_nova_modelagem/CALMET_extracao.json | meta.read_text.
# Entrada: E:/copasa_map/temp/cache_nova_modelagem/AERMOD_{unit}_1h.npy | np.load.
# Entrada: E:/copasa_map/CMAS/AERMOD/H2S_TOTAL.ADO | p.read_bytes.
# Entrada: E:/copasa_map/mod/AERMOD/H2S/H2S_TOTAL.ADO | .read_bytes.
# Entrada: E:/copasa_map/mod/AERMOD/H2S/H2S_TOTAL.err | err.read_text.
# Entrada: E:/copasa_map/in/AERMOD/AERMET/AERMET_COP.SFC | path.read_text.
# Entrada: E:/copasa_map/output/comparacao_modelos/Meteorologia_CALMET.csv | cache.open.
# Entrada: E:/copasa_map/output/auditoria/CALMET_DAT_verificado.json | .read_text.
# Entrada: E:/copasa_map/CMAS/CALPUFF/RANK({k})_ODOR_{token}HR_CONC_C.DAT | np.loadtxt.
# Campos/chaves em m: codes, nx, ny, origin_x_m, origin_y_m, source, spacing_m, xy.
# Campos/chaves em mm: c, code, x, y.
# Campos/chaves em v: area, height, ix0, iy0, mass_g_s, max_distance_m, min_distance_m, model, old_flux, params, sigma, type, u, unit, v, x, xy, y.
# Campos/chaves em totals: AERMOD, CALPUFF.
# Campos/chaves em r: code, direction, speed.
# Campos/chaves em hmeta: last_end, start_end.
# Campos/chaves em all_fields: 24h, AERMOD, CALPUFF.
# Campos/chaves em result: elapsed_seconds.
# Saída: {p} | p.write_text.
# Saída: {p} | p.open.
# Campos/chaves gerados em v: direction, speed.
# CÓDIGO DO PROCESSAMENTO

"""Auditoria e comparação descritiva das novas saídas COPASA.

Mantém as grades nativas para estatísticas. Interpolação é somente cartográfica.
Os RANK não são séries temporais e não permitem atribuir máximos à meteorologia.
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
import re,json,csv,struct,datetime as dt,time,sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import spearmanr
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
from auditar_e_preparar import parse_aer,parse_cal

R=Path(_cp_texto('', 'posix'));O=R/'output/comparacao_modelos';C=R/'temp/cache_nova_modelagem'
O.mkdir(parents=True,exist_ok=True);C.mkdir(parents=True,exist_ok=True)
# Dump
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')
# Csvout
def csvout(p,rows):
    if not rows:return
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Ident
def ident(p):return dict(path=str(p),bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns)
# Stamp
def stamp(code):
    code=int(code);h=code%100;return dt.datetime.strptime(str(code//100),'%y%m%d')+dt.timedelta(hours=h)
# Native
def native(p):
    rows=[];codes=[];header=[]
    with p.open(encoding='cp1252') as f:
        for l in f:
            q=l.split()
            if not q or q[0].startswith('*'):header.append(l.rstrip());continue
            rows.append(list(map(float,q[:3])));codes.append(int(q[8]))
    return np.array(rows),np.array(codes),header
# Hourly
def hourly(unit):
    p=R/f'CMAS/AERMOD/01_GWWTP{1 if unit=="VM" else 2}.POS';cache=C/f'AERMOD_{unit}_1h.npy';meta=C/f'AERMOD_{unit}_1h.json'
    if cache.exists() and meta.exists():
        m=json.loads(meta.read_text(encoding='utf8'))
        if m['source']==ident(p):return np.load(cache,mmap_mode='r'),np.array(m['xy']),np.array(m['codes']),m
    with p.open('rb') as f:
        header=[]
        while True:
            pos=f.tell();l=f.readline()
            if not l.startswith(b'*'):break
            header.append(l.decode('cp1252').rstrip())
    n=int(re.search(r'TOTAL OF\s+(\d+) RECEPTORS',' '.join(header))[1]);width=len(l)
    toks=list(re.finditer(rb'\S+',l));assert len(toks)>=9 and toks[6].group()==b'1-HR'
    off=[toks[i].start() for i in [0,1,2,8]];sizes=[toks[i].end()-off[j] for j,i in enumerate([0,1,2,8])]

    fmt=np.dtype({'names':['x','y','c','code'],'formats':['S14','S14','S14','S8'],'offsets':[0,14,28,toks[8].start()],'itemsize':width})
    rows=(p.stat().st_size-pos)//width;assert (p.stat().st_size-pos)%width==0 and rows%n==0
    mm=np.memmap(p,mode='r',offset=pos,dtype=fmt,shape=(rows,));nh=rows//n
    xy=np.column_stack([mm['x'][:n].astype(float),mm['y'][:n].astype(float)]);codes=mm['code'][::n].astype('i8')
    times=[stamp(v) for v in codes];assert all(b-a==dt.timedelta(hours=1) for a,b in zip(times,times[1:]))
    arr=np.lib.format.open_memmap(cache,mode='w+',dtype='float32',shape=(nh,n))
    for i in range(0,nh,96):
        j=min(i+96,nh);ss=slice(i*n,j*n)
        values=mm['c'][ss].astype('float32').reshape(j-i,n)
        assert np.isfinite(values).all() and (values>=0).all()
        cc=mm['code'][ss].astype('i8').reshape(j-i,n);assert np.all(cc==codes[i:j,None])
        assert np.allclose(mm['x'][i*n:(i+1)*n].astype(float),xy[:,0])
        arr[i:j]=values
    arr.flush();del arr,mm
    m=dict(source=ident(p),xy=xy.tolist(),codes=codes.tolist(),hours=nh,receptors=n,row_bytes=width,header_bytes=pos,start_end=times[0].isoformat(),last_end=times[-1].isoformat())
    dump(meta,m);print('AERMOD hourly cached',unit,nh,n,flush=True)
    return np.load(cache,mmap_mode='r'),xy,codes,m

# Met aermet
def met_aermet():
    p=R/'CMAS/AERMOD/H2S_TOTAL.ADO';err=R/'mod/AERMOD/H2S/H2S_TOTAL.err'

    assert p.read_bytes()==(err.parent/'H2S_TOTAL.ADO').read_bytes()
    missing=[];calm=[]
    for l in err.read_text(encoding='cp1252').splitlines():
        if 'I460' in l:missing.append(int(l.split()[-1])%100000000)
        if 'I440' in l:calm.append(int(l.split()[-1])%100000000)
    assert len(missing)==309 and len(calm)==124
    path=R/'in/AERMOD/AERMET/AERMET_COP.SFC';rows=[]
    for l in path.read_text(encoding='cp1252').splitlines()[1:]:
        q=l.split();v=list(map(float,q[:25]));code=int(q[0]+f'{int(q[1]):02}{int(q[2]):02}{int(q[4]):02}')
        rows.append(dict(code=code,time_end=stamp(code).isoformat(),speed=v[15],direction=v[16],wind_height_m=v[17],temperature_K=v[18],L=v[11],mix_convective_m=v[9],mix_mechanical_m=v[10],ustar=v[6],calm=code in calm,missing=code in missing))

    assert rows[0]['speed']==5.66 and rows[0]['direction']==86
    csvout(O/'Meteorologia_AERMET.csv',rows)
    return rows,missing,calm

# Met calmet
def met_calmet():
    cache=O/'Meteorologia_CALMET.csv';meta=C/'CALMET_extracao.json';p=R/'in/CALMET.DAT'
    if meta.exists() and cache.exists() and json.loads(meta.read_text())['source']==ident(p):
        with cache.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f)),json.loads(meta.read_text())
    from cartografia_copasa import centre
    m=json.loads((R/'output/auditoria/CALMET_DAT_verificado.json').read_text())['header'];nx=m['nx'];ny=m['ny'];spacing=m['spacing_m']
    cells={}
    for k in ['VM','NC']:
        x,y=centre(k);ix=int(np.floor((x-m['origin_x_m'])/spacing));iy=int(np.floor((y-m['origin_y_m'])/spacing))
        cells[k]=dict(ix0=ix,iy0=iy,x_m=m['origin_x_m']+(ix+.5)*spacing,y_m=m['origin_y_m']+(iy+.5)*spacing)
    rows=[];current={};count=0
    with p.open('rb') as f:
        while True:
            a=f.read(4)
            if not a:break
            n=struct.unpack('<i',a)[0];assert 0<=n<10000000
            b=f.read(min(n,12));label=b[:8];capture=label in [b'U-LEV  1',b'V-LEV  1',b'ZI      ',b'IPGT    ',b'USTAR   ',b'T-LEV  1']
            if capture:
                assert n==12+nx*ny*4;b+=f.read(n-len(b));code=struct.unpack('<i',b[8:12])[0]
                year=code//100000;day=(code%100000)//100;hour=code%100
                ts=dt.datetime(year,1,1)+dt.timedelta(days=day-1,hours=hour)
                vals=np.frombuffer(b[12:],dtype='<i4' if label==b'IPGT    ' else '<f4').reshape(ny,nx)
                if label==b'U-LEV  1':
                    if current:
                        for k,v in current.items():
                            v['speed']=float(np.hypot(v['u'],v['v']));v['direction']=float(np.degrees(np.arctan2(-v['u'],-v['v']))%360);rows.append(v)
                    current={k:dict(unit=k,time_end=ts.isoformat(),u=float(vals[v['iy0'],v['ix0']])) for k,v in cells.items()}
                else:
                    key={b'V-LEV  1':'v',b'ZI      ':'mixing_m',b'IPGT    ':'stability_PG',b'USTAR   ':'ustar',b'T-LEV  1':'temperature_K'}[label]
                    for k,v in cells.items():current[k][key]=float(vals[v['iy0'],v['ix0']])
            else:f.seek(n-len(b),1)
            assert struct.unpack('<i',f.read(4))[0]==n;count+=1
    if current:
        for k,v in current.items():v['speed']=float(np.hypot(v['u'],v['v']));v['direction']=float(np.degrees(np.arctan2(-v['u'],-v['v']))%360);rows.append(v)
    assert len(rows)==17517*2 and count==859399

    keys=list(dict.fromkeys(k for v in rows for k in v));rows=[{k:v.get(k,'') for k in keys} for v in rows]
    csvout(cache,rows);metaobj=dict(source=ident(p),records_checked=count,cells=cells,wind_level='first CALMET layer, 0-20 m; centre at 10 m AGL',timezone='UTC-03:00 declared by CALMET',time_label='hour end as encoded in CALMET',selection='containing cell at each plant, no spatial interpolation')
    dump(meta,metaobj);print('CALMET extracted',len(rows),flush=True);return rows,metaobj

# Main
def main():
    start=time.monotonic();source_t,aer=parse_aer(R/'CMAS/AERMOD/H2S_TOTAL.ADI');audit={};massrows=[];geo={}
    for k in ['VM','NC']:
        _,cal=parse_cal(R/f'CMAS/CALPUFF/CALPUFF-{k}.INP');polys=[]
        for n,v in aer.items():
            if not n.startswith(k+'_'):continue
            polys.append(Point(v['x'],v['y']).buffer(v['params'][2],quad_segs=100) if v['type']=='AREACIRC' else Polygon(v['xy']))
            massrows.append(dict(unit=k,model='AERMOD',source=n,area_m2=v['area'],mass_g_s=v['old_flux']*v['area'],height_m=v['height'],sigma_z_m=v['params'][-1]))
        geo[k]=unary_union(polys)
        for n,v in cal.items():massrows.append(dict(unit=k,model='CALPUFF',source=n,area_m2=v['area'],mass_g_s=v['old_flux']*v['area'],height_m=v['height'],sigma_z_m=v['sigma']))
        totals={m:sum(v['mass_g_s'] for v in massrows if v['unit']==k and v['model']==m) for m in ['AERMOD','CALPUFF']}
        audit[k]=dict(totals_g_s=totals,mass_difference_percent=(totals['CALPUFF']/totals['AERMOD']-1)*100)
    csvout(O/'Entradas_executadas_fontes.csv',massrows)
    met,missing,calm=met_aermet();calmet,meta_cal=met_calmet();descriptors=[];paired=[];radial=[];quality=[];fieldmeta=[];conditional=[]
    all_fields={};npz={};distance_bins=[0,25,50,100,250,500,1000,1800,5000,10000,100000]
    for k in ['VM','NC']:
        g=1 if k=='VM' else 2;h,xy,codes,hmeta=hourly(k);nh,n=h.shape
        assert len(met)==nh and np.array_equal(codes,[r['code'] for r in met])
        valid=~np.isin(codes,missing+calm);year=codes//1000000;day=codes//100;unique_days=np.unique(day)

        dd=[]
        for d in unique_days:
            sel=day==d;den=max(int(valid[sel].sum()),18);dd.append(np.asarray(h[sel],dtype='float64').sum(axis=0)/den)
        dd=np.asarray(dd);tab,dc,_=native(R/f'CMAS/AERMOD/24_GWWTP{g}.POS')
        assert len(tab)==len(dd)*n and np.array_equal(dc[::n]//100,unique_days)
        daily=tab[:,2].reshape(len(dd),n);err=float(np.max(np.abs(daily-dd)));assert err<.00002,(k,err)
        ann,ac,ah=native(R/f'CMAS/AERMOD/AN_GWWTP{g}.POS');years=np.unique(year);annarr=ann[:,2].reshape(len(years),n)
        yy=np.array([np.asarray(h[year==y],dtype='float64').sum(axis=0)/valid[year==y].sum() for y in years]);ae=float(abs(yy-annarr).max());assert ae<.00002,(k,ae)
        quality.append(dict(unit=k,hours=nh,calm_hours=int(np.isin(codes,calm).sum()),missing_hours=int(np.isin(codes,missing).sum()),daily_native_max_abs_error_ug_m3=err,annual_native_max_abs_error_ug_m3=ae,annual_by_year=[dict(year=2000+int(y),valid_hours=int(valid[year==y].sum()),expected_hours=int((year==y).sum())) for y in years],start=hmeta['start_end'],end=hmeta['last_end']))
        npz[f'{k}_AERMOD_xy']=xy
        vals={'1h':np.asarray(h).max(axis=0),'24h':daily.max(axis=0),'annual_calendar_max':annarr.max(axis=0),'period_mean':np.asarray(h,dtype='float64').sum(axis=0)/valid.sum()}
        times=[stamp(c)-dt.timedelta(minutes=30) for c in codes];ws=np.array([r['speed'] for r in met]);wd=np.array([r['direction'] for r in met]);hr=np.array([t.hour for t in times])
        distances=np.array([geo[k].distance(Point(x,y)) for x,y in xy]);_,keep=np.unique(xy,axis=0,return_index=True)

        for lo,hi in [(0,100),(100,500),(500,1800)]:
            si=keep[(distances[keep]>=lo)&(distances[keep]<hi)]
            if not len(si):continue
            series=np.mean(h[:,si],axis=1)
            for typ,cat in [('speed',np.digitize(ws,[1,2,4,6])),('direction',(np.floor((wd+22.5)%360/45)).astype(int)),('hour',hr)]:
                for v in np.unique(cat[valid]):
                    z=series[valid&(cat==v)];conditional.append(dict(unit=k,model='AERMOD',distance_min_m=lo,distance_max_m=hi,category=typ,bin=int(v),hours=len(z),receptors=len(si),median=float(np.median(z)),p90=float(np.quantile(z,.9)),mean=float(z.mean())))
        for per,values in vals.items():
            npz[f'{k}_AERMOD_{per}']=values;all_fields[k,'AERMOD',per]=(xy,values)
        for per,token in [('1h','1'),('24h','24'),('rank8760_max','8760'),('period_mean','17517')]:
            p=R/f'CMAS/CALPUFF/RANK({k})_ODOR_{token}HR_CONC_C.DAT';tab=np.loadtxt(p,skiprows=6);xx=tab[:,:2]*1000;cc=tab[:,2]
            assert np.isfinite(tab).all() and (cc>=0).all();npz[f'{k}_CALPUFF_{per}']=cc;npz[f'{k}_CALPUFF_xy']=xx;all_fields[k,'CALPUFF',per]=(xx,cc)
            fieldmeta.append(dict(unit=k,model='CALPUFF',period=per,source=ident(p),records=len(tab),maximum=float(cc.max())))
        for model,per in [(m,p) for m in ['AERMOD','CALPUFF'] for p in ['1h','24h','period_mean']]+[('AERMOD','annual_calendar_max'),('CALPUFF','rank8760_max')]:
            xx,cc=all_fields[k,model,per];_,ix=np.unique(xx,axis=0,return_index=True);dist=np.array([geo[k].distance(Point(x,y)) for x,y in xx[ix]])
            for i in range(len(distance_bins)-1):
                lo,hi=distance_bins[i:i+2];sel=(dist>=lo)&(dist<hi);v=cc[ix][sel]
                if len(v):radial.append(dict(unit=k,model=model,period=per,min_distance_m=lo,max_distance_m=hi,n=len(v),p25=float(np.quantile(v,.25)),median=float(np.median(v)),p75=float(np.quantile(v,.75)),p90=float(np.quantile(v,.9)),maximum=float(v.max())))
            descriptors.append(dict(unit=k,model=model,period=per,records=len(cc),unique_positions=len(ix),maximum=float(cc.max()),distance_at_peak_m=float(geo[k].distance(Point(xx[cc.argmax()]))),inside_source_receptors=int((dist==0).sum()),median_near_500m=float(np.median(cc[ix][dist<=500]))))

        xx,cc=all_fields[k,'CALPUFF','24h'];_,ix=np.unique(xx,axis=0,return_index=True);xx=xx[ix];tree=cKDTree(xx)
        near,ii=tree.query(xy[keep]);accept=near<=.75;ai=keep[accept];ci=ix[ii[accept]]
        assert len(set(ci))==len(ci),'Ambiguous coordinate matching'
        for per in ['1h','24h']:
            av=all_fields[k,'AERMOD',per][1][ai];cv=all_fields[k,'CALPUFF',per][1][ci];d=distances[ai]
            for lo,hi in [(0,100),(100,500),(500,1800),(0,1800),(0,100000)]:
                z=(d>=lo)&(d<hi);a=av[z];c=cv[z];positive=(a>0)&(c>0);tot=a+c
                if len(a)<3:continue
                rho=float(spearmanr(a,c).statistic);fac=float(np.mean((a[positive]/c[positive]>=.5)&(a[positive]/c[positive]<=2))) if positive.any() else None
                paired.append(dict(unit=k,period=per,min_distance_m=lo,max_distance_m=hi,n=len(a),positive_pairs=int(positive.sum()),spearman_rho=rho if np.isfinite(rho) else None,median_AERMOD=float(np.median(a)),median_CALPUFF=float(np.median(c)),median_CALPUFF_over_AERMOD=float(np.median(c[positive]/a[positive])) if positive.any() else None,factor_two_agreement_positive=fac,symmetric_mean_difference_CAL_minus_AER=float(2*(c.mean()-a.mean())/(c.mean()+a.mean())) if tot.sum()>0 else None))
            csvout(O/f'Pares_nativos_{k}_{per}.csv',[dict(x=float(xy[ia,0]),y=float(xy[ia,1]),distance_m=float(distances[ia]),AERMOD=float(all_fields[k,'AERMOD',per][1][ia]),CALPUFF=float(all_fields[k,'CALPUFF',per][1][ic]),match_error_m=float(ne)) for ia,ic,ne in zip(ai,ci,near[accept])])
    np.savez_compressed(O/'Campos_nativos.npz',**npz);csvout(O/'Perfis_distancia.csv',radial);csvout(O/'Estatisticas_pares.csv',paired);csvout(O/'Descritores_campos.csv',descriptors);csvout(O/'Resposta_meteorologica_AERMOD.csv',conditional)
    result=dict(execution_inputs=audit,quality_AERMOD=quality,fields=descriptors,paired=paired,CALMET=meta_cal,elapsed_seconds=round(time.monotonic()-start,2),annual_CALPUFF_status='Derived from new CONC by extrair_calpuff_novo.py; RANK 8760 not substituted',hourly_CALPUFF_status='New CONC and LST available; see CALPUFF_horario_validado.json',AERMET_time_zone='LOCATION 0 is a time adjustment, not proof of UTC. Supplied SAMSON header declares zone 0; original clock convention needs confirmation against CALMET UTC-3. Compare each model conditional on its own executed meteorology; paired absolute event times remain provisional.',spatial_method='Unique native coordinates, tolerance <=0.75 m for RANK coordinates rounded to 1 m. No interpolation in statistics. Distance to union of AERMOD emitting footprints. No inferential p values because spatial samples are dependent.',comparison_status='Model intercomparison, not validation against ambient measurements')
    dump(O/'Comparacao_consolidada.json',result);print(json.dumps(dict(inputs=audit,quality=quality,selected_stats=[v for v in paired if v['min_distance_m']==0 and v['max_distance_m']==1800],elapsed=result['elapsed_seconds']),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
