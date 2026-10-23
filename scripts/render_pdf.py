# -*- coding: utf-8 -*-
"""docx -> PDF -> PNG 渲染, 并提取各章标题所在页码(用于目录回填)"""
import subprocess, sys, os, glob
import pymupdf

WORK = r'C:\Users\<你的用户名>\Desktop\论文项目\_work'
DOCX = r'C:\Users\<你的用户名>\Desktop\论文项目\交付\智能配电网光储协同的电压治理系统方案设计_课程报告.docx'
import shutil
_CAND = [shutil.which('soffice'),
         r'C:\Program Files\LibreOffice\program\soffice.exe',
         r'C:\Users\<你的用户名>\LO_portable\program\soffice.exe']
SOFFICE = next((p for p in _CAND if p and os.path.exists(p)), None)
PROFILE = '-env:UserInstallation=file:///' + os.path.expanduser('~').replace('\\', '/') + '/LO_profile'
assert SOFFICE, '未找到LibreOffice(soffice)，请安装或将路径加入PATH'
PAGES_DIR = WORK + r'\pages'

def render(docx_path=DOCX, outdir=WORK):
    for f in glob.glob(outdir + r'\*.pdf'):
        os.remove(f)
    r = subprocess.run([SOFFICE, '--headless', '--norestore', PROFILE,
                        '--convert-to', 'pdf', '--outdir', outdir, docx_path],
                       capture_output=True, text=True, timeout=300)
    pdfs = glob.glob(outdir + r'\*.pdf')
    assert pdfs, 'PDF conversion failed: ' + r.stdout + r.stderr
    return pdfs[0]

def to_pngs(pdf_path, pages_dir=PAGES_DIR, dpi=110):
    os.makedirs(pages_dir, exist_ok=True)
    for f in glob.glob(pages_dir + r'\*.png'):
        os.remove(f)
    doc = pymupdf.open(pdf_path)
    n = doc.page_count
    mat = pymupdf.Matrix(dpi / 72, dpi / 72)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat)
        pix.save(pages_dir + f'\\page_{i+1:02d}.png')
    print('pages rendered:', n)
    return doc, n

HEADINGS_L1 = ['1　绪论', '2　分布式光伏并网电压越限机理与调压资源特性分析',
               '3　光储协同电压治理系统架构设计', '4　分档位递进式协同调压控制策略设计',
               '5　典型台区参数配置与仿真验证', '6　总结与展望', '参考文献']
HEADINGS_L2 = ['1.1 研究背景与意义', '1.2 国内外研究现状', '1.3 报告主要内容与结构安排',
               '2.1 高渗透率分布式光伏并网电压越限机理分析', '2.2 光伏逆变器无功调压原理与特性',
               '2.3 储能系统有功/无功调压原理与特性', '2.4 单一资源调压的局限性与光储协同的必要性',
               '3.1 总体设计原则', '3.2 \u201c就地快速控制＋区域协同优化\u201d双层控制架构',
               '3.3 系统组成与信息交互设计', '3.4 与智能电网技术体系的融合',
               '4.1 电压合格区间与分级阈值设定', '4.2 过电压场景分档位递进式协同调压逻辑',
               '4.3 欠电压场景与夜间工况适配逻辑', '4.4 储能SOC保护硬约束设计',
               '5.1 典型低压居民台区场景与参数配置', '5.2 储能接入位置选型与容量配置',
               '5.3 Matlab/Simulink仿真验证方案', '5.4 准稳态预分析结果与预期结论',
               '6.1 方案总结', '6.2 展望']

def extract_headings(doc):
    """返回 {heading_text: 1-based physical page}, 及正文起始物理页"""
    page_texts = [doc[i].get_text() for i in range(doc.page_count)]
    # 正文起始页: 第一处出现 "1　绪论" 的页
    body_start = None
    for i, t in enumerate(page_texts):
        if '绪论' in t and '摘' not in t.split('绪论')[0][:50]:
            pass
    for i, t in enumerate(page_texts):
        if '1　绪论' in t.replace(' ', '').replace('\u3000', '') or ('绪论' in t and '1.1' in t):
            body_start = i + 1
            break
    res = {}
    for h in HEADINGS_L1 + HEADINGS_L2:
        key = h.replace(' ', '').replace('\u3000', '')
        found = None
        for i, t in enumerate(page_texts):
            if key in t.replace(' ', '').replace('\u3000', '').replace('\n', ''):
                found = i + 1
                break
        res[h] = found
    return res, body_start

if __name__ == '__main__':
    pdf = render()
    print('PDF:', pdf)
    doc, n = to_pngs(pdf)
    res, body_start = extract_headings(doc)
    print('body physical start page:', body_start)
    for h, pg in res.items():
        print(pg, h)
