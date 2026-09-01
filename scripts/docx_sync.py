"""Post-process circa_1col.docx to visually match circa.html:
   (a) Figure 1 pipeline image -> full text-column width.
   (b) Worked-examples Table (Table 7): add cell borders, shade example bands
       (both the 'Ex. N' source rows and the '→ FHIR' band rows), color
       'conditional' / 'prohibited' amber and FHIR resource names in bold ink.
"""
from docx import Document
from docx.shared import Inches, RGBColor, Pt
from docx.oxml.ns import qn
from copy import deepcopy
from lxml import etree
import sys

INK   = RGBColor(0x19, 0x1d, 0x21)
TEAL  = RGBColor(0x0f, 0x76, 0x6e)
AMBER = RGBColor(0xb4, 0x53, 0x09)
MUTED = RGBColor(0x5c, 0x66, 0x70)
BAND_BG   = 'F3F4F2'   # matches --code-bg
RULE_HEX  = 'D2D7DB'   # --rule-strong
STRONG_HEX = '191D21'  # ink

def add_cell_border(cell, side, sz, color):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.find(qn('w:tcBorders'))
    if borders is None:
        borders = etree.SubElement(tcPr, qn('w:tcBorders'))
    old = borders.find(qn(f'w:{side}'))
    if old is not None:
        borders.remove(old)
    b = etree.SubElement(borders, qn(f'w:{side}'))
    b.set(qn('w:val'), 'single')
    b.set(qn('w:sz'), str(sz))
    b.set(qn('w:color'), color)

def shade_cell(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    old = tcPr.find(qn('w:shd'))
    if old is not None:
        tcPr.remove(old)
    shd = etree.SubElement(tcPr, qn('w:shd'))
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)

def cell_text(cell):
    return ''.join(p.text for p in cell.paragraphs)

def is_band_row(row, ncols):
    """Bands are colspan=8 rows in the HTML; python-docx sees them as N cells
    (merged). Detect via: text starts with 'Ex.' or '→' AND all cell texts equal
    (merged cells share the same text)."""
    texts = [cell_text(c) for c in row.cells]
    joined = texts[0].strip()
    if not joined:
        return False
    # merged-cell rows have all N cell.text equal to the joined text
    if all(t == texts[0] for t in texts):
        if joined.startswith('Ex.') or joined.startswith('→') or joined.startswith('→') or joined.startswith('->'):
            return True
    return False

def color_run(run, color, bold=False):
    run.font.color.rgb = color
    if bold:
        run.font.bold = True

def process_worked_table(tbl):
    """Style the worked-examples table."""
    ncols = len(tbl.rows[0].cells)
    # 1) light cell grid on every cell
    for row in tbl.rows:
        for cell in row.cells:
            for side in ('top','left','bottom','right'):
                add_cell_border(cell, side, 4, RULE_HEX)   # 4 = 0.5pt
    # 2) shade band rows + heavy top rule above 'Ex.' rows
    for row in tbl.rows:
        if is_band_row(row, ncols):
            for cell in row.cells:
                shade_cell(cell, BAND_BG)
                # detect Ex. row (source sentence header) vs → row (FHIR/use)
            if cell_text(row.cells[0]).strip().startswith('Ex.'):
                for cell in row.cells:
                    add_cell_border(cell, 'top', 18, STRONG_HEX)   # ~2.25pt heavy
    # 3) color runs: 'conditional' / 'prohibited' -> amber; FHIR resource -> bold ink
    FHIR = {'ServiceRequest','MedicationRequest','CommunicationRequest'}
    AMBER_WORDS = {'conditional','prohibited'}
    for row in tbl.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    if run.text.strip() in AMBER_WORDS:
                        color_run(run, AMBER)
                    elif run.text.strip() in FHIR:
                        color_run(run, INK, bold=True)
                    elif run.text.strip() in ('→','→'):
                        color_run(run, MUTED)

