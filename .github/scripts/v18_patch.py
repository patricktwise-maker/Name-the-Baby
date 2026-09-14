from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
changed = False

def replace_once(old, new, label):
    global text, changed
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f'Missing V18 anchor: {label}')
    text = text.replace(old, new, 1)
    changed = True

# Styles for partner disclosures and CTA links.
css_anchor = '    .monetize-cta{flex:0 0 auto;border:1px solid var(--line);background:#fff;border-radius:12px;padding:9px 11px;font-size:.74rem;font-weight:900;cursor:pointer}\n'
css_new = css_anchor + '''    a.monetize-cta{display:inline-block;text-decoration:none;color:var(--ink);text-align:center}\n    .partner-action{flex:0 0 auto;display:flex;flex-direction:column;gap:6px;align-items:stretch}\n    .partner-disclosure{margin-top:6px;font-size:.66rem;line-height:1.4;color:#8a7f86;max-width:520px}\n    .partner-disclosure b{color:#675d65}\n'''
replace_once(css_anchor, css_new, 'partner styles')

# Existing name-result partner card becomes a configurable slot with a safe fallback.
old_name_card = '''          <div class="monetize-card" id="namePartnerCard">\n            <div class="monetize-copy"><b id="namePartnerTitle">Personalize this name</b><span>Reserved for a tasteful partner offer such as a nursery sign, blanket, keepsake, or registry item.</span></div>\n            <button class="monetize-cta" id="namePartnerBtn">PARTNER WITH US</button>\n          </div>'''
new_name_card = '''          <div class="monetize-card" id="namePartnerCard" data-partner-slot="name_personalization">\n            <div class="monetize-copy"><b id="namePartnerTitle">Personalize this name</b><span id="namePartnerBody">Reserved for a tasteful partner offer such as a nursery sign, blanket, keepsake, or registry item.</span><div class="partner-disclosure" id="namePartnerDisclosure" hidden></div></div>\n            <div class="partner-action"><a class="monetize-cta" id="namePartnerLink" href="#" target="_blank" rel="sponsored noopener noreferrer" hidden>VIEW OFFER</a><button class="monetize-cta" id="namePartnerBtn">PARTNER WITH US</button></div>\n          </div>'''
replace_once(old_name_card, new_name_card, 'name partner card')

# Shortlist partner slot, hidden unless an approved active offer exists.
shortlist_anchor = '      <div class="battle" id="battle">\n'
shortlist_slot = '''      <div class="monetize-card" id="shortlistPartnerCard" data-partner-slot="shortlist">\n        <div class="monetize-copy"><b id="shortlistPartnerTitle"></b><span id="shortlistPartnerBody"></span><div class="partner-disclosure" id="shortlistPartnerDisclosure" hidden></div></div>\n        <div class="partner-action"><a class="monetize-cta" id="shortlistPartnerLink" href="#" target="_blank" rel="sponsored noopener noreferrer" hidden>VIEW OFFER</a></div>\n      </div>\n''' + shortlist_anchor
replace_once(shortlist_anchor, shortlist_slot, 'shortlist partner slot')

# Post-vote partner slot, hidden unless an approved active offer exists.
post_vote_anchor = '''        <div class="ballot-actions">\n          <button class="btn keep" id="shareVoteBtn">SHARE MY VOTE</button>\n          <button class="btn" id="startMyOwnBtn">NAME MY OWN BABY</button>\n        </div>\n'''
post_vote_new = post_vote_anchor + '''        <div class="monetize-card" id="postVotePartnerCard" data-partner-slot="post_vote">\n          <div class="monetize-copy"><b id="postVotePartnerTitle"></b><span id="postVotePartnerBody"></span><div class="partner-disclosure" id="postVotePartnerDisclosure" hidden></div></div>\n          <div class="partner-action"><a class="monetize-cta" id="postVotePartnerLink" href="#" target="_blank" rel="sponsored noopener noreferrer" hidden>VIEW OFFER</a></div>\n        </div>\n'''
replace_once(post_vote_anchor, post_vote_new, 'post vote partner slot')

# Owner dashboard monetization cards.
owner_anchor = '''        <div class="owner-conversions">\n'''
owner_cards = '''        <div class="field-label" style="margin-top:14px"><span>Monetization</span><span class="optional">sponsor + affiliate readiness</span></div>\n        <div class="retention-grid">\n          <div class="retention-card"><span>Partner impressions</span><strong id="omPartnerImpressions">0</strong></div>\n          <div class="retention-card"><span>Partner clicks</span><strong id="omPartnerClicks">0</strong></div>\n          <div class="retention-card"><span>Partner CTR</span><strong id="omPartnerCtr">0%</strong></div>\n          <div class="retention-card"><span>Unique clickers</span><strong id="omPartnerClickers">0</strong></div>\n        </div>\n''' + owner_anchor
replace_once(owner_anchor, owner_cards, 'owner monetization cards')

