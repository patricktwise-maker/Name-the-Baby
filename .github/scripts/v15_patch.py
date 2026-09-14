from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
changed = False

# Attribution helpers
marker = '''function liveBallotUrl(code){
  const u=new URL(ballotBaseUrl());
  u.searchParams.set("poll",code);
  return u.toString();
}'''
if 'function attributedShareUrl(' not in text:
    insert = marker + '''
function makeShareId(){
  try{return crypto.randomUUID().replace(/-/g,"").slice(0,16);}catch(e){return `${Date.now().toString(36)}${Math.random().toString(36).slice(2,8)}`;}
}
function attributedShareUrl(rawUrl,source,shareId=makeShareId()){
  const u=new URL(rawUrl,PUBLIC_SITE_ORIGIN);
  u.searchParams.set("src",source);
  u.searchParams.set("sid",shareId);
  return {url:u.toString(),shareId};
}
function landingAttribution(){
  const u=new URL(location.href);
  const source=(u.searchParams.get("src")||"").slice(0,32);
  const shareId=(u.searchParams.get("sid")||"").replace(/[^a-zA-Z0-9_-]/g,"").slice(0,40);
  return {source,share_id:shareId};
}'''
    if marker not in text:
        raise RuntimeError('liveBallotUrl marker not found')
    text = text.replace(marker, insert, 1)
    changed = True

# Name sharing
old = '''async function share(){
  if(!state.current)return;
  const sur=$("surname").value.trim();
  const text=`What do you think of ${state.current.name}${sur?" "+sur:""}? I found it on Name the Baby.`;
  try{
    if(navigator.share){await navigator.share({title:"Name the Baby",text});}
    else{await navigator.clipboard.writeText(text);toast("Name copied to clipboard");}
  }catch(e){}
}'''
new = '''async function share(){
  if(!state.current)return;
  const sur=$("surname").value.trim();
  const copy=`What do you think of ${state.current.name}${sur?" "+sur:""}? I found it on Name the Baby.`;
  const shared=attributedShareUrl(`${PUBLIC_SITE_ORIGIN}/`,"name_share");
  try{
    if(navigator.share)await navigator.share({title:"Name the Baby",text:copy,url:shared.url});
    else{await navigator.clipboard.writeText(`${copy}\\n${shared.url}`);toast("Name and link copied");}
    logEvent("name_shared",{source:"name_share",share_id:shared.shareId});
  }catch(e){}
}'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Ballot-copy sharing
old = '''async function copyBallotLink(){
  const url=await getShareUrl();if(!url){toast("Save at least two names first");return;}
  try{await navigator.clipboard.writeText(url);toast(initBackend()?"Live ballot link copied":"Demo ballot link copied");}catch(e){$("shareUrlPreview").textContent=url;$("shareUrlPreview").classList.add("show");toast("Use the link shown below");}
}'''
new = '''async function copyBallotLink(){
  const rawUrl=await getShareUrl();if(!rawUrl){toast("Save at least two names first");return;}
  const shared=attributedShareUrl(rawUrl,"ballot_share");
  try{await navigator.clipboard.writeText(shared.url);toast(initBackend()?"Live ballot link copied":"Demo ballot link copied");logEvent("ballot_shared",{live:initBackend(),source:"ballot_share",share_id:shared.shareId});}
  catch(e){$("shareUrlPreview").textContent=shared.url;$("shareUrlPreview").classList.add("show");toast("Use the link shown below");}
}'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Native ballot sharing
old = '''async function nativeShareBallot(){
  const data=currentBallotData(),url=await getShareUrl();if(!url){toast("Save at least two names first");return;}
  const who=data.family?`${data.family} need your help`:"We need your help";const text=`${who} choosing a baby name. Vote for your favorite on Name the Baby.`;
  try{if(navigator.share)await navigator.share({title:"Help Us Name the Baby",text,url});else{await navigator.clipboard.writeText(`${text}\\n${url}`);toast("Ballot link copied");}}catch(e){}
}'''
new = '''async function nativeShareBallot(){
  const data=currentBallotData(),rawUrl=await getShareUrl();if(!rawUrl){toast("Save at least two names first");return;}
  const shared=attributedShareUrl(rawUrl,"ballot_share");
  const who=data.family?`${data.family} need your help`:"We need your help";const copy=`${who} choosing a baby name. Vote for your favorite on Name the Baby.`;
  try{if(navigator.share)await navigator.share({title:"Help Us Name the Baby",text:copy,url:shared.url});else{await navigator.clipboard.writeText(`${copy}\\n${shared.url}`);toast("Ballot link copied");}logEvent("ballot_shared",{live:initBackend(),source:"ballot_share",share_id:shared.shareId});}catch(e){}
}'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Share after voting
old = '''async function shareBallotVote(){
  if(!activeBallotVote||!activeBallot)return;const family=activeBallot.family?` for ${activeBallot.family}`:"";const text=`I voted ${activeBallotVote}${family}. Cast your vote on Name the Baby.`;const url=activeBallot.live?liveBallotUrl(activeBallot.code):location.href;
  try{if(navigator.share)await navigator.share({title:"Help Us Name the Baby",text,url});else{await navigator.clipboard.writeText(`${text}\\n${url}`);toast("Vote and ballot link copied");}logEvent("ballot_shared",{live:Boolean(activeBallot.live)});}catch(e){}
}'''
new = '''async function shareBallotVote(){
  if(!activeBallotVote||!activeBallot)return;const family=activeBallot.family?` for ${activeBallot.family}`:"";const copy=`I voted ${activeBallotVote}${family}. Cast your vote on Name the Baby.`;const rawUrl=activeBallot.live?liveBallotUrl(activeBallot.code):location.href;const shared=attributedShareUrl(rawUrl,"vote_share");
  try{if(navigator.share)await navigator.share({title:"Help Us Name the Baby",text:copy,url:shared.url});else{await navigator.clipboard.writeText(`${copy}\\n${shared.url}`);toast("Vote and ballot link copied");}logEvent("ballot_shared",{live:Boolean(activeBallot.live),source:"vote_share",share_id:shared.shareId});}catch(e){}
}'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Landing attribution
old = 'logEvent("ballot_view",{option_count:(data.options||[]).length,code_present:true});'
new = 'logEvent("ballot_view",{option_count:(data.options||[]).length,code_present:true,...landingAttribution()});'
if old in text:
    text = text.replace(old, new, 1)
    changed = True