def find_worked_examples_table(doc):
    """The worked-examples table has a header row whose FIRST cell is 'action'
    (after we dropped the '#' column) — that's unique in this document."""
    for tbl in doc.tables:
        if not tbl.rows:
            continue
        first = [cell_text(c).strip().lower() for c in tbl.rows[0].cells]
        if first[:3] == ['action','type','target (code)']:
            return tbl
    return None

def enlarge_pipeline_figure(doc, target_inches=6.5):
    """Set the pipeline figure to full text-column width AND fix its containing
    figure-wrapper table (image left / caption right) by stacking rows: image on
    row 1 spanning both columns, caption on row 2 spanning both columns."""
    W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    for shape in doc.inline_shapes:
        w, h = int(shape.width), int(shape.height)
        if not h: continue
        ratio = w / h
        if ratio <= 1.15: continue
        # 1) resize
        new_w = Inches(target_inches)
        scale = float(new_w) / float(shape.width)
        shape.height = int(shape.height * scale)
        shape.width = new_w
        # 2) walk up to find containing <w:r> and its <w:p> parent
        node = shape._inline
        image_run = None
        while node is not None:
            if node.tag == f'{{{W_NS}}}r':
                image_run = node; break
            node = node.getparent()
        if image_run is None: continue
        para_el = image_run.getparent()
        if para_el is None or not para_el.tag.endswith('}p'): continue
        # 3) find enclosing figure-wrapper table (image cell + caption cell)
        node = para_el
        tc_el = tbl_el = None
        while node is not None:
            if node.tag.endswith('}tc') and tc_el is None:
                tc_el = node
            elif node.tag.endswith('}tbl'):
                tbl_el = node; break
            node = node.getparent()
        if tc_el is not None and tbl_el is not None:
            # We have a table wrapping (image_cell | caption_cell). Restructure
            # so image spans full width in row 1 and caption spans full width
            # in a new row 2. Preserve the caption cell's paragraphs.
            rows = [r for r in tbl_el if r.tag.endswith('}tr')]
            for row in rows:
                cells = [c for c in row if c.tag.endswith('}tc')]
                if len(cells) < 2:
                    continue
                first, second = cells[0], cells[1]
                # 1) grid-span the first cell to full width
                tcPr = first.find(qn('w:tcPr'))
                if tcPr is None:
                    tcPr = etree.SubElement(first, qn('w:tcPr'))
                    first.insert(0, tcPr)
                for tag in ('w:gridSpan','w:tcW'):
                    old = tcPr.find(qn(tag))
                    if old is not None: tcPr.remove(old)
                gs = etree.SubElement(tcPr, qn('w:gridSpan'))
                gs.set(qn('w:val'), str(len(cells)))
                # 2) build a NEW row that carries the caption content
                # copy the row's trPr if present, from the current row
                cap_row = etree.Element(qn('w:tr'))
                trPr_src = row.find(qn('w:trPr'))
                if trPr_src is not None:
                    cap_row.append(deepcopy(trPr_src))
                cap_tc = etree.SubElement(cap_row, qn('w:tc'))
                # grid-span the caption cell too
                cap_tcPr = etree.SubElement(cap_tc, qn('w:tcPr'))
                cap_gs = etree.SubElement(cap_tcPr, qn('w:gridSpan'))
                cap_gs.set(qn('w:val'), str(len(cells)))
                # move all paragraphs/tables from the ORIGINAL second cell into cap_tc
                for child in list(second):
                    if child.tag == qn('w:tcPr'): continue
                    second.remove(child)
                    cap_tc.append(child)
                # 3) remove the (now-empty) second cell from the original row
                row.remove(second)
                # 4) insert cap_row right after the current row
                row.addnext(cap_row)
            # widen the table grid to a single full-width column
            tblGrid = tbl_el.find(qn('w:tblGrid'))
            if tblGrid is not None:
                for gc in list(tblGrid):
                    tblGrid.remove(gc)
                new_gc = etree.SubElement(tblGrid, qn('w:gridCol'))
                new_gc.set(qn('w:w'), str(int(new_w * 1440 / 914400)))  # twips
        # 4) center the image paragraph
        pPr = para_el.find(qn('w:pPr'))
        if pPr is None:
            pPr = etree.SubElement(para_el, qn('w:pPr'))
            para_el.insert(0, pPr)
        jc = pPr.find(qn('w:jc'))
        if jc is not None: pPr.remove(jc)
        jc = etree.SubElement(pPr, qn('w:jc'))
        jc.set(qn('w:val'), 'center')
        # 5) style the caption paragraphs (in the new caption cell we just built)
        #    - Only 'Figure 1.' bold, rest normal
        #    - Paragraph alignment = justified
        if tbl_el is not None:
            style_pipeline_caption(tbl_el)
        return True
    return False

