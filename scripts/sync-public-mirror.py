"""public/ is authoritative; root is a compatibility mirror for GitHub Pages.
Never deletes files. Use --check in CI to reject drift.
"""
from pathlib import Path
import shutil,sys
bad=[]
for source in Path('public').rglob('*'):
 if not source.is_file() or '__qa' in source.parts or source.parts[1]=='data':continue
 target=Path(str(source.relative_to('public')))
 if not target.exists() or target.read_bytes()!=source.read_bytes():
  bad.append(str(target))
  if '--check' not in sys.argv:target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
if '--check' in sys.argv and bad:print('Mirror drift:',bad);sys.exit(1)
print('Mirror synchronized' if '--check' not in sys.argv else 'Mirror PASS')
