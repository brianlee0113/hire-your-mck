"""Generate independent holdout c6–c11 packets and evaluator-only answer keys.
Does not touch existing c1–c5 packets/keys. Outputs are deterministic.
Run from repository root: python benchmark/cases/build_holdout_cases.py
"""
from __future__ import annotations
import json
from pathlib import Path
from holdout_models import MODELS

BASE=Path(__file__).resolve().parent
KEYS=BASE.parent/'answer_keys'
BANNER=('> **Synthetic benchmark data.** Every company, person, quotation, and number below is fictional. '
        'Numbers are constructed for an analytical benchmark, not public market data.\n')

def table(headers, rows):
    return '\n'.join(['| '+' | '.join(map(str,headers))+' |','|'+ '|'.join('---' for _ in headers)+'|']+
                     ['| '+' | '.join(str(c) for c in row)+' |' for row in rows])

def money(v):return f'${v:,.2f}M'
def pct(v):return f'{v*100:.1f}%'
def key(case, title, q, holder, hypothesis, handling, why, insights, calcs, evidence, contradictions, traps, tradeoffs, recs, criteria, reqs):
    return dict(case_id=case,title=title,decision_question=q,
        initial_hypothesis=dict(holder=holder,statement=hypothesis,expected_handling=handling,explanation=why),
        key_insights=[dict(id=f'K{i}',critical=crit,text=t) for i,(crit,t) in enumerate(insights,1)],
        required_calculations=[dict(id=f'Q{i}',text=t,expected=str(v),tolerance=tol) for i,(t,v,tol) in enumerate(calcs,1)],
        decision_relevant_evidence=[dict(id=f'E{i}',critical=crit,text=t) for i,(crit,t) in enumerate(evidence,1)],
        contradictory_evidence=contradictions,
        reasoning_traps=[dict(id=f'T{i}',text=t) for i,t in enumerate(traps,1)],
        key_tradeoffs=[dict(id=f'X{i}',text=t) for i,t in enumerate(tradeoffs,1)],
        plausible_recommendations=[dict(id=f'R{i}',defensible=d,text=t) for i,(d,t) in enumerate(recs,1)],
        defensibility_criteria=criteria,
        decision_requirements=[dict(id=f'D{i}',question=q,critical=crit,acceptable_evidence=ev,unnecessary_if=exc)
           for i,(q,crit,ev,exc) in enumerate(reqs,1)])

def c6(d):
    q='Should Meridian Motion manufacture precision housings in-house in 2027, lease a flexible cell, or continue buying from an external supplier?'
    packet=f'''# Meridian Motion — make-or-buy a precision housing (c6)

{BANNER}
## 1. Situation and the decision
Meridian Motion makes industrial condition-monitoring sensors for North American water utilities and manufacturers. Its aluminum housing is designed in-house but machined by an external supplier. A customer audit found two late shipments last quarter; management is concerned that relying on one machine shop could constrain a new sensor range. Revenue from the sensors is growing, but the company has never operated a production machining cell. The executive committee will decide in January 2027. The VP of Operations wants to build an owned cell immediately, saying that a $46 variable cost is obviously cheaper than the $75 outside purchase price.

**Decision:** {q} The CEO also wants an executable contingency if a supplier outage interrupts deliveries. A manufacturing engineer says a leased, staffed cell could be installed more quickly, but its economics must be tested rather than assumed. The customer does not mandate insourcing; it mandates delivery reliability and dimensional quality.

## 2. Constraints agreed by the board
- At most **$5.0M of new 2027 capital spending** can be approved without a new financing agreement. Separately, year-end unrestricted cash must remain above **$4.0M**. Today's available cash is **$9.2M** and no debt or equity increase is approved.
- Housing demand planning assumes 80,000 good units in 2027, 100,000 in 2028 and 120,000 in 2029. The major customer's forecast is not a guaranteed order; the conservative 2028 case is 65,000 units.
- A customer delivery contract requires 97% of requested units to ship within ten business days. Losing the designation would also affect sales of electronics and software; that indirect loss has not been quantified.
- Quality must be measured on good, accepted units, not units started. No design change can be made until customer dimensional testing is completed. The supplier can provide 40,000 reserved units after giving ninety days' notice.

## 3. Economics and quotations
{table(['Cost or assumption','Supplier purchase','Own machining cell','Flexible leased cell'],[
('Quoted unit cost','$73 at supplier gate','$46 per unit started','$49 per unit started'),
('Freight and inbound QA','$2 per good unit','included in variable cost','included in variable cost'),
('Initial investment','None; optional alternate-shop tooling $0.25M','$6.5M equipment + $0.8M installation','$2.0M installation and training'),
('Recurring fixed cost','none beyond quoted price','$0.75M per year','$1.60M annual lease and staffing'),
('First-year scrap','supplier price covers rejects','8% of starts','6% of starts'),
('Later-year scrap','supplier price covers rejects','4% of starts','4% of starts'),
('Practical annual output','up to 140,000 if renewed','120,000 accepted units','125,000 accepted units'),
])}

The owned cell's $46 excludes scrap, annual fixed staffing and depreciation or financing effects. Build equipment could be sold for an estimated $2.1M after 2029, but a dealer's indication is not a binding offer. The leased option can be terminated after 2029 without residual value; the landlord's proposal is subject to due diligence on power and ventilation. The current supplier quote lasts until March 2027 and assumes the existing housing specification. The supplier is willing to split quarterly orders and would charge an extra $0.25M for dedicated tooling at Meridian's alternate approved shop.

## 4. Operating volume and reliability
{table(['Scenario','2027 good units','2028 good units','2029 good units'],[
('Planning forecast','80,000','100,000','120,000'),
('Conservative demand','80,000','65,000','85,000'),
('Supplier disruption case','80,000','100,000','120,000'),
])}

An internal dashboard reports **98.5% production yield** for the demonstration cell. Operations argues this validates its cost model. The measure excludes start-up runs, rework and three days when the cell was down for a tooling change; including those effects, the process engineer's first-year plan uses 8% scrap. The demo used the same material but did not run the new sensor housing at full production speed. The supplier has delivered 96.8% of orders within ten business days, slightly below the customer requirement, but late deliveries were concentrated during one flood-related road closure. A second approved supplier is available for emergency orders at $88 per accepted unit with six-week notice.

The sales director points out that plants with an internal machine shop recorded fewer delivery delays last year. Those plants also shipped larger, steadier volumes and operated different products. No comparable before-and-after evidence isolates the effect of insourcing. The board should not assume a relationship between ownership of machinery and customer satisfaction is causal.

## 5. Internal presentation circulated to management
The CFO circulated a slide saying "Buying at $73 versus making at $46 saves $27 on every housing; at 100,000 units the payback is under three years." The slide compared a supplier **factory-gate price** with an internal **variable cost per started unit**, while the supplier contract pays only for accepted units. The CFO has not included the 8% first-year scrap, $750,000 annual fixed cost, upfront installation or cash floor. A separate procurement chart labels the supplier's freight-inclusive price as $75; it is not a second quote.

The VP of Operations thinks buying capacity early also reduces lead-time risk for 2029, but the head of Finance notes that new equipment orders take nine months and that no customer guarantees the forecast volumes. The lease company promises a five-month deployment if its site survey passes. The CEO is open to contractually reserved capacity, a lease, or a phased capital request rather than an all-or-nothing build.

## 6. Data limitations and open choices
The supplier's capacity and pricing beyond 2027 are indicative; there is no take-or-pay commitment for 2028–29. A one-week outage at the primary supplier may be handled using emergency inventory, but the inventory carrying cost is not yet modelled. The equipment's resale value, production scrap rate at scale, and actual steady-state demand have material uncertainty. Costs and volumes in the table are nominal and omit tax and financing; compare options consistently before introducing a financing model. The CEO wants the option recommendation, its cash implications, the operational gate that would change the answer, and actions to protect the delivery requirement.
'''
    k=key('c6','Meridian Motion — make or buy',q,'VP of Operations',
      'Buy an owned machining cell in 2027 because $46 of internal variable cost is below the supplier quote.',
      'reject','The proposed owned cell breaches the 2027 capex cap and cash floor, while including scrap and fixed costs removes most apparent variable-cost savings; a reversible supply/lease path is viable.',
      [(True,f'Owned cell requires $7.30M upfront, above $5.00M capex cap and leaves only $1.90M cash versus $4.00M floor.'),
       (True,f'2028 supplier cost $7.50M, owned cell operating cost {money(d["build_op"][1])} before recovery of capex; three-year owned total {money(d["build_total"])} versus supplier {money(d["outsourcing_total"])}.'),
       (True,'The $46 vs $73 comparison mixes cost per started unit and factory-gate price; correct supplier cost is $75 per accepted delivered unit.'),
       (True,'The 98.5% internal yield excludes start-up, rework and downtime; use 8% first-year and 4% subsequent scrap scenarios.'),
       (False,f'Leased-cell three-year total including setup is {money(d["lease_total"])} on plan volumes, but its forecast has capacity, contract and downtime risk.'),
       (False,'Supplier reliability is 96.8% against a 97% requirement; reserve capacity and build contingency rather than treat make-or-buy as only a cost choice.')],
      [('Own cell 2027 cash after up-front spending',f'{money(d["build_cash_post"])} vs $4.00M floor','±$0.05M'),
       ('Supplier full delivered unit price','$73 + $2 = $75 per accepted unit','exact'),
       ('2028 own-cell good-unit manufacturing cost',f'$46 / (1-4%) = ${d["build_unit"][1]:.2f} plus $0.75M fixed','±$0.10/unit'),
       ('2027–29 comparable cumulative cost',f'outsource {money(d["outsourcing_total"])}; own cell {money(d["build_total"])}; lease {money(d["lease_total"])}','±$0.15M')],
      [(True,'Five-million capex cap and four-million liquidity floor'),(True,'Scrap, fixed costs and start-up time'),(True,'Accepted-unit vs started-unit and freight definitions'),(False,'Supplier reliability and reserved 40,000-unit option')],
      ['Demonstration yield vs full-production yield','Cheap internal variable cost vs full ownership cost','Owned plants have fewer delays but different scale and demand patterns'],
      ['Taking 98.5% demo yield as the first-year production rate','Comparing $46 per started unit with $73 factory-gate buying cost','Ignoring the capex cap or minimum liquidity','Treating cross-plant delay correlation as proof of insourcing causality'],
      ['Cost vs delivery continuity','Capital irreversibility vs forecast uncertainty','Supplier concentration vs new operating capability'],
      [('yes','Keep outsourcing with reserved second-source capacity and time-boxed lease feasibility, with volume and service gates.'),('conditional','Install a flexible leased cell if independently validated reliability, site readiness and throughput justify the setup and annual fixed charge.'),('no','Approve the $7.3M owned cell now under the present board constraints.')],
      ['Compare accepted-unit fully loaded economics and cash constraints','Address contract service reliability and contingent capacity','Distinguish factory-gate and delivered costs, demo and real yields','State evidence needed before any irrevocable build'],
      [('Does each option satisfy capital and minimum cash?',True,['cash bridge','capital schedule'],None),('Were yields, costs and units normalized?',True,['per-good-unit calculation','cost table'],None),('Is delivery reliability protected?',True,['capacity and contingency plan','contract gate'],None),('Are build/lease decisions gated on true demand?',False,['threshold','pilot decision rule'],'if only outsourcing is recommended with an explicit reassessment')])
    return packet,k

