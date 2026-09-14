from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
changed = False

# Retention panel styles
if '.return-panel{' not in text:
    marker = '    .owner-day b{color:var(--ink)}\n'
    css = '''    .return-panel{display:none;margin:0 0 20px;padding:17px 18px;border:1px solid #dfd8f0;background:linear-gradient(135deg,#fff,#f8f5ff);border-radius:20px;box-shadow:0 16px 40px rgba(67,47,58,.08)}\n    .return-panel.show{display:block;animation:pop .22s ease both}\n    .return-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}\n    .return-title{font-size:1.18rem;font-weight:950;letter-spacing:-.03em}\n    .return-copy{margin-top:4px;color:var(--muted);font-size:.82rem;line-height:1.45}\n    .return-close{border:0;background:transparent;color:var(--muted);font-size:1.15rem;cursor:pointer;padding:0 3px}\n    .return-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}\n    .return-actions .btn{flex:1 1 150px}\n    .return-recent{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}\n    .return-recent button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 10px;font-size:.72rem;font-weight:850;cursor:pointer}\n    .retention-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:12px}\n    .retention-card{border:1px solid #ded7ee;background:#faf8ff;border-radius:14px;padding:11px}\n    .retention-card span{display:block;color:var(--muted);font-size:.64rem;font-weight:850;text-transform:uppercase;letter-spacing:.05em}\n    .retention-card strong{display:block;font-size:1.25rem;margin-top:4px;letter-spacing:-.03em}\n    @media(max-width:700px){.retention-grid{grid-template-columns:repeat(2,1fr)}.return-top{gap:8px}.return-actions{display:grid;grid-template-columns:1fr}}\n'''
    if marker not in text:
        raise RuntimeError('CSS marker not found')
    text = text.replace(marker, marker + css, 1)
    changed = True

# Welcome-back panel before generator
if 'id="returnPanel"' not in text:
    marker = '    <section class="workspace" id="generator">\n'
    panel = '''    <section class="return-panel" id="returnPanel" aria-live="polite">\n      <div class="return-top">\n        <div><div class="return-title">Welcome back.</div><div class="return-copy" id="returnCopy">Your shortlist is still here on this device. Pick up where you left off.</div></div>\n        <button class="return-close" id="dismissReturn" aria-label="Dismiss welcome back">×</button>\n      </div>\n      <div class="return-actions">\n        <button class="btn keep" id="resumeShortlist">VIEW MY SHORTLIST</button>\n        <button class="btn" id="resumeExplore">KEEP EXPLORING</button>\n      </div>\n      <div class="return-recent" id="returnRecent"></div>\n    </section>\n\n'''
    if marker not in text:
        raise RuntimeError('Generator marker not found')
    text = text.replace(marker, panel + marker, 1)
    changed = True

# Owner retention cards
marker = '        <div class="owner-conversions">\n'
if 'id="omReturningVisitors"' not in text:
    retention_html = '''        <div class="retention-grid">\n          <div class="retention-card"><span>Returning visitors</span><strong id="omReturningVisitors">0</strong></div>\n          <div class="retention-card"><span>Return visits</span><strong id="omReturnVisits">0</strong></div>\n          <div class="retention-card"><span>Visitor return rate</span><strong id="omReturnRate">0%</strong></div>\n          <div class="retention-card"><span>Avg. return gap</span><strong id="omReturnGap">0h</strong></div>\n        </div>\n'''
    if marker not in text:
        raise RuntimeError('Owner conversion marker not found')
    text = text.replace(marker, retention_html + marker, 1)
    changed = True

# Recent-name helper and return experience
js_marker = 'function toast(msg){\n'
if 'function rememberRecentName(' not in text:
    js = '''const NTB_RETURN_LAST_KEY="ntb16_last_visit_at";\nconst NTB_RETURN_SESSION_KEY="ntb16_session_started";\nconst NTB_RECENT_NAMES_KEY="ntb16_recent_names";\nfunction recentNames(){try{return JSON.parse(localStorage.getItem(NTB_RECENT_NAMES_KEY)||"[]").filter(x=>typeof x==="string").slice(0,6);}catch(e){return [];}}\nfunction rememberRecentName(name){\n  if(!name)return;\n  const list=[name,...recentNames().filter(x=>x!==name)].slice(0,6);\n  localStorage.setItem(NTB_RECENT_NAMES_KEY,JSON.stringify(list));\n}\nfunction renderReturnRecent(){\n  const box=$("returnRecent");if(!box)return;box.textContent="";\n  recentNames().slice(0,4).forEach(name=>{const b=document.createElement("button");b.type="button";b.textContent=name;b.dataset.recentName=name;box.appendChild(b);});\n}\nfunction revisitRecentName(name){\n  const n=names.find(x=>x.name===name);if(!n)return;state.current=n;state.shown.add(n.name);renderResult();rememberRecentName(n.name);logEvent("recent_name_revisited",{recent_count:recentNames().length});$("generator").scrollIntoView({behavior:"smooth",block:"start"});\n}\nfunction initReturnExperience(){\n  const now=Date.now();\n  const prior=Number(localStorage.getItem(NTB_RETURN_LAST_KEY)||0);\n  const already=sessionStorage.getItem(NTB_RETURN_SESSION_KEY)==="1";\n  sessionStorage.setItem(NTB_RETURN_SESSION_KEY,"1");\n  localStorage.setItem(NTB_RETURN_LAST_KEY,String(now));\n  if(already||!prior)return;\n  const gapMs=now-prior;\n  if(gapMs<30*60*1000)return;\n  const u=new URL(location.href);if(u.searchParams.get("poll")||location.hash.startsWith("#poll=")||location.hash.startsWith("#vote="))return;\n  const gapHours=Math.round((gapMs/36e5)*10)/10;\n  const panel=$("returnPanel");if(!panel)return;\n  const savedCount=state.saved.length,recentCount=recentNames().length;\n  $("returnCopy").textContent=savedCount?`You still have ${savedCount} saved ${savedCount===1?"name":"names"} on this device. Pick up where you left off.`:recentCount?"Your recent names are still here on this device. Pick up where you left off.":"Ready for another round of names? Your preferences stay on this device.";\n  renderReturnRecent();panel.classList.add("show");\n  logEvent("return_visit",{gap_hours:gapHours,saved_count:savedCount,recent_count:recentCount});\n}\n'''
    if js_marker not in text:
        raise RuntimeError('Toast function marker not found')
    text = text.replace(js_marker, js + js_marker, 1)
    changed = True

