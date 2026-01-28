"""
# --- PATCH 1: RESET V28 WAR ROOM INPUTS/RESULTS FOR NEXT YEAR ---
"""

if st.button("Finish Recruiting & Advance Season →", type="primary"):
    grade, score, breakdown = compute_recruiting_class_grade()
    last_hist = st.session_state.history[-1] if st.session_state.history else None
    if last_hist and safe_int(last_hist.get("Year", 0), 0) == year:
        last_hist["RecruitingGrade"] = grade
    
    add_news(f"Recruiting class grade: {grade} ({score} pts)")
    st.session_state.year += 1
    st.session_state.tenure += 1
    st.session_state.inflation = safe_float(st.session_state.get("inflation", 1.0), 1.0) * 1.02
    OpponentManager.evolve_universe()
    
    invite = maybe_generate_conference_invite()
    if not invite:
        ai_conference_swap_lightweight()
        
    st.session_state.schedule = engine_generate_schedule(
        st.session_state.team_name, 
        st.session_state.team_conf, 
        st.session_state.team_rival
    )
    st.session_state.week_index = 0
    st.session_state.record = {"w": 0, "l": 0}
    st.session_state.season_logs = []
    st.session_state.season_simulated = False
    st.session_state.season_end_ready = False
    st.session_state.revenue_report = None
    st.session_state.nil_class = []
    st.session_state.hs_total_spend = 0

    # --- RESET V28 WAR ROOM INPUTS/RESULTS FOR NEXT YEAR ---
    st.session_state.hs_last_results = None
    for p in POSITIONS:
        st.session_state[f"hs_pos_input_{p}_v28"] = 0

    st.session_state.hs_alloc_by_pos = {p: 0 for p in POSITIONS}
    st.session_state.top8 = []
    st.session_state.top8_resolved = set()
    st.session_state.offseason_step = 1
    st.session_state.team_needs = compute_team_needs(st.session_state.roster, k=3)
    st.session_state.hotspots = generate_hotspots()
    sync_team_ratings()

    st.session_state.recruiting_summary = {"grade": grade, "score": score, "breakdown": breakdown}
    st.session_state.game_state = "RECRUITING_WRAP"
    st.rerun()


# --- PATCH 2: PREVENT HS WAR ROOM SKIPPING ---

if step == 2:
    # V28: New bottom-up HS recruiting
    show_offseason_hs_outreach()
    st.divider()

    block_continue = st.session_state.get("hs_last_results") is not None
    if st.button("Continue to Top-8 Battles →", type="primary", disabled=block_continue):
        st.session_state.offseason_step = 3
        st.rerun()

    if block_continue:
        st.info("Dismiss HS Outreach results above to continue.")