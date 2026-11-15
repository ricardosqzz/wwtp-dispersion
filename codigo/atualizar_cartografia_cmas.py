# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: c.F/Cartografia_metadados.json | .read_text.
# Entrada: c.R/output/comparacao_modelos/Campos_nativos.npz | np.load.
# Campos/chaves em c.META: Fontes_privacidade.
# Saída: plt.figure(figsize=(wc / 2.54, hc / 2.54)) | c.save.
# Saída: c.F/Cartografia_metadados.json | .write_text.
# Saída: c.F/Faixas_concentracao_poster.json | .write_text.
# Saída: c.O/index.html | .write_text.
# Campos/chaves gerados em v: process.
# Campos/chaves gerados em c.D: sources_aermod.
# CÓDIGO DO PROCESSAMENTO

"""Produtos cartográficos da execução recebida em 10/11/2026."""
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

import json,html,shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize,LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Patch
from matplotlib.patches import Rectangle
import matplotlib.patheffects as pe
from scipy.interpolate import LinearNDInterpolator
import cartografia_copasa as c
from auditar_e_preparar import parse_aer
R=c.R;O=c.O;F=c.F;A=R/'output/comparacao_modelos'
# Main
def main(only_methods=False):
    archive=R/'descontinuado/2026_11_10_estatistica_visual/figuras';archive.mkdir(parents=True,exist_ok=True)
    for stem in ['Fontes_privacidade','Comparacao_24h_faixa','Comparacao_anual_faixa','Comparacao_anual_2024']:
        for p in F.glob(stem+'*'):
            if p.is_file() and not (archive/p.name).exists():shutil.copy2(p,archive/p.name)
    c.META.update(json.loads((F/'Cartografia_metadados.json').read_text(encoding='utf8')))
    for key in ['Comparacao_24h_pre_harmonizacao','Comparacao_anual_8760h_pre_harmonizacao','Cenarios_24h_eventos_coerentes','Comparacao_anual_placeholder']:c.META.pop(key,None)
    _,src=parse_aer(R/'CMAS/AERMOD/H2S_TOTAL.ADI')
    for n,v in src.items():v['process']=next(p for p in ['VM_UASB','VM_PRE','VM_CALHA','NC_UASB','NC_PRE','NC_FB'] if n.startswith(p))
    c.D['sources_aermod']=src
    method_span,method_scale=400,2500
    side,left,gap,bottom,top,wc=16.,1.35,2.,1.3,1.0,52.5
    hc=bottom+side+top;fig=plt.figure(figsize=(wc/2.54,hc/2.54))
    axs=[fig.add_axes([(left+i*(side+gap))/wc,bottom/hc,side/wc,side/hc]) for i in range(2)]
    for ax,k,label in zip(axs,['VM','NC'],['WWTP 1','WWTP 2']):
        frame=c.frame(ax,k,method_span,method_scale);c.draw_context(ax,k,c.TO_GEO);c.sources(ax,k);ax.set_title(label,pad=9,fontweight='bold',fontsize=16,color='#173445')
        ax.tick_params(labelsize=11,pad=2.5);ax.tick_params(axis='y',pad=5.)
        for t in ax.texts:t.set_fontsize(10.5 if t.get_gid()!='datum_scale' else 9)
        for t in ax.texts:
            if t.get_text()=='N':t.set_fontsize(12)
        from geometria_ete import limite
        outline=np.asarray(limite(k).exterior.coords);ox,oy=c.TO_GEO.transform(outline[:,0],outline[:,1])
        assert np.all((ox>=frame[0])&(ox<=frame[2])&(oy>=frame[1])&(oy<=frame[3])), 'Facility boundary clipped'
    handles=[Patch(facecolor=color,edgecolor='#25414d',linewidth=.5,label={'PRE':'Preliminary treatment','UASB':'UASB reactors','FB':'Trickling filters','CALHA':'Outlet weir'}[p]) for p,color in c.COL.items()]+c.context_handles()
    legend_x=37.15;map_top=bottom+side
    fig.text(legend_x/wc,(map_top-.55)/hc,'Treatment units',ha='left',va='top',fontsize=24,fontweight='bold',color='#173445')
    legend_sources=fig.legend(handles=handles[:4],loc='upper left',bbox_to_anchor=(legend_x/wc,(map_top-1.65)/hc),borderaxespad=0,ncol=1,frameon=False,fontsize=25,labelspacing=.40,handlelength=1.65,handletextpad=.7,alignment='left')
    fig.text(legend_x/wc,(map_top-7.0)/hc,'Map context',ha='left',va='top',fontsize=23,fontweight='bold',color='#173445')
    legend_context=fig.legend(handles=handles[4:],loc='upper left',bbox_to_anchor=(legend_x/wc,(map_top-8.1)/hc),borderaxespad=0,ncol=1,frameon=False,fontsize=22,labelspacing=.30,handlelength=1.8,handletextpad=.7,alignment='left')
    fig.canvas.draw();renderer=fig.canvas.get_renderer();map_right=axs[-1].get_window_extent(renderer).x1
    legend_clearance=min(v.get_window_extent(renderer).x0 for v in [legend_sources,legend_context])-map_right
    assert legend_clearance>0
    c.credit(fig,.06/hc);c.save(fig,'Fontes_privacidade',method_scale)
    c.META['Fontes_privacidade'].update(legend_position='right',legend_fontsize_poster_pt=25,legend_context_fontsize_pt=22,legend_grouped=True,facility_boundaries_complete=True,legend_map_clearance_cm=legend_clearance/fig.dpi*2.54)
    if only_methods:
        (F/'Cartografia_metadados.json').write_text(json.dumps(c.META,indent=2),encoding='utf8')
        return
    fields=np.load(A/'Campos_nativos.npz');records=[]
    span,scale=1000,8500;side=span/scale*100;left,right,bottom,top=1.35,4.0,1.15,1.1;gaps=[.5,1.0,.5];wc=left+4*side+sum(gaps)+right;hc=bottom+side+top
    cmap=LinearSegmentedColormap.from_list('copasa_linear',['#cee9fa','#7cc2db','#72bc8c','#d4d96b','#f9df64','#f5a54b','#df503a','#b8182c']);cmap.set_under('#f2f4f4');cmap.set_over('#ae1325')
    for period,stem,vmin,vmax,ticks in [('24h','Comparacao_24h_faixa',.7,50,[.7,10,20,30,40,50]),('annual_calendar_max','Comparacao_anual_faixa',.7,10,[.7,2,4,6,8,10]),('annual_2024','Comparacao_anual_2024',.7,10,[.7,2,4,6,8,10])]:
        fig=plt.figure(figsize=(wc/2.54,hc/2.54));axes=[]
        for i,(unit,model) in enumerate([('VM','AERMOD'),('VM','CALPUFF'),('NC','AERMOD'),('NC','CALPUFF')]):
            ax=fig.add_axes([(left+i*side+sum(gaps[:i]))/wc,bottom/hc,side/wc,side/hc]);axes.append(ax);x0,y0,x1,y1=c.frame(ax,unit,span,scale)
            ax.tick_params(labelsize=12,pad=2.5);ax.tick_params(axis='y',pad=5.2)
            if i%2:ax.tick_params(axis='y',labelleft=False)
            for t in ax.texts:t.set_fontsize(10 if t.get_gid()!='datum_scale' else 9)
            ax._datum.set_text('WGS 84\nScale 1:8,500');ax._compact_datum=True

            for patch in ax.patches:
                if isinstance(patch,Rectangle):patch.set_height(patch.get_height()*1.5);patch.set_linewidth(.7)
            xy=fields[f'{unit}_{model}_xy'];values=fields[f'{unit}_{model}_{period}'];_,idx=np.unique(xy,axis=0,return_index=True);xy=xy[idx];values=values[idx];cx,cy=c.centre(unit)
            near=(abs(xy[:,0]-cx)<span*.7)&(abs(xy[:,1]-cy)<span*.7)
            gx=np.unique(np.r_[np.linspace(cx-span*.65,cx+span*.65,401),xy[near,0]]);gy=np.unique(np.r_[np.linspace(cy-span*.65,cy+span*.65,401),xy[near,1]])
            xx,yy=np.meshgrid(gx,gy);points=xy-[cx,cy];fun=LinearNDInterpolator(points,values,fill_value=np.nan);zz=fun(np.column_stack([xx.ravel()-cx,yy.ravel()-cy])).reshape(xx.shape)
            lon,lat=c.TO_GEO.transform(xx,yy);inside=(lon>=x0)&(lon<=x1)&(lat>=y0)&(lat<=y1);coverage=float(np.isfinite(zz[inside]).mean());assert coverage==1
            m=ax.contourf(lon,lat,zz,levels=np.linspace(vmin,vmax,81),norm=Normalize(vmin,vmax),cmap=cmap,extend='both',zorder=2);m.set_edgecolor('face');m.set_linewidth(.1)
            levels=[v for v in ([.7,3,7,15,30,50,100,200] if period=='24h' else [.7,1,2,4,7,10,20,50,100]) if v<float(np.nanmax(zz))]
            lines=ax.contour(lon,lat,zz,levels=levels,colors='#35485a',alpha=.65,linewidths=.65,zorder=4)
            labels=ax.clabel(lines,levels=[v for v in levels if v in ([7,15,30,50] if period=='24h' else [1,4,7,10])],fontsize=9,inline=True,inline_spacing=3,fmt='%g')
            for t in labels:t.set_path_effects([pe.withStroke(linewidth=1.4,foreground='white',alpha=.8)])
            c.draw_context(ax,unit,c.TO_GEO,True);c.sources(ax,unit,False);ax.set_title(f"WWTP {1 if unit=='VM' else 2} · {model}",y=1,pad=9,fontweight='bold',fontsize=14)
            nl,nt=c.TO_GEO.transform(xy[:,0],xy[:,1]);vis=(nl>=x0)&(nl<=x1)&(nt>=y0)&(nt<=y1);error=float(np.max(abs(fun(points)-values)));peak=float(np.nanmax(zz[inside]));assert error<1e-4 and peak>=values[vis].max()-1e-5
            records.append(dict(unit=unit,model=model,period=period,native_receptors=len(values),maximum_native=float(values.max()),maximum_native_in_frame=float(values[vis].max()),maximum_displayed=peak,native_node_max_error=error,finite_coverage=coverage,scale=scale,current_run=True,color_norm='linear',display_lower_reference_ug_m3=.7,upper_open_color_class=vmax,values_not_clipped=True))

        barx=axes[-1].get_position().x1+1.65/wc;bar_bottom=bottom+.6;bar_length=side-1.2
        cbax=fig.add_axes([barx,bar_bottom/hc,.58/wc,bar_length/hc]);cb=fig.colorbar(ScalarMappable(norm=m.norm,cmap=cmap),cax=cbax,orientation='vertical',ticks=ticks,extend='neither')
        cb.outline.set_edgecolor('#49606c');cb.outline.set_linewidth(.65)
        cb.ax.set_yticklabels([f'{v:g}' if v!=vmax else f'≥{v:g}' for v in ticks]);cb.ax.yaxis.set_ticks_position('left');cb.ax.tick_params(labelsize=15,length=3,pad=3,color='#49606c')

        ppb=cb.ax.secondary_yaxis('right',functions=(lambda ug:ug/1.40,lambda ppb:ppb*1.40))
        ppb.set_yticks(np.asarray(ticks)/1.40)
        ppb.set_yticklabels([(f'{v/1.40:.1f}'.rstrip('0').rstrip('.') if v!=vmax else f'≥{v/1.40:.1f}') for v in ticks])
        ppb.tick_params(labelsize=14,length=3,pad=3,color='#49606c')
        unit_left=fig.text(barx-.10/wc,(bar_bottom+bar_length+.90)/hc,'µg/m³',ha='right',va='center',fontsize=13,color='#173445')
        unit_right=fig.text(barx+.78/wc,(bar_bottom+bar_length+.90)/hc,'ppb',ha='left',va='center',fontsize=13,color='#173445')
        for spine in ppb.spines.values():spine.set_visible(False)
        fig.canvas.draw();renderer=fig.canvas.get_renderer();last_frame=axes[-1].get_window_extent(renderer)
        labels=cb.ax.get_yticklabels()+ppb.get_yticklabels()+[unit_left,unit_right]
        clear_cm=min(t.get_window_extent(renderer).x0-last_frame.x1 for t in labels)/fig.dpi*2.54
        assert clear_cm>.20, (stem,'Colourbar labels overlap map',clear_cm)
        assert max(t.get_window_extent(renderer).x1 for t in labels)<fig.bbox.x1, 'Colourbar labels clipped'

        c.save(fig,stem,scale);c.META[stem].update(placeholder=False,panels=4,colorbar_orientation='vertical',colorbar_end_shape='flat',colorbar_length_cm=bar_length,colorbar_thickness_cm=.58,colorbar_map_gap_cm=1.65,colorbar_text_clearance_cm=clear_cm,statistic=period,concentrations_plotted=True,current_run=True,color_norm='linear',display_lower_reference_ug_m3=.7,upper_open_color_class=vmax,context_legend=False,secondary_unit='ppb',ug_m3_per_ppb=1.40,conversion_reference='NIOSH rounded factor; 25 C, 1 atm; ppb equivalent, not meteorology-dependent conversion',primary_ticks_ug_m3=ticks,secondary_ticks_ppb=(np.asarray(ticks)/1.40).tolist())
    (F/'Cartografia_metadados.json').write_text(json.dumps(c.META,indent=2),encoding='utf8');(F/'Faixas_concentracao_poster.json').write_text(json.dumps(dict(current_fields=records,annual_status='Derived from native hourly outputs by calendar year; CALPUFF 2025 coverage 99.68%',annual_statistic='Highest 2024 or 2025 annual mean per receptor; native model averaging rules retained',poster_scale=scale),indent=2),encoding='utf8')

    for p in F.glob('Comparacao_anual_placeholder*'):
        target=archive/p.name
        if p.is_file():
            if target.exists():p.unlink()
            else:shutil.move(str(p),str(target))
    gallery();print(json.dumps(records,indent=2))
