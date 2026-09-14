from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
changed = False

TITLE = 'Baby Name Generator, Creator & Family Poll | Name the Baby'
DESC = 'Find boy, girl and unisex baby names with meanings, popularity filters and surname previews. Create unique names, save favorites and share a family poll.'
OG_DESC = 'Explore 1,500+ baby names, create unique names, preview them with a surname, save favorites, and share a live family baby-name poll.'

# Search title and descriptions.
replacements = {
    '<title>Name the Baby</title>': f'<title>{TITLE}</title>',
    '<meta name="description" content="Name the Baby is a one-page baby name finder and creation lab with smart recommendations, live family voting, custom names, saved favorites, and Name Battle." />': f'<meta name="description" content="{DESC}" />',
    '<meta property="og:title" content="Name the Baby" />': f'<meta property="og:title" content="{TITLE}" />',
    '<meta property="og:description" content="One tiny human. One very big decision. Explore 1,500+ names, create new ones, shortlist favorites, and share a family ballot." />': f'<meta property="og:description" content="{OG_DESC}" />',
    '<meta name="twitter:title" content="Name the Baby" />': f'<meta name="twitter:title" content="{TITLE}" />',
    '<meta name="twitter:description" content="Explore 1,500+ names, create new ones, shortlist favorites, and share a live family ballot." />': f'<meta name="twitter:description" content="{OG_DESC}" />',
    'const DEFAULT_PAGE_TITLE="Name the Baby";': f'const DEFAULT_PAGE_TITLE="{TITLE}";',
    'const DEFAULT_PAGE_DESCRIPTION="Name the Baby is a one-page baby name finder and creation lab with smart recommendations, live family voting, custom names, saved favorites, and Name Battle.";': f'const DEFAULT_PAGE_DESCRIPTION="{DESC}";',
    'if(ogDesc)ogDesc.content="One tiny human. One very big decision. Explore 1,500+ names, create new ones, shortlist favorites, and share a family ballot.";': f'if(ogDesc)ogDesc.content="{OG_DESC}";'
}
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)
        changed = True

# Preferred Google site name via WebSite structured data.
if '"@type":"WebSite"' not in text and '"@type": "WebSite"' not in text:
    marker = '  <meta name="twitter:image" content="https://namethebaby.site/api/og" />\n'
    schema = '''  <script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "WebSite",\n    "name": "Name the Baby",\n    "alternateName": ["NameTheBaby", "namethebaby.site"],\n    "url": "https://namethebaby.site/",\n    "description": "A baby name generator, name creator, shortlist, and live family baby-name polling tool."\n  }\n  </script>\n'''
    if marker not in text:
        raise RuntimeError('Twitter image marker not found')
    text = text.replace(marker, marker + schema, 1)
    changed = True

# Natural keyword-rich hero copy.
old = '      <p>Tell us the vibe, add the family name, and get one thoughtful baby-name suggestion at a time. Save the keepers. Battle the finalists.</p>'
new = '      <p>Use the baby name generator to explore boy, girl, and unisex baby names by style, origin, popularity, first letter, syllables, and surname. Save favorites, create a unique name, compare finalists, and share a family baby-name poll.</p>'
if old in text:
    text = text.replace(old, new, 1)
    changed = True

# Search-discovery section styles.
if '.seo-discovery{' not in text:
    marker = '    .sponsor-panel{margin-top:20px;display:grid;grid-template-columns:1.1fr .9fr;gap:16px;align-items:center;background:linear-gradient(135deg,#29232f,#3a3040);color:#fff;border:0}\n'
    css = '''    .seo-discovery{margin-top:20px}\n    .seo-discovery>p{max-width:850px}\n    .seo-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:16px}\n    .seo-item{border:1px solid var(--line);background:#fff;border-radius:17px;padding:16px}\n    .seo-item h3{font-size:1rem;margin:0;letter-spacing:-.025em}\n    .seo-item p{margin:7px 0 0;color:var(--muted);font-size:.79rem;line-height:1.55}\n    .seo-note{margin:14px 0 0;padding:12px 14px;border:1px solid #d8ebe7;background:#f5fbfa;border-radius:14px;color:#55706c;font-size:.8rem;line-height:1.55}\n    @media(max-width:820px){.seo-grid{grid-template-columns:1fr}}\n'''
    if marker not in text:
        raise RuntimeError('Sponsor CSS marker not found')
    text = text.replace(marker, css + marker, 1)
    changed = True

# Visible people-first SEO content. Remains part of the one-page product.
if 'id="babyNameTools"' not in text:
    marker = '    <section class="card sponsor-panel">\n'
    section = '''    <section class="card seo-discovery" id="babyNameTools">\n      <div class="eyebrow">Baby name tools</div>\n      <h2 style="margin-top:6px">Find, create, and vote on baby names.</h2>\n      <p class="sub">Name the Baby is a free one-page baby-name tool for parents and families who want more than a static list. Search 1,500 names, build a shortlist, test full-name flow, create new possibilities, and let family or friends vote on the finalists.</p>\n      <div class="seo-grid">\n        <article class="seo-item">\n          <h3>Baby name generator</h3>\n          <p>Explore boy names, girl names, and unisex baby names by origin, style, first letter, syllables, name length, ending sound, and recent U.S. popularity. You can also add a last name for a surname preview.</p>\n        </article>\n        <article class="seo-item">\n          <h3>Baby name creator with meanings</h3>\n          <p>Use the Name Creation Lab to build unique baby-name ideas from a desired meaning, source word, language inspiration, or two family names. Creative constructions are clearly labeled instead of being presented as traditional names.</p>\n        </article>\n        <article class="seo-item">\n          <h3>Family baby name poll</h3>\n          <p>Save your favorite baby names, compare finalists in Name Battle, and share a live baby-name voting link. Friends and relatives can vote from their own devices without creating an account.</p>\n        </article>\n      </div>\n      <div class="seo-note"><b>Baby name meanings and popularity:</b> reviewed profiles include meaning and origin notes where available, while matching names can use official recent U.S. Social Security Administration popularity data. Names outside the recent Top 200 are not automatically described as rare.</div>\n    </section>\n\n'''
    if marker not in text:
        raise RuntimeError('Sponsor section marker not found')
    text = text.replace(marker, section + marker, 1)
    changed = True

if 'V16 retention one-page build' in text:
    text = text.replace('V16 retention one-page build','V17 Google-discovery one-page build',1)
    changed = True

required = [
    TITLE,
    'application/ld+json',
    '"@type": "WebSite"',
    'id="babyNameTools"',
    'Baby name generator',
    'Family baby name poll',
    'Baby name creator with meanings'
]
missing = [x for x in required if x not in text]
if missing:
    raise RuntimeError(f'Missing V17 SEO pieces: {missing}')

if changed:
    path.write_text(text, encoding='utf-8')
    print('V17 Google discovery patch applied.')
else:
    print('V17 Google discovery already present.')
