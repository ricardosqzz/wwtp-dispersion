# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/in/CALMET.DAT | p.open.
# Campos/chaves em header: hours.
# Saída: E:/copasa_map/output/auditoria/CALMET_DAT_verificado.json | .write_text.
# CÓDIGO DO PROCESSAMENTO

"""Inspeciona registros Fortran sem carregar o CALMET inteiro na memória."""
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
import struct,json,datetime,time
R=Path(_cp_texto('', 'posix'));p=R/'in/CALMET.DAT';start=time.monotonic()
count=0;hours=[];header=None;lines=None
with p.open('rb') as f:
    while True:
        marker=f.read(4)
        if not marker:break
        assert len(marker)==4,'Marcador incompleto'
        n=struct.unpack('<i',marker)[0];assert 0<=n<10000000,(f.tell(),n)
        take=min(n,160 if count<1200 else 12);v=f.read(take);f.seek(n-take,1)
        tail=f.read(4);assert len(tail)==4 and struct.unpack('<i',tail)[0]==n,(count,f.tell())
        if count==0:assert v.startswith(b'CALMET.DAT')
        if count==1:lines=struct.unpack('<i',v)[0]
        if lines is not None and count==lines+2:
            q=struct.unpack('<10i3f',v[:52]);header=dict(year=q[0],month=q[1],day=q[2],hour_end=q[3],timezone_west_utc=q[4],hours=q[5],nx=q[7],ny=q[8],nz=q[9],spacing_m=q[10],origin_x_m=q[11],origin_y_m=q[12])
        if v[:8]==b'U-LEV  1':
            code=struct.unpack('<i',v[8:12])[0];year=code//100000;day=(code%100000)//100;hour=code%100
            dt=datetime.datetime(year,1,1)+datetime.timedelta(days=day-1,hours=hour)
            if hours:assert dt-hours[-1]==datetime.timedelta(hours=1),(dt,hours[-1])
            hours.append(dt)
        count+=1
    assert f.tell()==p.stat().st_size
assert header and len(hours)==header['hours']
d=dict(passed=True,path=str(p),bytes=p.stat().st_size,fortran_records_checked=count,embedded_control_lines=lines,header=header,hours_verified=len(hours),first_hour_end=hours[0].isoformat(),last_hour_end=hours[-1].isoformat(),hourly_sequence_continuous=True,elapsed_seconds=round(time.monotonic()-start,2),concentrations_recalculated=False)
(R/'output/auditoria/CALMET_DAT_verificado.json').write_text(json.dumps(d,indent=2),encoding='utf8');print(json.dumps(d))
