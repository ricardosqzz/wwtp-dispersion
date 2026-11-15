# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv | pd.read_csv.
# Entrada: E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv | source.read_bytes.
# Campos/chaves em data: unit.
# Campos/chaves em b: AERMOD, CALPUFF, high_m, label, low_m, median_difference_CAL_minus_AER, n.
# Campos/chaves em yy: median, q1, q3.
# Campos/chaves em u: WWTP, bins, n, samples, unit.
# Campos/chaves em sample: median, model, q1, q3, x.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos.json | .write_text.
# Saída: E:/copasa_map/output/comparacao_modelos/Perfis_P95_faixas_distancia.csv | .to_csv.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos.{ext} | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Perfis_comparacao_modelos_previa.png | fig.savefig.
# Campos/chaves gerados em b: median_difference_CAL_minus_AER.
# Campos/chaves gerados em yy: q1, q3.
# CÓDIGO DO PROCESSAMENTO

"""Perfis espaciais descritivos de P95 em pares nativos, sem ajuste do modelo."""
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
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,TwoSlopeNorm
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from scipy.interpolate import PchipInterpolator
R=Path(_cp_texto('', 'posix'));O=R/'output/comparacao_modelos';F=R/'output/cmas_poster/figuras'
EDGES=[0,50,100,200,300,500,1800]
LABELS=['0–50','50–100','100–200','200–300','300–500','500–1,800']
COL={'AERMOD':'#347fc0','CALPUFF':'#e18c39'}

