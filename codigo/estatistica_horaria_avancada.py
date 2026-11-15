# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: files[j] | np.loadtxt.
# Entrada: E:/copasa_map/output/auditoria/Auditoria_consolidada.json | .read_text.
# Entrada: E:/copasa_map/temp/cache_nova_modelagem/AERMOD_{k}_1h.json | .read_text.
# Entrada: E:/copasa_map/temp/cache_nova_modelagem/CALPUFF_{k}_1h.json | .read_text.
# Entrada: E:/copasa_map/temp/cache_nova_modelagem/AERMOD_{k}_1h.npy | np.load.
# Entrada: E:/copasa_map/temp/cache_nova_modelagem/CALPUFF_{k}_1h.npy | np.load.
# Entrada: E:/copasa_map/output/comparacao_modelos/Pares_nativos_{k}_24h.csv | pd.read_csv.
# Entrada: E:/copasa_map/output/comparacao_modelos/Meteorologia_AERMET.csv | pd.read_csv.
# Entrada: E:/copasa_map/output/comparacao_modelos/Estatistica_horaria_por_receptor.csv | pd.read_csv.
# Entrada: E:/copasa_map/output/comparacao_modelos/Estatistica_avancada.json | .read_text.
# Campos/chaves em art: boxes, medians.
# Campos/chaves em meta: source, start_times, xy.
# Campos/chaves em D: grid.
# Campos/chaves em a: area, base, boxes, height, medians, old_flux, params.
# Campos/chaves em v: area, base, height, old_flux, sigma, x, y.
# Campos/chaves em p: distance_m, x, y.
# Campos/chaves em hm: codes, xy.
# Campos/chaves em cm: start_times, xy.
# Campos/chaves em met: calm, missing.
# Campos/chaves em g: x, y.
# Campos/chaves em row: AERMOD_P95, AERMOD_mean, CALPUFF_P95, CALPUFF_mean.
# Campos/chaves em u: boxplot_eligible, distance_m, monitoring_location, screen_active.
# Campos/chaves em active: x, y.
# Campos/chaves em ax.spines: bottom, left.
# Campos/chaves em r: distance_m, receptor_id, unit.
# Campos/chaves em d: model, values.
# Campos/chaves em data: boxplot_eligible, unit.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}.{ext} | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{name}_previa.png | fig.savefig.
# Saída: {fig} | save.
# Saída: {fig} | pdf.savefig.
# Campos/chaves gerados em row: boxplot_eligible.
# receptor_id: identificador do receptor.
# CÓDIGO DO PROCESSAMENTO