def style_pipeline_caption(tbl_el):
    """Inside the pipeline figure's wrapper table, find caption paragraphs and:
    - justify them
    - keep bold ONLY on the leading 'Figure 1.' label, unbold the rest.
    """
    rows = [r for r in tbl_el if r.tag.endswith('}tr')]
    if len(rows) < 2: return
    caption_row = rows[-1]   # the row we just added
    for cell in [c for c in caption_row if c.tag.endswith('}tc')]:
        for para in [p for p in cell if p.tag.endswith('}p')]:
            # justify
            pPr = para.find(qn('w:pPr'))
            if pPr is None:
                pPr = etree.Element(qn('w:pPr'))
                para.insert(0, pPr)
            jc = pPr.find(qn('w:jc'))
            if jc is not None: pPr.remove(jc)
            jc2 = etree.SubElement(pPr, qn('w:jc'))
            jc2.set(qn('w:val'), 'both')   # justified in OOXML
            # unbold everything except the leading 'Figure N.' label
            runs = [r for r in para if r.tag.endswith('}r')]
            # concatenate run texts to find the boundary
            texts = []
            for r in runs:
                t = ''.join(el.text or '' for el in r.findall(qn('w:t')))
                texts.append(t)
            joined = ''.join(texts)
            # match 'Figure <N>.'
            import re as _re
            m = _re.match(r'^\s*Figure\s+\d+\.', joined)
            boundary = m.end() if m else 0
            # walk runs; keep bold up to boundary, remove bold after
            offset = 0
            for r, t in zip(runs, texts):
                start, end = offset, offset+len(t)
                offset = end
                rPr = r.find(qn('w:rPr'))
                if rPr is None: continue
                if start >= boundary:
                    # after boundary: remove bold
                    for tag in ('w:b','w:bCs'):
                        b = rPr.find(qn(tag))
                        if b is not None: rPr.remove(b)

def convert_accents_to_black(doc):
    """Camera-ready convention: all text black. Convert teal/muted/amber runs
    to black across the document body (does NOT touch table cell content — the
    banded Table 7 keeps its amber accents for meaningful signal)."""
    n = 0
    for para in doc.paragraphs:
        for run in para.runs:
            if run.font.color is not None and run.font.color.rgb is not None:
                rgb = run.font.color.rgb
                if rgb == TEAL or rgb == MUTED:
                    run.font.color.rgb = RGBColor(0, 0, 0)
                    n += 1
    # Also fix style-level colors on Heading styles + section-num
    for style_name in ('Heading 1','Heading 2','Heading 3','Heading 4','Title','Subtitle'):
        try:
            s = doc.styles[style_name]
            if s.font.color is not None and s.font.color.rgb is not None:
                s.font.color.rgb = RGBColor(0, 0, 0); n += 1
        except KeyError:
            pass
    return n

