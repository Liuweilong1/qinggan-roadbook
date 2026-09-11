from pathlib import Path
import subprocess
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding='utf-8')

start = s.find('<section id="services">')
if start < 0:
    raise SystemExit('services section not found')
end = s.find('</section>', start)
if end < 0:
    raise SystemExit('services section end not found')
end += len('</section>')

block = s[start:end]
s = s[:start] + s[end:]

marker = '<section id="xhs">'
pos = s.find(marker)
if pos < 0:
    raise SystemExit('xhs section not found')

s = s[:pos] + block + '\n\n' + s[pos:]
p.write_text(s, encoding='utf-8')

# Keep the production source parts untouched; enrich the final tickets section
# after section ordering has been normalized.
script = Path(__file__).with_name('enhance_tickets.py')
subprocess.run([sys.executable, str(script), sys.argv[1]], check=True)
