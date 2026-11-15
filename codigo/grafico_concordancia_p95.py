# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv | pd.read_csv.
# Entrada: E:/copasa_map/output/comparacao_modelos/Concordancia_espacial_P95.json | .read_text.
# Entrada: E:/copasa_map/output/comparacao_modelos/Pares_concordancia_P95.csv | .read_bytes.
# Campos/chaves em d: unit.
# Campos/chaves em summary: rows.
# Campos/chaves em x: distance_max_m, distance_min_m, unit.
# Campos/chaves em score: Spearman_rho_P95, WWTP, within_factor_2_percent.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.{ext} | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores_previa.png | fig.savefig.
# Saída: E:/copasa_map/output/cmas_poster/figuras/Concordancia_P95_receptores.json | .write_text.
# CÓDIGO DO PROCESSAMENTO

"""Dispersão P95 em pares nativos, com ampliação e visão integral dos extremos."""
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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch,Rectangle
R=Path(_cp_texto('', 'posix'));O=R/'output/comparacao_modelos';F=R/'output/cmas_poster/figuras'

# Main
def main():
    d=pd.read_csv(O/'Pares_concordancia_P95.csv');summary=json.loads((O/'Concordancia_espacial_P95.json').read_text(encoding='utf8'))
    plt.rcParams.update({'font.family':'Arial','font.size':12,'svg.fonttype':'path','pdf.fonttype':42,'axes.spines.right':False,'axes.spines.top':False})
    fig=plt.figure(figsize=(17,8));axs=[fig.add_axes([.065+.5*i,.23,.278,.59]) for i in range(2)]
    evidence=[];col=['#287e96','#d3704e']
    for i,(ax,k) in enumerate(zip(axs,['VM','NC'])):
        s=d[d.unit.eq(k)];a=s.AERMOD_P95.to_numpy();b=s.CALPUFF_P95.to_numpy();inside=s.P95_within_factor_2.to_numpy(bool)
        score=next(x for x in summary['rows'] if x['unit']==k and x['distance_min_m']==0 and x['distance_max_m']==1800)
        xx=np.linspace(0,30,301);ax.fill_between(xx,.5*xx,np.minimum(2*xx,30),color='#e4eeea',zorder=0)
        for selected,c in [(~inside,col[1]),(inside,col[0])]:ax.scatter(a[selected],b[selected],s=19,alpha=.72,c=c,linewidths=.2,edgecolors='white',zorder=3)
        ax.plot([0,30],[0,30],color='#526874',ls='--',lw=1.2,zorder=1)
        ax.set(xlim=(0,30),ylim=(0,30),xticks=[0,10,20,30],yticks=[0,10,20,30],xlabel='AERMOD hourly P95 (µg/m³)',ylabel='CALPUFF hourly P95 (µg/m³)')
        ax.set_aspect('equal');ax.grid(alpha=.12,lw=.5);ax.xaxis.labelpad=11;ax.yaxis.labelpad=12;ax.tick_params(pad=5)
        ax.set_title(f'WWTP {score["WWTP"]}',fontsize=16,fontweight='bold',pad=18)
        fig.text(.375+.5*i,.43,f'Spearman ρ\n{score["Spearman_rho_P95"]:.3f}\n\nWithin factor 2\n{score["within_factor_2_percent"]:.1f}%\n\nn = {len(s)} receptors',ha='left',va='top',fontsize=11.5,color='#173445',linespacing=1.35)

        inset=fig.add_axes([.375+.5*i,.51,.11,.234]);cap=500 if max(a.max(),b.max())>200 else 200
        xx=np.linspace(0,cap,101);inset.fill_between(xx,.5*xx,np.minimum(2*xx,cap),color='#e4eeea')
        for selected,c in [(~inside,col[1]),(inside,col[0])]:inset.scatter(a[selected],b[selected],s=3.4,alpha=.7,c=c,linewidths=0,zorder=3)
        inset.plot([0,cap],[0,cap],color='#526874',ls='--',lw=.65);inset.add_patch(Rectangle((0,0),30,30,fill=False,edgecolor='#173445',lw=.8))
        inset.set(xlim=(0,cap),ylim=(0,cap),xticks=[0,cap],yticks=[0,cap]);inset.tick_params(labelsize=8,pad=2,length=2);inset.set_title('Full range',fontsize=9,pad=5);inset.set_aspect('equal')
        visible=int(((a<=30)&(b<=30)).sum());ax.text(.5,-.20,f'Zoom: 0–30 µg/m³ ({visible}/{len(s)} receptors shown)',transform=ax.transAxes,ha='center',fontsize=10,color='#536b77')
        evidence.append(dict(unit=k,n=len(s),n_visible_main=visible,n_in_full_range=len(s),full_range_max=cap,stats_all_receptors=True,Spearman_rho=score['Spearman_rho_P95'],within_factor_2_percent=score['within_factor_2_percent']))
    fig.suptitle('Intermodel comparison at matched receptors · 2024',fontsize=19,fontweight='bold',color='#173445',y=.975)
    handles=[Line2D([],[],marker='o',ls='',color=col[0],label='Within factor 2'),Line2D([],[],marker='o',ls='',color=col[1],label='Outside factor 2'),Line2D([],[],ls='--',color='#526874',label='Equal concentration (1:1)'),Patch(facecolor='#e4eeea',label='Factor-of-two band')]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.92),ncol=4,frameon=False,fontsize=11)
    fig.text(.5,.035,'Each point is the hourly P95 at one receptor within 1,800 m. Insets retain the full range; all receptors enter the statistics.\nThe two native hourly distributions are compared descriptively. Neither model is treated as an ambient observation.',ha='center',fontsize=10,color='#536b77',linespacing=1.6)
    for ext in ['svg','pdf']:fig.savefig(F/f'Concordancia_P95_receptores.{ext}',facecolor='white')
    fig.savefig(F/'Concordancia_P95_receptores.png',dpi=450,facecolor='white');fig.savefig(F/'Concordancia_P95_receptores_previa.png',dpi=140,facecolor='white');plt.close(fig)
    (F/'Concordancia_P95_receptores.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256((O/'Pares_concordancia_P95.csv').read_bytes()).hexdigest(),main_axes='Linear 0 to 30 ug/m3',insets='Linear full native range',units=evidence),indent=2),encoding='utf8')
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