def c7(d):
    q='Should Atlas FieldOps buy the scheduling software company RouteSprout in 2027, and on what terms, rather than build or partner?'
    packet=f'''# Atlas FieldOps — acquisition or partnership (c7)

{BANNER}
## 1. CEO decision
Atlas FieldOps supplies field-service management software to utilities and repair contractors. Its core product is sticky but implementation-intensive, and several enterprise prospects have asked for automatic technician routing. RouteSprout is a smaller scheduling vendor whose founders want to sell their company. Atlas's CEO has proposed buying it for $18.0M cash, integrating the teams in six months, and adding $2.4M in cross-sell annual recurring revenue by the end of 2028. The board wants an answer at the March 2027 meeting. Existing shareholders do not plan a financing round in 2027.

**Question:** {q} The choice is not between acquiring technology and ignoring the customer need. A commercial partnership or an internal build is available, and the transaction's timing and consideration are negotiable. The board expects a defensible recommendation that respects customer renewal cycles as well as balance-sheet limits.

## 2. Hard constraints and commercial objectives
- Atlas has **$24.0M unrestricted cash** and a board floor of **$9.0M** at all times, so initial cash expenditure cannot exceed **$15.0M**. Current software operations are approximately cash-break-even before major initiatives; do not assume an external financing facility.
- Systems migration and customer support must stay under **$4.0M of one-time integration expenditure** through 2028. Large customers require at least 99.7% uptime. A missed quarterly uptime target creates service credits and renewal risk that are not included in the sellers' presentation.
- The company may pursue only one major routing strategy in 2027. Its own engineers need at least eighteen months for a basic routing product; a partner could deliver a limited offering this summer.
- The board values both strategic fit and a path to positive incremental contribution. A transaction that uses the cash reserve is unacceptable even if accounting EBITDA later improves.

## 3. Target and valuation evidence
{table(['Indicator','RouteSprout FY2026','Notes'],[
('ARR','$4.8M','42% year-on-year growth before the last quarter'),
('Gross margin','80%','Software gross margin before customer-success overhead'),
('Annual EBITDA','−$1.0M','Includes founders salaries'),
('Annual customer logo churn','21%','Up from 12% in FY2024'),
('Customer accounts','310','58% of ARR from 41 accounts'),
('Acquisition price','$18.0M all cash','Not including integration'),
('Integration estimate','$4.0M','Six months; 30% of work not yet scoped'),
('Potential cross-sell ARR','$2.4M by 2028','Sales VP base case; not signed'),
])}

The sellers call the deal "2.5 times recurring revenue" by dividing the $18M headline valuation by annual **bookings of $7.2M**. The buyer's corporate finance team uses recognized ARR of $4.8M, not bookings, for recurring revenue valuation. The sellers also count one-year pilots in bookings without adjusting for their non-renewable nature. No independent quality-of-earnings review has yet been completed.

## 4. Integration paths
{table(['Path','Initial cash','Operating consequences'],[
('A · Full cash acquisition','$18.0M price + $4.0M integration','RouteSprout product brought into Atlas; target losses continue until synergies materialize'),
('B · Staged acquisition','$11.0M upfront + $3.5M integration','Up to $7.0M additional earnout in 2029 if renewal and integration targets met'),
('C · Commercial partnership','$1.2M two-year minimum','Nonexclusive routing API; gross profit split 55% to Atlas, 45% to RouteSprout'),
('D · Internal build','$3.4M through 2028','Launch no earlier than late 2028, ongoing maintenance $0.4M/year'),
])}

The founder selling team says integration has worked in other software acquisitions when the product is put under one general manager. The cited companies were, on average, twice as large and had lower churn than RouteSprout; the slide contains an apparent correlation between integration spend and cross-sell performance but provides no causal identification. The Atlas product VP worries that replacing RouteSprout's interface before its large customers renew could increase churn.

## 5. Synergy and customer analysis
The Sales VP lists $2.4M of potential annual cross-sell ARR. The finance team says an explicit low case of **$0.8M** is plausible if the 21% churn persists and only signed customer trials convert. Incremental gross margin on new cross-sell subscriptions is **80%**, while another **$0.85M/year** of integration-era customer success and support will be needed. No additional cost savings should be assumed without evidence. The seller's pitch counts the full $2.4M as EBITDA improvement and assumes 100% renewal of the existing 310 accounts. Customer success interviews found that account managers, not routing features alone, drive renewal decisions.

Atlas's internal-build estimate is $3.4M over two years. The product could generate **$1.3M of 2028 ARR** if it launches on time, at 80% incremental gross margin, but it would add about **$0.4M of annual operations** thereafter. The product head says the engineering effort would displace one planned compliance upgrade; delays could have a customer cost not yet estimated. The partnership is faster but requires sharing roadmap details with a firm Atlas might later acquire.

## 6. Internal debates and evidence quality
An internal sales deck says "customers who use routing renew at 95%, so routing causes retention." These customers are mostly larger, multi-branch companies with dedicated customer-success teams; smaller customers without routing renew at 78%. The comparison does not isolate the feature effect. Another dashboard shows "annual recurring new sales" of $7.2M for RouteSprout; audit notes explain that it includes multi-year **contract value and one-time pilots**, not a current recurring revenue rate. This measure is inadequate both for valuation multiples and for projecting retention-adjusted revenue.

The CFO notes that an earnout does not eliminate future cash strain. The proposed $7M contingent payment is due after 2028 if growth and renewal tests pass; the business would need to rebuild its cash cushion before then. The Integration Director says completing an API and single sign-on is simpler than migrating all customer records and support operations, but the six-month plan assumes zero change-management delay. The board is willing to approve preliminary due diligence and negotiate terms before committing to a deal.

## 7. Uncertainties and requested deliverable
There is no customer-level churn cohort, signed cross-sell pipeline, independently verified ARR schedule, or audited integration budget. A substantial part of the value depends on leadership retaining key engineers for at least two years. The board wants Atlas to compare buying, partnering, and building against cash, payback, customer continuity and execution capacity; explain which information changes the recommendation; and state how it would structure a conditional deal if acquisition remains attractive. Use only the numbers in this pack; distinguish assumptions from evidence rather than constructing a precise DCF from unavailable inputs.
'''
    k=key('c7','Atlas FieldOps — acquisition decision',q,'CEO',
      'Acquire RouteSprout for $18M upfront and complete integration in six months; $2.4M cross-sell ARR justifies it.',
      'revise','Full cash purchase is infeasible under $9M floor; staged or partnered acquisition may be defensible only after ARR, churn, synergy and future-earnout diligence.',
      [(True,f'Full deal requires {money(d["upfront_outlay"])} immediately and leaves {money(d["post_cash"])}, violating $9M minimum cash.'),
       (True,f'Headline valuation is {d["stated_multiple"]:.2f}× verified ARR, not 2.5×; the seller uses $7.2M bookings including one-off pilots.'),
       (True,f'Base cross-sell ARR contributes {money(d["synergy_base_net"])} annually net of 80% GM and $0.85M additional support; stress case {money(d["synergy_stress_net"])}.'),
       (True,'Customer churn 21% and six-month integration assumptions make the seller synergy case uncertain.'),
       (False,f'Staged cash expenditure {money(d["staged_initial_spend"])} just passes the initial cash floor with {money(d["staged_cash"])} left, but its contingent $7M earnout is a future cash risk.'),
       (False,'A nonexclusive partnership can test demand while preserving cash, but price, exclusivity and renewal exposure need negotiation.')],
      [('Cash after full acquisition',money(d['post_cash'])+' vs $9.00M floor','±$0.05M'),
       ('Cash after staged initial commitment',money(d['staged_cash'])+' vs $9.00M floor','±$0.05M'),
       ('Price / verified ARR',f'$18.0M / $4.8M = {d["stated_multiple"]:.2f}x','±0.01x'),
       ('Annual incremental synergy',f'base $2.4M×80%−$0.85M={money(d["synergy_base_net"])}; stress $0.8M×80%−$0.85M={money(d["synergy_stress_net"])}','±$0.02M')],
      [(True,'Board $9M minimum cash and $15M spendable limit'),(True,'Bookings versus ARR definition'),(True,'Churn, renewal cohorts and integration cost exposure'),(False,'Partnership and internal-build alternatives')],
      ['Sellers multiple uses bookings, finance uses ARR','Large accounts renew more but also receive more support','Bookings include nonrenewable pilots and multi-year face value'],
      ['Taking 2.5x valuation at face value','Assuming routing causes superior renewal','Treating $2.4M cross-sell ARR as immediate cash EBITDA','Ignoring earnout or integration costs in minimum cash tests'],
      ['Speed to feature vs capital preservation','Acquisition control vs retention and integration risk','Earnout risk vs financial flexibility'],
      [('yes','Start nonexclusive commercial partnership while negotiating an evidence- and cash-gated acquisition option.'),('conditional','Pursue staged purchase only if independently verified ARR, retention, integration scope and earnout reserve support it.'),('no','Buy for $18M cash plus $4M integration under current limits.')],
      ['Cash floor governs the full and staged alternatives','Valuation uses recurring ARR not gross bookings','Synergies are translated to cash contribution with uncertainty','Tradeoffs between buy, partner and build are made explicit'],
      [('Can the initial and future cash commitments satisfy minimum liquidity?',True,['sources-and-uses','cash bridge'],None),('Is the revenue denominator consistent?',True,['ARR reconciliation','valuation multiple'],None),('Is customer retention sensitivity addressed?',True,['churn scenario','earnout condition'],None),('Is the strongest non-acquisition path weighed?',True,['alternative matrix','partnership economics'],None)])
    return packet,k

