import hashlib
import json
import os
from pathlib import Path
from urllib.request import urlopen

COMMIT = '963124e2c94b50305342d4f6f8dd47c4ea37125f'
BASE = '/asf-pr53-preview/asf-app/'
SOURCE = 'https://raw.githubusercontent.com/acarolmourad-commits/asf-app/' + COMMIT + '/'
HASHES = {
    'guia-apps.html': 'cd093042b805f3c70712b5beb59bac7777422438cc74b580696567919d6074bd',
    'asf-site-redesign.css': '3c9bf5809735f5482f08e08f1a29d009e29f3f1aa4af98afd247039eacb779a9',
    'asf-network.js': 'aa5fb4b13ceee8d2a1e6c9176f9e2b0c74e3e2d949bc002949bb97aafa2d65cc',
    'asf-redesign.js': '9c9e4095e360dfad9a513e5c34fbbddae6e2d3a14c5b688d5cbfd78ddd711f31',
    'data/apps-count.js': 'a01f6419c85b6d022eee4bad0637b91ea2585d176835e1ee727aec1f6041fb69',
    'asf-mural.css': 'ae7f1b5b55edb0fb01b8905bdf28859925608d20a8dd92802851d5654ee6cdcf',
    'asf-bottomnav.js': '4264ebfc7cadeac5e5550192b03d63e8c95e9c307745ab5d897af24b9fea87cb',
}
output = Path('site/asf-app')
output.mkdir(parents=True, exist_ok=True)
local_source = os.environ.get('PREVIEW_SOURCE_DIR')
files = {}
for name, digest in HASHES.items():
    if local_source:
        body = (Path(local_source) / name).read_bytes()
    else:
        with urlopen(SOURCE + name, timeout=30) as response:
            body = response.read()
    assert hashlib.sha256(body).hexdigest() == digest, 'Source hash mismatch: ' + name
    files[name] = body.decode('utf-8')

html = files['guia-apps.html']
def replace_once(text, old, new):
    assert text.count(old) == 1, 'Unexpected source: ' + old
    return text.replace(old, new, 1)
html = replace_once(html, 'href="/asf-app/asf-site-redesign.css"', 'href="' + BASE + 'asf-site-redesign.css"')
html = replace_once(html, 'src="/asf-app/asf-redesign.js"', 'src="' + BASE + 'asf-redesign.js"')
html = replace_once(html, 'src="https://acarolmourad-commits.github.io/asf-app/asf-network.js"', 'src="' + BASE + 'asf-network.js"')
html = replace_once(html, 'content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex, nofollow, noarchive"')
html = replace_once(html, '</head>', '<script>window.ASF_BASE=' + json.dumps(BASE) + ';</script>\n</head>')
banner = '<aside id="preview-notice" aria-label="Aviso de revisão" style="padding:12px 16px;background:#fff2cc;color:#0E2439;text-align:center;font:14px/1.5 system-ui"><strong>PRÉVIA DE TESTE — PR #53 / 963124e2</strong><br>Não é produção. Não insira dados pessoais. Os links dos apps levam aos sites públicos. Offline não faz parte deste teste.</aside>'
html = replace_once(html, '<body>', '<body>\n' + banner)
files['guia-apps.html'] = html

redesign = files['asf-redesign.js']
registration = "    if ('serviceWorker' in navigator) navigator.serviceWorker.register(base + 'sw.js').catch(function () {});"
redesign = replace_once(redesign, registration, '    // Preview only: service worker registration intentionally disabled.')
redesign = replace_once(redesign, "a.href=(location.pathname.indexOf('/asf-app')===0?'/asf-app/':'/');", "a.href='https://asf.surf/';")
files['asf-redesign.js'] = redesign
for name, content in files.items():
    target = output / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')

# Landing page links to the pinned preview without loading production assets.
Path('site/index.html').write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Prévia PR53 ASF</title></head><body style="font:18px/1.6 system-ui;padding:24px"><h1>Prévia de revisão ASF</h1><p>PR #53 · versão 963124e2 · não é produção.</p><p><a href="asf-app/guia-apps.html">Abrir guia para teste no iPhone</a></p></body></html>', encoding='utf-8')
Path('site/robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
Path('site/.nojekyll').write_text('', encoding='utf-8')
manifest = {'source_commit': COMMIT, 'source_sha256': HASHES, 'preview_html_sha256': hashlib.sha256(html.encode('utf-8')).hexdigest(), 'preview_only_changes': ['local asset URLs', 'noindex metadata', 'test notice', 'ASF_BASE prefix', 'service worker disabled', 'back pill goes to ASF hub']}
Path('site/preview-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('Pinned preview built:', manifest['preview_html_sha256'])
