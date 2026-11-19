import sys, os, subprocess, copy
from pptx import Presentation
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
n = len(Presentation(src).slides)
for i in range(n):
    p = Presentation(src)
    ids = p.slides._sldIdLst
    for j, sld in reversed(list(enumerate(list(ids)))):
        if j != i:
            rId = sld.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            p.part.drop_rel(rId); ids.remove(sld)
    f = os.path.join(outdir, f"s{i+1:02d}.pptx"); p.save(f)
    subprocess.run(["qlmanage", "-t", "-s", "1600", "-o", outdir, f], capture_output=True)
print(sorted(x for x in os.listdir(outdir) if x.endswith(".png")))
