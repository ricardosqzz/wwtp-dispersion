# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/auditoria/Auditoria_consolidada.json | .read_text.
# Entrada: {path} | path.read_text.
# Entrada: E:/copasa_map/output/cmas_poster/dados_cenarios24h/Cenarios24h_manifesto.json | .read_text.
# Entrada: selected['csv'] | np.loadtxt.
# Entrada: E:/copasa_map/output/cmas_poster/figuras/Faixas_concentracao_poster.json | .read_text.
# Campos/chaves em D: grid, sources_aermod.
# Campos/chaves em s: params, process, type, x, xy, y.
# Campos/chaves em event: period_end, period_start.
# Campos/chaves em v: color, finite_coverage, label, model, style, unit, width, x, y.
# Campos/chaves em selected: csv, period_end, period_start.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}.{ext} | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}_previa.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}_poster.{ext} | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}_poster.png | fig.savefig.
# Saída: plt.figure(figsize=(wc / 2.54, hc / 2.54)) | save.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Faixas_concentracao_poster.json | .write_text.
# Saída: E:/copasa_map/output/cmas_poster/index.html | .write_text.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Resultados_historicos.json | .write_text.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Cartografia_metadados.json | .write_text.
# Campos/chaves gerados em record: poster_figure_cm, poster_scale.
# CÓDIGO DO PROCESSAMENTO

"""Encarte geográfico COPASA, com escalas físicas e campos nativos completos."""
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
import json,html
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm,LinearSegmentedColormap
from matplotlib.patches import Polygon,Patch,Rectangle
from matplotlib.ticker import FuncFormatter
from matplotlib.text import Text
from scipy.interpolate import LinearNDInterpolator
from matplotlib.lines import Line2D
from pyproj import Transformer,Geod
from contexto_ete import draw as draw_context,export_metadata,ROAD_STYLES
from geometria_ete import limite
R=Path(_cp_texto('', 'posix'));O=R/'output/cmas_poster';F=O/'figuras';F.mkdir(parents=True,exist_ok=True)
D=json.loads((R/'output/auditoria/Auditoria_consolidada.json').read_text(encoding='utf8'))
TO_GEO=Transformer.from_crs(32723,4326,always_xy=True);GEOD=Geod(ellps='WGS84')
plt.rcParams.update({'font.family':'Arial','svg.fonttype':'path','pdf.fonttype':42,'font.size':9,'axes.titlesize':11,'axes.linewidth':.7})
COL={'PRE':'#52a8ad','UASB':'#e5a653','FB':'#8e77a3','CALHA':'#bc5362'}
META={};RESULTS=[]
# Centre
def centre(k):
    x0,y0,x1,y1=limite(k).bounds
    return (x0+x1)/2,(y0+y1)/2
# Bounds
def bounds(k,span):
    lon,lat=TO_GEO.transform(*centre(k))
    return GEOD.fwd(lon,lat,270,span/2)[0],GEOD.fwd(lon,lat,180,span/2)[1],GEOD.fwd(lon,lat,90,span/2)[0],GEOD.fwd(lon,lat,0,span/2)[1]
