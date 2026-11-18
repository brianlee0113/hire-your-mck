b=open('build.py').read()
i0=b.index('sections = ['); i1=b.index('content = [s for s')
b=b[:i0]+'''sections = [
    {"id": "1", "title": "Diagnosis: what drove the margin down", "exec_item_id": "1", "tracker_label": "Diagnosis"},
    {"id": "2", "title": "Options: why not the draft plan", "exec_item_id": "2", "tracker_label": "Options"},
    {"id": "3", "title": "Plan: seven firm levers and a second wave", "exec_item_id": "3", "tracker_label": "Plan"},
    {"id": "4", "title": "First moves, risks and decisions for the board", "exec_item_id": "4", "tracker_label": "First moves and asks"},
]
'''+b[i1:]
i0=b.index('exec_summary = ['); i1=b.index('next_steps = [')
b=b[:i0]+'''exec_summary = [
    {"id": "1", "text": "Promotions, shrink and home delivery drove the decline, not wages",
     "supports": by_sec["1"], "sub_points": [
        {"text": "Gross margin and e-commerce fulfillment explain 79% of the fall; store labor only 13%", "slide_id": "1b"},
        {"text": "Fully costed, e-commerce loses about $10M a year, about $12 on every home-delivered order", "slide_id": "1g"}]},
    {"id": "2", "text": "The draft 8% labor cut and e-commerce freeze would stall margin near 1.1%",
     "supports": by_sec["2"], "sub_points": [
        {"text": "The cut saves $14.5M on paper, but we expect $4–8M of it back as shrink in already lean stores", "slide_id": "2a"},
        {"text": "Only the margin-first plan reaches the target and keeps delivery; closing delivery is the fallback", "slide_id": "2b"}]},
    {"id": "3", "text": "Seven firm levers worth $30M reach 2.6%; a prepared second wave closes the gap to 3.0%",
     "supports": by_sec["3"], "sub_points": [
        {"text": "Gross margin $17.0M, labor $5.5M, delivery $3.3M, store exits $4.4M; range $17–38M", "slide_id": "3a"},
        {"text": "About half of the $9.9M second wave is needed; one-time cost of $17M stays inside the $25M cap", "slide_id": "3e"}]},
    {"id": "4", "text": "Four no-regret moves in 90 days keep FY2026 about $5M above the $20M covenant",
     "supports": by_sec["4"], "sub_points": [
        {"text": "A mid-FY2027 checkpoint triggers the full second wave if run-rate margin is below about 2.4%", "slide_id": "4b"},
        {"text": "We ask for three decisions today; vendor funding and ValuMart traffic are the key risks", "slide_id": "5c"}]},
]

'''+b[i1:]
open('build.py','w').write(b)
