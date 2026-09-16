from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Align every public URL signal with the host Vercel currently serves as primary.
text = text.replace('https://namethebaby.site/', 'https://www.namethebaby.site/')

text = text.replace(
    '<meta name="description" content="Find boy, girl and unisex baby names with meanings, popularity filters and surname previews. Create unique names, save favorites and share a family poll." />',
    '<meta name="description" content="Free baby name generator for boy, girl and unisex names. Explore names by origin, style, first letter, syllables and popularity, then save favorites and share a family poll." />'
)

text = text.replace(
    '<title>Baby Name Generator, Creator & Family Poll | Name the Baby</title>',
    '<title>Free Baby Name Generator by Origin, Style & Letter | Name the Baby</title>'
)

old_section = re.compile(r'    <section class="card seo-discovery" id="babyNameTools">.*?    </section>\n\n    <section class="card sponsor-panel">', re.S)
new_section = '''    <section class="card seo-discovery" id="babyNameTools">
      <div class="eyebrow">Explore baby names</div>
      <h2 style="margin-top:6px">Find baby names by gender, origin, style, letter, and meaning.</h2>
      <p class="sub">Name the Baby is a free one-page baby name generator built for the way families actually search. Start broad with boy, girl, or unisex names, or narrow the catalog by cultural tradition, first letter, style, syllables, length, ending sound, and recent U.S. popularity. Save the names you like and bring family or friends into the final decision.</p>
      <div class="seo-grid">
        <article class="seo-item" id="namesByGender">
          <h3>Boy, girl & unisex baby names</h3>
          <p>Choose boy names, girl names, unisex names, or leave gender open. Combine that choice with the other filters when you want a more specific set of ideas.</p>
        </article>
        <article class="seo-item" id="namesByOrigin">
          <h3>Baby names by origin or tradition</h3>
          <p>Explore reviewed names across traditions represented in the catalog, including African, Arabic, English, French, Greek, Hebrew, Irish, Italian, Latin, Spanish, Welsh, and more. Origin labels are only used where the catalog has reviewed support.</p>
        </article>
        <article class="seo-item" id="namesByLetter">
          <h3>Baby names starting with A–Z</h3>
          <p>Looking for baby names that start with a particular letter? Use the Starts With filter from A through Z, then combine the letter with gender, origin, style, syllables, or length.</p>
        </article>
        <article class="seo-item" id="namesByStyle">
          <h3>Unique, classic & distinctive baby names</h3>
          <p>Explore styles such as classic, modern, distinctive, Southern, biblical, vintage, strong, elegant, and nature-inspired. Style tags come from reviewed profiles rather than being assigned to every directory name automatically.</p>
        </article>
        <article class="seo-item" id="namesWithMeaning">
          <h3>Baby names with meanings</h3>
          <p>Reviewed profiles can include meaning, origin, pronunciation, and style notes. The catalog is being expanded carefully so uncertain etymologies are not presented as facts.</p>
        </article>
        <article class="seo-item" id="familyNamePoll">
          <h3>Baby name shortlist & family poll</h3>
          <p>Save favorites on your device, compare two finalists in Name Battle, or share a live baby-name poll so family and friends can vote without creating an account.</p>
        </article>
      </div>
      <div class="seo-note"><b>About the data:</b> Name the Baby currently includes 1,500 names, with reviewed meaning/origin/style profiles for a growing portion of the catalog. Official U.S. Social Security Administration 2020–2025 Top 200 data is layered onto matching names. A name outside that recent Top 200 is not automatically labeled rare.</div>
    </section>

    <section class="card sponsor-panel">'''
text, count = old_section.subn(new_section, text, count=1)
if count != 1:
    raise SystemExit('SEO discovery section not found exactly once')

# Keep social titles aligned with the new search-facing positioning.
text = text.replace('Baby Name Generator, Creator & Family Poll | Name the Baby', 'Free Baby Name Generator by Origin, Style & Letter | Name the Baby')

marker = '<!-- V19 SEO ranking readiness: canonical host + intent-led one-page discovery -->'
if marker not in text:
    text = text.replace('</head>', f'  {marker}\n</head>', 1)

p.write_text(text, encoding='utf-8')
