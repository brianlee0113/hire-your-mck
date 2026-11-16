"""US entry model for Onsoo Botanicals, built only from evidence/briefing-pack.md."""
YEARS = [2027, 2028, 2029, 2030]
EXF, FR_AMZ, FR_RET = 3.50, 0.55, 0.75

def amz_unit(acos=0.25, duty=0.15, price=24.0):
    return price - 0.15*price - 5.10 - EXF - FR_AMZ - duty*EXF - acos*price
def amz_landed(duty=0.15): return EXF + FR_AMZ + duty*EXF
def ret_unit(duty=0.15, ws=14.0):
    return ws - EXF - FR_RET - duty*EXF - 0.08*ws - 0.04*ws
def ret_landed(duty=0.15): return EXF + FR_RET + duty*EXF

A_UNITS = [300_000, 560_000, 850_000, 1_100_000]
B_DOORS = [600, 600, 800, 1000]

def option_a(acos=0.25, duty=0.15, units=A_UNITS):
    rows, cum, inv_prev, peak = [], 0, 0, 0
    for i, y in enumerate(YEARS):
        u = units[i]
        rev = u*24/1e6
        contrib = u*amz_unit(acos, duty)/1e6
        fixed = 2.1 + (0.8 if i == 0 else 0)
        op = contrib - fixed
        inv = u*amz_landed(duty)/3/1e6
        cash = op - (inv - inv_prev); inv_prev = inv
        cum += cash; peak = min(peak, cum)
        rows.append(dict(y=y, rev=rev, contrib=contrib, fixed=fixed, op=op, dwc=cash-op, cash=cash, cum=cum))
    return rows, peak

def option_b(acos=0.25, duty=0.15, upw=4.5, halo=1.3, doors=B_DOORS):
    rows, cum, inv_prev, peak, prev_doors = [], 0, 0, 0, 0
    for i, y in enumerate(YEARS):
        ru = doors[i]*upw*52
        au = A_UNITS[i]*halo
        rev = (ru*14 + au*24)/1e6
        contrib = (ru*ret_unit(duty) + au*amz_unit(acos, duty))/1e6
        new_doors = max(0, doors[i]-prev_doors); prev_doors = doors[i]
        fixed = 9.6 + (0.8 + 0.5 if i == 0 else 0) + new_doors*1100/1e6
        op = contrib - fixed
        inv = (ru*ret_landed(duty) + au*amz_landed(duty))/3/1e6
        cash = op - (inv - inv_prev); inv_prev = inv
        cum += cash; peak = min(peak, cum)
        rows.append(dict(y=y, rev=rev, ret_units=ru, amz_units=au, contrib=contrib, fixed=fixed, op=op, cash=cash, cum=cum))
    return rows, peak

def option_j():
    rev = [2.5, 4.5, 6.0, 7.0]; rows, cum = [], 0
    for i, y in enumerate(YEARS):
        op = rev[i]*0.30 - 0.8 - (1.0 if i == 0 else 0)
        cum += op
        rows.append(dict(y=y, rev=rev[i], op=op, cash=op, cum=cum))
    return rows, min(0, min(r['cum'] for r in rows))

GROUP_REV = [140, 146, 152, 158]
def group_margin(rows):
    return [(GROUP_REV[i]*0.11 + r['op'])/(GROUP_REV[i] + r['rev']) for i, r in enumerate(rows)]

if __name__ == '__main__':
    print('Amazon unit contrib @25/28/32/38:', [round(amz_unit(a),3) for a in (.25,.28,.32,.38)])
    print('Amazon landed', amz_landed(), 'retail unit', ret_unit(), 'retail landed', ret_landed())
    print('tariff 25%: amz@25', amz_unit(.25,.25), 'ret', ret_unit(.25))
    for name, (rows, peak) in [('A', option_a()), ('B', option_b()), ('J', option_j())]:
        print(f'\n== {name} peak {peak:.2f}')
        for r in rows: print({k: (round(v,3) if isinstance(v,float) else v) for k,v in r.items()})
        print('group margin', [f'{m:.1%}' for m in group_margin(rows)])
    print('\n-- A sensitivity: acos x duty -> peak, cum2030, min margin')
    for duty in (.15,.25):
        for acos in (.25,.28,.30,.32,.35,.38):
            rows, peak = option_a(acos, duty)
            print(duty, acos, round(peak,2), round(rows[-1]['cum'],2), f"{min(group_margin(rows)):.1%}", 'OP2030', round(rows[-1]['op'],2))
    # breakeven acos for payback
    for duty in (.15,.25):
        lo, hi = 0.2, 0.4
        for _ in range(60):
            m = (lo+hi)/2
            if option_a(m, duty)[0][-1]['cum'] >= 0: lo = m
            else: hi = m
        print('breakeven ACoS duty', duty, round(lo,4))
    print('\n-- A stall: flat 200k units @32%')
    rows, peak = option_a(.32, .15, [200_000]*4); print(round(peak,2), [round(r['cum'],2) for r in rows])
    print('\n-- B variants')
    for lab, kw in [('base',{}),('acos32',dict(acos=.32)),('2.6 upw',dict(upw=2.6)),('no halo',dict(halo=1.0)),('2.6+nohalo+32',dict(upw=2.6,halo=1.0,acos=.32))]:
        rows, peak = option_b(**kw); print(lab, round(peak,2), round(rows[-1]['cum'],2), [f'{m:.1%}' for m in group_margin(rows)], 'rev30', round(rows[-1]['rev'],1))
    # B incremental over A
    a,_ = option_a(); b,_ = option_b()
    print('B-A op', [round(b[i]['op']-a[i]['op'],2) for i in range(4)])
    print('retail-leg contrib', [round(b[i]['ret_units']*ret_unit()/1e6,2) for i in range(4)], 'halo contrib', [round(0.3*A_UNITS[i]*amz_unit()/1e6,2) for i in range(4)])
    # 2030 margin headroom with A
    for acos in (.25,.32):
        r,_ = option_a(acos); op = 158*.11 + r[-1]['op']; rev = 158 + r[-1]['rev']
        print('headroom 2030 acos', acos, round(op - 0.08*rev,2))
