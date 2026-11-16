p='build.py'; s=open(p).read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:60]); s=s.replace(a,b)
R('tfmt=lambda v: f"{v:.1f}%", lab=11, catlines=1, ymax=3.3, barfrac=0.5)','tfmt=lambda v: f"{v:.1f}%", lab=11, catlines=2, ymax=3.3, barfrac=0.5)')
R('rows = [["Per order, FY2025", "Click & collect", "Home delivery"],','rows = [["Per order, FY2025", "Collect", "Delivered"],')
R('["One-time cost ($M): lease exit + closure (assumed $0.4M per store)", "0 + 2.4", "7.5 + 1.2", "11.1"]','["One-time cost ($M): lease exit + closure", "0 + 2.4", "7.5 + 1.2", "11.1"]')
open(p,'w').write(s)
