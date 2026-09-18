from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Give users and crawlers a compact, descriptive path from the hero to the major
# discovery intents already supported on this single page.
hero_actions = '''      <div class="hero-actions">
        <button class="ghost-link" id="surpriseTop">Surprise me</button>
        <button class="ghost-link" id="jumpLab">Create a unique name</button>
        <button class="ghost-link" id="jumpSaved">View my shortlist</button>
      </div>'''
intent_nav = hero_actions + '''
      <nav class="intent-nav" aria-label="Explore baby names">
        <a href="#namesByGender">Boy, girl & unisex names</a>
        <a href="#namesByOrigin">Names by origin</a>
        <a href="#namesByLetter">Names A–Z</a>
        <a href="#namesByStyle">Unique & distinctive names</a>
        <a href="#namesWithMeaning">Names with meanings</a>
      </nav>'''
if 'class="intent-nav"' not in text:
    if hero_actions not in text:
        raise SystemExit('Hero actions block not found')
    text = text.replace(hero_actions, intent_nav, 1)

# Add useful calls back into the actual generator instead of leaving the SEO
# discovery copy as a dead-end reading block.
text = text.replace(
    '<div class="seo-note"><b>About the data:</b>',
    '<p class="seo-cta"><a href="#generator">Use the baby name generator with these filters</a> or <a href="#creationLab">create a unique baby name</a>.</p>\n      <div class="seo-note"><b>About the data:</b>',
    1
) if 'class="seo-cta"' not in text else text

# Styling remains lightweight and responsive, preserving the one-page design.
css_anchor = '    .hero-actions{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:18px}\n'
css_add = css_anchor + '''    .intent-nav{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:12px auto 0;max-width:860px}
    .intent-nav a{color:var(--muted);font-size:.76rem;font-weight:800;text-decoration:none;border-bottom:1px solid transparent;padding:5px 3px}
    .intent-nav a:hover,.intent-nav a:focus{color:var(--ink);border-color:var(--rose)}
'''
if '.intent-nav{' not in text:
    if css_anchor not in text:
        raise SystemExit('Hero CSS anchor not found')
    text = text.replace(css_anchor, css_add, 1)

seo_css = '    .seo-note{margin:14px 0 0;padding:12px 14px;border:1px solid #d8ebe7;background:#f5fbfa;border-radius:14px;color:#55706c;font-size:.8rem;line-height:1.55}\n'
seo_css_add = seo_css + '''    .seo-cta{margin:14px 0 0;font-size:.84rem;font-weight:800}
    .seo-cta a{color:var(--rose-deep);text-underline-offset:3px}
'''
if '.seo-cta{' not in text:
    if seo_css not in text:
        raise SystemExit('SEO CSS anchor not found')
    text = text.replace(seo_css, seo_css_add, 1)

# Add a modest SearchAction description only if there is a genuine URL-based
# search endpoint. There is not one today, so intentionally do NOT fabricate it.

marker = '<!-- V19.2 SEO: descriptive intent navigation + internal discovery links -->'
if marker not in text:
    text = text.replace('</head>', f'  {marker}\n</head>', 1)

p.write_text(text, encoding='utf-8')
