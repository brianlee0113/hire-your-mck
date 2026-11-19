"""Six independent, deterministic synthetic decision models for holdout cases c6–c11.
No random draws, external data, or dependency on the previous five benchmarks.
Run with: python benchmark/cases/build_holdout_cases.py
"""
from __future__ import annotations


def c6():
    units = [80_000, 100_000, 120_000]
    outsource = [u * 75 / 1e6 for u in units]
    build_unit = [46/(1-.08), 46/(1-.04), 46/(1-.04)]
    build_op = [units[i]*build_unit[i]/1e6 + .75 for i in range(3)]
    lease_unit = [49/(1-.06), 49/(1-.04), 49/(1-.04)]
    lease_op = [units[i]*lease_unit[i]/1e6 + 1.60 for i in range(3)]
    return dict(units=units, outsource_cost=outsource, build_unit=build_unit,
                build_op=build_op, lease_unit=lease_unit, lease_op=lease_op,
                build_capex=7.30, lease_setup=2., vendor_tooling=.25,
                cash=9.2, liquidity_floor=4.0, spendable=5.2, capex_ceiling_2027=5.0,
                build_cash_post=9.2-7.3, lease_cash_post=9.2-2,
                outsourcing_total=sum(outsource), build_total=sum(build_op)+7.3,
                lease_total=sum(lease_op)+2,
                build_savings_2028=outsource[1]-build_op[1],
                unit_saving_2028=75-build_unit[1],
                low_2028_units=65_000)


def c7():
    cash=24.0; floor=9.0; price=18.0; integration=4.0
    return dict(cash=cash, floor=floor, spendable=cash-floor,
                price=price, integration=integration, upfront_outlay=price+integration,
                post_cash=cash-price-integration,
                staged_upfront=11.0, staged_integration=3.5,
                staged_initial_spend=11+3.5, staged_cash=cash-11-3.5,
                contingent_earnout=7.0, target_arr=4.8,
                stated_multiple=price/4.8,
                cross_sell_base=2.4, cross_sell_stress=.8,
                synergies_gross_base=2.4*.8,
                synergies_gross_stress=.8*.8,
                incremental_opex=.85,
                synergy_base_net=2.4*.8-.85,
                synergy_stress_net=.8*.8-.85,
                churn=.21, customer_base=310,
                organic_build=3.4, organic_2028_arr=1.3,
                organic_net_2028=1.3*.8-.4,
                renewal_threshold=.85)


def c8():
    return dict(east=200000, central=160000, west=140000,
                fixed_east=1.30, fixed_central=1.80, fixed_west=1.20,
                east_cost=8, central_to_east=13, east_to_partner=11,
                east_keep_cost=200000*8/1e6+1.30,
                east_close_cost=200000*13/1e6,
                east_partner_cost=200000*11/1e6+.85,
                capacity_central=360000, capacity_after_close=360000,
                central_load_after_close=160000+200000,
                east_growth=0.10, central_growth=.06,
                central_2028_demand=160000*1.06+200000*1.10,
                current_sla=.96, modeled_close_sla=.84, modeled_partner_sla=.93,
                minimum_sla=.92, exit_penalty=.75,
                handling_damage_increment=.20,
                gross_transport_delta=(13-8)*200000/1e6,
                modeled_net_save=1.3-(13-8)*200000/1e6-.20,
                partner_commitment=.85)


def c9():
    forecast=[8.3,9.6,11.2,12.4]
    practical=10.0*.90
    overflow=[max(0,x-practical) for x in forecast]
    return dict(forecast=forecast, overflow=overflow, current_nameplate=10.,
                practical_capacity=practical, line_capex=4.8, deposit=.6,
                cash=11.0, r_and_d=2.2, liquidity_floor=7.,
                cash_after_now=11-2.2-4.8,
                cash_after_slot=11-2.2-.6,
                outsourcing_premium=.12,
                overflow_2028_cost=overflow[1]*.12,
                overflow_2029_cost=overflow[2]*.12,
                line_annual_fixed=.55,
                line_margin_per_unit=.45,
                line_2029_contribution=overflow[2]*.45-.55,
                expected_2028_orders=9.6,
                signed_2028_orders=8.5,
                contract_min_fill=.98,
                partner_capacity=2.5, partner_lead_months=5)


def c10():
    skus={
        'A':(14.,7.,1.2),'B':(9.,5.2,1.2),
        'C':(6.,2.2,3.3),'D':(4.,2.,.8)
    }
    reported={s:round((r-v-f)/r,4) for s,(r,v,f) in skus.items()}
    contribution={s:round(r-v,3) for s,(r,v,f) in skus.items()}
    return dict(skus=skus,reported_margins=reported,direct_contribution=contribution,
                c_shared_alloc=3.3, c_avoidable=.4, c_lost_contrib=3.8,
                transferred_revenue=6*.25,
                transferred_contrib=6*.25*.50,
                closure_penalty=2.1,
                closure_operating_delta=.4 + 6*.25*.5-3.8,
                closure_first_year_delta=.4 + 6*.25*.5-3.8-2.1,
                service_contracts=14, contracted_bundles=9,
                retention_above_min=.91, required_bundle_fill=.95,
                candidate_redesign_cost=.55,
                redesign_savings=1.25,
                redesigned_net_gain=1.25-.55)


def c11():
    units=[5000,10000,14000]
    fee_per_robot=300
    nominal=[u*fee_per_robot/1e6 for u in units]
    downside=[u*.65*fee_per_robot/1e6 for u in units]
    guarantee=2.0
    return dict(units=units, fee=fee_per_robot, nominal_royalties=nominal,
                downside_royalties=downside,
                guarantee=guarantee, first_year_cash=2.0,
                second_year_cash=max(0, nominal[0]+nominal[1]-guarantee),
                second_year_downside_cash=max(0, downside[0]+downside[1]-guarantee),
                support_per_robot=80,
                oem_annual_support=.9,
                direct_arr_at_risk=1.8, direct_gross_margin=.82,
                direct_profit_at_risk=1.8*.82,
                royalty_net_2028=nominal[1]-10000*80/1e6-.9,
                royalty_downside_net_2028=downside[1]-6500*80/1e6-.9,
                regulatory_audit_cost=.45,
                current_cash=4.9, floor=2.6,
                potential_pilot_units=1200, pilot_support_budget=.22)

MODELS={f'c{i}':globals()[f'c{i}'] for i in range(6,12)}
if __name__ == '__main__':
    import json
    print(json.dumps({k:v() for k,v in MODELS.items()},indent=2))