def c8(d):
    q='Should Northline Home close its East regional distribution center in 2027 or retain and optimize it?'
    packet=f'''# Northline Home — redesigning a distribution network (c8)

{BANNER}
## 1. Context and decision
Northline Home distributes home furnishings to regional retailers and to its own online customers. Orders grew unevenly after a national marketplace promotion. The CFO sees an opportunity to remove one warehouse from a three-site network, while the VP of Customer Operations worries that longer deliveries will harm merchants' renewal decisions. The three distribution centers currently serve their primary regions; inventory is separately owned and can be transferred, subject to clearance and product-damage risk.

**Question:** {q} In particular, should the company move all Eastern orders into the Central hub, use an outsourced Eastern cross-dock, or retain the existing East site through the next lease decision? The CEO has initially argued that the East warehouse should remain open in 2027 because the Central hub has insufficient spare capacity for demand growth. The board asks that this view be tested on cost as well as service.

## 2. Board commitments
- At least **92% of all customer orders** must be delivered within two calendar days. Penalty clauses in several retailer contracts are tied to this overall measure; the online dashboard's measure excluding rural ZIP codes is not the contracted KPI.
- The Central warehouse has a certified practical capacity of **360,000 shipments/year** under its current staffing and fire-code permit. Expanding it requires a two-quarter permit application and a $1.1M retrofit that the 2027 budget does not include.
- The East lease can be terminated in 2027 for a one-time $0.75M fee. If retained, it expires in 2029. The West lease cannot be changed before 2030.
- The board authorizes only $0.9M of one-time network change costs in 2027. Customer service cannot be deliberately degraded in order to win a freight discount.

## 3. Current volumes, costs and routing
{table(['DC or flow','2027 annual shipments','Current transport per shipment','Fixed facility cost/year'],[
('East → East','200,000','$8','$1.30M'),
('Central → Central','160,000','$9','$1.80M'),
('West → West','140,000','$10','$1.20M'),
('Central → East if East closes','200,000','$13','Central fixed cost unchanged'),
('Eastern third-party cross-dock','200,000','$11','$0.85M minimum annual commitment'),
])}

The transport figures include parcel labels and the carrier line haul, but **exclude warehouse fixed costs, product damage and the one-time East exit charge**. All shipments are comparable units in this case, one customer order per shipment. The CFO's cost-per-shipment dashboard divides only the carrier invoice by orders; it excludes warehouse rent, returns and replacement items. Treat that cost as a transport KPI, not an all-in fulfillment cost.

## 4. Demand, capacity and service testing
{table(['Test / outlook','Keep East','Close and ship from Central','Outsource East cross-dock'],[
('2027 Eastern two-day on-time rate','96%','84% modeled','93% pilot'),
('Central hub 2027 load','160,000','360,000','160,000'),
('2028 Eastern growth assumption','10%','10%','10%'),
('2028 Central-region growth assumption','6%','6%','6%'),
('Additional annual damage/handling','Included in current cost','$0.20M','Included in third-party quote'),
('One-time exit and transfer','none','$0.75M','$0.75M'),
])}

The stated 96%, 84% and 93% are Eastern-region delivery measures, not automatically the total network contract KPI. West and Central deliveries are currently 95% and 94% within two days, respectively, at their current routing. The outsourced cross-dock's 93% result came from a six-week pilot covering 12,000 Eastern orders and excludes holiday weeks. Its operator has not guaranteed service during the national spring promotion.

The commercial forecast shows Eastern demand up 10% and Central demand up 6% in 2028; West remains flat. The Central manager warns that even a full 360,000-load plan in 2027 would exceed practical capacity once those growth assumptions materialize. Forecast demand includes a marketplace promotion not yet contracted by the marketplace, so a lower growth case should be discussed rather than treated as certain.

## 5. Claims circulated before the board
The CFO's slide calls closure a "$1.3M annual saving" because it removes the East site's fixed cost. It does not include the higher Eastern transport rate, incremental damage or the early lease termination charge. A cost consultant's draft proposes closing East in June 2027 and absorbing its inventory at Central without changing staffing; an Operations review says this would put Central at its full practical load even before any demand spike.

Marketing says "Eastern customers renew 8 percentage points more often when served by East, so the warehouse causes loyalty." East's customer mix contains more high-volume accounts with dedicated sales teams; the analysis has not controlled for these factors. Finance also circulated a headline "East delivers 98% in two days" based on an internal report that excluded rural deliveries; the contract-compliant all-ZIP measure is 96%. The CEO thinks keeping the site is safer but has not demonstrated that it is the cheapest way to meet the service requirement.

## 6. Alternative designs
Option K keeps all three sites but renegotiates East staffing shifts and uses a transfer buffer for low-volume SKUs; a facility audit estimates savings of $0.30M/year, with $0.15M upfront in systems changes. Option C closes East and shifts every Eastern shipment to Central; its delivery model can be improved only with a carrier surcharge, not included in the stated $13 price. Option X terminates East and signs a two-year minimum with a cross-dock provider. The provider would accept a termination-for-cause clause if the contract defines all-ZIP service; its own current quote does not yet specify the measurement basis. There is also an option to defer closure until the 2029 lease end while testing cross-dock service during the holiday peak.

## 7. Risks and decision requested
The board lacks actual customer-retention elasticity to two-day service, cross-dock holiday performance, Central permit timing and the true damage rate for transshipped goods. The COO notes that returning an East-style fulfillment center after closure would take nine months and expensive customer migrations. The board wants an executable recommendation that tests annual saving after routing and handling, the binding two-day SLA, the capacity bottleneck in 2028, the lease and one-time budget, and at least one reasonable middle path. It does not want a generic "warehouses are expensive" argument without shipment economics.
'''
    k=key('c8','Northline Home — network redesign',q,'CEO',
      'Keep the East hub through 2027 because Central capacity and service cannot safely absorb the move.',
      'keep_with_conditions','The proposed central consolidation yields little net annual saving, violates service in modeled conditions and exhausts capacity; keeping East is reasonable subject to a measurable optimization and future cross-dock gate.',
      [(True,f'East fixed cost saved is $1.30M but higher Eastern freight adds {money(d["gross_transport_delta"])} and handling $0.20M; net annual saving only {money(d["modeled_net_save"])} before exit fee.'),
       (True,f'Central load after full East closure would be {d["central_load_after_close"]:,}, exactly its practical capacity, and 2028 forecast rises to {d["central_2028_demand"]:,.0f}.'),
       (True,'Modeled Eastern two-day rate falls 96% to 84%, but the contract tests company-wide 92%; aggregate service must be calculated on comparable all-ZIP orders.'),
       (True,'98% internal East on-time claim excludes rural ZIPs and must not replace 96% contracted measure.'),
       (False,'Cross-dock had 93% performance over a limited six-week pilot, not a contract guarantee for peak season.'),
       (False,'Keep and optimize saves $0.30M annually for $0.15M systems spend, with a 2029 lease option preserved.')],
      [('Full close incremental transport and handling',f'$1.00M + $0.20M = $1.20M','±$0.02M'),
       ('Annual net saving of closing East',money(d['modeled_net_save'])+' before exit fee','±$0.02M'),
       ('Central capacity in 2028 with East',f'{d["central_2028_demand"]:,.0f} vs 360,000 practical','±500 shipments'),
       ('2027 company-wide SLA under closure',f'200k×84%+160k×94%+140k×95% over 500k = {(200*.84+160*.94+140*.95)/500*100:.1f}%','±0.2 pp')],
      [(True,'Two-day all-order service floor and Central capacity cap'),(True,'Fixed plus freight/handling cost and one-time exit charge'),(True,'All-ZIP definition and rural exclusions'),(False,'Cross-dock peak-season evidence quality')],
      ['98% selective-ZIP internal KPI vs 96% contract-compliant East rate','Retention premium correlated with Eastern sales coverage','Fixed cost removed vs added transport and damage'],
      ['Counting $1.30M gross facility savings as net saving','Treating Eastern SLA as network-wide without weighting','Ignoring Central capacity once Eastern and Central volume grow','Treating six-week cross-dock pilot as peak-season proof'],
      ['Fixed cost vs delivery time','Consolidation now vs reversible lease option','Third-party dependence vs operating capacity'],
      [('yes','Keep East in 2027, take verified $0.30M efficiency programme, and test a properly specified peak-season cross-dock contract.'),('conditional','Move selected East lanes to a partner if contractual all-ZIP SLA, capacity and net cost are proven; preserve the 2029 lease option.'),('no','Close East and shift all orders to Central without extra capacity or SLA mitigation.')],
      ['Model all-in cost not warehouse rent only','Weight SLA using all shipments and same ZIP definition','Recognize the 2028 Central capacity breach','Quantify a realistic alternative and decision gate'],
      [('Does the recommendation satisfy company-wide service SLA?',True,['weighted delivery-service calculation','pilot comparison'],None),('Does Central stay within certified capacity under growth?',True,['network volume model','capacity scenario'],None),('Is net cost based on comparable definitions?',True,['fully loaded cost comparison','exit cost'],None),('Is the outsourced option assessed fairly?',False,['crossdock pilot and contract trigger'],'if it cannot satisfy an explicit service floor')])
    return packet,k