# Remember generated names
old = '  if(state.current) state.shown.add(state.current.name);\n  renderResult();'
new = '  if(state.current){state.shown.add(state.current.name);rememberRecentName(state.current.name);}\n  renderResult();'
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Owner render additions
old = '  $("omBallotsCreated").textContent=ownerNum(c.ballots_created);\n  $("omVoteRate").textContent=`${Number(v.ballot_view_to_vote_pct||0).toFixed(1)}%`;'
new = '  $("omBallotsCreated").textContent=ownerNum(c.ballots_created);\n  const r=data.retention||{};\n  $("omReturningVisitors").textContent=ownerNum(r.returning_visitors);\n  $("omReturnVisits").textContent=ownerNum(r.return_visits);\n  $("omReturnRate").textContent=`${Number(r.visitor_return_rate_pct||0).toFixed(1)}%`;\n  $("omReturnGap").textContent=`${Number(r.avg_gap_hours||0).toFixed(1)}h`;\n  $("omVoteRate").textContent=`${Number(v.ballot_view_to_vote_pct||0).toFixed(1)}%`;'
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Daily returns in owner panel
old = '[["Visits",day.visits],["Names",day.names],["Votes",day.votes],["Shares",day.shares],["Referrals",day.referrals]]'
new = '[["Visits",day.visits],["Names",day.names],["Votes",day.votes],["Shares",day.shares],["Referrals",day.referrals],["Returns",day.returns]]'
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Return panel interactions
marker = '$("ownerMetricsBtn").addEventListener("click",()=>{const key=ownerMetricsKey();if(key){$("ownerMetricsKey").value=key;loadOwnerMetrics();}});\n'
if 'resumeShortlist").addEventListener' not in text:
    events = '''$("resumeShortlist").addEventListener("click",()=>{$("returnPanel").classList.remove("show");$("savedArea").scrollIntoView({behavior:"smooth",block:"start"});logEvent("resume_shortlist",{saved_count:state.saved.length});});\n$("resumeExplore").addEventListener("click",()=>{$("returnPanel").classList.remove("show");$("generator").scrollIntoView({behavior:"smooth",block:"start"});logEvent("resume_explore",{recent_count:recentNames().length});});\n$("dismissReturn").addEventListener("click",()=>{$("returnPanel").classList.remove("show");logEvent("return_panel_dismissed",{});});\n$("returnRecent").addEventListener("click",e=>{const name=e.target?.dataset?.recentName;if(name)revisitRecentName(name);});\n'''
    if marker not in text:
        raise RuntimeError('Owner event marker not found')
    text = text.replace(marker, marker + events, 1)
    changed = True

# Initialize retention before page-view logging
marker = 'renderBackendStatus();\nconst startupPoll='
if 'initReturnExperience();\nconst startupPoll=' not in text:
    if marker not in text:
        raise RuntimeError('Startup marker not found')
    text = text.replace(marker, 'renderBackendStatus();\ninitReturnExperience();\nconst startupPoll=', 1)
    changed = True

if 'V15 growth-analytics one-page build' in text:
    text = text.replace('V15 growth-analytics one-page build','V16 retention one-page build',1)
    changed = True

required = ['returnPanel','initReturnExperience','return_visit','resume_shortlist','recent_name_revisited','omReturningVisitors','omReturnRate']
missing = [x for x in required if x not in text]
if missing:
    raise RuntimeError(f'Missing V16 pieces after patch: {missing}')

if changed:
    path.write_text(text, encoding='utf-8')
    print('V16 retention experience applied.')
else:
    print('V16 retention experience already present.')
