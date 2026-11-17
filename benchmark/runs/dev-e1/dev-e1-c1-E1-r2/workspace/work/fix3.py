p='build_spec.py'; s=open(p).read()
rep=[
# slide 11: drop cap line benchmark
('''[("Option A cumulative cash", ["A_cum27", "A_cum28", "A_cum29", "A_cum30"])], MFMT, ["2030"],
               benchmark=("Investment cap", "cap_line")),''', '''[("Option A cumulative cash", ["A_cum27", "A_cum28", "A_cum29", "A_cum30"])], MFMT, ["2030"]),'''),
# slide 7 sidebar -> bullets
('''{"kind": "big_number", "header": "Onsoo would likely be removed at the first review",
        "big_number": P("st_gap"), "caption": "shortfall of the median for Onsoo's band against the 4.0 removal line",
        "bullets": ["**Onsoo today:** 9% aided awareness among K-beauty buyers, the lowest band",''',
 '''{"kind": "bullets", "header": "Onsoo would likely be removed at the first review",
        "bullets": ["**Onsoo today:** 9% aided awareness among K-beauty buyers puts it in the lowest band, 35% short of the 4.0 line",'''),
# slide 13 sidebar -> bullets
('''{"kind": "big_number", "header": "Ad cost decides when Option A pays back, not if it is affordable",
        "big_number": P("cpp_cash"), "caption": "of end-2030 cash lost per percentage point of average ACoS",
        "bullets": ["**28% (pilot):** payback still comes in 2030, with almost nothing spare",''',
 '''{"kind": "bullets", "header": "Ad cost decides when Option A pays back, not if it is affordable",
        "bullets": ["**Each percentage point** of average ACoS costs $0.67M of end-2030 cash",
                    "**28% (pilot):** payback still comes in 2030, with almost nothing spare",'''),
# exec summary: two sub-points per item
('''{"text": "US K-beauty facial skincare sales rose from $1.9B to $3.6B in 2021–25", "slide_id": "1"},
                      ''', ''),
('''{"text": "It assumes 4.5 units a door a week; brands below 10% awareness sell 2.6", "slide_id": "7"}''', ''),
('''{"text": "Peak cash need is $1.9M; cumulative cash turns positive only in 2030", "slide_id": "11"},
                      ''', ''),
('''{"text": "The 2028 budget follows the mid-2027 tariff ruling and an ACoS review", "slide_id": "17"}''', ''),
]
bad=[a[:70] for a,b in rep if a not in s]
print("missing:", bad)
for a,b in rep: s=s.replace(a,b)
s=s.replace('"slide_id": "6"},\n                      ]','"slide_id": "6"}]').replace('"slide_id": "16"},\n                      ]','"slide_id": "16"}]')
open(p,'w').write(s)