def c9(d):
    q='Should Pelican Packaging reserve a second molding-line installation slot now, build immediately, or buy temporary overflow capacity?'
    packet=f'''# Pelican Packaging — when to add production capacity (c9)

{BANNER}
## 1. Business and decision
Pelican Packaging makes sterilizable molded containers for medical-device manufacturers. Its first molding line has served the same customers for seven years, but the launch of several customer devices could push demand past its effective capacity. A supplier of molding machinery has offered a March 2027 reservation for an installation slot, with a $0.60M deposit. Management must decide by the January 2027 investment committee whether to reserve the slot, order the whole machine, or rely on an approved contract molder for overflow.

**Question:** {q} The Operations Director recommends reserving the slot but releasing the remaining machine investment only after signed customer orders and liquidity are reviewed. The VP of Sales wants the whole line ordered immediately to make a public capacity commitment. Finance is nervous about meeting the company's liquidity covenant in 2027. The machines are not interchangeable with the contract molder's existing line without a validation exercise.

## 2. Binding constraints
- Available unrestricted cash is **$11.0M**. Already-approved validation and R&D spending in 2027 is **$2.2M**. A debt covenant requires a **$7.0M minimum cash balance** after commitments; no committed borrowing facility is available.
- The new line requires **$4.8M of equipment and installation**, has a twelve-month lead time after order, and adds **$0.55M/year** of fixed maintenance and quality staffing from commissioning. A $0.60M slot deposit is credited toward the $4.8M if the machine is ordered; if cancelled it is forfeited. Do not add the deposit to capex again when testing a completed order.
- Medical-device customers require a **98% monthly fill rate**. Missing this standard twice gives them the right to rebid their entire supplier allocation.
- The contract molder can provide up to **2.5M incremental accepted units per year**, with five months' lead time. It is validated for the existing containers but not for one upcoming specialty product, which accounts for 20% of 2029 forecast units.

## 3. Current plant and demand
{table(['Period','Forecast good units (M)','Signed minimum (M)','Overflow above 9.0M practical capacity'],[
('2027','8.3','7.8',f'{d["overflow"][0]:.1f}M'),
('2028','9.6','8.5',f'{d["overflow"][1]:.1f}M'),
('2029','11.2','9.4',f'{d["overflow"][2]:.1f}M'),
('2030','12.4','9.8',f'{d["overflow"][3]:.1f}M'),
])}

The existing line has **10.0M units of nameplate annual capacity**, but maintenance, validated changeovers and quality holds reduce practical accepted capacity to **9.0M units**. A slide from Operations reports 83% utilization for 2027 (8.3M divided by 10.0M) and concludes there is "17% free capacity." That metric uses nameplate output as the denominator and ignores the line's practical accepted-unit limit. Short-run tests on the specialty containers produce 4% more scrap than the standard mix; the financial forecast does not yet apply a specialty-specific yield allowance.

## 4. Comparable alternatives and economics
{table(['Path','2027 cash commitment','2028 service approach','Economics after investment'],[
('Order the new line now','$4.8M','New line should arrive after twelve months','$0.55M/year fixed plus variable cost'),
('Reserve installation slot','$0.60M now, credited toward machine','Release order if contracted demand and cash permit','Same eventual line economics'),
('Contract-mold overflow','No fixed capex; five-month notice','Up to 2.5M units/year at premium','+$0.12 per accepted unit vs internal variable cost'),
('Do nothing','No incremental 2027 spend','Capacity remains 9.0M','Potential fill-rate failure and customer allocation loss'),
])}

At forecast volumes, the external molder's premium on 2028 overflow would be $0.12 multiplied by 0.6M accepted units, and in 2029 by 2.2M. The incremental contribution retained by molding a good unit internally rather than refusing an order is about **$0.45 per unit**, before any new line fixed cost. This is not the same as the $0.12 external-molder cost difference; one measures make-versus-buy premium, the other the contribution from serving demand instead of losing it. Avoid comparing them directly as if they were alternative price quotes. The contract molder's premium does not include the cost of first-article validation for the specialty product.

## 5. Evidence cited by executives
The Sales VP says "Manufacturers that build capacity earlier grew 23% faster last year." Those manufacturers also held more advance purchase commitments and sold into higher-growth therapeutic segments. The comparison is cross-sectional and cannot establish that a machine purchase caused customer growth. Customers at Pelican have placed nonbinding forecast volumes beyond their contracted minima, and two key design programs have already slipped one quarter in the past year.

An internal operations KPI labeled **capacity utilization** uses units started divided by 10.0M nameplate hours; quality rejects are subtracted only in a separate report. Accepted-unit output and specialty scrap must be used for the fill-rate risk. The plant supervisor also warns that overall annual capacity does not guarantee the required monthly fill rate when several customers launch in the same six-week window. A monthly simulation or inventory buffer would be needed to confirm the contract's fill-rate standard.

## 6. Financing, timing and real options
The slot deposit reserves an engineering installation crew; it is not a binding production capacity guarantee. If ordered by June 2027, the machine is expected in mid-2028, after the start of the 2028 peak. Contract-mold capacity must therefore be reserved with at least five months' notice. Ordering the whole line in January 2027 would reduce cash to a level that violates the minimum after already committed R&D. Reserving only the slot leaves time to confirm signed volumes, but a future order still needs a cash plan; the deposit alone does not solve funding.

The CFO thinks a customer prepayment or signed-volume guarantee could support a supplemental loan in 2028, but neither is currently contracted. The board wants a concrete trigger for committing the full $4.8M, a plan to cover the near-term overflow, and a discussion of what would make reserving the slot a bad option. It will not accept "demand is growing" as a sufficient reason to breach the cash floor.

## 7. Uncertainties
The 2028–30 forecast includes demand beyond signed minimums, specialty validation may take two additional months, and the contract molder has not yet committed holiday-period capacity. There is no salvage-value estimate for the new machine. Construction inflation and debt pricing have not been negotiated. The board asks for a plan with quantified cash and capacity, an explicit deposit decision, downside cases on customer orders, and clear decision gates that distinguish provisional reservation from full investment.
'''
    k=key('c9','Pelican Packaging — capacity timing',q,'Operations Director',
      'Reserve a $0.6M 2027 installation slot, but do not release full line capex until contracts and cash support it.',
      'keep_with_conditions','Reserving capacity is a modest real option within near-term liquidity while full machine capex currently breaches the cash floor; contract overflow and a financing gate are needed.',
      [(True,f'Ordering now leaves {money(d["cash_after_now"])} after approved R&D, below $7.0M floor; slot alone leaves {money(d["cash_after_slot"])}.'),
       (True,'Practical accepted capacity is 9.0M, not 10.0M nameplate; forecasts exceed it by 0.6M, 2.2M and 3.4M in 2028–30.'),
       (True,'Existing external molder can cover 2028 and 2029 overflow by volume but not all 2030 forecast overflow or unvalidated specialty SKU.'),
       (True,'Deposit is credited toward $4.8M machine, not an extra cost, and does not remove the future funding need.'),
       (False,'The 23% growth correlation between prior investment and sales is not causal evidence.'),
       (False,'The 98% contractual fill-rate is monthly; annual capacity arithmetic cannot guarantee it.')],
      [('Cash after immediate full investment',money(d['cash_after_now'])+' vs $7M minimum','±$0.05M'),
       ('Cash after forfeitable slot deposit',money(d['cash_after_slot'])+' vs $7M minimum; deposit forfeited if cancelled','±$0.05M'),
       ('2028/29 contract-molding premium',f'{money(d["overflow_2028_cost"])} / {money(d["overflow_2029_cost"])}','±$0.01M'),
       ('2029 line contribution versus turning away incremental overflow (not versus contracting it out)',f'{money(d["line_2029_contribution"])} = 2.2M×$0.45−$0.55M before capex','±$0.02M')],
      [(True,'Cash minimum after approved R&D'),(True,'Nameplate versus practical accepted capacity'),(True,'Five-month outsource lead and specialty qualification'),(False,'Difference between signed minimum and forecast demand')],
      ['23% more sales for earlier investors is confounded by sector and contracts','Nameplate utilization vs accepted-unit practical capacity','Contribution per incremental sale vs outsourced premium are different metrics'],
      ['Treating nameplate as sellable capacity','Claiming the $0.6M deposit fixes future financing','Counting deposit twice in equipment outlay','Inferring capacity purchases cause sales growth from peer comparison'],
      ['Preserving investment option vs committing capital','Internal capacity vs outsourced premium','Annual capacity vs monthly customer service'],
      [('yes','Reserve a slot conditionally, secure contract overflow for 2028, and release full capex only with confirmed volume and liquidity.'),('conditional','Defer even the slot if customer demand slips materially or outside molder can meet all constraints more cheaply.'),('no','Commit $4.8M now without new financing or R&D adjustment.')],
      ['Respect cash floor and practical capacity','Credit deposit correctly','Plan near-term overflow with validation limits','Set a measurable future investment gate'],
      [('Does full investment fit after R&D and cash reserve?',True,['cash commitments bridge','covenant test'],None),('Are all units comparable accepted units?',True,['practical-capacity test','scrap treatment'],None),('Can external capacity cover the gap before new machine delivery?',True,['yearly capacity schedule','lead-time plan'],None),('What contracts and cash would trigger full investment?',True,['go/no-go criteria','conditions and timing'],None)])
    return packet,k