def shrink_narrow_figures_to_single_column(doc, single_col_inches=3.15,
                                            names_to_shrink=('fig1_field_presence',)):
    """Sparse/small figures should be single-column so prose flows around them
    (avoids half-empty pages when a full-width float dominates). Match by embedded
    image filename in `pic:cNvPr@descr`, so this is explicit and stable."""
    W_PIC = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
    n = 0
    for shape in doc.inline_shapes:
        inline = shape._inline
        cNvPr = inline.findall('.//'+ '{'+W_PIC+'}cNvPr')
        descrs = [el.get('descr','') for el in cNvPr]
        if not any(any(name in d for name in names_to_shrink) for d in descrs):
            continue
        new_w = Inches(single_col_inches)
        if shape.width > new_w:
            scale = float(new_w) / float(shape.width)
            shape.height = int(shape.height * scale)
            shape.width = new_w
            n += 1
    return n

def move_captions_into_wide_sections(doc):
    """When a table spans both columns (full-width float via continuous section
    breaks), its caption should also span both columns. Pandoc places the caption
    AFTER the section-return-to-2-columns, so it renders in one column.

    Detect: a paragraph whose text starts with 'Table N.' or 'Figure N.', that
    lives in a 2-column section, immediately after a full-width (1-column) block.
    Move it INSIDE the preceding 1-column section by inserting a sectPr right
    after the caption paragraph that mirrors the previous 1-column section, and
    push the return-to-2-columns to after the caption."""
    from copy import deepcopy
    W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    body = doc.element.body
    paras = [el for el in body if el.tag == qn('w:p')]
    moved = 0
    for i, p in enumerate(paras):
        text = ''.join(t.text or '' for t in p.findall('.//'+qn('w:t')))
        import re
        if not re.match(r'^\s*(Table|Figure)\s+\d+\.', text):
            continue
        # find the paragraph just before this one that carries a sectPr (section break)
        # its sectPr defines the section this caption's PREDECESSOR belonged to
        for j in range(i-1, -1, -1):
            q = paras[j]
            pPr = q.find(qn('w:pPr'))
            if pPr is None: continue
            sectPr = pPr.find(qn('w:sectPr'))
            if sectPr is None: continue
            # is that section 1-column (wide)?
            cols = sectPr.find(qn('w:cols'))
            if cols is None: continue
            n_cols = int(cols.get(qn('w:num')) or '1')
            if n_cols != 1: break  # not a wide section, don't touch
            # Move the sectPr from q -> caption p (so caption stays in 1-col; break comes AFTER caption)
            captionPr = p.find(qn('w:pPr'))
            if captionPr is None:
                captionPr = etree.SubElement(p, qn('w:pPr'))
                p.insert(0, captionPr)
            # remove any existing sectPr on caption
            old_cap_sect = captionPr.find(qn('w:sectPr'))
            if old_cap_sect is not None: captionPr.remove(old_cap_sect)
            captionPr.append(deepcopy(sectPr))
            # remove from q's pPr
            pPr.remove(sectPr)
            moved += 1
            break
    return moved

def fix_abstract_keywords_spacing(doc, gap_pt=6):
    """Add breathing room between the abstract paragraph and the keywords line
    (which currently sit flush against each other)."""
    n = 0
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text.startswith('Keywords:'):
            pf = p.paragraph_format
            pf.space_before = Pt(gap_pt)
            n += 1
    return n

