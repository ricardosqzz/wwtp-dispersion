# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {O}/Comparacao_consolidada.json | .read_text.
# Entrada: {O}/Campos_nativos.npz | np.load.
# Entrada: {O}/Entradas_executadas_fontes.csv | .open.
# Entrada: {O}/Meteorologia_AERMET.csv | pd.read_csv.
# Entrada: {O}/Meteorologia_CALMET.csv | pd.read_csv.
# Entrada: {C}/AERMOD_{k}_1h.npy | np.load.
# Entrada: {C}/AERMOD_{k}_1h.json | .read_text.
# Entrada: {C}/CALPUFF_{k}_1h.npy | np.load.
# Entrada: {C}/CALPUFF_{k}_1h.json | .read_text.
# Entrada: E:/copasa_map/CMAS/CALPUFF/CALPUFF-{k}.LST | .read_text.
# Entrada: {O}/Pares_nativos_{k}_24h.csv | pd.read_csv.
# Campos/chaves em meta: codes, xy.
# Campos/chaves em met: calm, missing, time_end.
# Campos/chaves em cmeta: embedded_input, end_times, start_times, xy.
# Campos/chaves em p: AERMOD, CALPUFF, distance_m, x, y.
# Campos/chaves em cm: unit.
# Campos/chaves em weather: clock.
# Campos/chaves em aa: calm, direction, missing, speed.
# Campos/chaves em bb: direction, speed.
# Campos/chaves em df: category, distance_min_m, model, unit.
# Campos/chaves em s: mean.
# Campos/chaves em v: max_distance_m, min_distance_m.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{stem}.{ext} | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{stem}.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/{stem}_previa.png | fig.savefig.
# Saída: {C}/CALPUFF_{k}_executado.INP | embedded.write_text.
# Saída: {fig} | savefig.
# Campos/chaves gerados em met: clock.
# Campos/chaves gerados em own: clock.
# CÓDIGO DO PROCESSAMENTO