# Main
def main():
    source=O/'Pares_concordancia_P95.csv';data=pd.read_csv(source);out=[]
    for unit in ['VM','NC']:
        s=data[data.unit.eq(unit)].copy();bins=[]
        for j,(lo,hi) in enumerate(zip(EDGES[:-1],EDGES[1:])):
            z=s[s.distance_m.ge(lo)&s.distance_m.lt(hi)]
            assert len(z)>=5
            b=dict(index=j,label=LABELS[j],low_m=lo,high_m=hi,n=len(z),median_distance_m=float(z.distance_m.median()))
            for model in COL:
                q=z[model+'_P95'].quantile([.25,.5,.75]).to_numpy()
                b[model]=dict(q1=float(q[0]),median=float(q[1]),q3=float(q[2]))
            b['median_difference_CAL_minus_AER']=b['CALPUFF']['median']-b['AERMOD']['median'];bins.append(b)
        assert sum(b['n'] for b in bins)==len(s)
        samples=[];xs=np.linspace(0,5,181)
        for model in COL:

            yy={stat:PchipInterpolator(np.arange(6),[b[model][stat] for b in bins])(xs) for stat in ['q1','median','q3']}
            yy['q1']=np.minimum(yy['q1'],yy['median']);yy['q3']=np.maximum(yy['q3'],yy['median'])
            samples.append(dict(model=model,x=xs.tolist(),q1=yy['q1'].tolist(),median=yy['median'].tolist(),q3=yy['q3'].tolist()))
        out.append(dict(unit=unit,WWTP=1 if unit=='VM' else 2,n=len(s),bins=bins,samples=samples))
    payload=dict(reference_year=2024,statistic='Hourly P95 per receptor, then spatial median and quartiles within distance bands',distance='Distance to closest emitting footprint',scope='All unique paired receptors within 1800 m; no concentration filter',band_axes='Categorical; equal display width does not imply equal distance width',ribbons='Spatial interquartile range, not confidence intervals',interpolation='Shape-preserving PCHIP for display only, no interpolation of model concentrations',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),units=out)
    (F/'Perfis_comparacao_modelos.json').write_text(json.dumps(payload,indent=2),encoding='utf8')
    rows=[]
    for u in out:
        for b in u['bins']:
            for model in COL:rows.append(dict(unit=u['unit'],model=model,low_m=b['low_m'],high_m=b['high_m'],n=b['n'],**b[model]))
    pd.DataFrame(rows).to_csv(O/'Perfis_P95_faixas_distancia.csv',index=False,encoding='utf-8-sig')
    plt.rcParams.update({'font.family':'Arial','font.size':12,'svg.fonttype':'path','pdf.fonttype':42,'axes.spines.right':False,'axes.spines.top':False})
    fig=plt.figure(figsize=(17.5,8.2));difference_cmap=LinearSegmentedColormap.from_list('model_difference',['#6da6d3','#f4f4ef','#edb579']);norm=TwoSlopeNorm(vmin=-40,vcenter=0,vmax=40)
    for i,u in enumerate(out):
        ax=fig.add_axes([.065+.50*i,.30,.40,.49]);ax.set_ylim(0,80);ax.set_xlim(-.4,5.4)
        ax.set_yticks([0,20,40,60,80]);ax.set_xticks(range(6),[f"{b['label']}\nn={b['n']}" for b in u['bins']],fontsize=10)
        ax.set_ylabel('Receptor hourly P95 (µg/m³)',labelpad=11);ax.tick_params(pad=6);ax.grid(axis='y',color='#e3eaed',lw=.8)
        ax.set_title(f"WWTP {u['WWTP']} · {u['n']} paired receptors",fontsize=17,weight='bold',pad=20,color='#173445')
        for sample in u['samples']:
            model=sample['model'];color=COL[model]
            ax.fill_between(sample['x'],sample['q1'],sample['q3'],color=color,alpha=.17,zorder=2)
            ax.plot(sample['x'],sample['median'],color=color,lw=3,zorder=3)
            vals=[b[model]['median'] for b in u['bins']];ax.scatter(range(6),vals,s=52,c=color,edgecolors='white',linewidths=1,zorder=4)

        z=ax.inset_axes([.43,.43,.54,.49]);z.set_facecolor('#ffffff')
        for model,color in COL.items():z.plot(range(4),[b[model]['median'] for b in u['bins'][2:]],'o-',color=color,lw=2,ms=4)
        z.set(xlim=(-.25,3.25),ylim=(0,4),yticks=[0,2,4]);z.set_xticks(range(4),['100–200','200–300','300–500','500–1,800'],fontsize=8)
        z.set_title('Median zoom ≥100 m (µg/m³)',fontsize=10,pad=8);z.grid(axis='y',color='#e9edef',lw=.6);z.tick_params(labelsize=8,pad=4)
        delta=fig.add_axes([.065+.5*i,.16,.40,.052]);delta.set_xlim(-.4,5.4);delta.set_ylim(0,1);delta.set_axis_off()
        for j,b in enumerate(u['bins']):
            v=b['median_difference_CAL_minus_AER'];delta.add_patch(Rectangle((j-.47,0),.94,1,facecolor=difference_cmap(norm(v)),edgecolor='white',lw=1))
            label=f'{v:+.1f}' if abs(v)>=1 else f'{v:+.2f}';delta.text(j,.5,label,ha='center',va='center',fontsize=11,color='#173445',weight='bold')
        fig.text(.065+.5*i,.13,'Δ median = CALPUFF − AERMOD (µg/m³)',fontsize=10.5,color='#536b77')
    fig.suptitle('How the model contrast changes with distance · 2024',fontsize=21,fontweight='bold',color='#173445',y=.97)
    handles=[Line2D([],[],color=c,lw=3,marker='o',label=m) for m,c in COL.items()]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.925),ncol=2,frameon=False,fontsize=13)
    fig.text(.5,.855,'Lines: spatial medians     Shaded bands: middle 50% of receptor P95     Points: calculated band summaries',ha='center',fontsize=11,color='#536b77')
    fig.text(.5,.055,'Distance bands are in metres and have equal display widths. All paired receptors within 1,800 m enter the summaries.\nInsets magnify medians only. Shaded bands describe spatial variability, not confidence intervals or model accuracy.',ha='center',fontsize=10.5,color='#536b77',linespacing=1.5)
    for ext in ['svg','pdf']:fig.savefig(F/f'Perfis_comparacao_modelos.{ext}',facecolor='white')
    fig.savefig(F/'Perfis_comparacao_modelos.png',dpi=450,facecolor='white');fig.savefig(F/'Perfis_comparacao_modelos_previa.png',dpi=140,facecolor='white');plt.close(fig)
    print(json.dumps([dict(unit=u['unit'],n=u['n'],bins=[b['n'] for b in u['bins']]) for u in out]))

if __name__=='__main__':main()
