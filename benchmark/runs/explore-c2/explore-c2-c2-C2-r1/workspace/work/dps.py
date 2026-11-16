# Data points for the Harlow deck. Every user number carries a verbatim excerpt from the briefing pack.
import re
DP = []      # list of dicts in order
V = {}       # id -> value

def U(i, sl, label, value, unit, period, excerpt, locator, used=""):
    DP.append(dict(id=i, slide_id=sl, label=label, value=value, unit=unit, period=period, source_id="s1",
                   excerpt=excerpt, locator=locator, used_in=used))
    V[i] = value

def _ev(calc):
    return eval(calc, {}, dict(V))

def D(i, sl, label, unit, period, calc, formula, est=False, assumptions=None, used="", rnd=None):
    refs = [r for r in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if r in V]
    val = _ev(calc)
    d = dict(id=i, slide_id=sl, label=label, value=round(val, 6), unit=unit, period=period, source_id="s2",
             derived_from=list(dict.fromkeys(refs)), formula=formula, calc=calc, used_in=used)
    if est:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP.append(d); V[i] = d["value"]

T1 = "Briefing pack, Table 1 (income statement)"
# ---- Table 1
U("sal23","1","Sales, FY2023",1420.0,"$M","FY2023",'Table 1 "Sales"; column FY2023 = "1,420.0"',T1)
U("sal25","1","Sales, FY2025",1503.0,"$M","FY2025",'Table 1 "Sales"; column FY2025 = "1,503.0"',T1)
U("gp23","1","Gross profit, FY2023",369.8,"$M","FY2023",'Table 1 "Gross profit"; column FY2023 = "369.8"',T1)
U("gp25","1","Gross profit, FY2025",376.1,"$M","FY2025",'Table 1 "Gross profit"; column FY2025 = "376.1"',T1)
U("lab23","1","Store labor, FY2023",167.6,"$M","FY2023",'Table 1 "Store labor"; column FY2023 = "167.6"',T1)
U("lab25","1","Store labor, FY2025",181.9,"$M","FY2025",'Table 1 "Store labor"; column FY2025 = "181.9"',T1)
U("occ23","1","Occupancy and energy, FY2023",82.4,"$M","FY2023",'Table 1 "Occupancy and energy"; column FY2023 = "82.4"',T1)
U("occ25","1","Occupancy and energy, FY2025",90.2,"$M","FY2025",'Table 1 "Occupancy and energy"; column FY2025 = "90.2"',T1)
U("ecf23","1","E-commerce fulfillment (net of delivery fees), FY2023",5.2,"$M","FY2023",'Table 1 "E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2023 = "5.2"',T1)
U("ecf25","1","E-commerce fulfillment (net of delivery fees), FY2025",18.1,"$M","FY2025",'Table 1 "E-commerce fulfillment (picking + delivery, net of delivery fees)"; column FY2025 = "18.1"',T1)
U("sga23","1","Other SG&A, FY2023",66.7,"$M","FY2023",'Table 1 "Other SG&A"; column FY2023 = "66.7"',T1)
U("sga25","1","Other SG&A, FY2025",70.6,"$M","FY2025",'Table 1 "Other SG&A"; column FY2025 = "70.6"',T1)
U("oi25","1","Operating income, FY2025",15.3,"$M","FY2025",'Table 1 "Operating income"; column FY2025 = "15.3"',T1)
U("om23","1","Operating margin, FY2023",0.0337,"%","FY2023",'Table 1 "Operating margin"; column FY2023 = "3.37%"',T1,"waterfall start")
U("om25","1","Operating margin, FY2025",0.0102,"%","FY2025",'Table 1 "Operating margin"; column FY2025 = "1.02%"',T1,"waterfall end")
# ---- 1.1 operating margin bridge (share of sales)
D("st_gm","1","Change in gross margin, FY2023-25, % of sales","%","FY2023-25","gp25 / sal25 - gp23 / sal23","376.1/1,503.0 − 369.8/1,420.0",used="waterfall step")
D("st_lab","1","Effect of store labor on margin, FY2023-25, % of sales","%","FY2023-25","lab23 / sal23 - lab25 / sal25","167.6/1,420.0 − 181.9/1,503.0",used="waterfall step")
D("st_occ","1","Effect of occupancy and energy on margin, FY2023-25, % of sales","%","FY2023-25","occ23 / sal23 - occ25 / sal25","82.4/1,420.0 − 90.2/1,503.0",used="waterfall step")
D("st_ecf","1","Effect of e-commerce fulfillment on margin, FY2023-25, % of sales","%","FY2023-25","ecf23 / sal23 - ecf25 / sal25","5.2/1,420.0 − 18.1/1,503.0",used="waterfall step")
D("st_sga","1","Effect of other SG&A on margin, FY2023-25, % of sales","%","FY2023-25","sga23 / sal23 - sga25 / sal25","66.7/1,420.0 − 70.6/1,503.0",used="waterfall step")
D("decl","1","Operating margin decline, FY2023-25","pp","FY2023-25","(om25 - om23) * 100","(1.02% − 3.37%) × 100",used="exec summary")
D("sh_gm","1","Gross margin's share of the margin decline","%","FY2023-25","st_gm / (om25 - om23)","gross-margin step ÷ total decline",used="sidebar")
D("sh_ecf","1","E-commerce fulfillment's share of the margin decline","%","FY2023-25","st_ecf / (om25 - om23)","fulfillment step ÷ total decline",used="sidebar")
D("sh_lab","1","Store labor's share of the margin decline","%","FY2023-25","st_lab / (om25 - om23)","labor step ÷ total decline",used="sidebar")
D("sh_occ","1","Occupancy's share of the margin decline","%","FY2023-25","st_occ / (om25 - om23)","occupancy step ÷ total decline",used="sidebar")
D("sh_ge","1","Gross margin and e-commerce fulfillment, share of the margin decline","%","FY2023-25","(st_gm + st_ecf) / (om25 - om23)","(gross-margin step + fulfillment step) ÷ total decline",used="title, sidebar big number")
# ---- 1.2 gross margin drivers (Table 2)
T2 = "Briefing pack, Table 2 (gross-margin drivers)"
U("ps23","2","Promotional sales, share of sales, FY2023",0.24,"%","FY2023",'Table 2 "Promotional sales, share of sales"; column FY2023 = "24.0%"',T2)
U("ps24","2","Promotional sales, share of sales, FY2024",0.262,"%","FY2024",'Table 2 "Promotional sales, share of sales"; column FY2024 = "26.2%"',T2)
U("ps25","2","Promotional sales, share of sales, FY2025",0.29,"%","FY2025",'Table 2 "Promotional sales, share of sales"; column FY2025 = "29.0%"',T2)
U("pls23","2","Private-label sales, share of sales, FY2023",0.17,"%","FY2023",'Table 2 "Private-label sales, share of sales"; column FY2023 = "17.0%"',T2)
U("pls25","2","Private-label sales, share of sales, FY2025",0.185,"%","FY2025",'Table 2 "Private-label sales, share of sales"; column FY2025 = "18.5%"',T2)
U("sh23","2","Shrink, % of sales, FY2023",0.021,"%","FY2023",'Table 2 "Shrink, % of sales"; column FY2023 = "2.1%"',T2)
U("sh25","2","Shrink, % of sales, FY2025",0.026,"%","FY2025",'Table 2 "Shrink, % of sales"; column FY2025 = "2.6%"',T2)
U("plg","2","Gross-margin gap of promotional vs. regular-price sales",14,"pp","FY2023-25","Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).","Briefing pack, section 5, note under Table 2")
U("plp","2","Gross-margin premium of private label over national brands",12,"pp","FY2023-25","Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).","Briefing pack, section 5, note under Table 2")
U("vf23","2","Vendor funding, share of promotional markdowns, FY2023",0.55,"%","FY2023","Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.","Briefing pack, section 5, note under Table 2")
U("vf25","2","Vendor funding, share of promotional markdowns, FY2025",0.46,"%","FY2025","Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.","Briefing pack, section 5, note under Table 2")
D("gm23","2","Gross margin, FY2023","%","FY2023","gp23 / sal23","369.8 ÷ 1,420.0",used="waterfall start")
D("gm_pr","2","Gross-margin effect of the higher promotional share","%","FY2023-25","(ps23 - ps25) * plg / 100","(24.0% − 29.0%) × 14 pp",used="waterfall step")
D("gm_sh","2","Gross-margin effect of higher shrink","%","FY2023-25","sh23 - sh25","2.1% − 2.6%",used="waterfall step")
D("gm_pl","2","Gross-margin effect of the higher private-label share","%","FY2023-25","(pls25 - pls23) * plp / 100","(18.5% − 17.0%) × 12 pp",used="waterfall step, title")
D("gm25","2","Gross margin, FY2025","%","FY2025","gp25 / sal25","376.1 ÷ 1,503.0",used="waterfall end")
D("gm_ps","2","Gross margin lost to promotions and shrink","pp","FY2023-25","(ps25 - ps23) * plg + (sh25 - sh23) * 100","5.0 pp × 14 pp + 0.5 pp = 1.2 pp",used="exec summary")
D("pl_off","2","Share of the promotion and shrink loss offset by private label","%","FY2023-25","gm_pl * 100 / gm_ps","0.18 pp ÷ 1.2 pp",used="sidebar")
# ---- 1.3 labor (Table 3)
T3 = "Briefing pack, Table 3 (store labor)"
U("wg23","3","Average hourly wage incl. benefits, FY2023",16.80,"$","FY2023",'Table 3 "Average hourly wage incl. benefits"; column FY2023 = "$16.80"',T3)
U("wg25","3","Average hourly wage incl. benefits, FY2025",18.38,"$","FY2025",'Table 3 "Average hourly wage incl. benefits"; column FY2025 = "$18.38"',T3)
U("hr23","3","Labor hours per $1,000 of sales, FY2023",7.02,"hours","FY2023",'Table 3 "Labor hours per $1,000 of sales"; column FY2023 = "7.02"',T3)
U("hr25","3","Labor hours per $1,000 of sales, FY2025",6.60,"hours","FY2025",'Table 3 "Labor hours per $1,000 of sales"; column FY2025 = "6.60"',T3)
U("k1000","3","Sales unit for labor hours",1000,"$","FY2023-25",'Table 3 "Labor hours per $1,000 of sales"',T3,"unit text")
U("ls23","3","Store labor, % of sales, FY2023",0.118,"%","FY2023",'Table 3 "Store labor, % of sales"; column FY2023 = "11.8%"',T3)
U("ls25","3","Store labor, % of sales, FY2025",0.121,"%","FY2025",'Table 3 "Store labor, % of sales"; column FY2025 = "12.1%"',T3)
D("wgc","3","Change in average hourly wage incl. benefits","%","FY2023-25","wg25 / wg23 - 1","$18.38 ÷ $16.80 − 1",used="KPI tile 1, title")
D("hrc","3","Change in labor hours per $1,000 of sales","%","FY2023-25","hr25 / hr23 - 1","6.60 ÷ 7.02 − 1",used="KPI tile 2, title")
D("lsc","3","Change in store labor as a share of sales","pp","FY2023-25","(ls25 - ls23) * 100","(12.1% − 11.8%) × 100",used="KPI tile 3, title")
D("w_eff","3","Margin effect of the wage rise alone, at FY2023 hours","pp","FY2023-25","hr23 * (wg25 - wg23) / 10","7.02 hours × ($18.38 − $16.80) ÷ $1,000, in pp of sales",used="KPI driver")
D("off","3","Share of the wage effect offset by fewer hours per sales dollar","%","FY2023-25","(hr23 - hr25) * wg25 / 10 / w_eff","(7.02 − 6.60) × $18.38 ÷ $1,000 ÷ wage effect",used="KPI driver, exec summary")
# ---- 2.1 shrink by labor quartile (Table 4)
T4 = "Briefing pack, Table 4 (shrink by store labor intensity, FY2025)"
U("q1","4","Shrink, % of sales, Q1 stores (fewest labor hours per $ sales)",0.031,"%","FY2025",'Table 4 "Q1 (fewest labor hours per $ sales)"; Shrink, % of sales = "3.1%"',T4,"column Q1, title")
U("q2","4","Shrink, % of sales, Q2 stores",0.027,"%","FY2025",'Table 4 "Q2"; Shrink, % of sales = "2.7%"',T4)
U("q3","4","Shrink, % of sales, Q3 stores",0.024,"%","FY2025",'Table 4 "Q3"; Shrink, % of sales = "2.4%"',T4)
U("q4","4","Shrink, % of sales, Q4 stores (most labor hours)",0.023,"%","FY2025",'Table 4 "Q4 (most)"; Shrink, % of sales = "2.3%"',T4,"column Q4, title")
U("sh25b","4","Shrink, % of sales, chain average, FY2025",0.026,"%","FY2025",'Table 2 "Shrink, % of sales"; column FY2025 = "2.6%"',T2,"benchmark line")
U("sw","4","Fresh and produce waste, share of shrink",0.45,"%","FY2025","Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.","Briefing pack, section 6, under Table 4")
U("st","4","Theft, share of shrink",0.35,"%","FY2025","Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.","Briefing pack, section 6, under Table 4")
U("se","4","Administrative and receiving errors, share of shrink",0.20,"%","FY2025","Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.","Briefing pack, section 6, under Table 4")
D("s_task","4","Share of shrink from waste and receiving errors","%","FY2025","sw + se","45% + 20%",used="sidebar bullet")
# ---- e-commerce inputs (Table 5) needed for FY2028 sales
T5 = "Briefing pack, Table 5 (e-commerce operating data)"
U("es23","9","E-commerce share of sales, FY2023",0.03,"%","FY2023",'Table 5 "E-commerce share of sales"; column FY2023 = "3.0%"',T5)
U("es25","9","E-commerce share of sales, FY2025",0.085,"%","FY2025",'Table 5 "E-commerce share of sales"; column FY2025 = "8.5%"',T5)
U("or23","9","E-commerce orders, FY2023, thousands",453,"k","FY2023",'Table 5 "Orders, thousands"; column FY2023 = "453"',T5)
U("or24","9","E-commerce orders, FY2024, thousands",865,"k","FY2024",'Table 5 "Orders, thousands"; column FY2024 = "865"',T5)
U("or25","9","E-commerce orders, FY2025, thousands",1331,"k","FY2025",'Table 5 "Orders, thousands"; column FY2025 = "1,331"',T5)
U("bk25","9","Average e-commerce basket, FY2025",96,"$","FY2025",'Table 5 "Average basket"; column FY2025 = "$96"',T5)
U("ds23","9","Share of orders delivered to the home, FY2023",0.45,"%","FY2023",'Table 5 "Share of orders delivered to the home (rest: click-and-collect)"; column FY2023 = "45%"',T5)
U("ds24","9","Share of orders delivered to the home, FY2024",0.52,"%","FY2024",'Table 5 "Share of orders delivered to the home (rest: click-and-collect)"; column FY2024 = "52%"',T5)
U("ds25","9","Share of orders delivered to the home, FY2025",0.58,"%","FY2025",'Table 5 "Share of orders delivered to the home (rest: click-and-collect)"; column FY2025 = "58%"',T5)
U("pc23","9","Picking cost per order, FY2023",7.20,"$","FY2023",'Table 5 "Picking cost per order (all orders)"; column FY2023 = "$7.20"',T5)
U("pc24","9","Picking cost per order, FY2024",7.30,"$","FY2024",'Table 5 "Picking cost per order (all orders)"; column FY2024 = "$7.30"',T5)
U("pc25","9","Picking cost per order, FY2025",7.40,"$","FY2025",'Table 5 "Picking cost per order (all orders)"; column FY2025 = "$7.40"',T5)
U("dc23","9","Third-party delivery cost per delivered order, FY2023",12.90,"$","FY2023",'Table 5 "Third-party delivery cost per delivered order"; column FY2023 = "$12.90"',T5)
U("dc24","9","Third-party delivery cost per delivered order, FY2024",13.40,"$","FY2024",'Table 5 "Third-party delivery cost per delivered order"; column FY2024 = "$13.40"',T5)
U("dc25","9","Third-party delivery cost per delivered order, FY2025",13.80,"$","FY2025",'Table 5 "Third-party delivery cost per delivered order"; column FY2025 = "$13.80"',T5)
U("df23","9","Average delivery fee collected per delivered order, FY2023",3.40,"$","FY2023",'Table 5 "Average delivery fee collected per delivered order"; column FY2023 = "$3.40"',T5)
U("df24","9","Average delivery fee collected per delivered order, FY2024",3.20,"$","FY2024",'Table 5 "Average delivery fee collected per delivered order"; column FY2024 = "$3.20"',T5)
U("df25","9","Average delivery fee collected per delivered order, FY2025",3.10,"$","FY2025",'Table 5 "Average delivery fee collected per delivered order"; column FY2025 = "$3.10"',T5)
U("thr","9","Order value above which delivery is free",75,"$","FY2025","Delivery is free above $75 (a $4.99 fee below). Click-and-collect is free.","Briefing pack, section 7, under Table 5")
U("sv70","10","Share of online purchases customers would otherwise have bought in a Harlow store",0.70,"%","FY2025","Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.","Briefing pack, section 7")
U("n23","10","E-commerce customer survey sample",2300,"respondents","FY2025","Survey of 2,300 e-commerce customers (FY2025)","Briefing pack, section 7")
U("cpn","10","Contribution per dollar of sales new to Harlow, before e-commerce fulfillment",0.20,"%","FY2025","Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.","Briefing pack, section 7")
U("tm61","10","E-commerce contribution margin reported by the e-commerce team",0.061,"%","FY2025",'"E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025."',"Briefing pack, section 10, e-commerce team update")
U("ft_do","11","Fee test: change in delivered orders",-0.09,"%","late FY2025, 10 weeks","Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the average fee collected per delivered order rose to $6.40.","Briefing pack, section 7, fee test")
U("ft_cc","11","Fee test: change in click-and-collect orders",0.14,"%","late FY2025, 10 weeks","Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%","Briefing pack, section 7, fee test")
U("ft_s","11","Fee test: change in total e-commerce sales",-0.02,"%","late FY2025, 10 weeks","total e-commerce sales fell 2%","Briefing pack, section 7, fee test")
U("ft_fee","11","Fee test: average fee collected per delivered order",6.40,"$","late FY2025, 10 weeks","the average fee collected per delivered order rose to $6.40","Briefing pack, section 7, fee test")
U("ft_new","11","Fee test: delivery fee",7.99,"$","late FY2025","delivery fee raised to $7.99 and the free-delivery threshold to $100","Briefing pack, section 7, fee test")
U("ft_thr","11","Fee test: free-delivery threshold",100,"$","late FY2025","delivery fee raised to $7.99 and the free-delivery threshold to $100","Briefing pack, section 7, fee test")
U("ft_st","11","Fee test: stores in the test",4,"stores","late FY2025","Fee test (4 stores, 10 weeks, late FY2025)","Briefing pack, section 7, fee test")
D("ecs25","10","E-commerce sales, FY2025","$M","FY2025","es25 * sal25","8.5% × $1,503.0M",used="equation term")
# ---- store portfolio (Table 6)
T6 = "Briefing pack, Table 6 (the nine weakest stores, FY2025)"
U("ws_n","12","Stores with negative four-wall EBITDA",9,"stores","FY2025",'Table 6 "Stores with negative four-wall EBITDA" = "9 of 58"',T6)
U("ws_s","12","Combined sales of the nine weakest stores",118.0,"$M","FY2025",'Table 6 "Their combined sales" = "$118.0M"',T6)
U("ws_e","12","Combined four-wall EBITDA of the nine weakest stores",-3.1,"$M","FY2025",'Table 6 "Their combined four-wall EBITDA" = "−$3.1M"',T6)
U("ws_l","12","Weak stores with leases expiring by end of 2027",6,"stores","by end of 2027",'Table 6 "Leases expiring by end of 2027" = "6 of the 9"',T6)
U("ws_x","12","Estimated lease-exit cost for the other three stores (one-time)",7.5,"$M","one-time",'Table 6 "Estimated lease-exit cost for the other 3" = "$7.5M (one-time)"',T6)
U("ws_t","12","Share of a closed store's sales expected to move to a nearby Harlow store",0.25,"%","past closures",'Table 6 "Share of their sales expected to move to a nearby Harlow store if closed (past closures)" = "25%"',T6)
U("ws_c","12","Contribution on sales moved to a receiving store",0.12,"%","past closures",'Table 6 "Contribution on sales moved to a receiving store" = "12%"',T6)
D("ws_o","12","Weak stores whose leases run beyond 2027","stores","FY2025","ws_n - ws_l","9 − 6",used="assumptions")
A_S28 = ["FY2028 sales start from FY2025's $1,503.0M with no market growth or inflation",
         "The nine weakest stores close; 25% of their $118.0M of sales moves to nearby Harlow stores, as in past closures",
         "The tested delivery fee lowers e-commerce sales by 2%, as in the four-store test"]
