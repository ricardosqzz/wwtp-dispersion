# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {p} | p.read_text.
# Entrada: E:/copasa_map/in/CALMET.INP | .read_text.
# Entrada: E:/copasa_map/in/CALMET.LST | .read_text.
# Entrada: E:/copasa_map/AERMET_COP.SFC | .read_text.
# Entrada: E:/copasa_map/output/entradas_corrigidas/CALPUFF-VM_corrigido.INP | .read_text.
# Entrada: E:/copasa_map/output/entradas_corrigidas/CALPUFF-NC_corrigido.INP | .read_text.
# Entrada: E:/copasa_map/temp/fontes_NC_xls_leitura.sha256 | sha.read_text.
# Entrada: E:/copasa_map/in/H2S_Grid_Sources-NC.xls | oldxls.read_bytes.
# Entrada: E:/copasa_map/temp/fontes_NC_xls_leitura.json | cache.read_text.
# Entrada: proc(n) | p.read_bytes.
# Campos/chaves em d: area, base, elev, flux, height, hill, index, mass, old_flux, origin, params, type, x, xy, xyinc, y.
# Campos/chaves em w: Comportamento, Entrada.
# Campos/chaves em s: B29, B31, B4, B54, B56, B58, B6, E13, K33, N17, N19, N20, N22, N23, N24.
# Campos/chaves em actual: NC, VM.
# Campos/chaves em cal: NC, VM.
# Campos/chaves em window: end, hours, start.
# Campos/chaves em z: Diam, Num_Coords, Type.
# Saída: {p} | p.write_text.
# Saída: {p} | p.open.
# Saída: E:/copasa_map/output/entradas_corrigidas/Grade_Receptora_Comum.ROU | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/{name} | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/CALPUFF-{k}_corrigido.INP | .write_text.
# Saída: E:/copasa_map/output/entradas_corrigidas/CALPUFF-CMAS_TOTAL_corrigido.INP | .write_text.
# Campos/chaves gerados em : area, params, xy, xyinc.
# Campos/chaves gerados em d: area, height, old_flux, receptor_id.
# receptor_id: identificador do receptor.
# CÓDIGO DO PROCESSAMENTO

"""Auditoria reproduzível; nunca sobrescreve os insumos recebidos."""
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
import sys,json,re,math,csv,hashlib,statistics,datetime
sys.path.append(_cp_externo('python_5ae2cb6'))
import openpyxl
from shapely.geometry import Polygon,Point
from geometria_ete import regularizar
R=Path(_cp_texto('', 'posix'));I=R/'in';O=R/'output/entradas_corrigidas';A=R/'output/auditoria'
O.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
# Dump
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
# Csvout
def csvout(p,rows):
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Nums
def nums(s):return [float(x) for x in re.findall(r'[-+]?\d*\.?\d+(?:[EeDd][-+]?\d+)?',s.replace('D','E'))]
# Parse cal
def parse_cal(p):
    t=p.read_text(encoding='cp1252');part=t.split('Subgroup (14b)')[1].split('Subgroup (14c)')[0]
    out={}
    for m in re.finditer(r'(\d+)\s*!\s*SRCNAM\s*=\s*(\w+)\s*!\s*\d+\s*!\s*X\s*=\s*([^!]+)!',part):
        v=nums(m[3]);out[m[2]]={'id':m[2],'index':int(m[1]),'height':v[0],'base':v[1],'sigma':v[2],'old_flux':v[3]}
    part=t.split('Subgroup (14c)')[1].split('Subgroup (14d)')[0]
    for m in re.finditer(r'(\d+)\s*!\s*SRCNAM\s*=\s*(\w+)\s*!\s*\d+\s*!\s*XVERT\s*=\s*([^!]+)!\s*\d+\s*!\s*YVERT\s*=\s*([^!]+)!',part):
        xy=list(zip([v*1000 for v in nums(m[3])],[v*1000 for v in nums(m[4])]))
        out[m[2]]['xy']=xy;out[m[2]]['area']=Polygon(xy).area
    return t,out