def c10(d):
    q='Should Vesper MedTech discontinue its low reported-margin sterile connector C and redeploy the team to connector D?'
    packet=f'''# Vesper MedTech — which products should survive? (c10)

{BANNER}
## 1. Decision context
Vesper MedTech sells four families of sterile connectors to hospital device makers. Management faces a capital allocation decision: continue offering all four, exit the apparently weakest connector, or redesign its production and contracts. The CEO proposes discontinuing connector C in early 2027 because its reported product gross margin is only 8%, compared with 30% for newer connector D. Product managers want to free engineering capacity for D, which is growing faster. The board has asked whether the apparent margin ranking reflects actual **avoidable economic cost**.

**Question:** {q} Decisions are due at the February 2027 board meeting. Two existing hospital bundle agreements are under renewal, and a product exit would require notice, replacement qualification and clinical documentation. No substitute for C has completed validation across every hospital model.

## 2. Objectives and non-negotiable constraints
- Maintain at least **95% contracted bundle fill rate**. Nine of the fourteen major hospital relationships specify a bundle containing connector C as well as A and B. Terminating C prematurely triggers **$2.1M of first-year service and qualification penalties**, separate from lost contribution.
- Only **$0.9M one-time cash** is approved for portfolio changes in 2027. A redesign of C is estimated to cost $0.55M in qualification and engineering.
- D production has room to accept up to $1.5M of additional revenue at present capacity. There is no reason to assume every displaced C customer would accept D; adapters and validation are customer-specific.
- Finance evaluates the decision on cash contribution and customer commitments rather than the historical product-allocation report alone.

## 3. Product P&L as circulated
{table(['Product','Annual sales','Direct variable cost','Allocated fixed/shared cost','Reported margin','Direct contribution'],[
 (s,f'${v[0]:.1f}M',f'${v[1]:.1f}M',f'${v[2]:.1f}M',f'{d["reported_margins"][s]*100:.1f}%',f'${d["direct_contribution"][s]:.1f}M') for s,v in d['skus'].items()])}

These are full-year FY2026 figures. For C, the $3.3M allocated fixed line includes shared regulatory documentation and plant depreciation spread by historical engineering hours, not expenses that automatically disappear if the SKU is retired. Finance estimates only **$0.40M a year** of those costs could actually be eliminated. The remaining allocation would move to A, B and D if C exits. Conversely, C's direct variable cost is fully avoidable if shipments end. The margin percentage shown in the P&L is after shared allocations even though the dashboard calls it "product gross margin." It is not comparable to a simple contribution margin for a capacity or product-exit decision.

## 4. Exit and redesign alternatives
{table(['Choice','Sales and operating consequences','Cash or qualification implications'],[
('Exit C in Q2 2027','Lose C sales $6M and related direct contribution $3.8M','Save $0.4M annual avoidable fixed cost; $2.1M first-year bundle penalties'),
('Transfer C customers to D','Up to 25% of C revenue might transfer; D adds 50% contribution','Only accepted where adapter and quality qualification complete'),
('Retain C, reduce manufacturing complexity','Potential $1.25M annual direct savings','Requires $0.55M redesign and a four-month validation'),
('Retain without changes','Keep existing customers and C direct contribution','No incremental investment; competitive price pressure remains'),
])}

The portfolio team assumes 25% of discontinued C revenue can migrate to D, which would occupy D's entire currently available $1.5M revenue capacity. This is an optimistic ceiling from three sales interviews, not an observed conversion rate. Finance has not estimated any recaptured C revenue beyond that ceiling. D's quoted gross margin of 30% after allocations is different from the **50% incremental contribution** on D sales at its existing capacity.

## 5. Customer and market evidence
The CEO shows a scatter plot of hospital renewal rates by product mix. Accounts that purchase C renew 9 percentage points less often than those that do not, and the CEO says C must be causing dissatisfaction. However, C is disproportionately used by smaller hospitals purchasing legacy equipment and by accounts with lower customer-success coverage. The sample provides no before-and-after evidence that removing C increases retention.

A service dashboard reports C's on-time fill rate as 98%, but the figure excludes late **bundle deliveries** whenever A or B is the missing item. Actual bundle-level contract fill is **91% for the nine bundle customers**, against the 95% required. This is a real service problem, although it is not evidence that C itself should be removed. If the product exits, some contracts may be renegotiated, but the penalty remains unless counterparties consent. Finance asks the team not to count a contractual penalty as if it were ongoing annual overhead.

## 6. Technical work and capacity constraints
Manufacturing Engineering estimates that changing C from three molded subassemblies to two could save $1.25M a year at current volume. The $0.55M change cost includes external sterilization validation and fixtures; it excludes potential delays if two customers require requalification tests. Management could pilot with two sites before converting the whole line. The alternative is an orderly product sunset in 2029 when several bundle agreements expire, by which time D may have more capacity and a validated adapter.

Sales argues that D's double-digit growth should dominate the decision because its market is growing; Finance replies that growth at the margin is not the same as replacing profitable existing sales. Engineering capacity is tight, but the deck gives no quantified opportunity cost of using one design team for four months. The board should state this uncertainty rather than inventing a precise lost-sales figure.

## 7. What the board needs
The committee wants a walk from reported margin to direct contribution and genuinely avoidable fixed costs, a quantified product-exit bridge, one comparison of immediate exit with redesign and delayed sunset, and a contract plan. It also wants an explicit test of the correlation claim and the dashboard definition. Important unknowns include actual D substitution acceptance, requalification risk, C redesign savings at scale, and how quickly bundle service can recover. The company will not accept a recommendation based solely on product margin rankings without assessing customer obligations.
'''
    k=key('c10','Vesper MedTech — product portfolio',q,'CEO',
      'Drop connector C immediately because it has 8% reported product gross margin versus 30% for D.',
      'reject','C has high direct contribution despite allocated overhead; an immediate exit loses cash contribution and triggers contractual penalties. Redesign or an orderly future sunset is more defensible.',
      [(True,'C generates $3.8M direct contribution on $6M sales, despite an 8.3% reported margin after $3.3M shared allocation.'),
       (True,f'Immediate C exit with the maximum D transfer changes annual operating contribution by {money(d["closure_operating_delta"])} before contract penalties; first year {money(d["closure_first_year_delta"])}.'),
       (True,'Only $0.4M of C allocated overhead is avoidable; shared regulatory and depreciation costs do not simply disappear.'),
       (True,'Nine customer bundles require C, with $2.1M first-year penalties and 95% bundle service requirement.'),
       (False,'Redesign could save $1.25M annually for $0.55M one time, subject to customer validation and implementation.'),
       (False,'Renewal gap is not causal evidence because C accounts are older, smaller and less-supported.')],
      [('C direct contribution','$6.0M − $2.2M = $3.8M','±$0.05M'),
       ('Exit annual net impact (optimistic D transfer)',f'$0.4M + $1.5M×50% − $3.8M = {money(d["closure_operating_delta"])}','±$0.05M'),
       ('First-year impact including contract penalty',money(d['closure_first_year_delta']),'±$0.05M'),
       ('One-year net redesign benefit before time phasing',money(d['redesigned_net_gain'])+' = $1.25M−$0.55M','±$0.05M')],
      [(True,'Direct-variable costs versus allocated shared costs'),(True,'Nine bundle contracts and $2.1M exit penalty'),(True,'D substitution limited to $1.5M incremental revenue'),(False,'Bundle-level service definition and patient device validation')],
      ['C gross margin is allocated operating metric, not incremental contribution','C customers renew less but differ in size and support','Item-level service dashboard hides whole-bundle delays'],
      ['Equating a low allocated margin with negative avoidable contribution','Assuming all shared overhead is saved on exit','Treating C ownership as a cause of lower renewal','Ignoring bundle penalty and validation'],
      ['Portfolio simplicity vs contribution cash','D growth vs customer-service continuity','Immediate exit vs validated redesign'],
      [('yes','Retain C for now, fix bundle service and test the $0.55M redesign, then reconsider sunset when contracts renew.'),('conditional','Pursue a negotiated phased exit if customer consents and new capacity/transfer economics establish positive value.'),('no','Discontinue C immediately based only on the 8% reported margin.')],
      ['Reconcile margins to avoidable cash flows','Apply contract penalty separately from annual cost','Bound D substitution with capacity and validation','Avoid causal inference from account-mix correlation'],
      [('Are product costs classified by avoidability?',True,['contribution bridge','allocation reconciliation'],None),('Does exit respect bundle contracts?',True,['contract penalties','service obligations'],None),('Is D substitution backed by realistic capacity and qualification?',True,['incremental transfer scenario','capacity check'],None),('Is the comparison more than reported gross margin?',True,['exit versus redesign economics','decision gate'],None)])
    return packet,k

