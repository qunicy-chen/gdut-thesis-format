# -*- coding: utf-8 -*-
"""迭代收敛: 构建带目录的docx -> 渲染 -> 提取页码 -> 直到目录页码与实际一致"""
import json, sys, os, subprocess
sys.path.insert(0, r'C:\Users\<你的用户名>\Desktop\论文项目\_work')
import pymupdf
from render_pdf import (HEADINGS_L1, HEADINGS_L2, render, DOCX, WORK)
import report_content

def compute_entries(pdf_path):
    doc = pymupdf.open(pdf_path)
    page_texts = [doc[i].get_text() for i in range(doc.page_count)]
    norm = lambda t: t.replace(' ', '').replace('\u3000', '').replace('\n', '')
    # 目录页特征: 含引导点串(......)
    is_toc = lambda t: '.....' in t
    # 正文起始页: 非目录页中第一个含 "1.1"+"绪论" 的页
    body_start = None
    for i, t in enumerate(page_texts):
        if is_toc(t):
            continue
        if '1.1' in t and '绪论' in t:
            body_start = i + 1
            break
    offset = body_start - 1
    res = {}
    for h in HEADINGS_L1 + HEADINGS_L2:
        key = norm(h)
        for i, t in enumerate(page_texts):
            if i < body_start - 1 or is_toc(t):
                continue
            if key in norm(t):
                res[h] = i + 1
                break
    final = []
    for h1 in HEADINGS_L1:
        pfx = h1.split('\u3000')[0]
        final.append({'level': 1, 'text': h1.replace('\u3000', ' '), 'page': res[h1] - offset})
        for h2 in HEADINGS_L2:
            num = h2.split(' ')[0]
            if num.startswith(pfx + '.') and '.' not in num[len(pfx) + 1:]:
                final.append({'level': 2, 'text': h2, 'page': res[h2] - offset})
    toc_pages = [i + 1 for i, t in enumerate(page_texts) if is_toc(t)]
    return final, offset, doc.page_count, toc_pages

if __name__ == '__main__':
    pdf = render()
    entries, offset, npages, tocp = compute_entries(pdf)
    print('iter0: pages=%d toc_pages=%s offset=%d entries=%d' % (npages, tocp, offset, len(entries)))
    for it in range(1, 5):
        report_content.build(entries)
        pdf = render()
        new_entries, offset, npages, tocp = compute_entries(pdf)
        print('iter%d: pages=%d toc_pages=%s offset=%d entries=%d' % (it, npages, tocp, offset, len(new_entries)))
        if new_entries == entries:
            print('CONVERGED, TOC page numbers stable.')
            break
        entries = new_entries
    else:
        print('WARNING: not converged in 4 iterations')
    with open(WORK + r'\toc_data.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    for e in entries:
        print(e['level'], e['page'], e['text'])
