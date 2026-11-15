# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/in/cartografia_contexto/OSM_{k}.json | p.read_text.
# Entrada: E:/copasa_map/CMAS/vias/malha_viaria.shp | gpd.read_file.
# Campos/chaves em data: elements.
# Campos/chaves em v: lat, lon.
# Campos/chaves em tags: highway.
# Campos/chaves em st: color, style, width.
# Saída: E:/copasa_map/output/auditoria/Contexto_cartografico.json | .write_text.
# CÓDIGO DO PROCESSAMENTO

"""Contexto vetorial sem rótulos: vias/edificações externas e limite fornecido."""
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
from shapely.geometry import Polygon,LineString,shape,mapping
from shapely.ops import transform,unary_union
from shapely.geometry import box
from pyproj import Transformer
from geometria_ete import limite
R=Path(_cp_texto('', 'posix'));TO_UTM=Transformer.from_crs(4326,32723,always_xy=True)
CACHE={}
ROAD_STYLES={
 'primary':dict(color='#95633d',width=.85,style='solid',label='Primary roads'),
 'secondary':dict(color='#586f7c',width=.65,style=(0,(5,2)),label='Secondary roads'),
 'collector':dict(color='#82959c',width=.45,style='solid',label='Collector roads'),
 'other':dict(color='#b0b9bd',width=.30,style=(0,(1.3,1.7)),label='Local/unclassified roads'),
}
# Road class
def road_class(kind):
    if kind in ['motorway','trunk','primary','motorway_link','trunk_link','primary_link']:return 'primary'
    if kind in ['secondary','secondary_link']:return 'secondary'
    if kind in ['tertiary','tertiary_link']:return 'collector'
    return 'other'
# Layers
def layers(k):
    if k in CACHE:return CACHE[k]
    border=limite(k);roads=[];buildings=[]
    p=R/f'in/cartografia_contexto/OSM_{k}.json'
    if p.exists():
        data=json.loads(p.read_text(encoding='utf8'))
        for e in data['elements']:
            tags=e.get('tags',{});coords=e.get('geometry')
            if not coords:continue
            xy=[(v['lon'],v['lat']) for v in coords if 'lon' in v and 'lat' in v]
            if len(xy)<2:continue
            if 'highway' in tags:
                g=transform(TO_UTM.transform,LineString(xy)).difference(border)
                if not g.is_empty:roads.append((g,tags['highway']))
            if 'building' in tags and len(xy)>=4:
                g=transform(TO_UTM.transform,Polygon(xy))
                if g.is_valid:
                    g=g.difference(border)
                    if not g.is_empty:buildings.append(g)

    import geopandas as gpd
    supplied=R/'CMAS/vias/malha_viaria.shp'
    if supplied.exists():
        cx,cy=border.centroid.x,border.centroid.y
        area=box(cx-2500,cy-2500,cx+2500,cy+2500)
        to_sirgas=Transformer.from_crs(32723,31983,always_xy=True)
        search=transform(to_sirgas.transform,area).bounds
        shp=gpd.read_file(supplied,bbox=search).to_crs(32723)
        known=[];unknown=[]
        for _,v in shp.iterrows():
            g=v.geometry.intersection(area).difference(border)
            if g.is_empty:continue
            name=str(v.get('hier_legal','')).upper().replace(' ','')
            if name in ['ARTERIALPRIMARIA','RODOVIAPRIMARIA']:kind='primary'
            elif name in ['ARTERIALSECUNDARIA','RODOVIASECUNDARIA']:kind='secondary'
            elif name in ['COLETORAPRINCIPAL','COLETORAVICINAL']:kind='tertiary'
            else:unknown.append((g,'local'));continue
            known.append((g,kind))
        known_mask=unary_union([g for g,t in known]).buffer(10)
        osm=[]
        for g,t in roads:
            rest=g.difference(known_mask)
            if not rest.is_empty:osm.append((rest,t))
        identified_mask=unary_union([g for g,t in known+osm]).buffer(10)
        local=[]
        for g,t in unknown:
            rest=g.difference(identified_mask)
            if not rest.is_empty:local.append((rest,t))
        roads=known+osm+local
    CACHE[k]=(border,roads,buildings)
    return CACHE[k]
# Line parts
def line_parts(g):
    if g.geom_type in ('LineString','LinearRing'):yield g
    elif g.geom_type=='Polygon':yield g.exterior
    elif hasattr(g,'geoms'):
        for v in g.geoms:yield from line_parts(v)
# Draw
def draw(ax,k,to_geo,plume=False):
    from matplotlib.collections import LineCollection
    border,roads,buildings=layers(k)
    limits=(ax.get_xlim(),ax.get_ylim())
    outline=[]
    for g in buildings:
        for part in line_parts(g):
            x,y=part.xy;outline.append(list(zip(*to_geo.transform(x,y))))
    if outline:
        if plume:ax.add_collection(LineCollection(outline,colors='white',linewidths=1.0,alpha=.6,zorder=8,clip_on=True))
        ax.add_collection(LineCollection(outline,colors='#81708b',linewidths=.40,alpha=.8,zorder=8.2,clip_on=True))
    for category in ['other','collector','secondary','primary']:
        arr=[]
        for g,kind in roads:
            if road_class(kind)!=category:continue
            for part in line_parts(g):
                x,y=part.xy;arr.append(list(zip(*to_geo.transform(x,y))))
        if arr:
            st=ROAD_STYLES[category]
            if category!='other':ax.add_collection(LineCollection(arr,colors='white',linewidths=st['width']+.6,alpha=.70,zorder=7,clip_on=True))
            ax.add_collection(LineCollection(arr,colors=st['color'],linewidths=st['width'],linestyles=st['style'],alpha=.88,zorder=7.2,clip_on=True))
    b=[]
    for part in line_parts(border):
        x,y=part.xy;b.append(list(zip(*to_geo.transform(x,y))))
    ax.add_collection(LineCollection(b,colors='white',linewidths=4.1 if plume else 3.0,alpha=1,zorder=24,clip_on=True));ax.add_collection(LineCollection(b,colors='#122f40',linewidths=2.3 if plume else 1.65,alpha=1,zorder=25,clip_on=True))
    ax.set_xlim(*limits[0]);ax.set_ylim(*limits[1])
# Export metadata
def export_metadata():
    result={}
    for k in ['VM','NC']:
        b,r,h=layers(k);result[k]=dict(boundary_file='v_maria/vm_limite.kmz' if k=='VM' else 'n_contagem/nc_limite.kmz',boundary_area_m2=b.area,road_features=len(r),road_classes={c:sum(road_class(t)==c for g,t in r) for c in ROAD_STYLES},classification='Provided hier_legal: arterial/rodovia primary and secondary; coletora principal/vicinal collector. Municipal or missing hierarchy remains local/unclassified. OSM highway fills uncovered context.',building_features=len(h),names_drawn=False,source='Provided CMAS/vias/malha_viaria.shp (EPSG:31983), reprojected to EPSG:32723; © OpenStreetMap contributors',cartographic_matching_tolerance_m=10,license='OSM complement: ODbL; supplied road dataset provenance retained as received',url='https://www.openstreetmap.org/copyright')
    (R/'output/auditoria/Contexto_cartografico.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    return result
