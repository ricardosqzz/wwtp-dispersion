# ENTRADAS: arquivos Markdown indicados na linha de comando; títulos, parágrafos, listas, tabelas e links.
# SAÍDAS: DOCX e PDF ao lado de cada Markdown; mesma estrutura editorial dos guias de preparação.
# CAMINHOS: argumentos de arquivo e DOCUMENT_FONT_DIR; executar com as dependências documentais instaladas.
from pathlib import Path
import argparse
import html
import os
import re
import textwrap
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

# Registrar fontes
def registrar_fontes():
    folder=Path(os.environ.get('DOCUMENT_FONT_DIR','C:/Windows/Fonts'))
    candidates=[(folder/'arial.ttf',folder/'arialbd.ttf',folder/'ariali.ttf',folder/'consola.ttf'),tuple(Path('/usr/share/fonts/truetype/dejavu')/n for n in ['DejaVuSans.ttf','DejaVuSans-Bold.ttf','DejaVuSans-Oblique.ttf','DejaVuSansMono.ttf'])]
    for normal,bold,italic,code in candidates:
        if all(p.exists() for p in [normal,bold,italic,code]):
            for name,path in [('Body',normal),('BodyBold',bold),('BodyItalic',italic),('Code',code)]:pdfmetrics.registerFont(TTFont(name,str(path)))
            pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold');return
    raise FileNotFoundError('Informe DOCUMENT_FONT_DIR com Arial e Consolas ou instale DejaVu Sans e DejaVu Sans Mono.')

# Blocos
def blocos(text):
    lines=text.splitlines();i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            yield 'code','\n'.join(code);i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                if not re.fullmatch(r'[| :\-]+',lines[i]):rows.append([s.strip() for s in lines[i].strip('|').split('|')])
                i+=1
            yield 'table',rows;continue
        if line.startswith('#'):
            n=len(line)-len(line.lstrip('#'));yield 'h'+str(min(n,3)),line.lstrip('# ');i+=1;continue
        if line=='<!-- PAGEBREAK -->':yield 'break','';i+=1;continue
        if line.startswith('- '):yield 'bullet',line[2:];i+=1;continue
        if line.startswith('> '):yield 'quote',line[2:];i+=1;continue
        buf=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','- ','> ')):
            buf.append(lines[i]);i+=1
        yield 'p',' '.join(buf)

# Texto simples
def texto_simples(s):
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
    return s.replace('**','').replace('`','')

# Inline pdf
def inline_pdf(s):
    s=html.escape(s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Code" size="9">\1</font>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<link href="\2" color="#19556d">\1</link>',s)
    return s

# Criar docx
def criar_docx(path,content):
    doc=Document();sec=doc.sections[0];sec.page_height=Cm(29.7);sec.page_width=Cm(21)
    sec.top_margin=sec.bottom_margin=Cm(2);sec.left_margin=sec.right_margin=Cm(2)
    for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','List Bullet']:
        st=doc.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0);st._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hAnsi'),'Arial')
    normal=doc.styles['Normal'];normal.font.size=Pt(11);normal.paragraph_format.space_after=Pt(6);normal.paragraph_format.line_spacing=1.12;normal.paragraph_format.widow_control=True
    doc.styles['Title'].font.size=Pt(21);doc.styles['Title'].font.bold=True
    for border in list(doc.styles.element.xpath('.//w:pBdr')):border.getparent().remove(border)
    for st,size in [('Heading 1',15),('Heading 2',12.5),('Heading 3',11.5)]:
        doc.styles[st].font.size=Pt(size);doc.styles[st].font.bold=True;doc.styles[st].paragraph_format.space_before=Pt(14);doc.styles[st].paragraph_format.space_after=Pt(7);doc.styles[st].paragraph_format.keep_with_next=True
    first=True
    for index,(kind,data) in enumerate(content):
        if kind.startswith('h'):
            p=doc.add_paragraph(data,'Title' if first else 'Heading '+str(min(int(kind[1:])-1,3) or 1));first=False
        elif kind=='table':
            n=max(len(row) for row in data);t=doc.add_table(rows=0,cols=n);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
            widths=[17/n]*n
            if n==3:widths=[3.0,5.0,9.0]
            if n==3 and data[0][0]=='Componente':widths=[4.1,6.3,6.6]
            if n==3 and data[0][0]=='Função/interface':widths=[5.4,1.8,9.8]
            if n==2:widths=[5.5,11.5]
            for j,row in enumerate(data):
                cells=t.add_row().cells
                for k,value in enumerate(row):
                    cells[k].width=Cm(widths[k]);p=cells[k].paragraphs[0];r=p.add_run(texto_simples(value));r.font.size=Pt(9.3);r.bold=j==0
                    p.paragraph_format.space_after=Pt(4);p.paragraph_format.space_before=Pt(4);p.paragraph_format.line_spacing=1.1
                    cells[k].vertical_alignment=1
                    tcpr=cells[k]._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
                    for side in ['top','left','bottom','right']:
                        edge=OxmlElement('w:'+side);edge.set(qn('w:val'),'single');edge.set(qn('w:sz'),'4');edge.set(qn('w:color'),'D9D9D9');borders.append(edge)
                    tcpr.append(borders)
                    if j==0:
                        shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E9EFF2');cells[k]._tc.get_or_add_tcPr().append(shade)
                if j==0:
                    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
                cant=OxmlElement('w:cantSplit');t.rows[-1]._tr.get_or_add_trPr().append(cant)
            doc.add_paragraph()
        elif kind=='code':
            wrapped=[]
            for line in data.expandtabs(4).splitlines():
                wrapped.extend(textwrap.wrap(line,width=98,replace_whitespace=False,drop_whitespace=False,subsequent_indent='    ') or [' '])
            for line in wrapped:
                p=doc.add_paragraph();p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.02;p.paragraph_format.left_indent=Cm(.3)
                r=p.add_run(line or ' ');r.font.name='Consolas';r.font.size=Pt(8.2)
            doc.add_paragraph().paragraph_format.space_after=Pt(3)
        elif kind=='break':doc.add_page_break()
        else:
            p=doc.add_paragraph(style='List Bullet' if kind=='bullet' else 'Normal')
            if kind=='quote':p.paragraph_format.left_indent=Cm(.5)
            if data.startswith('**') and data.endswith('?**'):p.paragraph_format.keep_with_next=True
            if index+1<len(content) and content[index+1][0]=='p' and content[index+1][1].startswith('**English answer.**'):p.paragraph_format.keep_with_next=True
            parts=re.split(r'(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))',data)
            for part in parts:
                if not part:continue
                link=re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)',part)
                if link:
                    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),doc.part.relate_to(link[2],RT.HYPERLINK,is_external=True));run=OxmlElement('w:r');rp=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),'19556D');rp.append(color);run.append(rp);t=OxmlElement('w:t');t.text=link[1];run.append(t);h.append(run);p._p.append(h);continue
                r=p.add_run(texto_simples(part));r.bold=part.startswith('**')
                if part.startswith('`'):r.font.name='Consolas';r.font.size=Pt(9)
    footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)
    doc.core_properties.author='Ricardo Silva Queiroz';doc.core_properties.title=next(v for k,v in content if k=='h1')
    doc.save(path)