# Privacy language includes aggregate partner interaction analytics.
privacy_old = 'the site may record privacy-light product events such as page views, generations, saves, passes, Lab use, ballot creation, and voting without sending surnames or exact generated-name choices in analytics.'
privacy_new = 'the site may record privacy-light product events such as page views, generations, saves, passes, Lab use, ballot creation, voting, and aggregate partner-offer impressions/clicks without sending surnames or exact generated-name choices in analytics.'
replace_once(privacy_old, privacy_new, 'privacy analytics copy')

# Terms disclose commercial relationships.
terms_old = '<p class="fineprint" style="font-size:.86rem">Meanings, origins, pronunciation, and popularity can vary by language, region, source, and time. Public-launch content should receive final editorial review and popularity data should identify its source and year.</p>'
terms_new = '<p class="fineprint" style="font-size:.86rem">Meanings, origins, pronunciation, and popularity can vary by language, region, source, and time. Public-launch content should receive final editorial review and popularity data should identify its source and year. Some clearly labeled partner links may be sponsored or affiliate links; Name the Baby may receive compensation or a commission when a visitor uses an eligible link.</p>'
replace_once(terms_old, terms_new, 'terms commercial disclosure')

# Footer version.
if 'V17 Google-discovery one-page build' in text:
    text = text.replace('V17 Google-discovery one-page build', 'V18 sponsor-and-affiliate-ready one-page build', 1)
    changed = True

# Partner runtime helpers. Insert before return-experience constants.
js_anchor = 'const NTB_RETURN_LAST_KEY="ntb16_last_visit_at";\n'
partner_js = r'''const partnerOfferCache=new Map();
const partnerImpressionSeen=new Set();
const PARTNER_SLOT_IDS={
  name_personalization:{card:"namePartnerCard",title:"namePartnerTitle",body:"namePartnerBody",disclosure:"namePartnerDisclosure",link:"namePartnerLink"},
  shortlist:{card:"shortlistPartnerCard",title:"shortlistPartnerTitle",body:"shortlistPartnerBody",disclosure:"shortlistPartnerDisclosure",link:"shortlistPartnerLink"},
  post_vote:{card:"postVotePartnerCard",title:"postVotePartnerTitle",body:"postVotePartnerBody",disclosure:"postVotePartnerDisclosure",link:"postVotePartnerLink"}
};
async function getPartnerOffer(slot){
  if(partnerOfferCache.has(slot))return partnerOfferCache.get(slot);
  if(!backendReady()){partnerOfferCache.set(slot,null);return null;}
  const {data,error}=await ntbRpc("get_partner_offer",{p_slot:slot});
  if(error||!data?.destination_url){partnerOfferCache.set(slot,null);return null;}
  try{const u=new URL(data.destination_url);if(u.protocol!=="https:")throw new Error("https required");}
  catch(e){partnerOfferCache.set(slot,null);return null;}
  partnerOfferCache.set(slot,data);return data;
}
function hidePartnerSlot(slot){
  const ids=PARTNER_SLOT_IDS[slot];if(!ids)return;
  if(slot==="name_personalization")return;
  $(ids.card)?.classList.remove("show");
}
async function renderPartnerSlot(slot){
  const ids=PARTNER_SLOT_IDS[slot];if(!ids)return;
  const offer=await getPartnerOffer(slot);
  if(!offer){hidePartnerSlot(slot);return;}
  const card=$(ids.card),title=$(ids.title),body=$(ids.body),disclosure=$(ids.disclosure),link=$(ids.link);
  if(!card||!title||!body||!disclosure||!link)return;
  title.textContent=offer.headline||offer.partner_name||"Partner offer";
  body.textContent=offer.body||"";
  disclosure.hidden=false;
  disclosure.textContent=(offer.relationship==="affiliate"?"Affiliate disclosure: ":"Sponsored placement: ")+(offer.disclosure||"Name the Baby may receive compensation from this partner.");
  link.textContent=offer.cta||"VIEW OFFER";
  link.href=offer.destination_url;
  link.hidden=false;
  if(slot==="name_personalization")$("namePartnerBtn").hidden=true;
  card.classList.add("show");
  const impressionKey=`${slot}:${offer.id}`;
  if(!partnerImpressionSeen.has(impressionKey)){
    partnerImpressionSeen.add(impressionKey);
    logEvent("partner_impression",{slot,relationship:offer.relationship||"unknown",partner_id:String(offer.id||"").slice(0,40)});
  }
}
function trackPartnerClick(slot){
  const offer=partnerOfferCache.get(slot);if(!offer)return;
  logEvent("partner_click",{slot,relationship:offer.relationship||"unknown",partner_id:String(offer.id||"").slice(0,40)});
}
Object.entries(PARTNER_SLOT_IDS).forEach(([slot,ids])=>{
  const link=$(ids.link);if(link)link.addEventListener("click",()=>trackPartnerClick(slot));
});
''' + js_anchor
replace_once(js_anchor, partner_js, 'partner runtime helpers')

