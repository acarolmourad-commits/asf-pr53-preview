"""Add isolated PR54 section preview; preserve the existing PR53 output."""
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

SOURCE_SHA = '2381a94b83a6cc535292e4c1c1cdb280ce1528c7'
EXPECTED_SHA256 = '27146a5d17e55c012133ac7c668897d0b0fb49bfc197006fb60d9522bd65083c'
SOURCE = f'https://raw.githubusercontent.com/acarolmourad-commits/asf-app/{SOURCE_SHA}/assets/js/inline/asf-inline-06.js'
request = urllib.request.Request(SOURCE, headers={'User-Agent': 'ASF-static-review-preview'})
with urllib.request.urlopen(request, timeout=30) as response:
    content = response.read()
if hashlib.sha256(content).hexdigest() != EXPECTED_SHA256:
    raise RuntimeError('Pinned review script integrity mismatch')
output = Path('site/home-review')
output.mkdir(parents=True, exist_ok=True)
shutil.copyfile('home-review/index.html', output / 'index.html')
(output / 'home-review.js').write_bytes(content)
(output / 'manifest.json').write_text(json.dumps({'pull_request': 54, 'source_commit': SOURCE_SHA, 'script_sha256': EXPECTED_SHA256, 'scope': 'isolated sections, not the full home', 'submission_disabled': True}, indent=2) + '\n')
print('PR54 isolated section preview built; PR53 output preserved.')
