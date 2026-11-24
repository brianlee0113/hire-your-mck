"""Where the time of a skill run goes: classify each main-agent model call of the holdout transcripts by what it
did (learning the skill's code, writing or patching the spec, measuring fit, render/check loop, ...) and sum the
generation and tool time. Usage: analyse_compile_time.py [CONDITION]  (default H2a; e.g. E1).
Written for docs/08-compile-time-analysis.md."""
import gzip, json, glob, re, collections, sys
from datetime import datetime
def ts(s): return datetime.fromisoformat(s.replace("Z","+00:00")).timestamp()
def phase(u):
    n=u["name"]; i=u["input"]; s=(i.get("command") or i.get("file_path") or i.get("content","")[:0] or i.get("description") or i.get("prompt","")[:200] or "")
    if n in ("Task","Agent"): return "subagent (review)"
    if n=="Write" and "build_spec" in s or n=="Write" and s.endswith(".json"): return "write spec"
    if "render.py" in s or "check.py" in s and "sed -n" not in s and "grep" not in s: return "render/check"
    if re.search(r"openpyxl|xlsx_render|postprocess|sources\.xlsx", s): return "sources workbook"
    if re.search(r"measure|from renderer|titles\.py|fit\.py|tablefit|_est_h|width_pt", s): return "measure/fit scripts"
    if re.search(r"build_spec|patch\d|s=open\(p\)\.read\(\)|sed -i", s): return "patch spec"
    if re.search(r"briefing-pack|analysis\.md|evidence/|extract", s): return "read inputs"
    if re.search(r"_plugin/|/skills/hire-your-mck|\$SK|references/|schema|pptx_render|check\.py|examples/", s): return "learn skill/renderer code"
    if re.search(r"Presentation\(|fitz|pymupdf|soffice", s): return "inspect pptx"
    return "other"
COND = sys.argv[1] if len(sys.argv) > 1 else "H2a"
tot=collections.defaultdict(collections.Counter); runs=[]
for run in sorted(glob.glob(f"benchmark/runs/holdout/holdout-c*-{COND}-r1")):
    ev=[json.loads(l) for l in gzip.open(f"{run}/transcript-attempt1.jsonl.gz")]
    msgs={}; order=[]; last=None; t0=None; pend={}
    per=collections.defaultdict(collections.Counter)
    for e in ev:
        if "timestamp" not in e or e.get("parent_tool_use_id"): continue
        t=ts(e["timestamp"]); t0=t0 or t
        if e["type"]=="assistant":
            mid=e["message"]["id"]
            if mid not in msgs:
                us=e["message"].get("usage",{})
                msgs[mid]=dict(start=last or t0,end=t,uses=[],ctx=us.get("cache_read_input_tokens",0)+us.get("cache_creation_input_tokens",0)+us.get("input_tokens",0)); order.append(mid)
            m=msgs[mid]; m["end"]=t
            m["uses"]+= [c for c in e["message"]["content"] if c.get("type")=="tool_use"]
        elif e["type"]=="user":
            for c in (e["message"]["content"] if isinstance(e["message"]["content"],list) else []):
                if c.get("type")=="tool_result" and c.get("tool_use_id") in pend:
                    p,t1=pend.pop(c["tool_use_id"]); per[p]["tool_s"]+=t-t1
            last=t
    for mid in order:
        m=msgs[mid]; p=phase(m["uses"][0]) if m["uses"] else "final answer/text"
        per[p]["gen_s"]+=m["end"]-m["start"]; per[p]["calls"]+=1; per[p]["ctx"]+=m["ctx"]
        for u in m["uses"]: pend[u["id"]]=(phase(u), m["end"])
    name=run.split("-")[1]; runs.append((name,per))
    for p,c in per.items(): tot[p].update(c)
allsec=sum(c["gen_s"]+c["tool_s"] for c in tot.values()); allctx=sum(c["ctx"] for c in tot.values())
print(f"6 runs: {allsec/60:.0f} min main-agent wall, {sum(c['calls'] for c in tot.values())} model calls\n")
print(f"{'phase':28}{'min':>6}{'share':>7}{'calls':>7}{'input tok share':>17}")
for p,c in sorted(tot.items(), key=lambda kv:-(kv[1]['gen_s']+kv[1]['tool_s'])):
    s=c["gen_s"]+c["tool_s"]; print(f"{p:28}{s/60:6.1f}{s/allsec:7.0%}{c['calls']:7}{c['ctx']/allctx:17.0%}")
print("\nper run, minutes: learn / write / patch / measure / render-check / sources / subagent")
for name,per in runs:
    g=lambda p:(per[p]['gen_s']+per[p]['tool_s'])/60
    print(f"{name:4} " + " / ".join(f"{g(p):4.1f}" for p in ["learn skill/renderer code","write spec","patch spec","measure/fit scripts","render/check","sources workbook","subagent (review)"]))
