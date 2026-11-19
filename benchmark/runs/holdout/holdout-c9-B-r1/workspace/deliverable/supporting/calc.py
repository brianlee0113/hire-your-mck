# Core calculations, all inputs from evidence/briefing-pack.md
cash, rnd, floor = 11.0, 2.2, 7.0
avail = cash - rnd
print("available", avail, "headroom", avail-floor)
for k, c in {"order now":4.8, "slot":0.6, "molder":0, "nothing":0}.items():
    print(k, round(avail-c,2), "vs floor", round(avail-c-floor,2))
print("after slot then balance", avail-0.6-4.2, "need", floor-(avail-4.8))
yrs=[2027,2028,2029,2030]; fc=[8.3,9.6,11.2,12.4]; sg=[7.8,8.5,9.4,9.8]
spec_share={2027:0,2028:0,2029:0.2,2030:0.2}
def over(d,y): 
    sp=d*spec_share[y]; return max(0,d-9.0)+sp*0.04, sp*0.04
for name, dem in [("forecast",fc),("signed",sg),("slip",[8.3,8.3,9.6,11.2])]:
    print(name,[ (y, round(over(d,y)[0],3), round(over(d,y)[1],3)) for y,d in zip(yrs,dem)])
print("util nameplate",[round(d/10,3) for d in fc],"practical",[round(d/9,3) for d in fc])
print("breakeven line vs molder units", 0.55/0.12)
print("2030 line", 3.50*0.45-0.55, "molder", 2.5*0.33)
print("do nothing lost", 0.6*.45, 2.29*.45, 3.5*.45, (0.6+2.29+3.5)*.45)
print("base contrib proxy", 9*.45, "25%", 9*.45*.25)
for loss in [0.45, 0.45+9*.45*.25, 0.45+9*.45*.5]: print("BE prob", loss, 0.6/loss)
print("reserve+bridge cost", 4.8+0.072+2.29*0.12/2+0.55*1.5)
print("order now cost", 4.8+3*0.55)
print("molder premiums fc", 0.6*.12, 2.29*.12, 2.5*.12, 0.6*.12+2.29*.12+2.5*.12)
print("slip prem", 0.68*.12+2.29*.12, "signed prem", .48*.12+.88*.12)