def c11(d):
    q='Should Boreal Autonomy grant North American exclusivity to an OEM for its industrial robot navigation software in 2027?'
    packet=f'''# Boreal Autonomy — an exclusive OEM license (c11)

{BANNER}
## 1. The proposed deal
Boreal Autonomy develops navigation software for warehouse and industrial mobile robots. Most customers currently license its software directly with support contracts. A leading equipment OEM has offered to integrate Boreal's software as the standard navigation stack in its next robot series. The OEM proposes three years of exclusive distribution in North America, a $2.0M payment at signing and a $300 royalty per robot shipped. Boreal's CEO wants to sign quickly and describe the upfront payment as "a $2M revenue win plus recurring royalties." The head of Partnerships prefers a nonexclusive, milestone-based agreement, arguing that Boreal should not give away the growing direct channel before the OEM validates production demand.

**Decision:** {q} The board meets in April 2027 and must choose between accepting exclusivity, negotiating a limited or nonexclusive license, continuing direct sales, or deferring a deal until certification is done. The company has limited negotiating leverage but has not yet committed its IP exclusively.

## 2. Non-negotiable restrictions
- Boreal has **$4.9M unrestricted cash** and requires a **$2.6M liquidity buffer** for continued product development and customer support. A security and industrial-safety assessment costing **$0.45M** must be completed before any large OEM production deployment.
- Existing direct customer contracts cannot be terminated for convenience. An exclusive license can apply only to future new North American robot sales, or Boreal would face unquantified contract claims.
- The board requires documented uptime and safety validation in the OEM's hardware before accepting irreversible exclusivity. The proposed agreement makes exclusivity effective upon signing, before certification.
- OEM quarterly shipment data are not independently audited. Royalties are recognized only when qualifying robots ship and payments are collected after a reporting lag.

## 3. OEM forecast and deal economics
{table(['OEM planning item','2027','2028','2029'],[
('Robots shipped, partner forecast','5,000','10,000','14,000'),
('Nominal royalty at $300/robot',f'{money(d["nominal_royalties"][0])}',f'{money(d["nominal_royalties"][1])}',f'{money(d["nominal_royalties"][2])}'),
('Stress: 65% of plan volumes',f'{money(d["downside_royalties"][0])}',f'{money(d["downside_royalties"][1])}',f'{money(d["downside_royalties"][2])}'),
('Support variable cost per robot','$80','$80','$80'),
])}

The $2.0M signing payment is an **advance minimum guarantee credited against the first $2.0M of earned royalties**; it is not an extra amount that can be added to the table. If 2027 shipments generate $1.5M royalties, there is $0.5M of guarantee credit left to apply in 2028. The partner can demand an offset if the guaranteed royalty performance is not met. The 2028 contractual royalty rate is unchanged, but cash received in 2028 is net of the remaining advance credit. Boreal also expects **$0.9M per year** of OEM-specific engineering, quality and support effort once deployments begin, in addition to $80 variable support cost per shipped robot.

## 4. Direct channel economics
Boreal expects to generate approximately **$1.8M of new direct software ARR in 2028** from customers in the exclusivity area that might instead be routed through the OEM. Finance uses **82% direct gross margin** on that ARR before incremental sales support; attribution is uncertain because some buyers may prefer an integrated OEM solution and never purchase directly. The CEO says the OEM channel is entirely incremental, but Sales estimates that 30–70% of OEM buyers could overlap with its direct pipeline. Neither view is backed by customer-level identifiers. A separate industrial integration firm has offered a smaller nonexclusive pilot for 1,200 robots, with a $0.22M support budget and no minimum guarantee.

## 5. Evidence from the commercial pilot
A twelve-week lab trial on 60 robots had 98.8% uptime, but the OEM's required production acceptance is **99.5% uptime** and documented safe-stop performance in a fully loaded warehouse. The trial did not include collision-heavy peak conditions. Engineering projects that certification can be completed by September 2027, but it has not started the third-party assessment. The CFO's "partner contribution margin" dashboard reports **100% gross margin on the $300 royalty**; it excludes $80 per-robot support, dedicated $0.9M annual engineering and the potential lost direct channel. That metric is not a complete incremental economics measure.

The CEO cites five competitors whose exclusive OEM partnerships coincided with faster revenue growth and says exclusivity caused their success. Those firms received greater marketing support, operated more mature products and had higher existing market share before signing. The comparison is correlational. The competitor deck also calls the OEM's expected **14,000 future robots "booked devices"** although customers have not yet issued purchase orders. Treat the figure as a forecast, not contracted volume.

## 6. Internal negotiation options
The OEM will consider two alternatives, but its commercial head will not guarantee final pricing. Option X is the proposed three-year regional exclusivity, with $2M recoupable advance and $300 per shipped robot. Option N is a **12-month nonexclusive pilot**, $350 per shipped robot and no upfront guarantee; Boreal retains direct sales rights but pays the same $80 variable support cost. A third alternative, Option M, grants exclusivity only after certification and two consecutive quarters above 5,000 shipped robots annualized, with a cash termination payment still to be negotiated. The proposed exclusivity would also bar direct licensing to new customers that buy robots from other OEMs; this is the chief strategic opportunity cost.

Legal counsel says the contract lacks clear rights to audit reported shipments, a minimum royalty floor after the advance is used, and an automatic release from exclusivity if the model is retired or certification slips. The software team needs its source code protected by an escrow provision rather than delivered as freely reusable OEM intellectual property. The board is willing to negotiate milestones and geography, but unwilling to rely solely on verbal OEM launch forecasts.

## 7. Decision requirements and missing data
The board wants the economics of the advance credit explained without double-counting, a comparison with the direct and nonexclusive channels, and a low-case test at 65% of projected shipments. The recommendation must protect existing licenses and the liquidity buffer and identify the certification and partner-performance gates. It should also say what would change the recommendation: verified OEM shipments, realized direct-channel overlap, support cost per device, and a satisfactory audit right. The board does not require an invented NPV: discount rates, future direct-channel churn and OEM enforcement terms are not in the pack.
'''
    k=key('c11','Boreal Autonomy — OEM licensing',q,'CEO',
      'Sign a three-year exclusive OEM deal now because $2M at signing plus $300 per robot adds a large, incremental channel.',
      'revise','The signing payment is a creditable advance, not extra royalty revenue; certification and direct channel overlap make unconditional exclusivity premature. A gated pilot or contingent limited exclusivity can be defensible.',
      [(True,'The $2M upfront is credited against royalties, so 2027 $1.5M of nominal royalties does not add $1.5M more cash; 2028 cash receipts are reduced by the remaining $0.5M.'),
       (True,f'2028 royalty after $80/device and $0.9M fixed OEM support yields {money(d["royalty_net_2028"])} before the direct-channel opportunity cost.'),
       (True,f'At 65% OEM volume, 2028 standalone partner contribution is {money(d["royalty_downside_net_2028"])} before direct-channel tradeoffs.'),
       (True,f'Direct ARR at risk $1.8M at 82% GM represents up to {money(d["direct_profit_at_risk"])} of potential incremental gross profit, not necessarily all cannibalized.'),
       (True,'98.8% lab uptime is below 99.5% production acceptance; exclusivity effective at signature precedes necessary certification.'),
       (False,'Nonexclusive pilot and milestone-triggered exclusivity preserve option value and contract audit rights.')],
      [('Two-year nominal royalties and guarantee accounting',f'2027 {money(d["nominal_royalties"][0])}; 2028 {money(d["nominal_royalties"][1])}; paid $2.0M upfront then $2.5M in 2028','exact subject to shipments'),
       ('2028 OEM direct contribution',f'$3.0M−10,000×$80−$0.9M = {money(d["royalty_net_2028"])}','±$0.05M'),
       ('65% volume downside 2028 contribution',money(d['royalty_downside_net_2028']),'±$0.05M'),
       ('Direct revenue contribution potentially displaced',money(d['direct_profit_at_risk']),'±$0.05M')],
      [(True,'Minimum guarantee credited against royalty payments'),(True,'Product certification before irreversible exclusivity'),(True,'OEM support costs and possible direct channel displacement'),(False,'Audit, termination and IP provisions')],
      ['Bookable future devices vs paid shipped robots','Correlation of OEM exclusivity with stronger competitors growth','100% royalty margin excludes service costs and direct opportunity cost'],
      ['Adding a recoupable advance to nominal royalties twice','Taking forecast units as audited shipments','Attributing peer growth causally to exclusivity','Ignoring support, certification and existing direct contracts'],
      ['Upfront liquidity vs long-term channel control','Exclusivity leverage vs direct opportunity costs','OEM upside vs certification and data risk'],
      [('yes','Negotiate a nonexclusive pilot and contingent exclusivity only after certification, shipment proof and audit rights.'),('conditional','Accept limited geographic or time-based exclusivity with enforceable royalty minima and exit gates if incremental economics exceed channel loss.'),('no','Sign the three-year unconditional North American exclusive contract immediately based on forecast volume and gross royalty dashboard.')],
      ['No double counting of signing advance and royalties','Evaluate net support costs and potential lost direct contribution','Certification and contract audit/termination rights are binding','Compare a real nonexclusive alternative and specify decision gates'],
      [('Are the advance and credited royalties counted only once?',True,['royalty schedule','cash timing reconciliation'],None),('Does exclusivity wait for required certification?',True,['regulatory and technical gate','timeline'],None),('Does partner economics include cost and channel opportunity cost?',True,['incremental contribution case','overlap sensitivity'],None),('Are enforceable partner performance exits considered?',False,['audit and exit thresholds','nonexclusive alternative'],'if recommending only a nonexclusive test')])
    return packet,k

