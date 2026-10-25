import sys, re, html
import markdown, subprocess, base64, hashlib, os
MM = os.path.dirname(os.path.abspath(__file__)) + '/mmd/'
def render_mermaid(src):
    h = hashlib.sha1(src.encode()).hexdigest()[:12]
    png = MM + 'it_%s.png' % h
    if not os.path.exists(png):
        open(MM + 'it_%s.mmd' % h, 'w').write(src)
        subprocess.run([MM + 'node_modules/.bin/mmdc', '-p', MM + 'pup.json', '-c', MM + 'cfg.json',
                        '-i', MM + 'it_%s.mmd' % h, '-o', png, '-b', 'white', '-s', '2'], check=True, capture_output=True)
    b64 = base64.b64encode(open(png, 'rb').read()).decode()
    return ('\n\n<figure class="diagram"><img alt="Diagramma" src="data:image/png;base64,%s">'
            '<details><summary>Sorgente Mermaid</summary><pre><code>%s</code></pre></details></figure>\n\n' % (b64, html.escape(src)))
D = '/private/tmp/claude-501/-Users-davide/636f4170-d97f-45e6-a732-1190f4bba78c/scratchpad/it/'
parts = [('state', 'competitions-in-openswos.md', 'Le competizioni oggi'),
         ('engine', 'competition-engine-proposal.md', 'Proposta del motore'),
         ('catalog', 'rule-catalogue.md', 'Moduli e regole'),
         ('tests', 'testing-strategy.md', 'Strategia di test'),
         ('ai', 'ai-development-guidelines.md', 'Linee guida AI')]
body, toc = [], []
for key, fn, short in parts:
    src = open(D + fn).read()
    title = src.splitlines()[0].lstrip('# ').strip()
    src = '\n'.join(src.splitlines()[1:])
    src = re.sub(r'```mermaid\n(.*?)```', lambda m: render_mermaid(m.group(1)), src, flags=re.S)
    # summary blockquote (IT) -> separate box
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists'],
                           extension_configs={'toc': {'slugify': lambda v, sep: key + '-' + re.sub(r'[^a-z0-9]+', '-', v.lower()).strip('-')}})
    h = md.convert(src)
    h = h.replace('<blockquote>', '<aside class="summary" lang="it"><span class="tag">In breve</span>', 1).replace('</blockquote>', '</aside>', 1)
    h = re.sub(r'<table>', '<div class="tw"><table>', h); h = h.replace('</table>', '</table></div>')
    h = re.sub(r'<pre><code', '<div class="cw"><pre><code', h); h = h.replace('</code></pre>', '</code></pre></div>')
    # links to sibling md files -> anchors
    for k2, f2, _ in parts:
        h = h.replace('href="%s"' % f2, 'href="#%s"' % k2)
    secs = [(m.group(1), re.sub('<[^>]+>', '', m.group(2))) for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', h)]
    toc.append((key, short, title, secs))
    body.append('<section class="part" id="%s"><p class="eyebrow">Parte %s</p><h1>%s</h1>%s</section>' % (key, 'ABCDE'[len(body)], html.escape(title), h))
nav = ''.join('<li><a class="p" href="#%s">%s</a><ol>%s</ol></li>' % (k, s, ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in secs)) for k, s, _, secs in toc)
tpl = open(sys.argv[1]).read()
open(sys.argv[2], 'w').write(tpl.replace('{{NAV}}', nav).replace('{{BODY}}', '\n'.join(body)))
