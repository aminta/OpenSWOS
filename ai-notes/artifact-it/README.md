# Italian artifact sources

Italian translation of docs/convergence/ used for the artifact
https://claude.ai/artifact/CUearZGHwKovnhV2c8XxC5 (repo docs stay English; keep this copy in sync).

Rebuild (scratchpad paths in build_doc.py: D = folder of the .md files, MM = mermaid dir):
- python-markdown 3.7 (`pip install --target <dir> markdown==3.7`, PYTHONPATH=<dir>)
- mermaid-cli 11.4.2 (`PUPPETEER_SKIP_DOWNLOAD=1 npm i @mermaid-js/mermaid-cli@11.4.2`),
  pup.json = {"executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
- `python3 build_doc.py tpl.html convergenza-openswos.html`, then publish the same file path
  (or pass the artifact url from another session).
