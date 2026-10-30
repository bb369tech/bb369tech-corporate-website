"""Compatibility command; the stable asset lock supersedes the historical CSS-only gate."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('stable-asset-lock.py')),run_name='__main__')