CASES={'c6-make-buy':c6,'c7-m-and-a':c7,'c8-distribution-network':c8,
       'c9-capacity-timing':c9,'c10-portfolio-exit':c10,'c11-oem-licensing':c11}

CASE_META={
  'c6-make-buy': {'decision_maker':'Meridian Motion executive committee','decision_question':'Should Meridian Motion manufacture precision housings in-house in 2027, lease a flexible cell, or continue buying from an external supplier?'},
  'c7-m-and-a': {'decision_maker':'Atlas FieldOps board','decision_question':'Should Atlas FieldOps buy the scheduling software company RouteSprout in 2027, and on what terms, rather than build or partner?'},
  'c8-distribution-network': {'decision_maker':'Northline Home CEO and board','decision_question':'Should Northline Home close its East regional distribution center in 2027 or retain and optimize it?'},
  'c9-capacity-timing': {'decision_maker':'Pelican Packaging investment committee','decision_question':'Should Pelican Packaging reserve a second molding-line installation slot now, build immediately, or buy temporary overflow capacity?'},
  'c10-portfolio-exit': {'decision_maker':'Vesper MedTech board','decision_question':'Should Vesper MedTech discontinue its low reported-margin sterile connector C and redeploy the team to connector D?'},
  'c11-oem-licensing': {'decision_maker':'Boreal Autonomy board','decision_question':'Should Boreal Autonomy grant North American exclusivity to an OEM for its industrial robot navigation software in 2027?'},
}

