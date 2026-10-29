"""Render only the core's explicit public projection; never open workspace files."""
from __future__ import annotations

import base64
import html
import json
import re
import posixpath


def prose(text, origin='', targets=None):
    """Safe Markdown subset for authored research, including tables and pinned links."""
    targets = targets or {}
    def inline(value):
        value = html.escape(value)
        def link(match):
            label, url = match.groups()
            raw = html.unescape(url)
            if raw.startswith(('http://', 'https://')):
                return '<a href="' + html.escape(raw, quote=True) + '" rel="noreferrer">' + label + ' ↗</a>'
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(origin), raw.split('#')[0]))
            if resolved in targets:
                return '<a href="#' + html.escape(targets[resolved], quote=True) + '">' + label + '</a>'
            return label + ' <small>〔外部材料：' + url + '〕</small>'
        value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, value)
        value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
        return re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    lines, blocks, i = str(text).splitlines(), [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            blocks.append('<pre>' + html.escape('\n'.join(code)) + '</pre>')
        elif line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[ :|\-]+\|$', lines[i+1]):
            cells = lambda row: row.strip().strip('|').split('|')
            headers = cells(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append('<tr>' + ''.join('<td>' + inline(x.strip()) + '</td>' for x in cells(lines[i])) + '</tr>'); i += 1
            blocks.append('<div class="table"><table><thead><tr>' + ''.join('<th>' + inline(x.strip()) + '</th>' for x in headers) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
            continue
        elif re.match(r'^#{1,6} ', line):
            blocks.append('<h3>' + inline(re.sub(r'^#+ ', '', line)) + '</h3>')
        elif re.match(r'^[-*] ', line):
            items = []
            while i < len(lines) and re.match(r'^[-*] ', lines[i]):
                items.append('<li>' + inline(lines[i][2:]) + '</li>'); i += 1
            blocks.append('<ul>' + ''.join(items) + '</ul>')
            continue
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|[-*] |\|)', lines[i]):
                paragraph.append(lines[i]); i += 1
            blocks.append('<p>' + '<br>'.join(inline(x) for x in paragraph) + '</p>')
            continue
        i += 1
    return ''.join(blocks)


def preview(lab, selected, title):
    bundle = lab.public_projection(selected)
    objects, artifacts = bundle['objects'], bundle['artifacts']
    by_key = {(o['id'], o['revision']): o for o in objects}
    targets = {o['body']['origin']: o['id'] + '-' + str(o['revision']) for o in objects if o['body'].get('origin')}
    blocks, markdown = [], ['# ' + title, '', 'Explicit public projection; private dependencies are withheld.', '']
    for obj in objects:
        anchor = obj['id'] + '-' + str(obj['revision'])
        body = obj['body']
        text = body.get('text', body.get('summary', body.get('interpretation', '')))
        if str(text).splitlines()[:1] == ['# ' + obj['title']]:
            text = str(text).split('\n', 1)[-1]
        content = prose(text, body.get('origin', ''), targets)
        limits = body.get('limits', [])
        if limits:
            content += '<aside>' + ''.join('<p>' + html.escape(str(x)) + '</p>' for x in limits) + '</aside>'
        digest = body.get('artifact_digest')
        if digest in artifacts:
            raw = artifacts[digest]
            if obj['kind'] == 'snapshot':
                payload = json.loads(raw)
                # SVG renders as an image, never active markup in the reader document.
                for key, svg in payload.get('assets', {}).items():
                    image = base64.b64encode(svg.encode()).decode()
                    content += '<details><summary>' + html.escape(key) + '</summary><img alt="' + html.escape(key) + '" src="data:image/svg+xml;base64,' + image + '"></details>'
            content += '<details><summary>展开随包保存的原文 / 模型材料</summary><pre>' + html.escape(raw) + '</pre></details>'
        links = []
        for ref in obj['refs']:
            if ref.get('withheld'):
                links.append('<li>' + html.escape(ref['relation']) + ' · 未披露依赖；本包不可验证</li>')
            else:
                target = by_key[(ref['id'], ref['revision'])]
                links.append('<li>' + html.escape(ref['relation']) + ' · <a href="#' + html.escape(ref['id'] + '-' + str(ref['revision'])) + '">' + html.escape(target['title']) + ' · r' + str(ref['revision']) + '</a></li>')
        if links:
            content += '<details open><summary>证据关系</summary><ul>' + ''.join(links) + '</ul></details>'
        metadata = {k: body[k] for k in ('evidence', 'acceptance', 'origin', 'version', 'reading_scope', 'commit', 'boundary') if k in body}
        if metadata:
            content += '<details><summary>版本、边界与证据状态</summary><pre>' + html.escape(json.dumps(metadata, ensure_ascii=False, indent=2)) + '</pre></details>'
        blocks.append('<section id="' + html.escape(anchor) + '"><p class="label">' + html.escape(obj['kind']) + ' · revision ' + str(obj['revision']) + '</p><h2>' + html.escape(obj['title']) + '</h2>' + content + '</section>')
        markdown += ['## ' + obj['title'], '', str(text), '', *['- ' + str(x) for x in limits], '', 'Evidence references:', *['- ' + r['relation'] + ': ' + ('withheld' if r.get('withheld') else r['id'] + ' revision ' + str(r['revision'])) for r in obj['refs']], '']
    inventory = [{'id': o['id'], 'revision': o['revision'], 'kind': o['kind'], 'title': o['title']} for o in objects]
    document = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '''</title><style>
body{margin:0;background:#f4f5ef;color:#183e36;font:18px/1.8 system-ui,sans-serif}main{max-width:850px;margin:48px auto;padding:24px}h1{font:48px/1.2 Georgia,serif}h2{font-size:28px}h3{font-size:21px}table{border-collapse:collapse;font-size:14px;width:100%}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #c9d3ca}th{background:#e5ebe2}.table{overflow:auto}code{font-size:.86em;overflow-wrap:anywhere}small{font-size:12px;color:#61756c}.label{font:12px/1.5 system-ui;color:#7b6541;letter-spacing:.1em}section{padding:24px 0;border-top:1px solid #c9d3ca}p,li,pre{overflow-wrap:anywhere}pre{white-space:pre-wrap;font:14px/1.6 ui-monospace,monospace;background:#e9ede5;padding:16px}aside{border-left:3px solid #9d7644;padding-left:20px;font-size:15px}details{margin-top:20px}summary{cursor:pointer}img{max-width:100%;height:auto}a{color:inherit;text-underline-offset:4px}footer{margin-top:48px;font-size:14px}@media(max-width:500px){main{margin:12px auto;padding:18px}h1{font-size:34px}}
</style><main><p class="label">RELATA / RESEARCH EDITION</p><h1>''' + html.escape(title) + '</h1>' + ''.join(blocks) + '<details><summary>披露清单</summary><pre>' + html.escape(json.dumps(inventory, ensure_ascii=False, indent=2)) + '</pre></details><footer>这是显式选择的公开投影。未披露依赖不随包恢复；原 native binding 不在此包验证。生成预览不等于对外发布。</footer></main></html>'
    return {'html': document, 'markdown': '\n'.join(markdown), 'inventory': inventory, 'bundle': bundle,
            'profile': 'public-publication', 'native_binding': 'not-verifiable-in-public-projection'}