# Gallery
def gallery():
    cards=[('Perfis_comparacao_modelos','How the model contrast changes with distance','Spatial medians and interquartile bands of hourly receptor P95 in six distance classes, using all 562/556 coincident receptors within 1800 m. Insets magnify smaller medians; the lower strip shows the difference of the two medians. These are descriptive spatial summaries, not confidence intervals.'),('Concordancia_P95_receptores','Receptor-level P95 comparison','Each point compares the hourly P95 at the same receptor in 2024. Main panels show a 0–30 ug/m3 zoom; separate full-range insets retain every extreme. Dashed line: equal concentrations. Shading: factor-of-two agreement. Indicators use every paired receptor within 1,800 m.'),('Fontes_privacidade','Sources and location','Current source geometry. Anonymous surrounding roads and buildings. Source map scale 1:2,500 at its intended poster dimensions. Treatment-unit and contextual keys are grouped separately.'),('Comparacao_24h_faixa','Maximum 24 h concentration envelopes','New native AERMOD POST and CALPOST RANK. Linear colours from light blue through green, yellow and orange to red, with an open upper class at 50 µg/m³. Grey is below 0.7 µg/m³. Each receptor may select a different date. CALPOST uses 24 h blocks starting at 23:00; AERMOD uses native calendar-day blocks.'),('Comparacao_anual_faixa','Highest annual mean per receptor, 2024–2025','Calculated from hourly outputs, not from 8,760 h RANK. CALPUFF includes all 8,784 hours of 2024 and 8,732 hours in 2025 (99.68%). Native model denominators are retained. Linear colour scale, open upper class at 10 µg/m³. The 0.7 µg/m³ display reference does not diagnose odour perception from annual means.'),('Boxplot_comparacao_poster','Hourly distributions: receptor P95 by distance','Complete year 2024. Each value is the hourly P95 at one receptor. Boxes describe the spatial distribution of these P95 values within each distance class. Tukey whiskers, outlier markers omitted. Concentrations remain on ordinary linear axes.'),('Boxplots_monitoramento_VM','WWTP 1: hourly boxplots at monitoring locations','Each pair shows the temporal distribution at one native location. Boxes are Q25–Q75, lines are medians and whiskers are P5–P95. No small values are deleted within selected points. Data are model predictions, not observed measurements.'),('Boxplots_monitoramento_NC','WWTP 2: hourly boxplots at monitoring locations','The two originally coincident monitoring IDs are represented by one spatial distribution. Every individual result remains in the detailed CSV and boxplot atlas.'),('Comparacao_distancia_poster','Concentration versus distance','Median and interquartile range of native maximum 24 h concentrations on coincident receptors. Different maxima may occur at different times.'),('Comparacao_anual_2024','Sensitivity: complete calendar year 2024 only','Avoids the incomplete last 28 hours of CALPUFF 2025. Complementary comparison.'),('Meteorologia_comparada','AERMET and CALMET meteorological distributions','Wind speed and direction distributions used by each model. CALMET first-layer centre: 10 m AGL. No event-time alignment assumed.'),('Resposta_meteorologica','Response conditional on each model’s weather','Concentrations at fixed common receptors within 100 m, grouped by wind speed and model-clock hour. Ordinary concentration axes.'),('Dispersao_pares_24h','Spatial comparison of 24 h maxima','Native unique coincident receptors. Colours indicate distance. This compares predictions, not accuracy against observations.')]
    s=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WWTP model comparison</title><style>body{font:16px Arial,sans-serif;max-width:1250px;margin:30px auto;padding:0 24px;color:#173445;background:#f4f7f8}article{background:white;margin:25px 0;padding:22px;border:1px solid #d7e0e3}img{display:block;max-width:100%;height:auto;margin:16px auto}a{color:#006b8d;margin-right:15px}p{line-height:1.5}</style><h1>Wastewater treatment plants · updated model comparison</h1><p>Current outputs supplied on 10 November 2026. Native concentrations are preserved. Linear triangulation is used for maps only, without extrapolation. Statistical comparisons use coincident native receptors and exclude duplicate locations. Anonymous source labels are retained.</p><p><a href="Poster_CMAS_Session05_WWTP.pdf">Poster PDF</a><a href="Poster_CMAS_Session05_WWTP.pptx">PowerPoint</a><a href="../comparacao_modelos/Comparacao_AERMOD_CALPUFF.pdf">Analysis report (Portuguese)</a></p><p>Context: supplied RMBH roads + © OpenStreetMap contributors, <a href="https://www.openstreetmap.org/copyright">ODbL</a>. No satellite imagery or facility names.</p>']
    s.append('<p><a href="../comparacao_modelos/Boxplots_Receptores.pdf">Individual receptor boxplot atlas</a><a href="../comparacao_modelos/Estatistica_horaria_por_receptor.csv">Hourly distribution statistics by receptor</a><a href="../comparacao_modelos/Comparacao_cota_altura_fontes.csv">Terrain elevation versus release height</a></p><p>The lower display reference of 0.7 µg/m³ corresponds to the lower end of the published ATSDR odour-threshold range at conventional conversion conditions. It is not a universal odour criterion. Values remain unchanged in the calculations and tables.</p>')
    s.append('<p>Vertical colour bars also show ppb equivalent on the right, using 1 ppb ≈1.40 µg/m³ at conventional 25°C and 1 atm (NIOSH). <a href="../comparacao_modelos/Concordancia_espacial_P95.csv">Spatial P95 agreement by distance</a><a href="../comparacao_modelos/Pares_concordancia_P95.csv">Receptor pairs and factor-two agreement</a>. These compare predictions without treating either model as an observation.</p>')
    for stem,title,note in cards:s.append(f'<article><h2>{html.escape(title)}</h2><p>{html.escape(note)}</p><img src="figuras/{stem}_previa.png" alt="{html.escape(title)}"><p><a href="figuras/{stem}.pdf">PDF vector</a><a href="figuras/{stem}.svg">SVG vector</a><a href="figuras/{stem}.png">PNG</a></p></article>')
    (O/'index.html').write_text('\n'.join(s+['</html>']),encoding='utf8')
if __name__=='__main__':main()