# Parse aer
def parse_aer(p):
    t=p.read_text(encoding='cp1252');out={}
    for l in t.splitlines():
        s=l.split()
        if not s:continue
        if s[0]=='LOCATION':out[s[1]]={'id':s[1],'type':s[2],'x':float(s[3]),'y':float(s[4]),'base':float(s[5]),'xy':[]}
        elif s[0]=='SRCPARAM':out[s[1]]['params']=list(map(float,s[2:]))
        elif s[0]=='AREAVERT':out[s[1]]['xy']+=list(zip(map(float,s[2::2]),map(float,s[3::2])))
    for d in out.values():
        d['area']=math.pi*d['params'][2]**2 if d['type']=='AREACIRC' else Polygon(d['xy']).area
        d['old_flux']=d['params'][0];d['height']=d['params'][1]
    return t,out
# Parse rou
def parse_rou(p):
    rows=[];nets={};network=None
    for l in p.read_text(encoding='cp1252').splitlines():
        s=l.split()
        if s and s[0]=='DISCCART':
            v=list(map(float,s[1:]));rows.append(dict(x=v[0],y=v[1],elev=v[2],hill=v[3],origin='DISCCART'))
        elif len(s)>2 and s[0]=='GRIDCART':
            network=s[1]
            if s[2]=='STA':nets[network]={'elev':{},'hill':{}}
            elif s[2] in ('ELEV','HILL'):
                d=nets[network][s[2].lower()];d.setdefault(int(s[3]),[]).extend(map(float,s[4:]))
        elif s and s[0]=='XYINC':nets[network]['xyinc']=list(map(float,s[1:]))
    for name,d in nets.items():
        x,nx,dx,y,ny,dy=d['xyinc'];
        for j in range(int(ny)):
            for k in range(int(nx)):
                rows.append(dict(x=x+k*dx,y=y+j*dy,elev=d['elev'][j+1][k],hill=d['hill'][j+1][k],origin=name))
    return rows
