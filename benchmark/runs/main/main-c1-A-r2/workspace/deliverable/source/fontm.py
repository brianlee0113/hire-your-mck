import struct
class TTF:
    def __init__(s,path):
        d=open(path,'rb').read(); s.d=d
        n=struct.unpack('>H',d[4:6])[0]; s.t={}
        for i in range(n):
            tag,_,off,ln=struct.unpack('>4sIII',d[12+16*i:28+16*i]); s.t[tag.decode()]=(off,ln)
        o=s.t['head'][0]; s.upm=struct.unpack('>H',d[o+18:o+20])[0]
        o=s.t['hhea'][0]; nh=struct.unpack('>H',d[o+34:o+36])[0]
        o=s.t['hmtx'][0]; s.adv=[struct.unpack('>H',d[o+4*i:o+4*i+2])[0] for i in range(nh)]
        s.cmap=s._cmap()
    def _cmap(s):
        d=s.d;o=s.t['cmap'][0];n=struct.unpack('>H',d[o+2:o+4])[0]
        for i in range(n):
            pid,eid,off=struct.unpack('>HHI',d[o+4+8*i:o+12+8*i])
            if (pid,eid) in ((3,1),(0,3)):
                so=o+off
                if struct.unpack('>H',d[so:so+2])[0]==4: return s._f4(so)
    def _f4(s,so):
        d=s.d;seg=struct.unpack('>H',d[so+6:so+8])[0]//2;m={}
        ends=struct.unpack('>%dH'%seg,d[so+14:so+14+2*seg]);st=so+16+2*seg
        starts=struct.unpack('>%dH'%seg,d[st:st+2*seg]);dl=st+2*seg
        deltas=struct.unpack('>%dh'%seg,d[dl:dl+2*seg]);ro=dl+2*seg
        rofs=struct.unpack('>%dH'%seg,d[ro:ro+2*seg])
        for i in range(seg):
            for c in range(starts[i],min(ends[i],0x2FFF)+1):
                if rofs[i]==0: g=(c+deltas[i])&0xFFFF
                else:
                    a=ro+2*i+rofs[i]+2*(c-starts[i]); g=struct.unpack('>H',d[a:a+2])[0]
                    if g: g=(g+deltas[i])&0xFFFF
                m[c]=g
        return m
    def width(s,text,pt):
        w=0
        for ch in text:
            g=s.cmap.get(ord(ch),0); w+=s.adv[min(g,len(s.adv)-1)]
        return w/s.upm*pt
