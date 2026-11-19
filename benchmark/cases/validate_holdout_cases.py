"""Sanity checks for six independent synthetic cases, their keys and computed numbers."""
from __future__ import annotations
import json
import math
from collections import Counter
from pathlib import Path
from holdout_models import MODELS
from build_holdout_cases import CASES, CASE_META

BASE=Path(__file__).resolve().parent
KEYS=BASE.parent/'answer_keys'
EXPECTED={'c6':'reject','c7':'revise','c8':'keep_with_conditions',
          'c9':'keep_with_conditions','c10':'reject','c11':'revise'}
REQUIRED={'case_id','title','decision_question','initial_hypothesis','key_insights',
          'required_calculations','decision_relevant_evidence','contradictory_evidence',
          'reasoning_traps','key_tradeoffs','plausible_recommendations',
          'defensibility_criteria','decision_requirements'}

def close(x,y,tol=1e-8):
    assert math.isclose(x,y,abs_tol=tol),f'{x}!={y}'

def test_models():
    m={k:v() for k,v in MODELS.items()}
    a=m['c6'];close(a['build_cash_post'],1.9);close(a['build_capex'],7.3)
    close(a['outsource_cost'][1],7.5)
    close(a['build_total'],sum(a['build_op'])+a['build_capex'])
    close(a['lease_total'],sum(a['lease_op'])+a['lease_setup'])
    b=m['c7'];close(b['post_cash'],2.0);close(b['staged_cash'],9.5)
    close(b['stated_multiple'],3.75);close(b['synergy_base_net'],1.07)
    c=m['c8'];close(c['central_2028_demand'],389600.)
    close(c['modeled_net_save'],.1)
    close((200*.84+160*.94+140*.95)/500,.9028)
    d=m['c9'];close(d['cash_after_now'],4.0);close(d['cash_after_slot'],8.2)
    close(d['overflow_2028_cost'],.072);close(d['overflow_2029_cost'],.264)
    e=m['c10'];close(e['direct_contribution']['C'],3.8)
    close(e['closure_operating_delta'],-2.65)
    close(e['closure_first_year_delta'],-4.75)
    f=m['c11'];close(f['second_year_cash'],2.5)
    close(f['royalty_net_2028'],1.30)
    close(f['royalty_downside_net_2028'],.53)

def test_content():
    found={}
    for slug in CASES:
        cid=slug.split('-')[0]
        p=(BASE/slug/'packet.md').read_text()
        k=json.loads((KEYS/f'{slug}.json').read_text())
        calc=json.loads((KEYS/f'{slug}.calc.json').read_text())
        words=len(p.split()); assert 800<=words<=1600,(cid,words)
        assert REQUIRED<=set(k),(cid,REQUIRED-set(k))
        assert k['case_id']==cid and cid in MODELS
        assert calc['case_id']==cid and calc['deterministic_model']==json.loads(json.dumps(MODELS[cid]()))
        assert k['initial_hypothesis']['expected_handling']==EXPECTED[cid]
        assert len(k['decision_requirements'])>=3
        for r in k['decision_requirements']:
            assert r['question'] and isinstance(r['critical'],bool) and r['acceptable_evidence']
        assert len(k['required_calculations'])>=4
        assert all('expected' in q and 'tolerance' in q for q in k['required_calculations'])
        assert len(k['plausible_recommendations'])>=3
        assert len(k['reasoning_traps'])>=3
        assert all(not s.startswith('EVALUATOR ONLY') for s in p.splitlines())
        found[cid]=words
    assert len(CASE_META)==6
    assert Counter(EXPECTED.values())==Counter({'reject':2,'revise':2,'keep_with_conditions':2})
    return found

if __name__=='__main__':
    test_models()
    print('PASS: model arithmetic; six packets; key schema; distinct hypothesis handling; case metadata')
    print('word counts:',test_content())