"""Gráficos científicos e descritores condicionais dos dois modelos."""
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
from cartografia_copasa import centre
from geometria_ete import limite
plt.rcParams.update({'font.family':'Arial','pdf.fonttype':42,'svg.fonttype':'path','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
F=R/'output/cmas_poster/figuras';COLORS={'AERMOD':'#234f7d','CALPUFF':'#27a69d'};UNITS={'VM':'WWTP 1','NC':'WWTP 2'}
# Savefig
def savefig(fig,stem):
    for ext in ['pdf','svg']:fig.savefig(F/f'{stem}.{ext}',facecolor='white')
    fig.savefig(F/f'{stem}.png',dpi=450,facecolor='white');fig.savefig(F/f'{stem}_previa.png',dpi=130,facecolor='white');plt.close(fig)
# Main
def main():
    data=json.loads((O/'Comparacao_consolidada.json').read_text(encoding='utf8'));fields=dict(np.load(O/'Campos_nativos.npz'));inputrows=list(csv.DictReader((O/'Entradas_executadas_fontes.csv').open(encoding='utf-8-sig')));external=[]
    met=pd.read_csv(O/'Meteorologia_AERMET.csv');cm=pd.read_csv(O/'Meteorologia_CALMET.csv');conditional=[];meteorological=[];lagscan=[];annualstats=[];source_check=[];bins=[0,25,50,100,250,500,1000,1800]
    for k in ['VM','NC']:
        h=np.load(C/f'AERMOD_{k}_1h.npy',mmap_mode='r');meta=json.loads((C/f'AERMOD_{k}_1h.json').read_text());xy=np.array(meta['xy']);codes=np.array(meta['codes']);valid=~met['calm'].to_numpy()&~met['missing'].to_numpy();years=codes//1000000
        ann=np.array([np.asarray(h[years==y],dtype='float64').sum(axis=0)/valid[years==y].sum() for y in [24,25]])
        fields[f'{k}_AERMOD_annual_2024']=ann[0];fields[f'{k}_AERMOD_annual_2025']=ann[1]
        cal=np.load(C/f'CALPUFF_{k}_1h.npy',mmap_mode='r');cmeta=json.loads((C/f'CALPUFF_{k}_1h.json').read_text());cxy=np.array(cmeta['xy'])

        embedded=C/f'CALPUFF_{k}_executado.INP';embedded.write_text('\n'.join(cmeta['embedded_input']),encoding='cp1252');_,cs=parse_cal(embedded);_,loose=parse_cal(R/f'CMAS/CALPUFF/CALPUFF-{k}.INP')
        assert set(cs)==set(loose)
        for sid,v in cs.items():
            for key in ['old_flux','height','sigma','area']:assert np.isclose(v[key],loose[sid][key],rtol=1e-10,atol=1e-9),(sid,key)
        source_check.append(dict(unit=k,embedded_matches_received=True,source_count=len(cs),normal_end='End of run -- Clock time:' in (R/f'CMAS/CALPUFF/CALPUFF-{k}.LST').read_text(encoding='cp1252')))
        p=pd.read_csv(O/f'Pares_nativos_{k}_24h.csv');tree=cKDTree(xy);err,ai=tree.query(p[['x','y']]);err2,ci=cKDTree(cxy).query(p[['x','y']]);assert max(err)<1e-5 and max(err2)<=.75
        own=cm[cm.unit==k].copy();own.index=pd.to_datetime(own.time_end);own=own.loc[pd.to_datetime(cmeta['end_times'])];assert len(own)==len(cal)
        met['clock']=pd.to_datetime(met.time_end)-pd.Timedelta(minutes=30);own['clock']=pd.to_datetime(cmeta['start_times'])+pd.Timedelta(minutes=30)

        for model,arr,indices,weather,ok in [('AERMOD',h,ai,met,valid),('CALPUFF',cal,ci,own,np.ones(len(cal),dtype=bool))]:
            ws=weather.speed.to_numpy();wd=weather.direction.to_numpy();clocks=pd.to_datetime(weather['clock']);clockhour=clocks.dt.hour.to_numpy() if hasattr(clocks,'dt') else clocks.hour.to_numpy()
            month=clocks.dt.month.to_numpy() if hasattr(clocks,'dt') else clocks.month.to_numpy()
            meteorological.append(dict(unit=k,model=model,hours=int(ok.sum()),median_wind_m_s=float(np.median(ws[ok])),mean_wind_m_s=float(np.mean(ws[ok])),low_wind_below_1_percent=float(100*np.mean(ws[ok]<1)),wind_p90_m_s=float(np.quantile(ws[ok],.9))))
            for lo,hi in [(0,100),(100,500),(500,1800)]:
                pick=(p.distance_m>=lo)&(p.distance_m<hi);ix=indices[pick]
                if not len(ix):continue
                response=np.mean(arr[:,ix],axis=1)
                for category,cat in [('speed',np.digitize(ws,[1,2,4,6])),('direction',np.floor((wd+22.5)%360/45).astype(int)),('hour',clockhour),('month',month)]:
                    for v in np.unique(cat[ok]):
                        s=ok&(cat==v);z=response[s];conditional.append(dict(unit=k,model=model,distance_min_m=lo,distance_max_m=hi,category=category,bin=int(v),hours=len(z),receptors=len(ix),mean=float(z.mean()),median=float(np.median(z)),p90=float(np.quantile(z,.9))))

        aa=met.set_index(pd.to_datetime(met.time_end));cc=cm[cm.unit==k].set_index(pd.to_datetime(cm[cm.unit==k].time_end))
        for lag in range(-4,5):
            bb=cc.copy();bb.index=bb.index+pd.Timedelta(hours=lag);pair=aa[['speed','direction','calm','missing']].join(bb[['speed','direction']],lsuffix='_AER',rsuffix='_CAL',how='inner');pair=pair[~pair.calm&~pair.missing];ad=abs((pair.direction_AER-pair.direction_CAL+180)%360-180)
            lagscan.append(dict(unit=k,CALMET_label_shift_hours=lag,n=len(pair),wind_speed_rho=float(spearmanr(pair.speed_AER,pair.speed_CAL).statistic),median_abs_speed_difference=float(abs(pair.speed_AER-pair.speed_CAL).median()),median_abs_direction_difference_deg=float(ad.median())))

        for per in ['annual_calendar_max','annual_2024','annual_2025']:
            av=fields[f'{k}_AERMOD_{per}'][ai];cv=fields[f'{k}_CALPUFF_{per}'][ci]
            for lo,hi in [(0,100),(100,500),(500,1800),(0,1800)]:
                sel=(p.distance_m>=lo)&(p.distance_m<hi);a=av[sel];c=cv[sel]
                if len(a)<3:continue
                pos=(a>0)&(c>0);annualstats.append(dict(unit=k,period=per,min_distance_m=lo,max_distance_m=hi,n=len(a),median_AERMOD=float(np.median(a)),median_CALPUFF=float(np.median(c)),median_CAL_over_AER=float(np.median(c[pos]/a[pos])),spearman_rho=float(spearmanr(a,c).statistic)))
        footprint=limite(k)
        for model in ['AERMOD','CALPUFF']:
            xx=fields[f'{k}_{model}_xy'];_,ix=np.unique(xx,axis=0,return_index=True);outside=np.array([not footprint.covers(Point(x,y)) for x,y in xx[ix]])
            for period in ['24h','annual_calendar_max']:
                values=fields[f'{k}_{model}_{period}'][ix];j=int(values.argmax());external.append(dict(unit=k,model=model,period=period,unique_receptors=len(ix),outside_receptors=int(outside.sum()),peak_inside_plant=not bool(outside[j]),maximum_all=float(values.max()),maximum_outside=float(values[outside].max())))
    np.savez_compressed(O/'Campos_nativos.npz',**fields);csvout(O/'Resposta_meteorologica_dois_modelos.csv',conditional);csvout(O/'Descritores_meteorologia.csv',meteorological);csvout(O/'Diagnostico_defasagem_relogios.csv',lagscan);csvout(O/'Comparacao_anual_pares.csv',annualstats);csvout(O/'Maximos_fora_limite_ETE.csv',external)
    dump(O/'Conferencia_entradas_embutidas.json',source_check)
    df=pd.DataFrame(conditional);fig,axs=plt.subplots(1,2,figsize=(11.7,5.8));fig.subplots_adjust(left=.09,right=.98,top=.83,bottom=.19,wspace=.30)
    for ax,k in zip(axs,['VM','NC']):
        p=pd.read_csv(O/f'Pares_nativos_{k}_24h.csv')
        for model in ['AERMOD','CALPUFF']:
            rows=[]
            for lo,hi in zip(bins,bins[1:]):
                z=p.loc[(p.distance_m>=lo)&(p.distance_m<hi),model]
                if len(z)>=3:rows.append([max(12.5,(lo+hi)/2),*np.quantile(z,[.25,.5,.75])])
            z=np.array(rows);ax.fill_between(z[:,0],z[:,1],z[:,3],color=COLORS[model],alpha=.14,lw=0);ax.plot(z[:,0],z[:,2],marker='o',ms=4,lw=2,color=COLORS[model],label=model)
        ax.set_xscale('symlog',linthresh=50);ax.set_ylim(bottom=0);ax.set_xticks([25,100,250,500,1000,1800]);ax.set_xticklabels(['25','100','250','500','1,000','1,800']);ax.set_xlim(0,1800);ax.set_title(UNITS[k],weight='bold',pad=9,fontsize=13);ax.set_xlabel('Distance to nearest emitting footprint (m)',labelpad=7,fontsize=11);ax.grid(axis='y',alpha=.16);ax.tick_params(labelsize=12)
    axs[0].set_ylabel('Maximum 24 h H$_2$S (µg/m³)',fontsize=13,labelpad=8);fig.legend([Line2D([],[],color=COLORS[m],lw=2) for m in COLORS],list(COLORS),ncol=2,loc='upper center',bbox_to_anchor=(.52,.97),frameon=False,fontsize=11);savefig(fig,'Comparacao_distancia_poster')

    fig,axs=plt.subplots(2,2,figsize=(11.7,8.3));fig.subplots_adjust(left=.09,right=.96,top=.92,bottom=.11,hspace=.47,wspace=.27)
    for j,k in enumerate(['VM','NC']):
        for model,weather,ok in [('AERMOD',met,~met.calm&~met.missing),('CALPUFF',cm[cm.unit==k],np.ones(sum(cm.unit==k),dtype=bool))]:
            ws=weather.speed.to_numpy()[ok];dire=weather.direction.to_numpy()[ok];v=np.sort(ws);axs[0,j].plot(v,np.arange(1,len(v)+1)/len(v)*100,color=COLORS[model],label=model,lw=1.8)
            sectors=np.floor((dire+22.5)%360/45).astype(int);cnt=np.bincount(sectors,minlength=8)/len(sectors)*100;axs[1,j].plot(range(8),cnt,marker='o',color=COLORS[model],lw=1.8,label=model)
        axs[0,j].set(title=UNITS[k],xlabel='Wind speed (m/s)',ylabel='Cumulative frequency (%)');axs[0,j].grid(alpha=.15);axs[1,j].set_xticks(range(8),['N','NE','E','SE','S','SW','W','NW']);axs[1,j].set(xlabel='Wind from direction',ylabel='Frequency (%)');axs[1,j].grid(axis='y',alpha=.15)
    axs[0,0].legend(frameon=False);savefig(fig,'Meteorologia_comparada')
    fig,axs=plt.subplots(2,2,figsize=(11.7,8.3));fig.subplots_adjust(left=.095,right=.96,top=.9,bottom=.12,hspace=.5,wspace=.25)
    for j,k in enumerate(['VM','NC']):
        for i,cat in enumerate(['speed','hour']):
            for model in COLORS:
                s=df[(df.unit==k)&(df.model==model)&(df.distance_min_m==0)&(df.category==cat)].sort_values('bin');axs[i,j].plot(s.bin,s['mean'],marker='o',ms=3,color=COLORS[model],lw=1.8,label=model)
            axs[i,j].set_ylim(bottom=0);axs[i,j].grid(axis='y',alpha=.15);axs[i,j].set_title(UNITS[k]+' · receptors <100 m',fontsize=11);axs[i,j].set_ylabel('Mean H$_2$S (µg/m³)')
            if cat=='speed':axs[i,j].set_xticks(range(5),['<1','1–2','2–4','4–6','≥6']);axs[i,j].set_xlabel('Wind speed class used by each model (m/s)')
            else:axs[i,j].set_xticks([0,4,8,12,16,20,23]);axs[i,j].set_xlabel('Hour on each model’s executed clock')
    axs[0,0].legend(frameon=False);savefig(fig,'Resposta_meteorologica')
    fig,axs=plt.subplots(1,2,figsize=(11.7,5.2));fig.subplots_adjust(left=.085,right=.98,top=.90,bottom=.16,wspace=.3)
    for ax,k in zip(axs,['VM','NC']):
        p=pd.read_csv(O/f'Pares_nativos_{k}_24h.csv');p=p[p.distance_m<1800];z=ax.scatter(p.AERMOD,p.CALPUFF,c=p.distance_m,cmap='viridis',s=12,alpha=.75,edgecolors='none');ax.set_xlim(left=0);ax.set_ylim(bottom=0);low=min(p[['AERMOD','CALPUFF']].min());high=max(p[['AERMOD','CALPUFF']].max());ax.plot([low,high],[low,high],color='#88949b',lw=1,ls='--');ax.set(title=UNITS[k],xlabel='AERMOD max. 24 h (µg/m³)',ylabel='CALPUFF max. 24 h (µg/m³)');ax.grid(alpha=.12)
    cb=fig.colorbar(z,ax=axs,shrink=.8,pad=.03);cb.set_label('Distance (m)');savefig(fig,'Dispersao_pares_24h')
    print(json.dumps(dict(meteorology=meteorological,source_check=source_check,annual_near=[v for v in annualstats if v['min_distance_m']==0 and v['max_distance_m']==1800]),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