# Render active name partner after each generated result. Fallback stays visible when no offer exists.
render_anchor = '  $("namePartnerTitle").textContent=`Personalize ${n.name}`;\n\n}'
render_new = '  $("namePartnerTitle").textContent=`Personalize ${n.name}`;\n  renderPartnerSlot("name_personalization");\n\n}'
replace_once(render_anchor, render_new, 'name partner render')

# Shortlist slot appears only when an active offer exists and there is a shortlist.
shortlist_js_anchor = '  if($("shareBuilder").classList.contains("show"))renderSharePreview();\n  renderBattleBoard();\n}'
shortlist_js_new = '  if($("shareBuilder").classList.contains("show"))renderSharePreview();\n  if(state.saved.length)renderPartnerSlot("shortlist");else $("shortlistPartnerCard")?.classList.remove("show");\n  renderBattleBoard();\n}'
replace_once(shortlist_js_anchor, shortlist_js_new, 'shortlist partner render')

# Show post-vote offer for prior voters and immediately after a vote.
prior_anchor = '  if(live&&hasPrior)startBallotSync();\n'
prior_new = '  if(live&&hasPrior)startBallotSync();\n  if(hasPrior)renderPartnerSlot("post_vote");\n'
replace_once(prior_anchor, prior_new, 'returning voter partner render')

vote_anchor = '  $("ballotAfter").classList.add("show");\n}\nasync function shareBallotVote(){'
vote_new = '  $("ballotAfter").classList.add("show");\n  renderPartnerSlot("post_vote");\n}\nasync function shareBallotVote(){'
replace_once(vote_anchor, vote_new, 'post vote partner render')

# Extend owner metrics with the separate protected monetization RPC.
owner_render_anchor = 'function clearOwnerMetricsAccess(){sessionStorage.removeItem(OWNER_METRICS_SESSION_KEY);$("ownerMetricsKey").value="";$("ownerDashboard").classList.remove("show");setOwnerStatus("Owner access cleared from this browser tab.");}\n'
owner_render_new = r'''function renderOwnerMonetization(data){
  if(!data?.ok)return;
  $("omPartnerImpressions").textContent=ownerNum(data.impressions);
  $("omPartnerClicks").textContent=ownerNum(data.clicks);
  $("omPartnerCtr").textContent=`${Number(data.partner_ctr_pct||0).toFixed(1)}%`;
  $("omPartnerClickers").textContent=ownerNum(data.unique_clickers);
}
''' + owner_render_anchor
replace_once(owner_render_anchor, owner_render_new, 'owner monetization renderer')

load_anchor = '  sessionStorage.setItem(OWNER_METRICS_SESSION_KEY,key);\n  renderOwnerMetrics(data);\n}'
load_new = '''  sessionStorage.setItem(OWNER_METRICS_SESSION_KEY,key);\n  renderOwnerMetrics(data);\n  const monetization=await ntbRpc("get_owner_monetization",{p_owner_key:key});\n  if(!monetization.error&&monetization.data?.ok)renderOwnerMonetization(monetization.data);\n}'''
replace_once(load_anchor, load_new, 'owner monetization load')

# Validation markers.
required = [
    'V18 sponsor-and-affiliate-ready one-page build',
    'get_partner_offer',
    'partner_impression',
    'partner_click',
    'rel="sponsored noopener noreferrer"',
    'Affiliate disclosure:',
    'get_owner_monetization',
    'id="omPartnerCtr"'
]
missing = [x for x in required if x not in text]
if missing:
    raise RuntimeError(f'Missing V18 pieces: {missing}')

if changed:
    path.write_text(text, encoding='utf-8')
    print('V18 sponsor and affiliate readiness patch applied.')
else:
    print('V18 patch already present.')