# Frame
def frame(ax,k,span,scale):
    x0,y0,x1,y1=bounds(k,span)
    ax.set_xlim(x0,x1);ax.set_ylim(y0,y1);ax.set_aspect((x1-x0)/(y1-y0));ax.set_facecolor('#f5f5f1');ax.set_xlabel('');ax.set_ylabel('')
    ax.set_xticks(np.linspace(x0,x1,5)[1:-1]);ax.set_yticks(np.linspace(y0,y1,5)[1:-1]);dec=4 if span<=500 else 3
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.{dec}f}°W'));ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{abs(v):.{dec}f}°S'))
    ax.tick_params(axis='both',labelsize=8,length=2,pad=3);ax.tick_params(axis='y',labelrotation=90,pad=5.3)
    for t in ax.get_yticklabels():t.set(ha='center',va='center',rotation_mode='anchor')
    for s in ax.spines.values():s.set(visible=True,color='#35413d',linewidth=.7,zorder=30)
    ax.grid(alpha=.09,linewidth=.35)
    ax.text(.963,.955,'N',transform=ax.transAxes,ha='center',va='bottom',fontsize=8,fontweight='bold',color='#39433f',zorder=40)
    ax.annotate('',xy=(.963,.946),xytext=(.963,.858),xycoords='axes fraction',arrowprops=dict(arrowstyle='-|>',mutation_scale=12,lw=1,color='#39433f',shrinkA=0,shrinkB=0),zorder=40)
    datum=ax.text(.97,.025,f'Datum: WGS 84\nGeographic · EPSG:4326\nScale 1:{scale:,}',transform=ax.transAxes,ha='right',va='bottom',multialignment='center',fontsize=5.5,linespacing=1.2,color='#646962',bbox=dict(boxstyle='round,pad=.35,rounding_size=.15',facecolor='white',edgecolor='#b9bdb6',linewidth=.45,alpha=.96),zorder=40)
    datum.set_gid('datum_scale');ax._datum=datum;ax._scale=scale;ax._span=span
    length=100 if span<=500 else 200 if span<=1200 else 500;x=x0+(x1-x0)*.07;y=y0+(y1-y0)*.075
    xm=GEOD.fwd(x,y,90,length/2)[0];xe=GEOD.fwd(x,y,90,length)[0];h=(y1-y0)*.012
    for a,b,c in [(x,xm,'#4b504c'),(xm,xe,'white')]:ax.add_patch(Rectangle((a,y),b-a,h,facecolor=c,edgecolor='#4b504c',lw=.45,zorder=40))
    for xx,lab in [(x,'0'),(xm,str(length//2)),(xe,f'{length} m')]:ax.text(xx,y-(y1-y0)*.016,lab,ha='center',va='top',fontsize=6,zorder=40)
    return x0,y0,x1,y1
# Sources
def sources(ax,k,filled=True):
    for n,s in D['sources_aermod'].items():
        if not n.startswith(k+'_'):continue
        if s['type']=='AREACIRC':
            a=np.linspace(0,2*np.pi,101);xx=s['x']+s['params'][2]*np.cos(a);yy=s['y']+s['params'][2]*np.sin(a)
        else:xx,yy=np.asarray(s['xy']).T
        xy=np.column_stack(TO_GEO.transform(xx,yy));color=COL[s['process'].split('_')[1]]
        ax.add_patch(Polygon(xy,facecolor=color if filled else 'none',edgecolor='#25414d',lw=.65 if filled else .35,zorder=20))
# Physical layout
def physical_layout(rows,span,scale,bottom_override=None):
    side=span/scale*100;left,gap,right,top,bottom=(1.35,2.25,1.55,1.,2.5) if rows==1 else (1.35,1.9,1.55,1.2,3.0);rowgap=1.6 if rows>1 else 0
    if bottom_override is not None:bottom=bottom_override
    wc=left+2*side+gap+right;hc=bottom+rows*side+(rows-1)*rowgap+top
    fig=plt.figure(figsize=(wc/2.54,hc/2.54));axs=[]
    for j in range(rows):
        row=[]
        for i in range(2):row.append(fig.add_axes([(left+i*(side+gap))/wc,(bottom+(rows-1-j)*(side+rowgap))/hc,side/wc,side/hc]))
        axs.append(row)
    return fig,np.array(axs),wc,hc
# Save
def save(fig,name,poster_scale=None):
    axes=[a for a in fig.axes if hasattr(a,'_span')];fig.canvas.draw();native=[]
    for ax in axes:
        paper=ax.get_position().width*fig.get_figwidth()*.0254;actual=ax._span/paper;assert abs(actual-ax._scale)<.01,(name,actual,ax._scale)
        native.append(dict(scale=ax._scale,measured_scale=actual,span_m=ax._span,axis_width_cm=paper*100))
    record=dict(native_scale=axes[0]._scale,figure_cm=(fig.get_size_inches()*2.54).tolist(),maps=native)
    for ext in ['svg','pdf']:fig.savefig(F/f'{name}.{ext}',facecolor='white')
    fig.savefig(F/f'{name}.png',dpi=600,facecolor='white');fig.savefig(F/f'{name}_previa.png',dpi=180,facecolor='white')
    if poster_scale:
        factor=axes[0]._scale/poster_scale;fig.set_size_inches(fig.get_size_inches()*factor,forward=True)
        for t in fig.findobj(match=Text):t.set_fontsize(t.get_fontsize()*factor)
        for ax in axes:
            ax._datum.set_text((f'WGS 84\nScale 1:{poster_scale:,}') if getattr(ax,'_compact_datum',False) else f'Datum: WGS 84\nGeographic · EPSG:4326\nScale 1:{poster_scale:,}');ax.tick_params(axis='both',pad=3*factor,length=2*factor);ax.tick_params(axis='y',pad=5.3*factor)
            for t in ax.texts:
                if getattr(t,'arrow_patch',None):t.arrow_patch.set_mutation_scale(12*factor)
        fig.canvas.draw();record['poster_scale']=poster_scale;record['poster_figure_cm']=(fig.get_size_inches()*2.54).tolist()
        for ax in axes:assert abs(ax._span/(ax.get_position().width*fig.get_figwidth()*.0254)-poster_scale)<.01
        for ext in ['svg','pdf']:fig.savefig(F/f'{name}_poster.{ext}',facecolor='white')
        fig.savefig(F/f'{name}_poster.png',dpi=300,facecolor='white')
    META[name]=record;plt.close(fig)
# Read field
def read_field(path,km=False):
    v=[]
    for line in path.read_text(encoding='cp1252').splitlines():
        q=line.split()
        if len(q)<3:continue
        try:x,y,c=map(float,q[:3])
        except ValueError:continue
        if km:x*=1000;y*=1000
        if np.isfinite([x,y,c]).all() and c>=0:v.append([x,y,c])
    a=np.array(v);assert len(a)>20 and a[:,2].max()>0,str(path);_,idx=np.unique(a[:,:2],axis=0,return_index=True);return a[idx]
# Event title
def event_title(event):
    from datetime import datetime
    start=datetime.fromisoformat(event['period_start']);end=datetime.fromisoformat(event['period_end'])
    if start.hour==0:return start.strftime('%d %b %Y')+' · 00:00–24:00'
    return f'{start.day:02d}–{end.day:02d} '+end.strftime('%b %Y')+f' · {start:%H:%M}–{end:%H:%M}'

# Plume pair
def plume_pair(period='24',event=False):
    cmap=LinearSegmentedColormap.from_list('plume',['#fff8db','#e5efba','#b6dfbe','#73c7bc','#35a7b3','#227d9e','#245482','#183459'])
    span,scale=1000,10000
    fig,axs,wc,hc=physical_layout(2,span,scale);vmax=1200 if period=='24' else 500;norm=LogNorm(.1,vmax);levels=np.geomspace(.1,vmax,65);info=[]
    events=json.loads((O/'dados_cenarios24h/Cenarios24h_manifesto.json').read_text(encoding='utf8'))['events'] if event else []
    for j,(k,suffix,group) in enumerate([('VM','V-MARIA','001'),('NC','N-CONT','002')]):
        paths=[R/f'CMAS/24H1G{group}_{suffix}.PLT',R/f'CMAS/RANK(ALL)_ODOR_24HR_CONC_C_{suffix}.DAT'] if period=='24' else [R/f'CMAS/AN00G{group}_{suffix}.PLT',R/f'CMAS/RANK(ALL)_ODOR_8760HR_CONC_C_{suffix}.DAT']
        for i,path in enumerate(paths):
            model=['AERMOD','CALPUFF'][i]
            selected=next((v for v in events if v['unit']==k and v['model']==model),None)
            if selected:
                path=Path(selected['csv']);a=np.loadtxt(path,delimiter=',',skiprows=1);_,idx=np.unique(a[:,:2],axis=0,return_index=True);a=a[idx]
            else:a=read_field(path,km=i==1)
            ax=axs[j,i];x0,y0,x1,y1=frame(ax,k,span,scale);cx,cy=centre(k)
            gx=np.linspace(cx-span*.65,cx+span*.65,401);gy=np.linspace(cy-span*.65,cy+span*.65,401);near=(abs(a[:,0]-cx)<span*.7)&(abs(a[:,1]-cy)<span*.7)

            gx=np.unique(np.r_[gx,a[near,0]]);gy=np.unique(np.r_[gy,a[near,1]]);xx,yy=np.meshgrid(gx,gy)
            points=a[:,:2]-[cx,cy];query=np.column_stack((xx.ravel()-cx,yy.ravel()-cy))
            interpolator=LinearNDInterpolator(points,a[:,2],fill_value=np.nan)
            zz=interpolator(query).reshape(xx.shape)
            lo,la=TO_GEO.transform(xx,yy);inside=(lo>=x0)&(lo<=x1)&(la>=y0)&(la<=y1)
            coverage=float(np.isfinite(zz[inside]).mean());assert coverage>.999,(path,coverage)
            m=ax.contourf(lo,la,np.maximum(zz,1e-12),levels=levels,cmap=cmap,norm=norm,extend='both',zorder=2);m.set_edgecolor('face');m.set_linewidth(.1)
            ax.contour(lo,la,zz,levels=[v for v in [1,10,100,1000] if v<vmax],colors='#24445b',alpha=.20,linewidths=.35,zorder=4)
            draw_context(ax,k,TO_GEO,True);sources(ax,k,False)
            label=model
            if period!='24':label+=' · annual mean' if i==0 else ' · max. 8,760 h mean'
            title=f'WWTP {j+1} · {label}'+('\n'+event_title(selected) if selected else '')
            ax.set_title(title,pad=6,fontsize=9.2 if event or period!='24' else 8.7,fontweight='bold',linespacing=1.4)
            nl,nt=TO_GEO.transform(a[:,0],a[:,1]);visible=(nl>=x0)&(nl<=x1)&(nt>=y0)&(nt<=y1)
            raw=a[visible,2].max();draw=float(np.nanmax(zz[inside]));assert draw>=raw*(1-1e-5),(path,draw,raw)
            fit=interpolator(points);node_error=float(np.nanmax(abs(fit-a[:,2])))
            assert node_error<1e-4,(path,node_error)
            info.append(dict(unit=k,model=model,period=period,source=str(path),native_receptors=len(a),maximum_native=float(a[:,2].max()),maximum_displayed=draw,maximum_native_in_frame=float(raw),finite_coverage=coverage,interpolation='Linear triangulation of native receptor values; no extrapolation or IDW; display only',native_node_max_error=node_error,interpolated_minimum=float(np.nanmin(zz[inside])),statistic='coherent 24h event' if event else 'receptor-wise highest 24h envelope' if period=='24' else ('native annual mean' if i==0 else 'highest 8760h mean'),simultaneous=event,period_start=selected['period_start'] if selected else None,period_end=selected['period_end'] if selected else None))
    left=axs[1,0].get_position().x0;right=axs[1,1].get_position().x1;cbax=fig.add_axes([left,2.0/hc,right-left,.22/hc]);cb=fig.colorbar(m,cax=cbax,orientation='horizontal',ticks=[.1,1,10,100,1000] if period=='24' else [.1,1,10,100,500]);cb.ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'));cb.ax.tick_params(labelsize=8,length=2,pad=2);cb.set_label('H$_2$S concentration (µg/m³)',fontsize=9,labelpad=3)
    context_legend(fig,.30/hc);credit(fig,.06/hc)
    name='Cenarios_24h_eventos_coerentes' if event else 'Comparacao_24h_pre_harmonizacao' if period=='24' else 'Comparacao_anual_8760h_pre_harmonizacao';save(fig,name,5800 if event else 6000 if period=='24' else None);RESULTS.extend(info)
# Context handles
def context_handles():
    return [Line2D([],[],color='#122f40',linewidth=1.8,label='WWTP boundary')]+[Line2D([],[],color=v['color'],linewidth=v['width'],linestyle=v['style'],label=v['label']) for v in ROAD_STYLES.values()]+[Patch(facecolor='none',edgecolor='#756083',linewidth=.65,label='Building outlines')]
# Context legend
def context_legend(fig,y):
    fig.legend(handles=context_handles(),loc='lower center',bbox_to_anchor=(.5,y),ncol=3,frameon=False,fontsize=7.1,columnspacing=2,labelspacing=.7,alignment='left')
# Credit
def credit(fig,y):
    fig.text(.5,y,'Roads: supplied RMBH dataset + © OpenStreetMap contributors · openstreetmap.org/copyright',ha='center',va='bottom',fontsize=5.6,color='#606a70')

# Poster concentration rows
def poster_concentration_rows(only_annual=False):
    """Four matching map frames per row, plus an explicitly empty annual layout."""
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    span,scale=1000,8000;side=span/scale*100
    left,gap,right,bottom,top=1.4,1.0,.3,3.2,1.2
    wc,hc=left+4*side+3*gap+right,bottom+side+top
    palette=['#fff8db','#e5efba','#b6dfbe','#73c7bc','#35a7b3','#227d9e','#245482','#183459']
    cmap=LinearSegmentedColormap.from_list('plume_poster',palette);records=[]
    if only_annual and (F/'Faixas_concentracao_poster.json').exists():records=json.loads((F/'Faixas_concentracao_poster.json').read_text(encoding='utf8'))['historical_24h']
    panels=[('VM','V-MARIA','001','AERMOD'),('VM','V-MARIA','001','CALPUFF'),('NC','N-CONT','002','AERMOD'),('NC','N-CONT','002','CALPUFF')]
    for placeholder in ([True] if only_annual else [False,True]):
        fig=plt.figure(figsize=(wc/2.54,hc/2.54));axes=[]
        for i,(unit,suffix,group,model) in enumerate(panels):
            ax=fig.add_axes([(left+i*(side+gap))/wc,bottom/hc,side/wc,side/hc]);axes.append(ax)
            x0,y0,x1,y1=frame(ax,unit,span,scale)
            ax.tick_params(labelsize=10,pad=3);ax.tick_params(axis='y',pad=5.3)
            for t in ax.texts:t.set_fontsize(8.5 if t.get_gid()!='datum_scale' else 7)
            if placeholder:
                ax.set_facecolor('#f3f5f3')
                ax.text(.5,.5,'Annual results\npending',ha='center',va='center',transform=ax.transAxes,fontsize=12,color='#526675',linespacing=1.4,bbox=dict(facecolor='white',edgecolor='#b8c5ca',linewidth=.5,pad=8,alpha=.96),zorder=28)
            else:
                path=R/(f'CMAS/24H1G{group}_{suffix}.PLT' if model=='AERMOD' else f'CMAS/RANK(ALL)_ODOR_24HR_CONC_C_{suffix}.DAT')
                a=read_field(path,km=model=='CALPUFF');cx,cy=centre(unit)
                near=(abs(a[:,0]-cx)<span*.7)&(abs(a[:,1]-cy)<span*.7)
                gx=np.unique(np.r_[np.linspace(cx-span*.65,cx+span*.65,401),a[near,0]])
                gy=np.unique(np.r_[np.linspace(cy-span*.65,cy+span*.65,401),a[near,1]])
                xx,yy=np.meshgrid(gx,gy);points=a[:,:2]-[cx,cy]
                interpolation=LinearNDInterpolator(points,a[:,2],fill_value=np.nan)
                z=interpolation(np.column_stack((xx.ravel()-cx,yy.ravel()-cy))).reshape(xx.shape)
                lon,lat=TO_GEO.transform(xx,yy);inside=(lon>=x0)&(lon<=x1)&(lat>=y0)&(lat<=y1)
                coverage=float(np.isfinite(z[inside]).mean());assert coverage==1
                norm=LogNorm(.1,1200)
                m=ax.contourf(lon,lat,np.maximum(z,1e-12),levels=np.geomspace(.1,1200,65),cmap=cmap,norm=norm,extend='both',zorder=2)
                m.set_edgecolor('face');m.set_linewidth(.1)
                ax.contour(lon,lat,z,levels=[1,10,100,1000],colors='#24445b',alpha=.20,linewidths=.35,zorder=4)
                nl,nt=TO_GEO.transform(a[:,0],a[:,1]);visible=(nl>=x0)&(nl<=x1)&(nt>=y0)&(nt<=y1)
                raw=float(a[visible,2].max());peak=float(np.nanmax(z[inside]));node_error=float(np.nanmax(abs(interpolation(points)-a[:,2])))
                assert peak>=raw-1e-5 and node_error<1e-4
                records.append(dict(unit=unit,model=model,source=str(path),statistic='native highest 24 h per receptor',maximum_native=float(a[:,2].max()),maximum_displayed=peak,maximum_native_in_frame=raw,finite_coverage=coverage,native_node_max_error=node_error,historical_before_rerun=True))
            draw_context(ax,unit,TO_GEO,not placeholder);sources(ax,unit,False)
            ax.set_title(f"WWTP {1 if unit=='VM' else 2} · {model}",y=1.0,pad=7,fontweight='bold',fontsize=12)
        cbax=fig.add_axes([axes[0].get_position().x0,2.05/hc,axes[-1].get_position().x1-axes[0].get_position().x0,.24/hc])
        if placeholder:
            cb=fig.colorbar(ScalarMappable(norm=Normalize(0,1),cmap=cmap),cax=cbax,orientation='horizontal',ticks=[])
            cb.set_label('Maximum calendar-year mean H$_2$S (µg/m³) · numerical range pending',fontsize=11,labelpad=5)
        else:
            cb=fig.colorbar(m,cax=cbax,orientation='horizontal',ticks=[.1,1,10,100,1000]);cb.ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'));cb.ax.tick_params(labelsize=10,length=2,pad=2);cb.set_label('H$_2$S concentration (µg/m³)',fontsize=11,labelpad=4)
        fig.legend(handles=context_handles(),loc='lower center',bbox_to_anchor=(.5,.22/hc),ncol=6,frameon=False,fontsize=10,columnspacing=2,alignment='left')
        credit(fig,.025/hc)
        stem='Comparacao_anual_placeholder' if placeholder else 'Comparacao_24h_faixa'
        save(fig,stem,scale)
        META[stem].update(placeholder=placeholder,panels=4,columns=['WWTP 1 · AERMOD','WWTP 1 · CALPUFF','WWTP 2 · AERMOD','WWTP 2 · CALPUFF'])
        if placeholder:META[stem].update(concentrations_plotted=False,numerical_color_range=None,statistic='Maximum across calendar-year means at each receptor',requires='New AERMOD hourly POST with annual masks and equivalent calendar-year CALPUFF/CALPOST RANK for matching years; existing rolling 8760 h RANK not substituted; native multi-year ANNUAL mean is a different summary')
    (F/'Faixas_concentracao_poster.json').write_text(json.dumps(dict(historical_24h=records,annual_status='placeholder; no concentration values plotted',annual_statistic='Maximum across calendar-year means at each receptor; confirmed by author',poster_scale=scale),indent=2),encoding='utf8')
# Gallery
def gallery():
    cards=[('Fontes_privacidade','Sources and location','Mapped emitting surfaces, anonymous surrounding road hierarchy and building outlines. Supplied RMBH road data are complemented by OpenStreetMap where coverage is absent. No satellite imagery or facility names.'),('Grade_comum_privacidade','Common receptor grid','1,790 model records at 1,789 distinct terrain-processed locations. All 40 supplied sensitive IDs are retained: NC_6 and NC_BAG intentionally share one coordinate. Orange markers identify sensitive receptors. Regional receptors outside the close-up remain in both model inputs.'),('Comparacao_24h_pre_harmonizacao','Receptor-wise maximum 24 h envelope · poster','Each native PLT/RANK receptor uses its highest 24 h value, possibly on a different date. The envelope is not a simultaneous plume. All four panels share a logarithmic concentration scale. Linear triangulation preserves receptor values without extrapolation.'),('Cenarios_24h_eventos_coerentes','Complement: worst date-specific 24 h events','All receptors in each panel share its displayed 24 h interval. The worst interval is selected independently for each model and plant. Historical runs before emission corrections. AERMET time convention remains to be confirmed.'),('Comparacao_anual_8760h_pre_harmonizacao','Complement: long-duration fields','AERMOD annual mean and CALPOST maximum 8,760 h mean are different statistics. These historical outputs are not a controlled annual model comparison.')]
    if (F/'Comparacao_anual_placeholder_previa.png').exists():
        cards[2:2]=[('Comparacao_24h_faixa','Poster: maximum 24 h envelopes','Four aligned panels share one concentration scale. Historical outputs remain in use until the new runs are supplied.'),('Comparacao_anual_placeholder','Poster: maximum calendar-year mean · pending','The author selected the highest calendar-year mean at each receptor across matched modelled years. The present figure is a layout placeholder, without annual concentrations or numerical colour limits. New AERMOD hourly POST and equivalent per-year CALPUFF/CALPOST RANK are required. Neither the existing rolling 8,760 h maximum nor the native multi-year mean is substituted for this annual envelope.')]
    s=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WWTP · maps</title><style>body{font:16px Arial,sans-serif;max-width:1250px;margin:30px auto;padding:0 24px;color:#173445;background:#f4f7f8}article{background:white;margin:25px 0;padding:22px;border:1px solid #d7e0e3}img{display:block;max-width:100%;height:auto;margin:16px auto}h1,h2{color:#173445}a{color:#006b8d;margin-right:15px}p{line-height:1.5}</style><h1>Wastewater treatment plants · map viewer</h1><p>Existing dispersion results, before the corrected inventory and geometry are rerun. Date-specific 24 h fields have been extracted from hourly results and checked against native ranked maxima. Contours use linear triangulation without IDW smoothing or extrapolation. The common receptor grid and input emissions have not changed in this map revision. The three WWTP 2 UASB polygons were regularized to equal areas, preserving the total 1,309 m².</p><p>Background: © OpenStreetMap contributors, <a href="https://www.openstreetmap.org/copyright">ODbL</a>. Provided KMZ plant boundaries; surrounding roads and building outlines are shown without names.</p><p><a href="Poster_CMAS_Session05_WWTP.pdf">Poster PDF</a><a href="Poster_CMAS_Session05_WWTP.pptx">PowerPoint</a><a href="../auditoria/Origem_cenarios_24h.pdf">24 h methods (Portuguese)</a></p>']
    s[0]=s[0].replace('The common receptor grid and input emissions have not changed in this map revision.','The new import grid preserves the supplied sensitive IDs and existing terrain data. The historical concentration maps have not been rerun with that input.').replace('Background: © OpenStreetMap contributors','Background: supplied RMBH road dataset (CMAS/vias), complemented by © OpenStreetMap contributors')
    for unit in ['NC','VM','NC_VM']:
        s.append(f'<p>{unit}: <a href="../entradas_corrigidas/AERMOD/Grade_Receptora_{unit}_AERMOD.csv">AERMOD View · CSV</a><a href="../entradas_corrigidas/CALPUFF/Grade_Receptora_{unit}_CALPUFF.xls">CALPUFF View · XLS</a></p>')
    s.append('<p><a href="../Receptores_importacao_AERMOD_CALPUFF.zip">Receptor import package</a><a href="../entradas_corrigidas/LEIA_PRIMEIRO.md">Import instructions</a><a href="../auditoria/Guia_grade_e_poster_COPASA.pdf">Interpretation guide (Portuguese)</a></p>')
    for stem,title,note in cards:s.append(f'<article><h2>{html.escape(title)}</h2><p>{html.escape(note)}</p><img loading="eager" src="figuras/{stem}_previa.png" alt="{html.escape(title)}"><p><a href="figuras/{stem}.pdf">PDF · vector</a><a href="figuras/{stem}.svg">SVG · vector</a><a href="figuras/{stem}.png">PNG · high resolution</a></p></article>')
    (O/'index.html').write_text('\n'.join(s+['</html>']),encoding='utf8')
# Main
def main():
    if (R/'CMAS/AERMOD/01_GWWTP1.POS').exists() and (R/'output/comparacao_modelos/Campos_nativos.npz').exists():
        from atualizar_cartografia_cmas import main as current_main
        current_main()
        return
    fig,axs,_,hc=physical_layout(1,500,4000)
    for ax,k,label in zip(axs[0],['VM','NC'],['WWTP 1','WWTP 2']):frame(ax,k,500,4000);draw_context(ax,k,TO_GEO);sources(ax,k);ax.set_title(label,pad=5,fontweight='bold')
    handles=[Patch(facecolor=c,edgecolor='#25414d',linewidth=.5,label={'PRE':'Preliminary treatment','UASB':'UASB reactors','FB':'Trickling filters','CALHA':'Outlet weir'}[p]) for p,c in COL.items()]
    handles+=context_handles()
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.035),ncol=4,frameon=False,fontsize=8.0,columnspacing=1.5,handletextpad=.55,alignment='left');credit(fig,.08/hc);save(fig,'Fontes_privacidade',2500)
    fig,axs,_,hc=physical_layout(1,1000,10000)
    for ax,k,label in zip(axs[0],['VM','NC'],['WWTP 1','WWTP 2']):
        frame(ax,k,1000,10000);draw_context(ax,k,TO_GEO)
        for sensitive,color,size in [(0,'#20566f',13),(1,'#c87536',25)]:
            points=[v for v in D['grid'] if v.get('sensitive',0)==sensitive];lon,lat=TO_GEO.transform([v['x'] for v in points],[v['y'] for v in points]);ax.scatter(lon,lat,s=size,facecolor=color,edgecolor='white',linewidth=.3,alpha=.92,zorder=9+sensitive)
        sources(ax,k,False);ax.set_title(label,pad=5,fontweight='bold')
    fig.legend(handles=[Line2D([],[],marker='o',color='none',markerfacecolor='#20566f',markeredgecolor='white',markersize=5,label='Regular receptors'),Line2D([],[],marker='o',color='none',markerfacecolor='#c87536',markeredgecolor='white',markersize=5,label='Sensitive receptors')]+context_handles(),loc='lower center',bbox_to_anchor=(.5,.30/hc),ncol=4,frameon=False,fontsize=7.5,columnspacing=1.6,labelspacing=.7,alignment='left')
    credit(fig,.08/hc);save(fig,'Grade_comum_privacidade');plume_pair('24',True);plume_pair('24');plume_pair('annual')
    poster_concentration_rows()
    (F/'Resultados_historicos.json').write_text(json.dumps(RESULTS,indent=2),encoding='utf8');(F/'Cartografia_metadados.json').write_text(json.dumps(META,indent=2),encoding='utf8');gallery();print(json.dumps(dict(figures=len(META),context=export_metadata(),complete_fields=all(v['finite_coverage']>.999 for v in RESULTS),results=RESULTS)))
if __name__=='__main__':main()