# Pdfcommarcadores
class PDFComMarcadores(SimpleDocTemplate):
    def afterFlowable(self,flow):
        if isinstance(flow,Paragraph) and getattr(flow,'bookmark_level',None) is not None:
            level=flow.bookmark_level;key='s'+str(self.seq.nextf('heading'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(flow.getPlainText(),key,level=level,closed=False)

# Criar pdf
def criar_pdf(path,content):
    registrar_fontes()
    styles={
        'title':ParagraphStyle('title',fontName='BodyBold',fontSize=20,leading=25,spaceAfter=16,textColor=colors.black,keepWithNext=True),
        'h1':ParagraphStyle('h1',fontName='BodyBold',fontSize=14,leading=18,spaceBefore=14,spaceAfter=7,keepWithNext=True),
        'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=12,leading=16,spaceBefore=12,spaceAfter=6,keepWithNext=True),
        'h3':ParagraphStyle('h3',fontName='BodyBold',fontSize=11.2,leading=15,spaceBefore=10,spaceAfter=5,keepWithNext=True),
        'body':ParagraphStyle('body',fontName='Body',fontSize=10.6,leading=14.7,spaceAfter=7,splitLongWords=True,allowWidows=0,allowOrphans=0),
        'table':ParagraphStyle('table',fontName='Body',fontSize=8.6,leading=11,splitLongWords=True),
        'code':ParagraphStyle('code',fontName='Code',fontSize=7.8,leading=10.1,spaceAfter=5,leftIndent=7),
    }
    story=[];first=True
    for kind,data in content:
        if kind.startswith('h'):
            style=styles['title'] if first else styles['h'+str(min(int(kind[1:])-1,3) or 1)];p=Paragraph(inline_pdf(data),style)
            if not first:p.bookmark_level=min(int(kind[1:])-2,1) if int(kind[1:])>=2 else 0
            first=False;story.append(p)
        elif kind=='table':
            n=max(len(row) for row in data);widths=[481/n]*n
            if n==3:widths=[77,133,271]
            if n==2:widths=[156,325]
            rows=[[Paragraph(inline_pdf(str(v)),styles['table']) for v in row] for row in data]
            t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9EFF2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#CFD9DE'))]));story.extend([t,Spacer(1,10)])
        elif kind=='code':
            wrapped=[]
            for line in data.expandtabs(4).splitlines():wrapped.extend(textwrap.wrap(line,width=102,replace_whitespace=False,drop_whitespace=False,subsequent_indent='    ') or [' '])
            story.append(Preformatted('\n'.join(wrapped),styles['code']))
        elif kind=='break':story.append(PageBreak())
        else:
            text=inline_pdf(data)
            if kind=='bullet':text='• '+text
            story.append(Paragraph(text,styles['body']))
    def footer(canv,doc):
        canv.setFont('Body',8);canv.setFillColor(colors.HexColor('#586771'));canv.drawRightString(538,30,str(doc.page))
    pdf=PDFComMarcadores(str(path),pagesize=A4,rightMargin=56.7,leftMargin=56.7,topMargin=51,bottomMargin=48,title=next(v for k,v in content if k=='h1'),author='Ricardo Silva Queiroz')
    pdf.build(story,onFirstPage=footer,onLaterPages=footer)

# Main
def main():
    p=argparse.ArgumentParser();p.add_argument('arquivos',nargs='+');p.add_argument('--somente-pdf',action='store_true');p.add_argument('--somente-word',action='store_true');args=p.parse_args()
    for name in args.arquivos:
        src=Path(name);content=list(blocos(src.read_text('utf-8-sig')))
        if not args.somente_pdf:criar_docx(src.with_suffix('.docx'),content)
        if not args.somente_word:criar_pdf(src.with_suffix('.pdf'),content)
        print('DOCUMENTO',str(src.with_suffix('.docx') if args.somente_word else src.with_suffix('.pdf')),flush=True)

if __name__=='__main__':main()