old = '''const startupPoll=new URL(location.href).searchParams.get("poll")||location.hash.startsWith("#poll=");
logEvent("page_view",{mode:startupPoll?"poll":location.hash.startsWith("#vote=")?"demo_poll":"main"});'''
new = '''const startupPoll=new URL(location.href).searchParams.get("poll")||location.hash.startsWith("#poll=");
const landing=landingAttribution();
logEvent("page_view",{mode:startupPoll?"poll":location.hash.startsWith("#vote=")?"demo_poll":"main",source:landing.source||"direct",share_id:landing.share_id||""});'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Dashboard metric cards
marker = '''          <div class="owner-metric"><span>Sponsor inquiries</span><strong id="omSponsorInquiries">0</strong></div>
        </div>'''
if 'id="omReferredVisits"' not in text:
    replacement = '''          <div class="owner-metric"><span>Sponsor inquiries</span><strong id="omSponsorInquiries">0</strong></div>
          <div class="owner-metric"><span>Referred visits</span><strong id="omReferredVisits">0</strong></div>
          <div class="owner-metric"><span>Tracked shares</span><strong id="omTrackedShares">0</strong></div>
          <div class="owner-metric"><span>Shares creating visits</span><strong id="omSharesWithVisit">0</strong></div>
          <div class="owner-metric"><span>Ballots created</span><strong id="omBallotsCreated">0</strong></div>
        </div>'''
    if marker not in text:
        raise RuntimeError('Owner metric card marker not found')
    text = text.replace(marker, replacement, 1)
    changed = True

marker = '''          <div class="owner-conversion">Sponsor open to inquiry<b id="omSponsorRate">0%</b></div>
        </div>'''
if 'id="omReferralRate"' not in text:
    replacement = '''          <div class="owner-conversion">Sponsor open to inquiry<b id="omSponsorRate">0%</b></div>
          <div class="owner-conversion">Visit to generate<b id="omGenerateRate">0%</b></div>
          <div class="owner-conversion">Generate to save<b id="omGenerateSaveRate">0%</b></div>
          <div class="owner-conversion">Save to ballot<b id="omSaveBallotRate">0%</b></div>
          <div class="owner-conversion">Share to referred visit<b id="omReferralRate">0%</b></div>
        </div>'''
    if marker not in text:
        raise RuntimeError('Owner conversion marker not found')
    text = text.replace(marker, replacement, 1)
    changed = True

old = '''  $("omSponsorInquiries").textContent=ownerNum(c.sponsor_inquiries);
  $("omVoteRate").textContent=`${Number(v.ballot_view_to_vote_pct||0).toFixed(1)}%`;'''
new = '''  $("omSponsorInquiries").textContent=ownerNum(c.sponsor_inquiries);
  const g=data.growth||{};
  $("omReferredVisits").textContent=ownerNum(g.referred_visits);
  $("omTrackedShares").textContent=ownerNum(g.tracked_shares);
  $("omSharesWithVisit").textContent=ownerNum(g.shares_with_visit);
  $("omBallotsCreated").textContent=ownerNum(c.ballots_created);
  $("omVoteRate").textContent=`${Number(v.ballot_view_to_vote_pct||0).toFixed(1)}%`;'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