D("sales28","4","Harlow sales, FY2028, after the store exits and the delivery fee change","$M","FY2028E",
  "sal25 - ws_s * (1 - ws_t) - ecs25 * (0 - ft_s)","$1,503.0M − $118.0M × (1 − 25%) − $127.8M × 2%",True,A_S28,"sidebar row basis, equation term, basis strip")
# ---- 2.1 shrink lever
A_SHR = ["The chain average falls from 2.6% to the 2.3% that the best-staffed quartile of stores achieves today",
         "The gain comes from produce rotation and receiving checks, which drive waste (45% of shrink) and errors (20%)",
         "Hours for these tasks are redeployed within today's store labor budget, not added",
         "Sized on FY2028 sales after the store exits"]
D("shr_gain","4","Gain if chain shrink falls to the best-staffed quartile's level","$M","FY2028E run-rate",
  "(sh25b - q4) * sales28","(2.6% − 2.3%) × $1,412M",True,A_SHR,"sidebar row")
# ---- 2.2 labor cut
U("cut","5","Management's estimated saving from cutting scheduled store labor hours by 8%",14.5,"$M","FY2026, a year",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)","Briefing pack, section 4 (management's current view)","equation term, title")
U("hc","5","Planned cut in scheduled store labor hours",0.08,"%","FY2026","cut scheduled store labor hours by 8% in FY2026","Briefing pack, section 4")
A_LEAK = ["All of the FY2023–25 rise in shrink (2.1% to 2.6% of sales) is attributed to the 6.0% fall in hours per $1,000 of sales",
          "Shrink responds in proportion to hours: an 8% cut adds 8/6 of that rise, about 0.67 percentage points of sales",
          "If only waste and receiving errors (65% of shrink) respond to hours, the loss is about $6.5M",
          "Effects on checkout waits and stock-outs are not counted"]
D("leak","5","Shrink cost of an 8% cut in store labor hours, upper case","$M","FY2026E, a year",
  "(sh25 - sh23) / (0 - hrc) * hc * sal25","0.5 pp ÷ 6.0% × 8% × $1,503.0M",True,A_LEAK,"equation term, title")
D("leaklo","5","Shrink cost of an 8% hour cut if only waste and errors respond","$M","FY2026E, a year",
  "leak * s_task","$10.0M × 65%",True,A_LEAK,"assumption text")
D("cutnet","5","Net saving from the 8% hour cut after higher shrink","$M","FY2026E, a year","cut - leak","$14.5M − $10.0M",True,A_LEAK,"equation result")
U("tgt","5","Operating margin target, FY2028",0.03,"%","FY2028","operating margin back to at least 3.0% by FY2028.","Briefing pack, section 3 (objectives)","so-what bar")
D("mg_mgmt","5","FY2028 operating margin under the labor-cut plan, with no shrink leak","%","FY2028E",
  "(oi25 + cut) / sal25","($15.3M + $14.5M) ÷ $1,503.0M",True,
  ["The full $14.5M saving is kept, with no rise in shrink","Sales stay at FY2025's $1,503.0M","E-commerce is frozen at its current size and loss"],"so-what bar, comparison table")
# ---- 3.1 promotions vs price image
U("me23","6","Customers who say Harlow is more expensive than other options, FY2023",0.33,"%","FY2023",'Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%)',"Briefing pack, section 9")
U("me25","6","Customers who say Harlow is more expensive than other options, FY2025",0.41,"%","FY2025",'Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%)',"Briefing pack, section 9; latest survey, read as FY2025","column, title")
U("n31","6","Customer survey sample",3100,"respondents","FY2025","Customer survey (n = 3,100)","Briefing pack, section 9")
D("psd","6","Rise in promotional share of sales","pp","FY2023-25","(ps25 - ps23) * 100","(29.0% − 24.0%) × 100",used="panel delta, equation term")
D("med","6","Rise in customers saying Harlow is more expensive","pp","FY2023-25","(me25 - me23) * 100","(41% − 33%) × 100",used="panel delta")
U("pe38","6","FY2025 promotional events that lost money after counting the extra units sold",0.38,"%","FY2025","A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.","Briefing pack, section 5")
U("cs18","6","Comparable sales growth, stores with the deepest promotions",0.018,"%","FY2025",'"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work."',"Briefing pack, section 10, category team")
U("cs02","6","Comparable sales growth, other stores",0.002,"%","FY2025",'grew comparable sales 1.8%, against 0.2% for the rest',"Briefing pack, section 10, category team")
# ---- 3.2 ValuMart and reasons to shop
U("vm_n","7","ValuMart stores opened in Harlow trade areas since 2023",11,"stores","since 2023","A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.","Briefing pack, section 9")
U("vm_in","7","Comparable sales, Harlow stores within three miles of a new ValuMart",-0.042,"%","FY2025","Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.","Briefing pack, section 9","column, title")
U("vm_out","7","Comparable sales, other Harlow stores",0.011,"%","FY2025","against +1.1% for other Harlow stores","Briefing pack, section 9","column")
U("rs_f","7","Customers naming fresh produce as a top reason to shop Harlow",0.58,"%","FY2025","top reasons to shop Harlow are fresh produce (58%) and convenience (44%)","Briefing pack, section 9 (customer survey, n = 3,100)","bar, exec summary")
U("rs_c","7","Customers naming convenience as a top reason to shop Harlow",0.44,"%","FY2025","top reasons to shop Harlow are fresh produce (58%) and convenience (44%)","Briefing pack, section 9 (customer survey, n = 3,100)","bar, exec summary")
# ---- 3.3 promotion lever
A_PR = ["Cuts start with the 38% of FY2025 events that lost money even after counting extra units, so lost volume does not erode the gain",
        "Sales leaving promotion are bought at regular price, earning the 14 percentage points of margin promotions give up",
        "Vendor funding, down from 55% to 46% of markdowns, is not counted; recovering it is upside",
        "Sized on FY2028 sales after the store exits"]
D("promo_gain","8","Gain from returning promotional share to the FY2023 level of 24%","$M","FY2028E run-rate",
  "psd / 100 * plg / 100 * sales28","5.0 pp × 14 pp × $1,412M",True,A_PR,"equation result, title")
D("pcut","8","Share of promotional sales removed to return to 24%","%","FY2028E","psd / 100 / ps25","5.0 pp ÷ 29.0%",used="assumption text")
# ---- 4.1 fulfillment cost split
for y in ("23","24","25"):
    D(f"pk{y}","9",f"Picking cost, FY20{y}","$M",f"FY20{y}",f"or{y} * pc{y} / 1000",f"orders × picking cost per order",used=f"stacked column FY20{y}: picking")
    D(f"nd{y}","9",f"Delivery cost net of fees, FY20{y}","$M",f"FY20{y}",f"or{y} * ds{y} * (dc{y} - df{y}) / 1000",f"orders × delivered share × (delivery cost − fee)",used=f"stacked column FY20{y}: net delivery")
D("ecm","9","Growth multiple of e-commerce fulfillment cost","x","FY2023-25","(pk25 + nd25) / (pk23 + nd23)","($9.8M + $8.3M) ÷ ($3.3M + $1.9M)",used="title")
D("ndm","9","Growth multiple of net delivery cost","x","FY2023-25","nd25 / nd23","$8.3M ÷ $1.9M",used="title, sidebar")
D("orm","9","Growth multiple of e-commerce orders","x","FY2023-25","or25 / or23","1,331k ÷ 453k",used="sidebar")
D("dloss","9","Loss per delivered order before picking","$","FY2025","dc25 - df25","$13.80 − $3.10",used="sidebar")
# ---- 4.2 true e-commerce economics
D("nsh","10","Share of online sales new to Harlow","%","FY2025","1 - sv70","100% − 70%",used="equation term")
D("fee25","10","Delivery fees collected, FY2025","$M","FY2025","or25 * ds25 * df25 / 1000","1,331k × 58% × $3.10",used="assumption text")
D("ecp","10","E-commerce profit after cannibalization and full fulfillment cost","$M","FY2025","ecs25 * nsh * cpn - ecf25",
  "$127.8M × 30% × 20% − $18.1M",used="equation result, title")
D("ecpm","10","E-commerce profit as a share of e-commerce sales","%","FY2025","ecp / ecs25","−$10.4M ÷ $127.8M",used="assumption text")
# ---- 4.3 fee test rollout
A_FEE = ["The four-store test results hold chain-wide: delivered orders −9%, click-and-collect orders +14%, average fee per delivered order $6.40",
         "Picking ($7.40) and carrier cost ($13.80) per order stay at FY2025 levels; the proposed 3% carrier rise is treated as a risk",
         "The 2% of e-commerce sales lost would have earned 20 cents per new dollar on the 30% that is new to Harlow"]
D("dto","11","Delivered orders at test terms, thousands","k","FY2028E run-rate","or25 * ds25 * (1 + ft_do)","1,331k × 58% × (1 − 9%)",True,A_FEE,"basis caption")
D("cco","11","Click-and-collect orders at test terms, thousands","k","FY2028E run-rate","or25 * (1 - ds25) * (1 + ft_cc)","1,331k × 42% × (1 + 14%)",True,A_FEE,"basis caption")
D("ecf_t","11","E-commerce fulfillment cost at test terms","$M","FY2028E run-rate",
  "(dto + cco) * pc25 / 1000 + dto * (dc25 - ft_fee) / 1000",
  "(703k delivered + 637k collected orders) × $7.40 + 702k × ($13.80 − $6.40)",True,A_FEE,"basis term")
D("fee_lost","11","Contribution lost on e-commerce sales that the fee change removes","$M","FY2028E run-rate",
  "ecs25 * (0 - ft_s) * nsh * cpn","$127.8M × 2% × 30% × 20%",True,A_FEE,"basis term")
D("fee_gain","11","Gain from rolling out the tested delivery fee","$M","FY2028E run-rate","ecf25 - ecf_t - fee_lost",
  "$18.1M − $15.1M − $0.2M",True,A_FEE,"basis result, title")
# ---- 4.4 store exits
A_ST = ["Six of the nine leases expire by the end of 2027, so those stores close without a board vote",
        "The other three need a board vote and an estimated $7.5M one-time lease-exit cost",
        "25% of the nine stores' sales moves to a nearby Harlow store, as in past closures, earning 12% contribution there",
        "Four-wall EBITDA excludes depreciation, so the operating-income gain is, if anything, larger"]
D("ws_rm","12","Four-wall EBITDA losses removed by exiting the nine stores","$M","FY2028E run-rate","0 - ws_e","−(−$3.1M)",used="equation term")
D("ws_gain","12","Gain from exiting the nine loss-making stores","$M","FY2028E run-rate","ws_rm + ws_s * ws_t * ws_c",
  "$3.1M + $118.0M × 25% × 12%",True,A_ST,"equation result, title")
D("ef_gain","12","Gain from the delivery fee and the store exits together","$M","FY2028E run-rate","fee_gain + ws_gain","$2.8M + $6.6M",True,A_ST+A_FEE,"exec summary")
# ---- private label lever (shown on slide 2 sidebar)
A_PL = ["Private label keeps its FY2023–25 pace of 0.75 percentage points of share a year for three more years, to about 20.75% of sales",
        "The 12-percentage-point margin premium over national brands holds",
        "Sized on FY2028 sales after the store exits"]
D("pl_add","2","Private-label share added by FY2028 at the FY2023-25 pace","pp","FY2025-28E","(pls25 - pls23) / 2 * 3 * 100","1.5 pp ÷ 2 years × 3 years",True,A_PL,"sidebar row basis")
D("pl_gain","2","Gain from private label keeping its FY2023-25 pace to FY2028","$M","FY2028E run-rate","gm_pl / 2 * 3 * sales28",
  "0.18 pp of margin per two years × 3 years × $1,412M",True,A_PL,"sidebar row")
# ---- 5.1 plan bridge
A_PLAN = ["Each action is sized on the earlier pages; the five gains add up without overlap",
          "FY2028 sales of about $1,412M after the store exits and the delivery fee change; no market growth",
          "The 2027 minimum-wage rise and the proposed carrier rate rise are not included (risks, last page)"]
D("act","13","Run-rate gain from the five actions","$M","FY2028E","promo_gain + ws_gain + shr_gain + pl_gain + fee_gain",
  "$9.9M + $6.6M + $4.2M + $3.8M + $2.8M",True,A_PLAN,"basis term")
D("oi28","13","Operating income, FY2028, with the five actions","$M","FY2028E","oi25 + act","$15.3M + $27.4M",True,A_PLAN,"basis term")
D("m28","13","Operating margin, FY2028, with the five actions","%","FY2028E","oi28 / sales28","$42.7M ÷ $1,412M",True,A_PLAN,"waterfall end, title")
D("b_base","13","Margin effect of the smaller sales base","%","FY2028E","oi25 / sales28 - oi25 / sal25","$15.3M ÷ $1,412M − $15.3M ÷ $1,503M",True,A_PLAN,"waterfall step")
for k,lab in (("promo","Promotions back to 24% of sales"),("ws","Exit of the nine loss-making stores"),("shr","Shrink down to 2.3% of sales"),("pl","Private label at its FY2023-25 pace"),("fee","Tested delivery fee rolled out")):
    D(f"b_{k}","13",f"Margin effect: {lab}","%","FY2028E",f"{k}_gain / sales28",f"gain ÷ FY2028 sales",True,A_PLAN,"waterfall step")
U("cap","13","Plan budget for one-time cost or capital, FY2026-28",25,"$M","FY2026-28","at most $25M of one-time cost or capital for the plan over FY2026–FY2028.","Briefing pack, section 3 (objectives)","sidebar")
# ---- 5.3 FY2026 covenant
U("cov","15","Minimum operating income under the lender covenant, FY2026",20,"$M","FY2026","a covenant requires operating income of at least $20M in FY2026.","Briefing pack, section 3 (objectives)","basis caption")
A_26 = ["The tested delivery fee runs for about 75% of FY2026 (rolled out within the first quarter)",
        "Promotion cuts deliver half their run-rate in FY2026, as event calendars are reset",
        "Shrink and private label deliver a third of their run-rate; store exits add nothing before leases expire",
        "FY2026 is treated as the first plan year, as in management's draft; no wage or carrier rise in FY2026"]
D("fee26","15","Delivery fee gain in FY2026","$M","FY2026E","fee_gain * 0.75","$2.8M × 75%",True,A_26,"basis term")
D("promo26","15","Promotion gain in FY2026","$M","FY2026E","promo_gain * 0.5","$9.9M × 50%",True,A_26,"basis term")
D("oth26","15","Shrink and private-label gain in FY2026","$M","FY2026E","(shr_gain + pl_gain) / 3","($4.2M + $3.8M) ÷ 3",True,A_26,"basis term")
D("fy26","15","Operating income, FY2026, with first-wave actions","$M","FY2026E","oi25 + fee26 + promo26 + oth26","$15.3M + $2.1M + $4.9M + $2.7M",True,A_26,"basis result, title")
D("mg26","14","FY2026 operating income under the labor-cut plan, before shrink effects","$M","FY2026E","oi25 + cut","$15.3M + $14.5M",True,
  ["The full $14.5M saving is kept in FY2026","Everything else stays at FY2025 levels"],"comparison table")
D("mg26s","14","FY2026 operating income under the labor-cut plan, if shrink rises as in FY2023-25","$M","FY2026E","oi25 + cut - leak","$15.3M + $14.5M − $10.0M",True,A_LEAK,"comparison table")
# ---- 5.4 risks
U("mw","16","State minimum wage rise in 2027",0.04,"%","2027","Wage rates: the state minimum wage rises again in 2027 (+4%).","Briefing pack, section 11 (uncertainties)")
U("dr3","16","Delivery provider's proposed rate rise",0.03,"%","2026 renewal","Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).","Briefing pack, section 11 (uncertainties)")
A_W = ["Upper bound: every store wage rises 4%, not only those at the minimum","Applied to FY2025 store labor of $181.9M, before any productivity offset"]
D("wr","16","Cost of the 2027 minimum-wage rise, upper bound","$M","FY2027E, a year","lab25 * mw","$181.9M × 4%",True,A_W,"table cell, title")
D("m28w","16","FY2028 operating margin if the wage rise is not offset","%","FY2028E","(oi28 - wr) / sales28","($42.7M − $7.3M) ÷ $1,412M",True,A_W+A_PLAN,"callout")
D("drr","16","Cost of the proposed 3% carrier rate rise at test volumes","$M","FY2026E, a year","or25 * ds25 * (1 + ft_do) * dc25 * dr3 / 1000","703k delivered orders × $13.80 × 3%",True,
  ["Delivered orders at test levels (−9%)","Carrier cost of $13.80 per delivered order rises 3%"],"table cell")
D("trs","16","Gain lost for every 10 percentage points less sales transfer after store exits","$M","FY2028E","ws_s * 0.1 * ws_c","$118.0M × 10 pp × 12%",True,
  ["Each 10 percentage points of the nine stores' sales that does not move to another Harlow store loses 12% contribution"],"table cell")
