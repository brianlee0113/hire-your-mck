"""Confidence grade of every number (V-05, V-06), shown in the source workbook.

A  T1/T2 source, excerpt re-found on the page, and for title or exec summary numbers a second
   independent source that agrees
B  T1/T2 (or the user's own data) and the excerpt matches, but no re-check or no second source yet
C  rests on a T3 source, the page could not be re-checked, or sources disagree without a reason
E  our estimate: calc and assumptions, basis shown on the slide (B-08)
"""

GRADES = {
    "A": "Primary or research source, re-checked on the page, key numbers confirmed by a second source",
    "B": "Excerpt matches its source; not yet re-checked or not confirmed by a second source",
    "C": "Lower confidence: secondary source, page could not be re-checked, or sources disagree",
    "E": "Team estimate: built from sourced inputs with stated assumptions",
}
_RANK = "ABCE"


def agrees(a, b, rel=0.02):
    """Two values for the same metric agree within 2%."""
    if a == b:
        return True
    return abs(a - b) <= rel * max(abs(a), abs(b))


def key_refs(spec_dict):
    """Numbers the reader takes away: those in action titles and in the executive summary."""
    from .pptx_render import collect_refs
    refs = set()
    for s in spec_dict.get("slides", []):
        if s.get("role") == "content":
            refs |= set(collect_refs(s.get("lead_message") or {}))
    refs |= set(collect_refs((spec_dict.get("storyline") or {}).get("exec_summary", [])))
    return refs


def grade(spec, dp_id, key=frozenset(), _seen=None):
    """(letter, reason) for one data point. spec is a renderer Spec."""
    d = spec.dp.get(dp_id)
    if d is None:
        return "C", "unknown data point"
    if d.get("estimate"):
        return "E", "estimate"
    src = spec.src.get(d.get("source_id"), {})
    if src.get("kind") == "derived":
        # a calculation is as good as its weakest input
        _seen = (_seen or set()) | {dp_id}
        ins = [grade(spec, i, key, _seen) for i in d.get("derived_from", []) if i not in _seen]
        if any(g == "E" for g, _ in ins):
            return "E", "built on an estimate"
        worst = max(ins, key=lambda g: _RANK.index(g[0]), default=("B", "derived"))
        return worst[0], f"derived; weakest input: {worst[1]}"
    ver = d.get("verified") or {}
    if src.get("kind") == "web":
        if src.get("tier") in ("T3", "T4") or not src.get("tier"):
            return "C", f"{src.get('tier') or 'untiered'} source"
        if ver.get("result") in ("not_found", "unreachable"):
            return "C", f"re-check: {ver['result'].replace('_', ' ')}"
    for c in d.get("corroboration", []):
        if isinstance(c.get("value"), (int, float)) and not agrees(c["value"], d["value"]) and not c.get("note"):
            return "C", f"second source {c.get('source_id')} says {c['value']:g}"
    if src.get("kind") != "web":
        return "B", "user data" if src.get("kind") == "user_provided" else src.get("kind", "")
    if ver.get("result") != "match":
        return "B", "not re-checked"
    if dp_id in key and not d.get("corroboration"):
        return "B", "key number with one source"
    return "A", "re-checked" + (", corroborated" if d.get("corroboration") else "")