old = '''  $("omSponsorRate").textContent=`${Number(v.sponsor_open_to_inquiry_pct||0).toFixed(1)}%`;
  $("omSince").textContent=data.since?`Since ${new Date(data.since).toLocaleString()}`:"";'''
new = '''  $("omSponsorRate").textContent=`${Number(v.sponsor_open_to_inquiry_pct||0).toFixed(1)}%`;
  $("omGenerateRate").textContent=`${Number(v.visit_to_generate_pct||0).toFixed(1)}%`;
  $("omGenerateSaveRate").textContent=`${Number(v.generate_to_save_pct||0).toFixed(1)}%`;
  $("omSaveBallotRate").textContent=`${Number(v.save_to_ballot_pct||0).toFixed(1)}%`;
  $("omReferralRate").textContent=`${Number(v.share_to_visit_pct||0).toFixed(1)}%`;
  $("omSince").textContent=data.since?`Since ${new Date(data.since).toLocaleString()}`:"";'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

old = '''    [["Visits",day.visits],["Names",day.names],["Votes",day.votes],["Shares",day.shares]].forEach(([label,value])=>{const span=document.createElement("span");span.textContent=`${label}: ${value||0}`;row.appendChild(span);});'''
new = '''    [["Visits",day.visits],["Names",day.names],["Votes",day.votes],["Shares",day.shares],["Referrals",day.referrals]].forEach(([label,value])=>{const span=document.createElement("span");span.textContent=`${label}: ${value||0}`;row.appendChild(span);});'''
if old in text:
    text = text.replace(old, new, 1)
    changed = True

if 'V14 owner-metrics one-page build' in text:
    text = text.replace('V14 owner-metrics one-page build','V15 growth-analytics one-page build',1)
    changed = True

required = ['attributedShareUrl','landingAttribution','name_shared','share_id','omReferredVisits','omReferralRate']
missing = [x for x in required if x not in text]
if missing:
    raise RuntimeError(f'Missing V15 pieces after patch: {missing}')

if changed:
    path.write_text(text, encoding='utf-8')
    print('V15 growth analytics applied.')
else:
    print('V15 growth analytics already present.')