# Main
def main():
    met=None;window=None
    if (I/'CALMET.INP').exists() and (I/'CALMET.LST').exists():
        mt=(I/'CALMET.INP').read_text(encoding='cp1252');ml=(I/'CALMET.LST').read_text(encoding='cp1252')
        def value(k):return nums(re.search(rf'!\s*{k}\s*=\s*([^!]+)!',mt)[1])[0]
        last=re.search(r'LAST DAY/HOUR PROCESSED:\s*Year:\s*(\d+)\s*Month:\s*(\d+)\s*Day:\s*(\d+)\s*Julian day:\s*\d+\s*Hour:\s*(\d+)',ml)
        assert last and 'End of run -- Clock time:' in ml
        calstart=datetime.datetime(int(value('IBYR')),int(value('IBMO')),int(value('IBDY')))+datetime.timedelta(hours=value('IBHR'))
        calend=datetime.datetime(*map(int,last.groups()))
        sr=(R/'AERMET_COP.SFC').read_text(encoding='cp1252').splitlines()[1:]
        def sfctime(line):
            y,m,day,j,h=map(int,line.split()[:5]);return datetime.datetime(2000+y,m,day)+datetime.timedelta(hours=h)
        first=max(calstart,sfctime(sr[0]));end=min(calend,sfctime(sr[-1]));count=int((end-first).total_seconds()/3600)+1
        window=dict(start=first.isoformat(),end=end.isoformat(),hours=count)
        met=dict(start=calstart.isoformat(),end=calend.isoformat(),hours=int(value('IRLG')),timezone_west_utc=value('IBTZ'),nx=int(value('NX')),ny=int(value('NY')),grid_km=value('DGRIDKM'),surface_stations=int(value('NSSTA')),upper_stations=int(value('NUSTA')),prognostic_files=int(value('NM3D')),warning='BIAS(1) reset to -1 to be consistent with IEXTRP',normal_end=True)
    w=openpyxl.load_workbook(I/'Resumo_MOD.xlsx',data_only=True);s=w['Entrada'];profile=[w['Comportamento'].cell(r,3).value for r in range(3,27)]
    molecular=1/(1+10**(s['B4'].value-s['B6'].value));assert abs(molecular-s['E13'].value)<1e-12
    at,aer=parse_aer(I/'H2S_TOTAL.ADI');ct={};cal={}
    for k in ['VM','NC']:ct[k],cal[k]=parse_cal(I/f'CALPUFF-{k}.INP')
    geometry_revision=regularizar(aer,cal)
    dump(A/'Geometria_UASB_WWTP2.json',geometry_revision)
    actual={'VM':sum(d['area'] for n,d in aer.items() if n.startswith('VM_UASB')),'NC':sum(d['area'] for n,d in aer.items() if n.startswith('NC_UASB'))}
    process={'VM_PRE':s['N17'].value,'VM_UASB':s['B29'].value*actual['VM']*s['B31'].value+s['K33'].value,'VM_CALHA':s['N19'].value,'NC_PRE':s['N20'].value,'NC_UASB':s['B54'].value*actual['NC']*s['B56'].value*s['B58'].value,'NC_FB':s['N22'].value,'CT_ONCA':s['N23'].value,'CT_PAMP':s['N24'].value}
    def proc(n):
        for p in sorted(process,key=len,reverse=True):
            if n.startswith(p):return p
        raise ValueError(n)
    records=[]
    for model,src in [('AERMOD',aer),('CALPUFF',dict(**cal['VM'],**cal['NC']))]:
        areas={p:sum(d['area'] for n,d in src.items() if proc(n)==p) for p in process}
        for n,d in src.items():
            p=proc(n);d.update(process=p,flux=process[p]/areas[p],mass=process[p]*d['area']/areas[p])
            records.append(dict(model=model,id=n,process=p,area_m2=d['area'],old_area_m2=d.get('old_area',d['area']),height_m=d['height'],base_m=d['base'],old_flux_g_s_m2=d['old_flux'],old_mass_g_s=d['old_flux']*d.get('old_area',d['area']),corrected_flux_g_s_m2=d['flux'],corrected_mass_g_s=d['mass'],corrected_t_year=d['mass']*31.536))
        for p in process:
            subset=[d for n,d in src.items() if proc(n)==p]
            if subset:assert abs(sum(d['mass'] for d in subset)-process[p])<1e-12
    csvout(A/'Auditoria_fontes_modelos.csv',records)

    mean=statistics.mean(profile);f=[v/mean for v in profile];hours=f[1:]+f[:1]
    assert abs(statistics.mean(hours)-1)<1e-14
    csvout(O/'Perfil_horario_normalizado.csv',[dict(hour_end=i+1,original=profile[(i+1)%24],normalized=hours[i]) for i in range(24)])

    ref=I/'AERMOD/H2S_Ref/H2S_TOTAL.ROU';rr=parse_rou(ref);chosen={}
    centres=[(614080,7834430),(589190,7805680)]
    for d in rr:
        near=min(math.hypot(d['x']-x,d['y']-y) for x,y in centres)<=1800
        if d['origin']=='UCART4' or near:
            key=(round(d['x'],2),round(d['y'],2));chosen.setdefault(key,d)
    grid=sorted(chosen.values(),key=lambda d:(d['y'],d['x']))
    for i,d in enumerate(grid):d['receptor_id']=i+1
    csvout(O/'Grade_Receptora_Comum.csv',grid)
    (O/'Grade_Receptora_Comum.ROU').write_text('RE ELEVUNIT METERS\n'+''.join(f"   DISCCART {d['x']:.2f} {d['y']:.2f} {d['elev']:.2f} {d['hill']:.2f}\n" for d in grid),encoding='ascii')

    def newadi(include_ct=False):
        lines=['CO STARTING',' TITLEONE H2S - inventory corrected 2026-11-09',' MODELOPT DFAULT CONC',' AVERTIME 1 24 ANNUAL',' POLLUTID H2S',' RUNORNOT RUN','CO FINISHED','SO STARTING']
        for n,d in aer.items():
            if not include_ct and n.startswith('CT_'):continue
            lines+=[f" LOCATION {n} {d['type']} {d['x']:.8f} {d['y']:.8f} {d['base']:.3f}"]
            pr=d['params'][1:];lines+=[f" SRCPARAM {n} {d['flux']:.12g} "+' '.join(f'{v:.9g}' for v in pr)]
            for i in range(0,len(d['xy']),2):lines+=[f' AREAVERT {n} '+' '.join(f'{x:.8f} {y:.8f}' for x,y in d['xy'][i:i+2])]
            for i in range(0,24,6):lines+=[f' EMISFACT {n} HROFDY '+' '.join(f'{v:.10f}' for v in hours[i:i+6])]
        for k in ['VM','NC']:lines+=[' SRCGROUP '+k+' '+' '.join(n for n in aer if n.startswith(k+'_'))]
        if include_ct:lines+=[' SRCGROUP CT CT_ONCA CT_PAMP']
        lines+=[' SRCGROUP ALL','SO FINISHED','RE STARTING',' INCLUDED Grade_Receptora_Comum.ROU','RE FINISHED','ME STARTING',_cp_adaptar(r' SURFFILE E:\copasa_map\AERMET_COP.SFC'),_cp_adaptar(r' PROFFILE E:\copasa_map\in\AERMOD\AERMET\AERMET_COP.PFL'),' SURFDATA 1 2024',' UAIRDATA 83566 2024',' PROFBASE 854.0 METERS','ME FINISHED','OU STARTING',' RECTABLE ALLAVE 1ST',' PLOTFILE 24 ALL 1ST H2S_24H.PLT',' PLOTFILE ANNUAL ALL H2S_ANNUAL.PLT',' PLOTFILE 24 VM 1ST H2S24_W1.PLT',' PLOTFILE 24 NC 1ST H2S24_W2.PLT',' PLOTFILE ANNUAL VM H2SAN_W1.PLT',' PLOTFILE ANNUAL NC H2SAN_W2.PLT','OU FINISHED']
        if window:
            b=datetime.datetime.fromisoformat(window['start']);e=datetime.datetime.fromisoformat(window['end'])
            assert b.hour>0 and e.hour>0
            lines.insert(lines.index('ME FINISHED'),f' STARTEND {b.year} {b.month} {b.day} {b.hour} {e.year} {e.month} {e.day} {e.hour}')
        return '\n'.join(lines)+'\n'
    for name,cton in [('H2S_CMAS_corrigido.ADI',False),('H2S_COMPLETO_corrigido.ADI',True)]: (O/name).write_text(newadi(cton),encoding='ascii')

    def subgroup(t,letter):
        start=t.index(f'Subgroup (14{letter})');return start,t.index('---------------',start+25)
    for k,t in ct.items():
        if window:
            b=datetime.datetime.fromisoformat(window['start'])
            for key,val in dict(IBYR=b.year,IBMO=b.month,IBDY=b.day,IBHR=b.hour,IRLG=window['hours']).items():
                t=re.sub(rf'(!\s*{key}\s*=\s*)\d+',lambda m:m[1]+str(val),t)
        for n,d in cal[k].items():
            pat=rf'(\d+\s*!\s*SRCNAM\s*=\s*{n}\s*!\s*\d+\s*!\s*X\s*=\s*)([^!]+)(!)'
            def repl(m):
                vals=nums(m[2]);vals[3]=d['flux'];return m[1]+', '.join(f'{v:.12g}' for v in vals)+m[3]
            t,count=re.subn(pat,repl,t);assert count==1
            if n.startswith('NC_UASB'):
                pat=rf'(\d+\s*!\s*SRCNAM\s*=\s*{n}\s*!\s*\d+\s*!\s*XVERT\s*=\s*)([^!]+)(!\s*\d+\s*!\s*YVERT\s*=\s*)([^!]+)(!)'
                xs=', '.join(f'{x/1000:.11f}' for x,y in d['xy']);ys=', '.join(f'{y/1000:.11f}' for x,y in d['xy'])
                t,count=re.subn(pat,lambda m:m[1]+xs+m[3]+ys+m[5],t);assert count==1

        st=t.index('Subgroup (14d)');en=t.index('INPUT GROUPS: 15',st)
        old=t[st:en]
        for n,d in cal[k].items():
            pattern=rf'\d+\s*!\s*SRCNAM\s*=\s*{n}\s*!\s*\d+\s*!\s*IVARY\s*=\s*1\s*![^!]*?\d+\s*!\s*ODOR\s*=\s*[^!]+!\s*!END!'
            h=',\n       '.join(','.join(f'{v:.10f}' for v in hours[i:i+6]) for i in range(0,24,6))
            replacement=f"{d['index']} ! SRCNAM = {n} !\n {d['index']} ! IVARY = 1 !\n {d['index']} ! ODOR = {h} !\n!END!"
            old,count=re.subn(pattern,replacement,old);assert count==1,(k,n,count)
        t=t[:st]+old+t[en:]
        t=re.sub(r'(!\s*LSAMP\s*=\s*)T',r'\g<1>F',t)
        t=re.sub(r'(!\s*NREC\s*=\s*)\d+',lambda m:m[1]+str(len(grid)),t)

        g16=t.index('Subgroup (17b)')
        tail=t[g16:];m=re.search(r'(?m)^\s*1\s*!\s*X\s*=',tail)
        if not m:
            m=re.search(r'(?m)^\s*1\s+[-+]?\d',tail)
        assert m,tail[:1800]

        e=tail.rindex('!END!')+len('!END!')
        records16=''.join(f" {i+1} ! X = {d['x']/1000:.8f}, {d['y']/1000:.8f}, {d['elev']:.3f}, 0.0 ! !END!\n" for i,d in enumerate(grid))
        t=t[:g16]+tail[:m.start()]+records16+tail[e:]

        (O/f'CALPUFF-{k}_corrigido.INP').write_text(t,encoding='cp1252')

    tv=(O/'CALPUFF-VM_corrigido.INP').read_text(encoding='cp1252')
    tn=(O/'CALPUFF-NC_corrigido.INP').read_text(encoding='cp1252')
    def block(t,letter):
        start=t.index(f'Subgroup (14{letter})');end=t.index('Subgroup (14'+chr(ord(letter)+1)+')') if letter!='d' else t.index('INPUT GROUPS: 15',start)
        part=t[start:end];ms=list(re.finditer(r'(?m)^\s*\d+\s*!\s*SRCNAM\s*=',part));assert len(ms)==6
        a=ms[0].start();b=part.rindex('!END!')+5
        return start+a,start+b,part[a:b]
    for letter in ['d','c','b']:
        av,bv,bvm=block(tv,letter);an,bn,bnc=block(tn,letter)
        bnc=re.sub(r'(?m)^(\s*)(\d+)(\s*!)',lambda m:m[1]+str(int(m[2])+6)+m[3],bnc)
        tv=tv[:av]+bvm+'\n'+bnc+tv[bv:]
    tv=re.sub(r'(!\s*(?:NAR1|NSAR1)\s*=\s*)6\b',r'\g<1>12',tv)
    tv=re.sub(r'(!\s*MSOURCE\s*=\s*)0',r'\g<1>1',tv)
    (O/'CALPUFF-CMAS_TOTAL_corrigido.INP').write_text(tv,encoding='cp1252')
    sums=[]
    for k in ['VM','NC']:
        sums.append(dict(unit=k,alias='WWTP 1' if k=='VM' else 'WWTP 2',uasb_actual_m2=actual[k],old_process_total=sum(s[f'N{r}'].value for r in (range(17,20) if k=='VM' else range(20,23))),new_process_total=sum(v for p,v in process.items() if p.startswith(k+'_')),old_aermod_total=sum(d['old_flux']*d.get('old_area',d['area']) for n,d in aer.items() if n.startswith(k+'_')),old_calpuff_total=sum(d['old_flux']*d.get('old_area',d['area']) for d in cal[k].values())))

    cache=R/'temp/fontes_NC_xls_leitura.json';sha=R/'temp/fontes_NC_xls_leitura.sha256';oldxls=I/'H2S_Grid_Sources-NC.xls'
    if not sha.exists() or sha.read_text().strip()!=hashlib.sha256(oldxls.read_bytes()).hexdigest():
        import subprocess
        subprocess.run([_cp_externo('pwsh_exe_72a6651'),'-NoProfile','-File',str(R/'codigo/ler_xls_original.ps1')],check=True)
    oldbooks=[]
    for fn,hr in [('H2S_TOTAL_Sources-AERMOD.xlsx',51),('H2S_Grid_Sources-VM.xlsx',49),('H2S_Grid_Sources-NC.xls',49)]:
        if fn.endswith('.xls'):rrr=json.loads(cache.read_text(encoding='utf-8-sig'))
        else:
            wb=openpyxl.load_workbook(I/fn,data_only=True,read_only=True);rrr=list(wb.active.values);wb.close()
        head=list(rrr[hr-1]);field='Emission_Rate' if 'AERMOD' in fn else 'ODOR'
        for row in rrr[hr+1:]:
            z=dict(zip(head,row));n=z.get('ID')
            if not n or not z.get('Type'):continue
            pts=[(z.get(f'X{j}'),z.get(f'Y{j}')) for j in range(1,int(z['Num_Coords'])+1)]
            ar=math.pi*z['Diam']**2 if z['Type']=='AREA_CIRC' else Polygon(pts).area
            refsrc=aer if 'AERMOD' in fn else dict(**cal['VM'],**cal['NC'])
            matches=[d for name,d in refsrc.items() if name==n or name.startswith(n+'_')]
            expected=sum(d['old_flux']*d['area'] for d in matches)/sum(d['area'] for d in matches) if matches else None
            v=z.get(field);oldbooks.append(dict(workbook=fn,id=n,type=z['Type'],area_m2=ar,flux_g_s_m2=v,mass_g_s=v*ar,model_flux_g_s_m2=expected,divergent=expected is not None and abs(v-expected)>max(1e-9,abs(expected)*.01)))
    csvout(A/'Auditoria_planilhas_importacao_originais.csv',oldbooks)
    bases=[I/'Resumo_MOD.xlsx',I/'H2S_TOTAL_Sources-AERMOD.xlsx',I/'H2S_Grid_Sources-VM.xlsx',oldxls,I/'H2S_TOTAL.ADI',I/'CALPUFF-VM.INP',I/'CALPUFF-NC.INP',ref]
    if met:bases += [I/'CALMET.INP',I/'CALMET.LST']
    manifest=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in bases]
    data=dict(process=process,actual_uasb_areas=actual,molecular_fraction=molecular,profile_mean_old=mean,profile_hour_end=hours,sources_aermod=aer,sources_calpuff=cal,summary=sums,grid=grid,grid_count=len(grid),inputs=manifest,source_records=records,old_source_workbooks=oldbooks,calmet=met,common_window=window,geometry_revision=geometry_revision)
    dump(A/'Auditoria_consolidada.json',data)
    print(json.dumps({'summary':sums,'grid_count':len(grid),'profile_mean_old':mean},ensure_ascii=True))
if __name__=='__main__':main()
