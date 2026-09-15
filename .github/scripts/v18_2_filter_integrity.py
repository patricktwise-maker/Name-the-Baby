from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = '''function generate(forceAny=false){
  let pool=forceAny?names:eligible();
  if(!pool.length){
    toast("No exact match. Loosening the filters.");
    pool=names.filter(n=>state.gender==="any"||n.gender===state.gender||n.gender==="unisex");
  }
  state.current=pick(pool);
  if(state.current){state.shown.add(state.current.name);rememberRecentName(state.current.name);}
  renderResult();
  if(state.current)logEvent("name_generated",{gender:state.current.gender,profile:state.current.profileLevel||"curated",popularity:recentPopularityBand(state.current)});
}'''

new = '''// V18.2 strict generator filter integrity.
// Explicit user filters are never silently discarded. If no exact record matches,
// the generator asks the user to broaden a filter instead of showing a conflicting name.
function renderNoExactMatch(){
  state.current=null;
  $("result").classList.remove("show");
  const empty=$("emptyState");
  const first=$("initial").value;
  const origin=$("origin").value;
  const details=[];
  if(first)details.push(`starts with ${first}`);
  if(origin)details.push(origin);
  empty.style.display="grid";
  empty.innerHTML=`<div><div class="empty-icon">↺</div><strong>No exact match yet.</strong>${details.length?`We don't currently have a name that matches <b>${details.join(" + ")}</b> together with every other filter you selected.`:`We don't currently have a name that matches every filter you selected.`}<div class="data-note">Try broadening one filter. Your selected letter and origin will never be silently ignored.</div></div>`;
}
function generate(forceAny=false){
  const pool=forceAny?names:eligible();
  if(!pool.length){
    renderNoExactMatch();
    toast("No exact match. Try broadening one filter.");
    logEvent("generator_no_match",{has_initial:!!$("initial").value,has_origin:!!$("origin").value,has_style:state.style!=="any",has_gender:state.gender!=="any"});
    return;
  }
  state.current=pick(pool);
  if(state.current){state.shown.add(state.current.name);rememberRecentName(state.current.name);}
  renderResult();
  if(state.current)logEvent("name_generated",{gender:state.current.gender,profile:state.current.profileLevel||"curated",popularity:recentPopularityBand(state.current)});
}'''

if new in text:
    print('V18.2 filter-integrity patch already present.')
elif old in text:
    text = text.replace(old, new, 1)
    path.write_text(text, encoding='utf-8')
    print('Applied V18.2 strict generator filter-integrity patch.')
else:
    raise SystemExit('Expected generator fallback block was not found; refusing to patch an unknown build.')
