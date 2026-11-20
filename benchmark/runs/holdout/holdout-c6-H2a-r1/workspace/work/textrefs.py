# Numbers each slide shows inside table or text cells (rendered as text so they keep the source's formatting).
# Used only to list them on the slide's sheet of the source workbook.
VOLS = ["v27", "v28p", "v29p", "v28c", "v29c"]
TEXT_REFS = {
    "3": ["caplim", "floor", "cash0", "vol_plan", "vol_cons", "otd_req", "v28p", "v28c", "lease49", "lease_s1"],
    "3b": ["gate73", "frt2", "buy75", "lease49", "lease_cpu1", "lease_cpu2", "own46", "own_cpu1", "own_cpu2", "tool025", "lease_up", "own_up",
           "own_eq", "own_inst", "lease_fix", "own_fix", "lease_s1", "s_later", "own_s1", "cap_buy", "cap_lease", "cap_own", "lt_lease", "lt_own", "resale"],
    "4": ["l_d_p", "l_share", "l_d_c", "caplim", "floor", "lease_up", "cash_lease", "otd_req", "otd", "lease_s1", "demo", "own_up", "o_d_p"],
    "5": ["caplim", "floor", "tool025", "cash_buy", "lease_up", "cash_lease", "own_up", "cash_own", "l_d_p", "l_share", "l_d_c", "o_d_p", "o_d_c",
          "resale", "otd_req", "otd", "own_s1", "lt_lease", "price_gap", "own_pb_vol", "own_cap2", "sens_7pr", "sens_7fy"],
    "6": ["own_sav_ops", "sav_ss_unit", "fix_pu100", "sav_ss_net", "ann_cfo", "ann100", "ann65", "proc75"],
    "7": ["cash_own_pay", "demo", "own_s1", "lt_own", "buy27", "buf"],
    "8": ["buy75", "l_pu_p", "l_pu_c", "o_pu_p", "o_pu_c", "on_pu_p", "on_pu_c", "lease49", "lease_cpu1", "lease_cpu2", "lease_fix", "lfix_be", "own_up", "resale", "l_d_p", "l_d_c"],
    "9": ["be_vol", "vol2829p", "be_p", "be_c", "buy75", "price_gap", "l27_7pr", "l27_7fy", "lsav27"],
    "10": ["otd", "otd_req", "late_units", "res40", "emg88", "notice_res", "lt_lease", "lt_own"],
    "11": ["buf", "buf_wks", "buf_units", "wk_units", "wks50", "tool025", "split25", "res40", "notice_res", "emg88", "notice_emg", "emg_frt", "emg_prem",
           "mon_units", "emg_month", "lease_up", "lease_fix", "l_d_c", "emg_months", "otd_req"],
    "12": ["head_buy", "head_trig", "cap_share", "d_per1", "floor", "caplim"],
    "13": ["p3", "lease_s1", "demo", "t1", "be_vol", "vol2829p", "vol2829c", "t2a", "t2b", "be_p", "be_c", "buy75", "otd_req", "otd", "own_up", "caplim",
           "cap_own", "s_later", "dec12", "lt_own", "lt_lease"],
    "14": ["tool025", "res40", "buf_wks", "split25", "buf"],
    "15": ["d_per1", "t2a", "otd_req", "cap_buy", "l_d_c", "o_d_c", "buy75", "carry_rate", "carry"],
    "A1": ["buy27", "buy28p", "buy29p", "buy_tot_p", "l27", "l28p", "l29p", "lease_up", "l_tot_p", "l_d_p", "l_pu_p", "o27", "o28p", "o29p", "own_up",
           "o_tot_p", "o_d_p", "o_pu_p", "own_up_net", "on_tot_p", "on_d_p", "on_pu_p", "buy28c", "buy29c", "buy_tot_c", "l28c", "l29c", "l_tot_c",
           "l_d_c", "l_pu_c", "o28c", "o29c", "o_tot_c", "o_d_c", "o_pu_c", "on_tot_c", "on_d_c", "on_pu_c", "resale"] + VOLS,
    "A2": ["gate73", "frt2", "lease49", "lease_s1", "s_later", "lease_fix", "lease_up", "own46", "own_s1", "own_fix", "own_up", "resale"] + VOLS +
          ["l27", "o28p", "cash0", "cash_own", "cash_lease", "buy27", "be_vol", "lsav27", "lease_cpu2", "buy75", "be_p", "be_c", "l_tot_p", "l_tot_c", "vol2829p", "vol2829c"],
    "B1": ["gate73", "frt2", "buy75", "emg88", "emg_frt", "cash0", "buf", "lt_lease", "lt_own"],
    "B2": ["lease_up", "caplim", "tool025", "buf_wks", "wk_units", "wks50", "demo", "own_s1"],
    "C": ["own46", "buy75", "own_fix", "own_up", "o_pu_p", "cfo27", "frt2", "own_s1", "sav27", "pb100", "pb65", "v28p", "v28c", "demo", "lt_own", "lt_lease"],
}