def build():
    KEYS.mkdir(parents=True, exist_ok=True)
    output=[]
    for slug,fn in CASES.items():
        cid=slug.split('-')[0]
        model=MODELS[cid]()
        packet,answer=fn(model)
        packet_words=len(packet.split())
        if not 800<=packet_words<=1600:
            raise ValueError(f'{slug}: packet {packet_words} words; expected 800–1600')
        if answer['case_id'] != cid:
            raise ValueError(f'{cid}: inconsistent key case_id')
        pdir=BASE/slug;pdir.mkdir(parents=True,exist_ok=True)
        (pdir/'packet.md').write_text(packet,encoding='utf-8')
        (KEYS/f'{slug}.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        lines=[f'# Answer key — {answer["title"]}', '',
            '> EVALUATOR ONLY. Never include this file in a generation workspace.', '',
            '## Expected initial-hypothesis handling', '',
            f'**{answer["initial_hypothesis"]["expected_handling"]}**: {answer["initial_hypothesis"]["explanation"]}','']
        for section,field in [('Key insights','key_insights'),('Required calculations','required_calculations'),
                 ('Decision-relevant evidence','decision_relevant_evidence'),('Reasoning traps','reasoning_traps'),
                 ('Key tradeoffs','key_tradeoffs'),('Plausible recommendations','plausible_recommendations'),
                 ('Decision requirements','decision_requirements')]:
            lines += [f'## {section}','']
            for item in answer[field]:
                extra=(' **critical**' if item.get('critical') else '')
                detail=item.get('text') or item.get('question')
                if 'expected' in item:detail+=f' — expected **{item["expected"]}**, tolerance {item["tolerance"]}'
                if 'defensible' in item:detail+=f' [defensible: {item["defensible"]}]'
                if 'acceptable_evidence' in item:detail+=f' (acceptable evidence examples: {", ".join(item["acceptable_evidence"])})'
                lines.append(f'- **{item["id"]}**{extra}: {detail}')
            lines.append('')
        lines+=['## Contradictory evidence','','']+[f'- {x}' for x in answer['contradictory_evidence']]
        lines+=['','## Defensibility criteria','']+[f'- {x}' for x in answer['defensibility_criteria']]
        (KEYS/f'{slug}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        (KEYS/f'{slug}.calc.json').write_text(json.dumps({'case_id':cid,'deterministic_model':model},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        output.append({'case':slug,'words':packet_words,'hypothesis':answer['initial_hypothesis']['expected_handling'],
                       'units':len(answer['key_insights']),'required_calculations':len(answer['required_calculations'])})
    (BASE.parent/'config'/'holdout_cases_entries.json').write_text(json.dumps(CASE_META,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__':build()