"""Distribuições horárias por receptor, sem tratar um modelo como observação.

Ano completo de referência: 2024. Horas válidas nativas em cada modelo.
Sem ajuste do relógio por otimização da concordância. Limite de exibição 0,7
ug/m3 é uma referência baixa da faixa de percepção, não um limite universal.
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
import json,csv,datetime as dt,re,sys,math
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance,ks_2samp
from scipy.spatial import cKDTree
from shapely.geometry import Point
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Patch
from auditar_e_preparar import parse_aer,parse_cal
from geometria_ete import limite
from comparar_modelos_cmas import csvout,dump
R=Path(_cp_texto('', 'posix'));O=R/'output/comparacao_modelos';F=R/'output/cmas_poster/figuras';C=R/'temp/cache_nova_modelagem';CUT=.7
COL={'AERMOD':'#2465a8','CALPUFF':'#e3873a'}
plt.rcParams.update({'font.family':'Arial','font.size':11,'pdf.fonttype':42,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False,'axes.formatter.useoffset':False})
# Save
def save(fig,name):
    for ext in ['svg','pdf']:fig.savefig(F/f'{name}.{ext}',facecolor='white')
    fig.savefig(F/f'{name}.png',dpi=450,facecolor='white');fig.savefig(F/f'{name}_previa.png',dpi=150,facecolor='white');plt.close(fig)
# Statsbox
def statsbox(row,model,label=''):
    return dict(label=label,whislo=float(row[f'{model}_P05']),q1=float(row[f'{model}_P25']),med=float(row[f'{model}_P50']),q3=float(row[f'{model}_P75']),whishi=float(row[f'{model}_P95']),fliers=[])
# Add boxes
def add_boxes(ax,stats,pos,color,width=.30):
    art=ax.bxp(stats,positions=pos,widths=width,showfliers=False,patch_artist=True,manage_ticks=False)
    for z in art['boxes']:z.set(facecolor=color,alpha=.72,edgecolor=color,linewidth=1.1)
    for name in ['whiskers','caps']:
        for z in art[name]:z.set(color=color,linewidth=1)
    for z in art['medians']:z.set(color='#182f3d',linewidth=1.3)
    return art
# Validate exports
def validate_exports(k,arr,meta):
    files=sorted((R/f'CMAS/CALPUFF/ODOR-{k}').rglob('*_1HR_CONC.DAT'));out=[]
    if not files:return dict(available_files=0,sampled=[])
    dates={s:i for i,s in enumerate(meta['start_times'])};xy=np.array(meta['xy'])
    for j in sorted(set(np.linspace(0,len(files)-1,min(9,len(files))).astype(int))):
        p=files[j];ma=re.search(r'(\d{4})_M(\d{2})_D(\d{2})_(\d{2})(\d{2})',p.name);date=dt.datetime(*map(int,ma.groups())).isoformat();assert date in dates,(p,date)
        a=np.loadtxt(p,skiprows=6);assert len(a)==arr.shape[1];assert np.allclose(a[:,:2]*1000,xy,atol=.001)
        z=np.asarray(arr[dates[date]],dtype='float64');error=float(abs(a[:,2]-z).max());assert np.allclose(a[:,2],z,rtol=6e-5,atol=1e-6),(p,error)
        out.append(dict(file=str(p),start_label=date,max_abs_error=error,passed=True))
    return dict(available_files=len(files),sampled=out,complete_series_source=meta['source']['path'],all_hours_from_binary=True)
# Main
def main():
    D=json.loads((R/'output/auditoria/Auditoria_consolidada.json').read_text(encoding='utf8'));grid=D['grid'];print('grid keys',list(grid[0]),flush=True)
    monitor=[v for v in grid if v.get('sensitive')];rows=[];poster={};summary={};atlas=[];export_validation={};inputrows=[]
    _,aer=parse_aer(R/'CMAS/AERMOD/H2S_TOTAL.ADI')
    for k in ['VM','NC']:
        _,cal=parse_cal(R/f'CMAS/CALPUFF/CALPUFF-{k}.INP')
        for name,v in cal.items():
            aid='VM_PRE' if name.startswith('VM_PRE') else name;a=aer[aid]
            inputrows.append(dict(unit=k,source_AERMOD=aid,source_CALPUFF=name,ground_elevation_AERMOD_m=a['base'],ground_elevation_CALPUFF_m=v['base'],release_height_AGL_AERMOD_m=a['height'],release_height_AGL_CALPUFF_m=v['height'],absolute_release_AERMOD_m=a['base']+a['height'],absolute_release_CALPUFF_m=v['base']+v['height'],sigma_z_AERMOD_m=a['params'][-1],sigma_z_CALPUFF_m=v['sigma'],mass_AERMOD_g_s=a['old_flux']*a['area'],mass_CALPUFF_g_s=v['old_flux']*v['area']))
        hm=json.loads((C/f'AERMOD_{k}_1h.json').read_text());cm=json.loads((C/f'CALPUFF_{k}_1h.json').read_text());ah=np.load(C/f'AERMOD_{k}_1h.npy',mmap_mode='r');ch=np.load(C/f'CALPUFF_{k}_1h.npy',mmap_mode='r')
        export_validation[k]=validate_exports(k,ch,cm)
        p=pd.read_csv(O/f'Pares_nativos_{k}_24h.csv');xy=p[['x','y']].to_numpy();_,ai=cKDTree(hm['xy']).query(xy);_,ci=cKDTree(cm['xy']).query(xy)
        met=pd.read_csv(O/'Meteorologia_AERMET.csv');asel=(np.array(hm['codes'])//1000000==24)&~met.calm.to_numpy()&~met.missing.to_numpy();csel=np.array([s.startswith('2024-') for s in cm['start_times']]);A=np.asarray(ah[asel][:,ai],dtype='float64');B=np.asarray(ch[csel][:,ci],dtype='float64')
        assert A.shape[0]==8496 and B.shape[0]==8784
        quantiles=[.05,.1,.25,.5,.75,.9,.95,.98,.99];aq=np.quantile(A,quantiles,axis=0);bq=np.quantile(B,quantiles,axis=0)
        near_monitor=[]
        for v in monitor:
            dist,ind=cKDTree(xy).query([v['x'],v['y']])
            if dist<=.01:near_monitor.append((ind,str(v.get('id',v.get('receptor_id',v.get('ID',''))))))
        ids={}
        for ind,ident in near_monitor:ids.setdefault(ind,[]).append(ident)
        outline=limite(k);unitrows=[]
        for j,point in enumerate(xy):
            match=cKDTree([[g['x'],g['y']] for g in grid]).query(point)[1];g=grid[match];ident=str(g.get('id',g.get('receptor_id',g.get('ID',f'P{j+1:04}'))))
            row=dict(unit=k,WWTP=1 if k=='VM' else 2,receptor_id='/'.join(ids.get(j,[ident])),x=float(point[0]),y=float(point[1]),distance_m=float(p.distance_m.iloc[j]),inside_plant=bool(outline.covers(Point(point))),monitoring_location=j in ids,hours_AERMOD=len(A),hours_CALPUFF=len(B),screen_active=bool(max(A[:,j].max(),B[:,j].max())>=CUT))
            for name,z,q in [('AERMOD',A,aq),('CALPUFF',B,bq)]:
                row.update({f'{name}_P{round(v*100):02}':float(q[i,j]) for i,v in enumerate(quantiles)});row.update({f'{name}_mean':float(z[:,j].mean()),f'{name}_std':float(z[:,j].std()),f'{name}_max':float(z[:,j].max()),f'{name}_hours_ge_0_7_percent':float(100*np.mean(z[:,j]>=CUT))})
            row.update(mean_difference_CAL_minus_AER=row['CALPUFF_mean']-row['AERMOD_mean'],P95_difference_CAL_minus_AER=row['CALPUFF_P95']-row['AERMOD_P95'],wasserstein_ug_m3=float(wasserstein_distance(A[:,j],B[:,j])),KS_D=float(ks_2samp(A[:,j],B[:,j],method='asymp').statistic))
            row['boxplot_eligible']=max(row['AERMOD_P95'],row['CALPUFF_P95'])>=CUT
            rows.append(row);unitrows.append(row)
        u=pd.DataFrame(unitrows);active=u[(u.distance_m<1800)&u.screen_active].copy();atlas.extend(u[u.boxplot_eligible].to_dict('records'))
        bands=[(0,100),(100,500),(500,1800)];poster[k]=[]
        for lo,hi in bands:
            sub=active[(active.distance_m>=lo)&(active.distance_m<hi)]
            for model in COL:poster[k].append(dict(model=model,distance_min=lo,distance_max=hi,n=len(sub),values=sub[f'{model}_P95'].tolist(),median=float(sub[f'{model}_P95'].median())))

        rng=np.random.default_rng(724);blocks=np.floor(active[['x','y']].to_numpy()/250).astype(int);_,bid=np.unique(blocks,axis=0,return_inverse=True);clusters=[np.flatnonzero(bid==b) for b in np.unique(bid)];delta=active.P95_difference_CAL_minus_AER.to_numpy();boot=[]
        for rep in range(500):
            idx=np.concatenate([clusters[i] for i in rng.integers(0,len(clusters),len(clusters))]);boot.append(float(np.median(delta[idx])))
        summary[k]=dict(reference_year=2024,n_native_pairs=len(u),n_near_active=len(active),n_monitoring_locations=int(u.monitoring_location.sum()),n_boxplot_eligible=int(u.boxplot_eligible.sum()),hours_AERMOD=len(A),hours_CALPUFF=len(B),median_Wasserstein_near_ug_m3=float(active.wasserstein_ug_m3.median()),median_KS_D_near=float(active.KS_D.median()),median_P95_difference_CAL_minus_AER=float(np.median(delta)),bootstrap_spatial_blocks_250m=len(clusters),bootstrap_replicates=500,spatial_CI95_median_P95_difference=np.quantile(boot,[.025,.975]).tolist(),fraction_Cal_higher_P95=float(np.mean(active.CALPUFF_P95>active.AERMOD_P95)),screen_cut_ug_m3=CUT)
        render_monitor(u,k)
        print(k,summary[k],flush=True)
    csvout(O/'Estatistica_horaria_por_receptor.csv',rows);csvout(O/'Comparacao_cota_altura_fontes.csv',inputrows);dump(O/'Estatistica_avancada.json',dict(summary=summary,poster_distributions=poster,export_validation=export_validation,method='Full 2024 model-native valid hourly distributions at coincident unique receptors. No concentration deletion within selected sites. Odour-range lower reference 0.7 ug/m3 for display/screening only.',bootstrap_scope='Spatial sampling variability of receptor P95 contrasts; not total model uncertainty and not observational validation.'))
    from complementar_metricas_p95 import main as metricas_p95
    metricas_p95()
    render_comparison_and_atlas(poster,atlas)

# Render monitor
def render_monitor(u,k):

    fig,axs=plt.subplots(1,2,figsize=(11.7,5.3));fig.subplots_adjust(left=.09,right=.97,bottom=.18,top=.85,wspace=.26)
    mon=u[u.monitoring_location].sort_values('receptor_id');mrows=mon.to_dict('records');half=int(np.ceil(len(mrows)/2))
    for ax,part in zip(axs,[mrows[:half],mrows[half:]]):
        for model,shift in [('AERMOD',-.17),('CALPUFF',.17)]:add_boxes(ax,[statsbox(r,model) for r in part],np.arange(len(part))+shift,COL[model],.28)
        ax.spines['bottom'].set_position(('outward',8));ax.spines['left'].set_position(('outward',5));ax.set_xticks(range(len(part)),[r['receptor_id'] for r in part],rotation=65,ha='right',fontsize=8);ax.set_ylabel('Hourly H$_2$S (µg/m³)',labelpad=14);ax.set_ylim(bottom=0);ax.ticklabel_format(axis='y',style='plain');ax.grid(axis='y',alpha=.15)
    fig.suptitle(f'WWTP {1 if k=="VM" else 2} · monitoring receptors · hourly distributions (2024)',fontsize=13,weight='bold');fig.legend(handles=[Patch(facecolor=c,label=m) for m,c in COL.items()],loc='upper center',bbox_to_anchor=(.5,.94),ncol=2,frameon=False);save(fig,f'Boxplots_monitoramento_{k}')

# Render comparison and atlas
def render_comparison_and_atlas(poster,atlas):

    fig,axs=plt.subplots(1,2,figsize=(11.7,6));fig.subplots_adjust(left=.10,right=.985,bottom=.21,top=.82,wspace=.24)
    for ax,k in zip(axs,['VM','NC']):
        for model,shift in [('AERMOD',-.19),('CALPUFF',.19)]:
            lists=[d['values'] for d in poster[k] if d['model']==model];a=ax.boxplot(lists,positions=np.arange(3)+shift,widths=.31,showfliers=False,patch_artist=True,manage_ticks=False)
            for box in a['boxes']:box.set(facecolor=COL[model],alpha=.75,edgecolor=COL[model],linewidth=1.5)
            for name in ['whiskers','caps']:
                for v in a[name]:v.set(color=COL[model],linewidth=1.3)
            for v in a['medians']:v.set(color='#173445',linewidth=1.8)
        ax.set_xticks(range(3),['0–100 m','100–500 m','500–1,800 m']);ax.set_ylim(bottom=0);ax.set_title(f'WWTP {1 if k=="VM" else 2}',fontsize=15,weight='bold',pad=12);ax.tick_params(labelsize=11);ax.grid(axis='y',alpha=.15);ax.set_xlabel('Distance to nearest emitting surface',fontsize=12,labelpad=12);ax.spines['bottom'].set_position(('outward',8));ax.spines['left'].set_position(('outward',5))
    axs[0].set_ylabel('Receptor P95 of hourly H$_2$S (µg/m³)',fontsize=13,labelpad=10);fig.legend(handles=[Patch(facecolor=c,label=m) for m,c in COL.items()],loc='upper center',bbox_to_anchor=(.5,.97),ncol=2,frameon=False,fontsize=14);save(fig,'Boxplot_comparacao_poster')

    with PdfPages(O/'Boxplots_Receptores.pdf') as pdf:
        for k in ['VM','NC']:
            unit=sorted([r for r in atlas if r['unit']==k],key=lambda r:r['distance_m'])
            for first in range(0,len(unit),40):
                fig,axs=plt.subplots(2,1,figsize=(11.7,8.3));fig.subplots_adjust(left=.08,right=.97,bottom=.14,top=.88,hspace=.56)
                for ax,start in zip(axs,[first,first+20]):
                    part=unit[start:start+20]
                    if not part:ax.set_visible(False);continue
                    for model,shift in [('AERMOD',-.18),('CALPUFF',.18)]:add_boxes(ax,[statsbox(r,model) for r in part],np.arange(len(part))+shift,COL[model],.28)
                    ax.spines['bottom'].set_position(('outward',7));ax.spines['left'].set_position(('outward',5));ax.set_xticks(range(len(part)),[r['receptor_id'] for r in part],rotation=65,ha='right',fontsize=7);ax.tick_params(axis='y',labelsize=8);ax.set_ylim(bottom=0,top=max(.7,ax.get_ylim()[1]));ax.ticklabel_format(axis='y',style='plain',useOffset=False);ax.set_ylabel('Hourly H$_2$S (µg/m³)',fontsize=9,labelpad=13);ax.grid(axis='y',alpha=.15)
                fig.suptitle(f'WWTP {1 if k=="VM" else 2} · hourly distribution by receptor · 2024',fontsize=14,weight='bold');fig.legend(handles=[Patch(facecolor=c,label=m) for m,c in COL.items()],loc='upper center',bbox_to_anchor=(.5,.95),ncol=2,frameon=False,fontsize=10);fig.text(.5,.025,'Boxes: Q25–Q75; median line; whiskers: P5–P95. Locations with P95 ≥0.7 µg/m³ in either model. All other points and extremes retained in CSV.',ha='center',fontsize=8);pdf.savefig(fig);plt.close(fig)
    print('Advanced hourly statistics and boxplot atlas completed',flush=True)

# Render cached
def render_cached():
    data=pd.read_csv(O/'Estatistica_horaria_por_receptor.csv')
    for k in ['VM','NC']:render_monitor(data[data.unit.eq(k)],k)
    poster=json.loads((O/'Estatistica_avancada.json').read_text(encoding='utf8'))['poster_distributions']
    render_comparison_and_atlas(poster,data[data.boxplot_eligible].to_dict('records'))

if __name__=='__main__':
    import sys
    render_cached() if '--figures-only' in sys.argv else main()