def add_top_margin_above_wide_floats(doc, gap_pt=10):
    """Wide (full-width) tables/figures land flush against the top text margin
    in Word because the paragraph carrying the section break has its own height
    minimized. Add a small SPACER paragraph inside each 1-column section,
    immediately before the first content block, with an exact line height so the
    gap actually renders."""
    W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    body = doc.element.body
    added = 0
    # walk block children of body in order; a 1-col section is marked by a
    # sectPr with <w:cols w:num='1'/> on some paragraph; the previous 2-col
    # section ends there. The 1-col section spans from the previous sectPr-end
    # to that paragraph.
    def is_one_col_break(pPr):
        if pPr is None: return False
        sectPr = pPr.find(qn('w:sectPr'))
        if sectPr is None: return False
        cols = sectPr.find(qn('w:cols'))
        if cols is None: return True   # default = 1-col
        return int(cols.get(qn('w:num')) or '1') == 1
    kids = list(body)
    # for each paragraph carrying a 1-col section break, walk back to find the
    # start of that 1-col section (right after the previous sectPr) and insert
    # a spacer paragraph AT that start position, in front of the first non-break block
    for i, el in enumerate(kids):
        if el.tag != qn('w:p'): continue
        pPr = el.find(qn('w:pPr'))
        if not is_one_col_break(pPr): continue
        # find start of THIS 1-col section: paragraph after the most recent sectPr in [:i]
        start = 0
        for j in range(i-1, -1, -1):
            prev = kids[j]
            if prev.tag != qn('w:p'): continue
            prev_pPr = prev.find(qn('w:pPr'))
            if prev_pPr is None: continue
            if prev_pPr.find(qn('w:sectPr')) is not None:
                start = j + 1; break
        # skip empty leading paragraphs to find first content block
        first_content = None
        for j in range(start, i):
            k = kids[j]
            if k.tag == qn('w:tbl') or (k.tag == qn('w:p') and (k.findall('.//'+qn('w:t')) or k.findall('.//'+qn('w:drawing')))):
                first_content = k; break
        if first_content is None: continue
        # insert a spacer paragraph BEFORE first_content
        spacer = etree.Element(qn('w:p'))
        sp_pPr = etree.SubElement(spacer, qn('w:pPr'))
        sp_sp = etree.SubElement(sp_pPr, qn('w:spacing'))
        # exact line height so Word doesn't clamp it
        twips = int(gap_pt * 20)   # 20 twips per pt
        sp_sp.set(qn('w:line'), str(twips))
        sp_sp.set(qn('w:lineRule'), 'exact')
        sp_sp.set(qn('w:before'), '0')
        sp_sp.set(qn('w:after'), '0')
        first_content.addprevious(spacer)
        added += 1
    return added

def tighten_caption_spacing(doc, before_pt=2, after_pt=2):
    """Reduce space above/below captions so figures/tables sit close to their
    caption text. The Word 'Table Caption' style defaults to a 12pt space-before
    which looks like an accidental gap in 2-column journal layout. We tighten
    both 'Table Caption' and 'Image Caption' to ~2pt each side."""
    n = 0
    for style_name in ('Table Caption','Image Caption','Caption'):
        try:
            s = doc.styles[style_name]
            pf = s.paragraph_format
            pf.space_before = Pt(before_pt)
            pf.space_after = Pt(after_pt)
            n += 1
        except KeyError:
            pass
    # also override on each caption paragraph in case a direct property was set
    import re
    for p in doc.paragraphs:
        if re.match(r'^\s*(Table|Figure)\s+\d+\.', p.text):
            pf = p.paragraph_format
            pf.space_before = Pt(before_pt)
            pf.space_after = Pt(after_pt)
    return n

def main(path):
    doc = Document(path)
    tbl = find_worked_examples_table(doc)
    if tbl:
        process_worked_table(tbl)
        print(f'Table 7 styled: {len(tbl.rows)} rows')
    else:
        print('WARN: worked-examples table not found')
    ok = enlarge_pipeline_figure(doc)
    print(f'Figure 1 enlarged to full width: {ok}')
    n_shrunk = shrink_narrow_figures_to_single_column(doc)
    print(f'narrow figures shrunk to single column: {n_shrunk}')
    n_cap = move_captions_into_wide_sections(doc)
    print(f'captions moved into wide sections: {n_cap}')
    n_black = convert_accents_to_black(doc)
    print(f'runs/styles color -> black: {n_black}')
    n_cap_sp = tighten_caption_spacing(doc)
    print(f'caption styles tightened: {n_cap_sp}')
    n_topmar = add_top_margin_above_wide_floats(doc)
    print(f'top-margin spacers added above wide floats: {n_topmar}')
    n_kw = fix_abstract_keywords_spacing(doc)
    print(f'abstract/keywords spacing fixed: {n_kw}')
    doc.save(path)
    print(f'saved -> {path}')

if __name__ == '__main__':
    main(sys.argv[1])
