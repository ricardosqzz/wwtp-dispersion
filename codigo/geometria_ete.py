# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/'v_maria/vm_limite.kmz' if k == 'VM' else 'n_contagem/nc_limite.kmz' | zipfile.ZipFile.
# Campos/chaves em cal: NC.
# Campos/chaves em d: area.
# Campos/chaves em record: sources.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# Campos/chaves gerados em d: area, old_area, xy.
# CÓDIGO DO PROCESSAMENTO

"""Limites fornecidos e regularização geométrica autorizada dos UASB NC."""
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
import zipfile,xml.etree.ElementTree as ET,math
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import transform,unary_union
from pyproj import Transformer
R=Path(_cp_texto('', 'posix'));NS={'k':'http://www.opengis.net/kml/2.2'}
TO_UTM=Transformer.from_crs(4326,32723,always_xy=True)
# Limite
def limite(k):
    p=R/('v_maria/vm_limite.kmz' if k=='VM' else 'n_contagem/nc_limite.kmz')
    with zipfile.ZipFile(p) as z:r=ET.fromstring(z.read(next(n for n in z.namelist() if n.endswith('.kml'))))
    polygons=[]
    for c in r.findall('.//k:Polygon/k:outerBoundaryIs/k:LinearRing/k:coordinates',NS):
        xy=[tuple(map(float,v.split(',')[:2])) for v in c.text.split()];polygons.append(Polygon(xy))
    assert polygons,str(p)
    return transform(TO_UTM.transform,unary_union(polygons))
# Regularizar
def regularizar(aer,cal):
    keys=['NC_UASB1','NC_UASB2','NC_UASB3'];old=[Polygon(aer[n]['xy']) for n in keys]
    centres=np.array([[p.centroid.x,p.centroid.y] for p in old]);mid=centres.mean(axis=0)
    _,_,vh=np.linalg.svd(centres-mid);along=vh[0]
    if np.dot(along,centres[2]-centres[0])<0:along=-along
    across=np.array([-along[1],along[0]])

    widths=[]
    for p in old:
        corners=np.asarray(p.minimum_rotated_rectangle.exterior.coords)[:-1]
        edges=np.roll(corners,-1,axis=0)-corners
        widths.append(float(np.max(np.abs(edges@across))))
    width=float(np.mean(widths));area=sum(p.area for p in old)/3;depth=area/width
    step=float(np.dot(centres[2]-centres[0],along)/2)
    record=dict(method='Three congruent rectangles; common alignment and equal centre spacing; original total area preserved',total_area_m2=area*3,each_area_m2=area,width_m=width,depth_m=depth,centre_spacing_m=step,clear_gap_m=step-depth,reference='regularization of supplied coordinates; no independent field survey',sources=[])
    boundary=limite('NC')
    for i,n in enumerate(keys):
        center=mid+(i-1)*step*along
        xy=[center+sx*width/2*across+sy*depth/2*along for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        xy=[(float(v[0]),float(v[1])) for v in xy];poly=Polygon(xy)
        assert poly.is_valid and boundary.covers(poly),(n,'outside supplied boundary')
        for d in [aer[n],cal['NC'][n]]:
            d['old_area']=d['area'];d['xy']=xy;d['area']=poly.area
            if 'x' in d:d['x'],d['y']=xy[0]
        record['sources'].append(dict(id=n,old_xy=[list(v) for v in old[i].exterior.coords][:-1],xy=xy,centroid=[float(v) for v in center],area_m2=poly.area,shift_m=float(np.linalg.norm(center-centres[i]))))
    return record
