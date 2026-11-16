"""Builds work/onsoo-us-entry.json from model.py (data) and the slide definitions below."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = open(os.path.join(HERE, "..", "evidence", "briefing-pack.md"), encoding="utf-8").read()


def P(i):
    assert i in M.DP, i
    return {"data_ref": i}


def N(text, i):
    assert i in M.DP, i
    return {"text": text, "data_ref": i}


def chart(ctype, cats, series, highlight=(), fmt=None, sort="none", **kw):
    b = {"kind": "chart", "chart_type": ctype, "categories": list(cats),
         "series": [{"name": n, "points": [P(i) for i in ids]} for n, ids in series],
         "sort": sort, "highlight": list(highlight)}
    if fmt: b["value_format"] = fmt
    b.update(kw)
    return b


def content(id, sec, text, arch, mtype, body, node=None, numbers=(), highlights=None, **kw):
    s = {"id": id, "role": "content", "section_id": sec, "status": "filled",
         "lead_message": {"text": text}, "message_type": mtype, "archetype": arch, "body": body}
    if numbers: s["lead_message"]["numbers"] = list(numbers)
    if highlights is not None: s["lead_message"]["highlights"] = list(highlights)
    for k in ("count_word", "clauses"):
        if k in kw: s["lead_message"][k] = kw.pop(k)
    if node: s["tree_node"] = node
    s.update(kw)
    return s


def backup(id, sec, text, arch, body, of=None, numbers=(), **kw):
    s = {"id": id, "role": "backup", "section_id": sec, "status": "filled",
         "lead_message": {"prefix": "BACKUP:", "text": text}, "message_type": "item", "archetype": arch, "body": body}
    if numbers: s["lead_message"]["numbers"] = list(numbers)
    if of: s["backup_of"] = of
    for k in ("count_word",):
        if k in kw: s["lead_message"][k] = kw.pop(k)
    s.update(kw)
    return s


def nav(id, role, sec=None):
    s = {"id": id, "role": role, "status": "filled"}
    if role == "agenda_tracker":
        s.update({"section_id": sec, "archetype": "agenda-tracker", "message_type": "navigation"})
    if role == "exec_summary":
        s.update({"archetype": "exec-summary", "message_type": "navigation"})
    return s


def row(label, ids_or_cells, **kw):
    cells = []
    for c in ids_or_cells:
        if isinstance(c, dict): cells.append(c)
        elif c in M.DP: cells.append({"point": P(c)})
        else: cells.append({"text": c})
    r = {"label": label, "cells": cells}
    r.update(kw)
    return r


MODEL_NOTE = "Cash flow = contribution after ads − fixed and one-time costs − inventory; method in the backup model pages"
YEARS = ["2027", "2028", "2029", "2030"]
Y = (27, 28, 29, 30)

slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "q", "role": "problem_statement", "status": "filled"},
    nav("es", "exec_summary"),

    # ================================================================ 1 · US prize
    nav("d1", "agenda_tracker", "1"),
    content("L1", "1", "The US is the better use of the single 2027 launch: a fast-growing market where Onsoo products already sell",
            "numbered-levers", "argument",
            {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
                {"code": "1a", "text": "US K-beauty facial skincare nearly doubled in four years, four times the category's growth",
                 "point": P("kb_mult"), "metric": "K-beauty facial skincare sales in 2025 compared with 2021"},
                {"code": "1b", "text": "A three-SKU Amazon pilot sold more every month, at 4.5 stars, without a US team or entity",
                 "point": P("pilot_total"), "metric": "units sold on Amazon US, January–June 2026"},
                {"code": "1c", "text": "On plan, the Amazon route builds almost four times the 2030 revenue a Japan scale-up would add",
                 "point": P("a_vs_j"), "metric": "US 2030 revenue as a multiple of Japan's added 2030 revenue"}]},
            unit_line="**Status of each finding**, briefing-pack data, 2021–26"),
    content("1a1", "1", "K-beauty facial skincare nearly doubled to $3.6B in four years, four times the category's growth over 2021–25",
            "stacked-column", "time-series",
            chart("stacked_column", ["2021", "2022", "2023", "2024", "2025"],
                  [("K-beauty brands", [f"kb{y}" for y in range(21, 26)]), ("Other brands", [f"oth{y}" for y in range(21, 26)])],
                  highlight=["K-beauty brands"], fmt="0.0"),
            node="n1a", numbers=[N("$3.6B", "kb25")], highlights=["K-beauty brands"],
            unit_line="**US facial skincare sales**, $ billions, 2021–25",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "header": "K-beauty is where the category's growth is",
                "big_number": P("kb_share_gr"), "caption": "of the growth in US facial skincare from 2021 to 2025 went to K-beauty brands",
                "bullets": ["**K-beauty brands:** sales rose 1.9 times from 2021 to 2025, against 1.2 times for all facial skincare",
                            "**Share:** K-beauty rose from 9.5% to 14.7% of the category, while other brands grew only 15%",
                            "**Market definition:** the $5.2B trade-press figure adds makeup and hair care, so it overstates Onsoo's pool (backup)"]}},
            footnotes=["K-beauty = facial skincare sold by K-beauty brands (briefing pack, Table 1). The trade-press figure of $5.2B for 2025 covers skincare, makeup and hair care and is not used"]),
    content("1b1", "1", "Pilot sales nearly doubled in six months with three SKUs and no US team, a demand signal worth scaling",
            "column-time-series", "time-series",
            chart("column", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [("Units sold", [f"m{i}" for i in range(1, 7)])],
                  highlight=["Jun"], fmt="#,##0"),
            node="n1b", highlights=["Jun"],
            unit_line="**Onsoo units sold on Amazon US**, units per month, three SKUs through a cross-border seller, January–June 2026",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "header": "Demand grew without Onsoo pushing it",
                "big_number": P("pilot_rev"), "caption": "of Amazon sales in the six-month pilot, at an average price of $24.00",
                "bullets": ["**June pace:** 168,000 units a year; the 2027 plan of 300,000 units needs 1.8 times that pace, with seven SKUs instead of three",
                            "**Little paid push:** the pilot ran on a small ad budget at 28% ACoS, through a seller Onsoo does not control"]}},
            footnotes=["Three SKUs listed by a cross-border seller since January 2026; Onsoo has no US entity today"]),
    content("1b2", "1", "Buyers rate Onsoo 4.5 stars and rebuy at close to the US newcomer rate, and English labels fix the top complaint",
            "kpi-big-numbers", "item",
            {"kind": "kpi", "items": [
                {"point": P("rating"), "caption": "average star rating from 2,140 reviews",
                 "relation": "The product itself is not the issue",
                 "drivers": ["Ratings cover the three SKUs sold January–June 2026",
                             "The most common complaint concerns labels, not the product",
                             "The four SKUs added in 2027 will need to match it"]},
                {"point": P("rep"), "caption": "of first-time buyers bought again within 90 days",
                 "relation": "Close to the 31% benchmark for first-year skincare brands on Amazon US",
                 "drivers": ["Well below Onsoo's 48% in Korea: US loyalty has to be built",
                             "Unclear whether more SKUs raise it; track it from the first 2027 cohort"]},
                {"point": P("complaint"), "caption": "of reviews flag Korean-only label text",
                 "relation": "The top complaint, and a compliance point",
                 "drivers": ["US labeling falls under MoCRA compliance, budgeted at $0.5M a year",
                             "English labels come with Onsoo's own entity and the $0.8M setup",
                             "Fix it before ad spend scales, so the complaint does not grow with sales"]}]},
            node="n1b", numbers=[N("4.5 stars", "rating")],
            unit_line="**Amazon pilot quality measures**, three SKUs, January–June 2026",
            footnotes=["Repeat benchmark: agency data for skincare brands in their first year on Amazon US"]),
    content("1c1", "1", "On plan, the US builds almost four times the 2030 revenue of a Japan scale-up, in a segment growing far faster",
            "multi-chart-panel", "item",
            {"kind": "panels", "panels": [
                {"header": "The Amazon route reaches $26.4M in 2030, against $7.0M added in Japan",
                 "unit_line": "**Revenue**, $ millions, 2027–30, planning-team forecasts",
                 "body": chart("column", YEARS, [("US, Option A (Amazon-led)", [f"rev_a{y}" for y in Y]),
                                                ("Japan, Option J (added revenue)", [f"jr{y}" for y in Y])],
                               highlight=["US, Option A (Amazon-led)"], fmt="0.0")},
                {"header": "US K-beauty grew more than ten times as fast as Japan's facial skincare",
                 "unit_line": "**Market growth**, % a year",
                 "body": chart("bar", ["US K-beauty facial skincare, 2025", "Japan facial skincare, a typical year"],
                               [("Growth", ["kb_g25", "jp_growth"])], highlight=["US K-beauty facial skincare, 2025"], fmt="0.0%")}]},
            node="n1c", layout={"variant": "split_2"},
            so_what="Japan adds profit sooner with less risk, but only the US builds the growth business the board wants",
            so_what_style="bar",
            footnotes=["Japan: Onsoo already holds a 3.1% share; revenue is the planning team's incremental forecast for Option J"]),

    # ================================================================ 2 · Retail-led
    nav("d2", "agenda_tracker", "2"),
    content("L2", "2", "A national retail launch in 2027 fails the board's tests even on the planning team's own assumptions",
            "framework-pillars", "argument",
            {"kind": "framework", "shape": "pillars", "items": [
                {"header": "2a · Sales per door would fall below the retailer's cut-off", "point": P("st_lo"),
                 "point_caption": "median weekly units per door in Onsoo's band",
                 "detail": ["Onsoo's aided awareness is 4% among skincare buyers",
                            "The plan's 4.5 comes from successful newcomers only",
                            "Mooncrest went retail-first in 450 doors and was removed in 2025"]},
                {"header": "2b · The Amazon halo is a correlation, not a proven effect", "point": P("halo"),
                 "point_caption": "Amazon volume multiple in Option B",
                 "detail": ["Bigger brands have both more doors and more Amazon sales",
                            "Saebom added doors only after reaching about $30M on Amazon",
                            "Its only basis is a 0.71 correlation across 30 brands"]},
                {"header": "2c · The cash cap and the margin floor both break", "point": P("peak_b"), "emphasis": True,
                 "point_caption": "peak cash need by 2030",
                 "detail": ["No payback: cash still falls by $1.9M in 2030",
                            "Group margin of 4.5% in 2027, against the 8% floor",
                            "Extra costs run 3.5 times the extra contribution"]}]}),
    content("2a1", "2", "At 4% awareness Onsoo would sell 2.6 units per door per week, below the 4.0 needed to stay on shelf",
            "bar-ranking", "item",
            chart("bar", ["Below 10% awareness", "10–20% awareness", "Above 20% awareness", "Option B plan"],
                  [("Units per door per week", ["st_lo", "st_mid", "st_hi", "upw_plan"])],
                  highlight=["Below 10% awareness"], fmt="0.0",
                  benchmark={"label": "Retailer removes brands below", "point": P("thr")}),
            node="n2a", numbers=[N("4%", "aw_all"), N("2.6", "st_lo"), N("4.0", "thr")], highlights=["Below 10% awareness"],
            unit_line="**Newcomer sell-through in US specialty beauty**, median units per door per week, by aided awareness, 2025",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "header": "Onsoo sits in the band that gets delisted",
                "big_number": P("aw_all"), "caption": "aided awareness of Onsoo among US facial skincare buyers (9% among K-beauty buyers)",
                "bullets": ["**Below 10%:** even the top quartile, 3.4 units, stays under the cut-off",
                            "**Plan assumption:** taken from the retailer's deck on successful newcomers, so it matches brands above 20% awareness",
                            "**First year:** 600 doors at 2.6 units sell about 81,120 units, against 140,400 in the plan"]}},
            footnotes=["Retail analytics firm, 2025, 46 newcomer brands; the leading retailer reviews newcomers after 12 months",
                       "Awareness: survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026"]),
    content("2a2", "2", "Mooncrest, the one recent retail-first K-beauty entrant, was off the shelves within two years at a $21M loss",
            "case-example", "item",
            {"kind": "case", "subject": "Mooncrest: K-beauty skincare brand that entered the US through specialty beauty retail in 2023",
             "situation_header": "Mooncrest launched retail-first in 450 doors",
             "situation": ["Entered the US in 2023 on a retail-first route",
                           "Launched in 450 specialty-retail doors at once",
                           "Removed from shelves in 2025",
                           "Estimated cumulative US loss of $21M, more than the board's $18M cap"],
             "approach_header": "Option B would repeat the pattern at a larger scale",
             "approach": ["600 doors in 2027, a third more than Mooncrest's launch",
                          "Onsoo would start at 4% awareness, where newcomers sell a median 2.6 units per door per week",
                          "The leading retailer reviews after 12 months and removes brands below 4.0",
                          "$7.5M a year of retail marketing and field sales is spent before that review"],
             "impact": [{"point": P("mc_loss"), "caption": "Mooncrest's estimated cumulative US loss by 2025"},
                        {"point": P("mc_doors"), "caption": "doors at Mooncrest's 2023 launch"},
                        {"point": P("b_doors_vs_mc"), "caption": "Option B's 2027 doors compared with Mooncrest's"}]},
            node="n2a", numbers=[N("$21M", "mc_loss")],
            footnotes=["Competitor outcomes from public reporting and interviews (briefing pack, Table 9)"]),
    content("2b1", "2", "The 1.3 times Amazon halo rests on a correlation that cannot show retail causes Amazon sales",
            "text-columns", "argument",
            {"kind": "text", "style": "columns", "columns": [
                {"header": "Option B lifts every year's Amazon units by the halo", "point": P("halo"),
                 "point_caption": "Amazon volume multiple in Option B",
                 "detail": ["Applied to every year, 2027–30", "Adds 843,000 Amazon units over four years",
                            "Worth $4.0M of contribution in the cash case (2c)"]},
                {"header": "Its only evidence is a 0.71 correlation across 30 brands",
                 "detail": ["The board member's memo links doors to Amazon sales, brand by brand",
                            "Compares brands at one moment, not before and after a retail launch",
                            "Larger, older brands have both more doors and more Amazon sales",
                            "Cause can run the other way: retailers take brands that already sell"]},
                {"header": "The one Amazon-first success added doors after it scaled", "point": P("sb_rev"), "emphasis": True,
                 "point_caption": "Saebom US revenue, 2025",
                 "detail": ["Saebom added 300 doors only in 2025, after scaling online",
                            "Its doors followed its Amazon sales, not the reverse",
                            "Onsoo can test a halo later by tracking Amazon sales around a small retail test"]}]},
            node="n2b", numbers=[N("1.3 times", "halo")],
            footnotes=["Correlation from the independent board member's memo (briefing pack, §12)"]),
    content("2c1", "2", "Retail's extra costs are 3.5 times its extra contribution, turning Option A's $2.4M surplus into a $20.8M cash need",
            "waterfall-bridge", "component",
            chart("waterfall", ["Retail marketing and field sales", "Launch fee and fixtures", "Extra inventory",
                                "Retail contribution", "Amazon halo", "Option A surplus", "Option B cash need"],
                  [("Cash need", ["need_fix", "need_one", "need_inv", "need_ret", "need_halo", "need_a", "peak_b"])],
                  highlight=["Option A surplus"], fmt="0.0",
                  waterfall_steps=["total", "step", "step", "step", "step", "step", "total"]),
            node="n2c", numbers=[N("3.5 times", "cost_ratio"), N("$2.4M", "need_a"), N("$20.8M", "peak_b")], highlights=["Option A surplus"],
            unit_line="**Option B cumulative cash need at end-2030, built up from its extra costs over Option A**, $ millions, 2027–30, ACoS 25%",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "header": "The national marketing budget sinks the case",
                "big_number": P("cost_ratio"), "caption": "dollars of extra cost for every dollar of extra contribution, 2027–30",
                "bullets": ["**Marketing and field sales:** $7.5M a year; at 600 doors they need 31.9 units per door per week to pay for themselves, 7.1 times the plan",
                            "**Amazon halo:** counted in full at 1.3 times, though its only basis is a correlation (2b)"]}},
            footnotes=[MODEL_NOTE]),
    content("2c2", "2", "Option B would hold group margin below the 8% floor for three years, with a low of 4.5% in 2027",
            "column-time-series", "time-series",
            chart("column", YEARS, [("Option A (Amazon-led)", [f"gm_a{y}" for y in Y]), ("Option B (retail-led)", [f"gm_b{y}" for y in Y])],
                  highlight=["Option B (retail-led)"], fmt="0.0%", benchmark={"label": "Board floor", "point": P("floor")}),
            node="n2c", numbers=[N("8%", "floor"), N("4.5%", "gm_b27")], highlights=["Option B (retail-led)"],
            unit_line="**Group operating margin including the US**, %, 2027–30; group excluding the US planned at 11.0%",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Option B's first-year loss is far beyond what the floor absorbs",
                "bullets": ["**2027:** Option B's US operating loss of $8.7M is 2.6 times the $3.3M the floor can absorb",
                            "**2027–30:** Option B loses $18.2M of operating profit over four years and never breaks even",
                            "**Option A:** costs the group 1.55 percentage points of margin in 2027 and stays well clear of the floor"]}},
            footnotes=["Group excluding the US: $140M–$158M of planned revenue at an 11.0% operating margin"]),

    # ================================================================ 3 · Amazon-led
    nav("d3", "agenda_tracker", "3"),
    content("L3", "3", "The Amazon-led route meets the cash, payback and margin tests on plan, and gets two-thirds of the way to the ambition",
            "numbered-levers", "argument",
            {"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
                {"code": "3a", "text": "US K-beauty buyers shop on Amazon most, though they find new brands on TikTok",
                 "point": P("sv_amz"), "metric": "of K-beauty buyers buy K-beauty on Amazon most often"},
                {"code": "3b", "text": "Every Amazon unit earns a contribution after fees, product cost and ads",
                 "point": P("cmu25"), "metric": "contribution per unit at the plan's 25% ACoS"},
                {"code": "3c", "text": "Cash need peaks at $1.9M and is repaid within 2030, with group margin above 9% every year",
                 "point": P("a_amb_share"), "metric": "of the $40M ambition reached by 2030 US revenue"}]},
            unit_line="**Status of each finding**, planning-team inputs and September 2026 survey"),
    content("3a1", "3", "Amazon is where US K-beauty buyers shop, but TikTok is where they find new brands",
            "multi-chart-panel", "frequency",
            {"kind": "panels", "panels": [
                {"header": "Amazon takes 41% of US K-beauty skincare sales",
                 "unit_line": "**US K-beauty skincare sales by channel**, % of sales, 2025",
                 "body": chart("bar", ["Amazon", "Specialty beauty", "Mass retail", "Brand websites", "Other"],
                               [("Share of sales", ["ch_amz", "ch_spec", "ch_mass", "ch_dtc", "ch_oth"])], highlight=["Amazon"], fmt="0%")},
                {"header": "61% of K-beauty buyers buy it on Amazon most often",
                 "unit_line": "**Where K-beauty buyers buy most often**, % of buyers, 2026",
                 "body": chart("bar", ["Amazon", "Specialty beauty"], [("Share of buyers", ["sv_amz", "sv_spec"])], highlight=["Amazon"], fmt="0%")},
                {"header": "TikTok leads discovery, at more than twice the rate of stores",
                 "unit_line": "**Where they found their last new brand**, % of buyers, 2026",
                 "body": chart("bar", ["TikTok", "In a store"], [("Share of buyers", ["sv_tiktok", "sv_store"])], highlight=["TikTok"], fmt="0%")}]},
            node="n3a", clauses=2, layout={"variant": "split_2"},
            so_what="Lead with Amazon for sales, and keep the $0.7M a year off-Amazon budget for TikTok and influencers, where discovery happens",
            so_what_style="line",
            footnotes=["Panels 2–3: survey of 1,200 US women aged 18–44 who bought facial skincare in the last six months, September 2026; base K-beauty buyers"]),
    content("3b1", "3", "Each Amazon unit keeps about $4.7 after fees, product cost and ads, roughly a fifth of its $24 price",
            "waterfall-bridge", "component",
            chart("waterfall", ["Price", "Referral fee", "FBA fee", "Advertising", "Product cost", "Freight", "Duty", "Contribution"],
                  [("$ per unit", ["price", "neg_ref", "neg_fba", "neg_ad", "neg_exf", "neg_frt", "neg_duty", "cmu25"])],
                  highlight=["Contribution"], fmt="0.00",
                  waterfall_steps=["total", "step", "step", "step", "step", "step", "step", "total"]),
            node="n3b", numbers=[N("$4.7", "cmu25"), N("$24", "price")], highlights=["Contribution"],
            unit_line="**Rice Ferment Barrier Cream sold on Amazon US**, $ per unit, planning-team inputs, ACoS 25%",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Advertising is the cost Onsoo controls",
                "bullets": ["**Advertising:** the largest single cost; each percentage point of ACoS costs 24 cents a unit",
                            "**Amazon fees:** referral and FBA fees take 36% of the price, and Onsoo cannot change them",
                            "**Break-even:** a unit still contributes up to 44.7% ACoS, but repaying the fixed costs needs far less (4a)"]}},
            footnotes=["Duty at 15% of the $3.50 ex-factory cost. The planning team applies the hero product's per-unit economics to all SKUs"]),
    content("3c1", "3", "Only Option A stays inside the $18M cash cap and pays back by 2030, with a peak cash need of $1.9M",
            "line-trend", "time-series",
            chart("line", YEARS, [("Option A (Amazon-led)", [f"cum_a{y}" for y in Y]), ("Option B (retail-led)", [f"cum_b{y}" for y in Y]),
                                  ("Board cap", ["capneg"] * 4)],
                  highlight=["Option A (Amazon-led)"], fmt="0.0"),
            node="n3c", numbers=[N("$18M", "capneg"), N("$1.9M", "cum_a27")], highlights=["Option A (Amazon-led)"],
            unit_line="**Cumulative US cash flow**, $ millions, end of each year, 2027–30, planning-team inputs",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "bullets", "header": "Option A's downside is small; Option B's keeps growing",
                "bullets": ["**Option A:** its peak need is 11% of the cap, which leaves room for the downside cases in section 4",
                            "**Option B:** crosses the cap in 2029 and still burns $1.9M of cash in 2030",
                            "**Payback:** Option A's cash turns positive in 2030, the last year the board allows"]}},
            footnotes=[MODEL_NOTE]),
    content("3c2", "3", "Scored on the board's tests, only the Amazon-led route builds a US business within the limits",
            "harvey-ball-table", "structure",
            {"kind": "table", "table_type": "harvey",
             "columns": ["$40M ambition", "Cash cap", "Payback by 2030", "Margin floor", "Peak cash need", "Verdict"],
             "rows": [
                 row("A · Amazon-led", [{"rating": 3}, {"rating": 4}, {"rating": 3}, {"rating": 4}, "peak_a",
                                        "Recommended: passes on plan; payback needs ACoS at or below 28.6%"], highlight=True),
                 row("B · Retail-led", [{"rating": 2}, {"rating": 0}, {"rating": 0}, {"rating": 1}, "peak_b",
                                        "Reject: breaks the cap and the floor even on its own plan"]),
                 row("J · Japan scale-up", [{"rating": 0}, {"rating": 4}, {"rating": 4}, {"rating": 4}, "peak_j",
                                            "Safe, but builds no US business; adds $7.0M of revenue by 2030"])],
             "legend": "Full circle = meets the test on planning-team inputs. Ambition scored on 2030 US revenue: A $26.4M; B $37.6M on a sell-through the evidence does not support (2a); J none"},
            node="n3c", layout={"variant": "full"},
            unit_line="**Options against the board's tests**, team assessment on planning-team inputs; peak cash need in $ millions",
            footnotes=["Option J peak cash need is its 2027 operating loss; the briefing pack gives no working capital for Japan"]),

    # ================================================================ 4 · Risks
    nav("d4", "agenda_tracker", "4"),
    content("L4", "4", "The Amazon case turns on ad cost: payback by 2030 needs ACoS at or below 28.6%, but the cash cap holds",
            "numbered-levers", "argument",
            {"kind": "levers", "headers": ["Risk", "Evidence"], "items": [
                {"code": "4a", "text": "Ad costs rise at scale instead of falling to the plan's 25%",
                 "point": P("acos_be"), "metric": "highest ACoS that still pays back by end-2030"},
                {"code": "4b", "text": "A tariff rise to 25% would cut the contribution of every unit",
                 "point": P("tariff_cpu"), "metric": "cents less contribution per unit"},
                {"code": "4c", "text": "Sales could stall, as they did for two of three Amazon-first peers",
                 "point": P("peer_low"), "metric": "2025 US revenue ceiling of the two peers that stalled"}]},
            numbers=[N("28.6%", "acos_be")], unit_line="**Size of each risk**, planning-team inputs and briefing-pack benchmarks"),
    content("4a1", "4", "At the ad cost typical for brands at Onsoo's planned scale, Option A would miss payback by $2.3M in 2030",
            "column-time-series", "item",
            chart("column", ["25%, plan", "28%, pilot", "32%, benchmark median", "38%, benchmark high"],
                  [("Cumulative cash, end-2030", ["cum_a30", "a28_cum30", "a32_cum30", "a38_cum30"])],
                  highlight=["32%, benchmark median"], fmt="0.0"),
            node="n4a", numbers=[N("$2.3M", "a32_cum30")], highlights=["32%, benchmark median"],
            unit_line="**Option A cumulative US cash flow at end-2030**, $ millions, by ACoS; other planning-team inputs unchanged",
            layout={"variant": "takeaway_sidebar", "sidebar": {
                "kind": "big_number", "header": "Every point of ad cost moves the payback",
                "big_number": P("acos_pp_cash"), "caption": "of cumulative cash by 2030 for each percentage point of ACoS",
                "bullets": ["**Plan, 25%:** assumes ACoS falls as the brand matures, but costs per click rise as brands bid on broader keywords",
                            "**Benchmark, 32%:** the median for skincare brands growing from $5M to $20M a year, the band Option A crosses in 2027–29"]}},
            footnotes=["ACoS benchmark: agency data for skincare brands scaling from $5M to $20M a year on Amazon US (median 32%, range 26%–38%)"]),
    content("4a2", "4", "Payback by 2030 holds only while ACoS stays at or below 28.6%, barely above what the small pilot achieved",
            "calculation-bridge", "component",
            {"kind": "equation", "terms": [
                {"point": P("pre_ad_tot"), "caption": "contribution before ads, 2027–30: 2,810,000 units at about $10.7 (3b)"},
                {"op": "−", "point": P("fixed_tot"), "caption": "fixed costs, setup and inventory to repay by end-2030"},
                {"op": "÷", "point": P("sales_tot"), "caption": "Amazon sales, 2027–30, at $24 a unit"},
                {"op": "=", "point": P("acos_be"), "caption": "highest ACoS that still pays back by end-2030"}],
             "assumptions_header": "The ceiling holds the plan's volumes and costs fixed",
             "assumptions": ["Volumes as planned: 300,000 Amazon units in 2027 rising to 1,100,000 in 2030",
                             "Fixed US costs of $2.1M a year plus $0.8M of setup in 2027",
                             "Inventory at four months of landed product cost",
                             "Duty at today's 15%; at 25% the ceiling falls to 26.9% (4b)"]},
            node="n4a", numbers=[N("28.6%", "acos_be")],
            unit_line="**Break-even ACoS for payback by end-2030, Option A**, $ millions over 2027–30, planning-team inputs",
            footnotes=["The pilot ran at 28% ACoS on a small budget; the agency median for brands at this scale is 32%"]),
    content("4b1", "4", "Even with a higher tariff and benchmark ad costs, peak cash need would stay at $3.9M, a fifth of the cap",
            "kpi-big-numbers", "item",
            {"kind": "kpi", "items": [
                {"point": P("tariff_cpu"), "caption": "cents less contribution per Amazon unit if duty rises from 15% to 25%",
                 "relation": "Decision expected in mid-2027",
                 "drivers": ["Charged on the $3.50 ex-factory cost only",
                             "Lowers the ACoS ceiling from 28.6% to 26.9%"]},
                {"point": P("a28t_cum30"), "caption": "cumulative cash at end-2030 at the pilot's 28% ACoS and a 25% duty",
                 "relation": "Payback narrowly missed",
                 "drivers": ["Short of payback by less than $1M",
                             "About one point less ACoS recovers it"]},
                {"point": P("worst_peak"), "caption": "peak cash need at 32% ACoS and a 25% duty, reached in 2029",
                 "relation": "22% of the $18M cap",
                 "drivers": ["The cap holds in every case we ran",
                             "Mooncrest lost $21M going retail-first"]}]},
            node="n4b", numbers=[N("$3.9M", "worst_peak")],
            unit_line="**Option A under a 25% duty**, planning-team volumes and costs",
            basis={"header": "How the tariff hit is calculated", "terms": [
                {"point": P("exf"), "caption": "ex-factory cost per unit, on which duty is charged"},
                {"op": "×", "point": P("tariff_diff"), "caption": "of extra duty if the rate rises from 15% to 25%"},
                {"op": "=", "point": P("tariff_cpu"), "caption": "cents less contribution per unit"}]},
            footnotes=["Duty applied at 25% from 2027, the harsher case; the decision is expected in mid-2027"]),
    content("4c1", "4", "A stall at the pilot pace, the fate of two of three Amazon-first peers, would cost Onsoo $6.8M by 2030",
            "comparison-table", "item",
            {"kind": "table", "table_type": "comparison", "columns": ["Entry route", "Outcome"], "verdict_header": "Lesson for Onsoo",
             "rows": [
                 row("Saebom", ["Amazon-first, 2022", "About $30M US revenue; added 300 retail doors in 2025"], note="The path Option A plans: scale online, then add retail"),
                 row("Gaon Lab", ["Amazon-first, 2022", "Below $5M US revenue"], note="Stalled: the case to manage for"),
                 row("Yeoreum", ["Amazon-first, 2023", "Below $5M US revenue"], note="Stalled: the case to manage for"),
                 row("Mooncrest", ["Retail-first, 2023, 450 doors", "Removed from shelves; estimated US loss of $21M"], note="Option B's risk (2a)"),
                 row("Onsoo stall case", ["Amazon, flat at the June 2026 pace of about $4.0M a year", "stall_cum30"], highlight=True,
                     note="Cumulative cash by 2030 if nothing changes")]},
            node="n4c", numbers=[N("$6.8M", "stall_cum30")],
            callout={"target": "Onsoo stall case", "header": "Set a stop rule", "detail": "A review at the end of 2027 caps the loss near $2.5M"},
            basis={"header": "How the stall case is calculated", "terms": [
                {"point": P("stall_contrib"), "caption": "contribution after ads, 2027–30: 168,000 units a year at $4.0 a unit, the pilot's 28% ACoS"},
                {"op": "−", "point": P("stall_fixed"), "caption": "fixed costs, setup and inventory, as in the plan"},
                {"op": "=", "point": P("stall_cum30"), "caption": "cumulative cash at end-2030"}]},
            unit_line="**Recent K-beauty entrants to the US, and Onsoo's stall case**, outcomes by 2025; stall case 2027–30",
            footnotes=["Peers: public reporting and interviews (briefing pack, Table 9). Stall case: our estimate, sales flat at 12 × the June 2026 pilot month"]),

    # ================================================================ 5 · Make it happen
    nav("d5", "agenda_tracker", "5"),
    content("L5", "5", "Three steps take Onsoo from a compliant Amazon launch in 2027 to a retail decision once awareness passes 20%",
            "process-flow", "structure",
            {"kind": "process", "steps": [
                {"header": "Set up, Q2 2027", "point": P("setup"), "point_caption": "one-time setup cost, $M",
                 "detail": ["US entity, MoCRA registration and safety substantiation", "English labels on all US stock",
                            "Take over the pilot listings from the cross-border seller"],
                 "footer": "Gate: labels compliant first"},
                {"header": "Scale on Amazon, H2 2027–2028", "point": P("ua27"), "point_caption": "Amazon units planned for 2027", "emphasis": True,
                 "detail": ["Add four SKUs, seven in all", "Run the ad budget to an ACoS ceiling of 28.6%",
                            "Spend the $0.7M a year off-Amazon budget on TikTok and influencers"],
                 "footer": "Gate: end-2027 review"},
                {"header": "Retest retail, from 2029", "point": P("aw_trig"), "point_caption": "aided awareness needed before retail",
                 "detail": ["Survey awareness among category buyers every year", "Re-run the retail case only above 20% awareness and $10M of Amazon sales",
                            "Start small and track Amazon sales around it"],
                 "footer": "Gate: board approves retail"}]},
            numbers=[N("20%", "aw_trig")], count_word=3),
    content("5a", "5", "Four gates tell the board early whether to scale, fix or stop the US launch, led by the ad-cost ceiling",
            "comparison-table", "item",
            {"kind": "table", "table_type": "comparison", "columns": ["What we track", "Threshold", "If missed"], "verdict_header": "Why it matters",
             "rows": [
                 row("Ad cost (ACoS)", ["Amazon ad spend as a share of Amazon sales, each quarter", "At or below 28.6%; 26.9% if duty rises to 25%",
                                        "Cut spend on the weakest keywords and SKUs before adding budget"], note="Protects payback"),
                 row("Sales pace", ["Amazon units against plan, end-2027", "300,000 units in 2027, and well above the 168,000 June 2026 pace",
                                    "Cut fixed costs and pause new SKUs"], note="Stops a stall early"),
                 row("Tariff", ["US duty on Korean cosmetics, decision in mid-2027", "15% today; 25% possible",
                                "Re-run the case and lower the ACoS ceiling"], note="Resets the ceiling"),
                 row("Retail trigger", ["Aided awareness among category buyers, and Amazon sales", "Above 20% awareness and above $10M of Amazon sales",
                                        "Stay Amazon-led and retest a year later"], note="Opens retail")]},
            count_word=4,
            callout={"target": "Ad cost (ACoS)", "header": "Most important gate", "detail": "Each percentage point costs about $0.7M of cash by 2030"}),
    content("5b", "5", "The plan keeps the CEO's Amazon-first idea but raises the retail trigger and budgets for higher ad costs",
            "from-to", "argument",
            {"kind": "from_to", "from_label": "From: the CEO's initial hypothesis", "to_label": "To: the recommended plan", "rows": [
                {"label": "Retail trigger", "from": "Aided awareness above 15%", "to": "Aided awareness above 20%",
                 "to_detail": "At 10–20%, newcomers sell a median 3.5 units per door per week, under the 4.0 cut-off"},
                {"label": "Ad cost", "from": "ACoS falls to 25% as the brand matures", "to": "A 28.6% ceiling, checked quarterly",
                 "to_detail": "The agency median at this scale is 32%"},
                {"label": "Seller", "from": "Cross-border seller, Korean-only labels", "to": "Own US entity, English labels",
                 "to_detail": "Labels are the top complaint, in 6% of reviews"},
                {"label": "Downside", "from": "One forecast, no stop rule", "to": "A stall case and an end-2027 review",
                 "to_detail": "A stall would lose $6.8M by 2030 without a stop"},
                {"label": "Ambition", "from": "$40M by 2030", "to": "$26.4M by 2030, $40M after retail",
                 "to_detail": "Saebom reached about $30M on Amazon before adding doors"},
                {"label": "Tariff", "from": "Duty fixed at 15%", "to": "Case re-run after the mid-2027 decision",
                 "to_detail": "A 25% duty costs 35 cents a unit"}]}),
    content("5c", "5", "The board is asked to approve three decisions at its March 2027 meeting",
            "text-columns", "argument",
            {"kind": "text", "style": "columns", "columns": [
                {"header": "Approve the Amazon-led US entry for 2027", "emphasis": True, "point": P("worst_peak"),
                 "point_caption": "worst-case peak cash need",
                 "detail": ["Option A on the planning team's volumes", "US entity, compliance and labels in Q2 2027",
                            "Japan scale-up held back under the one-launch rule"], "footer": "Owner: CEO"},
                {"header": "Hold the launch to four gates", "point": P("acos_be"), "point_caption": "ACoS ceiling, reviewed every quarter",
                 "detail": ["End-2027 review of the sales pace against plan", "Case re-run after the mid-2027 tariff decision",
                            "Quarterly report to the board"], "footer": "Owner: CFO and US lead"},
                {"header": "Restate the $40M ambition as a goal beyond 2030", "point": P("a_amb_share"),
                 "point_caption": "of $40M reached by 2030 on Amazon alone",
                 "detail": ["Retail decided only above 20% awareness", "Saebom's path: about $30M online before adding 300 doors",
                            "Revisit the goal once 2028 results are in"], "footer": "Owner: board"}]},
            count_word=3),

    # ================================================================ Appendix
    {"id": "app", "role": "appendix_divider", "status": "filled"},
    backup("bx", "1", "Three branches were left out on purpose: one Onsoo cannot move and two the briefing pack gives no basis to size",
           "comparison-table",
           {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the deck"], "rows": [
               row("Exchange rate", ["A weaker won would lower dollar product costs enough to change the route", "Outside management's control and only an upside; the pack gives no FX path"]),
               row("Other routes", ["A DTC-led or mass-retail entry would beat both modeled routes", "Not modeled by the planning team; DTC is 12% and mass retail 14% of K-beauty skincare sales"]),
               row("Small retail test", ["A small specialty-retail test in 2027 would build awareness cheaply", "No cost or door data for a small test; it returns at the 20% awareness trigger (5)"])]},
           tree_node=["nx1", "nx2", "nx3"]),
    backup("b5", "1", "A Japan scale-up would add $1.8M of operating profit by 2030 at low risk, but only $7.0M of revenue",
           "data-table",
           {"kind": "table", "table_type": "data", "columns": YEARS, "rows": [
               row("Added revenue, $M", [f"jr{y}" for y in Y]),
               row("Contribution at 30%, $M", [f"cj{y}" for y in Y]),
               row("Fixed and one-time cost, $M", ["fx_j27", "jfix", "jfix", "jfix"]),
               row("Operating profit, $M", [f"op_j{y}" for y in Y]),
               row("Cumulative operating profit, $M", ["jc27", "jc28", "jc29", "j_cum"], highlight=True),
               row("Group operating margin", [f"gm_j{y}" for y in Y])]},
           of="1c1", numbers=[N("$1.8M", "j_cum"), N("$7.0M", "jr30")], layout={"variant": "full"},
           unit_line="**Option J · Japan scale-up instead of the US in 2027**, planning-team inputs",
           footnotes=["The briefing pack gives no working capital for Japan; Japan facial skincare grows about 1.5% a year"]),
    backup("b4", "2", "Five figures in the board material need correcting before the board relies on them",
           "comparison-table",
           {"kind": "table", "table_type": "comparison", "columns": ["As circulated", "What is wrong with it", "Use instead"], "rows": [
               row("US K-beauty market, $B", ["tp52", "Adds makeup and hair care to skincare", "kb25"]),
               row("Retail sell-through, units per door per week", ["upw_plan", "From the retailer's deck on successful newcomers only", "st_lo"]),
               row("Amazon halo", ["halo", "Rests on a cross-brand correlation; no cause shown", "No halo in the base case"]),
               row("ACoS at scale", ["acos_plan", "Assumes ACoS falls; the benchmark shows it rising", "acos_bench"]),
               row("Awareness trigger for retail", ["aw_trig_ceo", "At 10–20% awareness, the median is under the 4.0 cut-off", "aw_trig"])]},
           of="L2", count_word=5, layout={"variant": "full"}),
    backup("b6", "2", "Options A and J keep group margin above the floor every year, while Option B breaches it three years running",
           "heatmap",
           {"kind": "table", "table_type": "heatmap", "columns": YEARS, "rows": [
               row("Board floor", ["floor", "floor", "floor", "floor"], benchmark=True),
               row("A · Amazon-led", [f"gm_a{y}" for y in Y], note="Dips in 2027 on setup costs, then recovers as US profit grows"),
               row("B · Retail-led", [f"gm_b{y}" for y in Y], highlight=True, note="Below the floor in 2027–29: US losses of $8.7M, $5.1M and $3.2M"),
               row("J · Japan scale-up", [f"gm_j{y}" for y in Y], note="Barely moves group margin: small revenue at a 30% contribution")], "verdict_header": "Reading"},
           of="2c2", layout={"variant": "full"},
           footnotes=["Group excluding the US planned at an 11.0% operating margin on $140M–$158M of revenue; each option's results added at planning-team inputs"],
           unit_line="**Group operating margin by option**, %, 2027–30, planning-team inputs"),
    backup("b2", "2", "Option B never pays back: operating losses in every year and cumulative cash of −$20.8M by 2030",
           "data-table",
           {"kind": "table", "table_type": "data", "columns": YEARS, "rows": [
               row("Amazon units", [f"ub{y}" for y in Y]),
               row("Specialty-retail units", [f"ru{y}" for y in Y]),
               row("Revenue, $M", [f"rev_b{y}" for y in Y]),
               row("Contribution after ads, $M", [f"cb{y}" for y in Y]),
               row("Fixed and one-time cost, $M", ["fxb27", "fb", "fxb29", "fxb30"]),
               row("Operating profit, $M", [f"op_b{y}" for y in Y]),
               row("Inventory at year end, $M", [f"inv_b{y}" for y in Y]),
               row("Cumulative cash, $M", [f"cum_b{y}" for y in Y], highlight=True)]},
           of="2c1", numbers=[N("−$20.8M", "cum_b30")], layout={"variant": "full"},
           unit_line="**Option B · retail-led US model**, planning-team inputs: 4.5 units per door per week, 1.3 times halo, ACoS 25%",
           footnotes=[MODEL_NOTE]),
    backup("b3", "3", "A retail unit earns more than an Amazon unit, but only after $7.5M a year of fixed retail costs is paid",
           "data-table",
           {"kind": "table", "table_type": "data", "columns": ["Amazon", "Specialty retail"], "rows": [
               row("Price Onsoo receives, $", ["price", "whsl"]),
               row("Channel fees and allowances, $", ["amz_fees", "ch_fees_r"]),
               row("Product, freight and duty, $", ["landed_amz", "landed_ret"]),
               row("Advertising, $", ["ad25", "In the fixed retail marketing budget"]),
               row("Contribution per unit, $", ["cmu25", "cmu_r"], highlight=True),
               row("Extra fixed channel cost a year, $M", ["None beyond the base US costs", "w_fix_yr"])]},
           of="3b1", numbers=[N("$7.5M", "w_fix_yr")], layout={"variant": "full"},
           unit_line="**Per-unit economics by channel**, Rice Ferment Barrier Cream, $ per unit, planning-team inputs",
           footnotes=["Amazon fees: 15% referral fee and $5.10 FBA fee; retail allowances: 8% co-op and 4% returns on the $14.00 wholesale price"]),
    backup("b1", "3", "Option A turns cash-positive in 2030 on the planning team's inputs",
           "data-table",
           {"kind": "table", "table_type": "data", "columns": YEARS, "rows": [
               row("Amazon units", [f"ua{y}" for y in Y]),
               row("Revenue, $M", [f"rev_a{y}" for y in Y]),
               row("Contribution after ads, $M", [f"ca{y}" for y in Y]),
               row("Fixed and one-time cost, $M", ["fx_a27", "fa", "fa", "fa"]),
               row("Operating profit, $M", [f"op_a{y}" for y in Y]),
               row("Inventory at year end, $M", [f"inv_a{y}" for y in Y]),
               row("Cumulative cash, $M", [f"cum_a{y}" for y in Y], highlight=True)]},
           of="3c1", layout={"variant": "full"},
           unit_line="**Option A · Amazon-led US model**, planning-team inputs: ACoS 25%, duty 15%",
           footnotes=["Only inventory counts as working capital: the pack gives no Amazon payout lag or receivables. One-time costs run through operating profit; inventory is not released in 2030"]),
    {"id": "end", "role": "end_page", "status": "filled"},
]

# ---------------------------------------------------------------- storyline
storyline = {
    "governing_thought": "Enter the US in 2027 through Amazon, not national retail, and cap ad costs at 28.6% of sales so the launch pays back by 2030",
    "exec_summary": [
        {"id": "1", "text": "The US is the better use of the one 2027 launch, and Onsoo products already sell there",
         "supports": ["L1", "1a1", "1b1", "1b2", "1c1"],
         "sub_points": [{"text": "US K-beauty facial skincare rose 1.9 times in four years, to $3.6B", "slide_id": "1a1"},
                        {"text": "On plan, the US reaches $26.4M of revenue in 2030; Japan adds $7.0M", "slide_id": "1c1"}]},
        {"id": "2", "text": "A national retail launch fails the board's tests even on its own plan",
         "supports": ["L2", "2a1", "2a2", "2b1", "2c1", "2c2"],
         "sub_points": [{"text": "At 4% awareness, sales per door would sit below the retailer's 4.0 cut-off", "slide_id": "2a1"},
                        {"text": "Cash need reaches $20.8M against the $18M cap; group margin falls to 4.5%", "slide_id": "2c1"}]},
        {"id": "3", "text": "The Amazon-led route passes the cash, payback and margin tests on plan",
         "supports": ["L3", "3a1", "3b1", "3c1", "3c2"],
         "sub_points": [{"text": "Cash need peaks at $1.9M and is repaid in 2030, with about $4.7 kept per unit", "slide_id": "3c1"}]},
        {"id": "4", "text": "Its payback hinges on ad cost: ACoS must stay at or below 28.6%",
         "supports": ["L4", "4a1", "4a2", "4b1", "4c1"],
         "sub_points": [{"text": "At the 32% benchmark, cumulative cash ends 2030 at −$2.3M", "slide_id": "4a1"},
                        {"text": "Even with a 25% tariff, peak cash need stays at $3.9M, a fifth of the cap", "slide_id": "4b1"}]},
        {"id": "5", "text": "Approve the Amazon launch with four gates; open retail only above 20% awareness",
         "supports": ["L5", "5a", "5b", "5c"],
         "sub_points": [{"text": "Raise the CEO's retail trigger from 15%, and restate $40M as a goal beyond 2030", "slide_id": "5b"}]}],
    "next_steps": [
        {"action": "Approve the Amazon-led US entry and a cash envelope sized to the $3.9M worst-case peak", "owner": "CEO and board", "timing": "March 2027"},
        {"action": "Set up the US entity, MoCRA registration and English labels; take over the pilot listings", "owner": "US lead (to be appointed) and COO", "timing": "Q2 2027"},
        {"action": "Rebuild the 2027 ad plan around a 28.6% ACoS ceiling and report ACoS every quarter", "owner": "US lead and CFO", "timing": "From Q3 2027"},
        {"action": "Re-run the case on the US tariff decision", "owner": "CFO", "timing": "Mid-2027"},
        {"action": "Survey aided awareness every year; bring a retail case only above 20%", "owner": "CMO", "timing": "From 2028"}],
}

sections = [
    {"id": "1", "title": "The US prize", "tracker_label": "US vs Japan", "exec_item_id": "1", "tree_node": "n1", "lead_slide": "L1",
     "question": "Is the US a better use of the one 2027 launch than a Japan scale-up?"},
    {"id": "2", "title": "The retail-led route", "tracker_label": "Retail-led", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
     "question": "Does a national specialty-retail launch in 2027 meet the board's tests?"},
    {"id": "3", "title": "The Amazon-led route", "tracker_label": "Amazon-led", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
     "question": "Does an Amazon-led launch meet the board's tests?"},
    {"id": "4", "title": "Risks to the Amazon case", "tracker_label": "Risks", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
     "question": "Does the Amazon case hold if ad costs, tariffs or sales growth go against plan?"},
    {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
     "question": "How should Onsoo launch, and what would make it change course?"},
]


def node(id, code, parent, hyp, imp, infl, analysis, exhibit, sources, verdict, note, ko=False, label=None):
    n = {"id": id, "code": code, "hypothesis": hyp}
    if parent: n["parent"] = parent
    if label: n["label"] = label
    if imp:
        n["priority"] = {"importance": imp, "influence": infl}
        n["workplan"] = {"analysis": analysis, "exhibit": exhibit, "sources": sources}
        if ko: n["workplan"]["knock_out"] = True
    if verdict: n["finding"] = {"verdict": verdict, "note": note}
    return n


issue_tree = [
    {"id": "n1", "code": "1", "label": "US prize", "hypothesis": "The US is a better use of the one 2027 launch than a Japan scale-up"},
    node("n1a", "1a", "n1", "US K-beauty facial skincare is large and growing faster than the category", "high", "low",
         "K-beauty and category sales, 2021–25; check the trade-press market figure", "stacked-column, 2021–25", ["Briefing pack Table 1", "Trade-press article (§12)"],
         "confirmed", "Grew 89% to $3.6B against 22% for the category; the $5.2B figure also counts makeup and hair care"),
    node("n1b", "1b", "n1", "Onsoo's products already sell to US buyers on Amazon", "high", "medium",
         "Pilot units by month; rating, repeat and complaints against benchmarks", "column by month; KPI tiles", ["Briefing pack §6"],
         "confirmed", "Units nearly doubled in six months at 4.5 stars; repeat of 29% is close to the 31% US benchmark; labels need fixing", ko=True),
    node("n1c", "1c", "n1", "A US launch builds more revenue by 2030 than a Japan scale-up", "high", "high",
         "2030 revenue of Option A against Option J; market growth", "two panels: revenue by year, growth rates", ["Briefing pack Tables 5 and 7"],
         "confirmed", "$26.4M against $7.0M on plan; Japan adds profit sooner with less risk"),
    {"id": "n2", "code": "2", "label": "Retail-led", "hypothesis": "A national specialty-retail launch in 600 doors in 2027 meets the board's tests"},
    node("n2a", "2a", "n2", "Onsoo would sell the 4.5 units per door per week the plan assumes", "high", "medium",
         "Sell-through by awareness band against the removal threshold; Mooncrest case", "bar with threshold line; case example", ["Briefing pack Tables 8 and 9", "Survey §10"],
         "refuted", "At 4% awareness newcomers sell a median 2.6, under the retailer's 4.0 cut-off; Mooncrest was delisted", ko=True),
    node("n2b", "2b", "n2", "Retail lifts Onsoo's Amazon sales by 1.3 times", "medium", "low",
         "Test the basis of the halo multiple", "text columns", ["Board member memo (§12)", "Table 9"],
         "refuted", "Its only basis is a 0.71 cross-brand correlation; Saebom's doors followed its Amazon sales"),
    node("n2c", "2c", "n2", "Option B stays within the $18M cash cap and the 8% margin floor", "high", "high",
         "Cumulative cash and group margin by year on planning-team inputs", "waterfall A to B; margin by year", ["Briefing pack Tables 4–6, group plan"],
         "refuted", "Peak cash need of $20.8M by 2030 with no payback; group margin of 4.5% in 2027", ko=True),
    {"id": "n3", "code": "3", "label": "Amazon-led", "hypothesis": "An Amazon-led launch in 2027 meets the board's tests"},
    node("n3a", "3a", "n3", "US K-beauty buyers both shop and discover new brands on Amazon", "medium", "medium",
         "Channel shares; where buyers buy and discover", "three panels of bars", ["Briefing pack Table 2", "Survey §10"],
         "revised", "They shop there (41% of sales, 61% buy there most often) but find new brands on TikTok (38%)"),
    node("n3b", "3b", "n3", "Each Amazon unit makes a positive contribution after ads", "high", "medium",
         "Per-unit waterfall from price to contribution", "waterfall per unit", ["Briefing pack Table 4"],
         "confirmed", "About $4.7 a unit at 25% ACoS; positive up to 44.7%"),
    node("n3c", "3c", "n3", "Option A stays within the cash cap, pays back by 2030 and holds the margin floor", "high", "high",
         "Cumulative cash by year against the cap; scorecard on the board's tests", "line with cap; Harvey-ball table", ["Briefing pack Tables 4–7"],
         "confirmed", "Peak need of $1.9M, repaid in 2030, group margin at least 9.5%; 66% of the $40M ambition", ko=True),
    {"id": "n4", "code": "4", "label": "Risks", "hypothesis": "The Amazon-led case holds if ad costs, tariffs or sales growth go against plan"},
    node("n4a", "4a", "n4", "Ad costs fall to 25% of sales as the brand matures", "high", "high",
         "Cumulative cash by ACoS; break-even ACoS", "columns by ACoS; equation", ["Agency benchmark (§11)", "Pilot (§6)"],
         "refuted", "The benchmark median at this scale is 32%; payback needs 28.6% or less", ko=True),
    node("n4b", "4b", "n4", "A tariff rise to 25% would not break the case", "medium", "low",
         "Contribution and cash at a 25% duty", "KPI tiles with basis", ["Uncertainties (§13)", "Table 4"],
         "revised", "Costs 35 cents a unit; with the pilot's ad cost it pushes payback beyond 2030, but the cap holds"),
    node("n4c", "4c", "n4", "Onsoo's Amazon sales will grow like Saebom's rather than stall like Gaon Lab's and Yeoreum's", "high", "medium",
         "Peer outcomes; stall case at the pilot pace", "table with stall case", ["Table 9", "Pilot (§6)"],
         "revised", "Unproven: a stall would lose $6.8M by 2030, and an end-2027 review caps it near $2.5M"),
    {"id": "nx1", "label": "Exchange rate", "hypothesis": "A weaker won would lower dollar product costs enough to change the route",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Outside management's control, an upside only, and the briefing pack gives no FX path"},
    {"id": "nx2", "label": "Other routes", "hypothesis": "A DTC-led or mass-retail entry would beat both modeled routes",
     "cut_reason": "Not modeled by the planning team; out of scope for this decision"},
    {"id": "nx3", "label": "Small retail test", "hypothesis": "A small specialty-retail test in 2027 would build awareness at low cost",
     "cut_reason": "No cost or door data in the briefing pack; it returns at the 20% awareness trigger"},
]

problem = {
    "statement": "Should Onsoo enter the US market in 2027, and if so, by which route, within $18M of peak cash and with payback by 2030?",
    "decision_maker": "CEO and board of Onsoo Botanicals, choosing the 2027 new-market launch",
    "success_criteria": ["A US business on the way to $40M of revenue by 2030",
                         "Peak negative cumulative US cash of no more than $18M through 2030",
                         "Cumulative US cash back to zero by the end of 2030",
                         "Group operating margin at or above 8% in every year",
                         "Only one major new-market launch in 2027"],
    "deadline": "Board meeting, March 2027",
    "accuracy": "Direction and order of magnitude (±20%) on planning-team inputs",
    "out_of_scope": ["Markets other than the US and Japan", "Routes the planning team did not model (DTC-led, mass retail)",
                     "Exchange-rate scenarios"],
    "one_day_answer": {
        "situation": "Onsoo is a profitable Korean skincare brand with no US entity, and a three-SKU Amazon pilot sold 64,800 units in six months",
        "complication": "The board can fund one launch in 2027, and the three proposals (Amazon-led, national retail, Japan) carry very different cash and risk",
        "resolution": storyline["governing_thought"]},
}

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Entering the US market", "subtitle": "Should Onsoo enter the US in 2027, and by which route? Discussion document for the CEO and board",
             "company_name": "Onsoo Botanicals", "audience": "CEO and board", "purpose": problem["statement"],
             "date": "2026-11-15", "language": "en-US",
             "confidentiality": "Synthetic benchmark data: company and figures are fictional",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Onsoo Botanicals US market entry briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline, "problem": problem, "issue_tree": issue_tree, "sections": sections, "slides": slides,
}

# ---------------------------------------------------------------- assign slide_id to every data point
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)

first = {}
for s in slides:
    for r in refs({k: s.get(k) for k in ("lead_message", "body", "layout", "callout", "basis")}):
        first.setdefault(r, s["id"])
# inputs not shown: the slide of the first shown number built from them
users = {}
for d in M.DP.values():
    for r in d.get("derived_from", []):
        users.setdefault(r, []).append(d["id"])
order = [s["id"] for s in slides]
def slide_of(i, seen=()):
    if i in first: return first[i]
    cands = [slide_of(u, seen + (i,)) for u in users.get(i, []) if u not in seen]
    cands = [c for c in cands if c]
    return min(cands, key=order.index) if cands else None
dps = []
for i, d in M.DP.items():
    d = dict(d)
    d["slide_id"] = slide_of(i) or "L1"
    dps.append(d)
spec["data_points"] = dps
sources = [{"id": k, "kind": "user_provided", "name": v, "input_id": "in-1"} for k, v in M.SRC.items()]
sources.append({"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"})
spec["sources"] = sources

out = os.path.join(HERE, "onsoo-us-entry.json")
json.dump(spec, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, len(slides), "slides", len(dps), "data points")
