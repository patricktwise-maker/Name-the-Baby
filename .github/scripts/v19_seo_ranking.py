from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Align every public URL signal with the host Vercel currently serves as primary.
text = text.replace('https://namethebaby.site/', 'https://www.namethebaby.site/')

# Search-facing metadata: descriptive rather than stuffed.
text = re.sub(
    r'<meta name="description" content="[^"]*" />',
    '<meta name="description" content="Free baby name generator for boy, girl and unisex names. Explore verified names by origin, meaning, style and first letter, save favorites, and share a family poll." />',
    text,
    count=1
)
text = re.sub(
    r'<title>.*?</title>',
    '<title>Free Baby Name Generator by Origin, Meaning & Letter | Name the Baby</title>',
    text,
    count=1
)
text = re.sub(
    r'<meta property="og:title" content="[^"]*" />',
    '<meta property="og:title" content="Free Baby Name Generator by Origin, Meaning & Letter | Name the Baby" />',
    text,
    count=1
)
text = re.sub(
    r'<meta name="twitter:title" content="[^"]*" />',
    '<meta name="twitter:title" content="Free Baby Name Generator by Origin, Meaning & Letter | Name the Baby" />',
    text,
    count=1
)

old_section = re.compile(r'    <section class="card seo-discovery" id="babyNameTools">.*?    </section>\n\n    <section class="card sponsor-panel">', re.S)
new_section = '''    <section class="card seo-discovery" id="babyNameTools">
      <div class="eyebrow">Explore baby names</div>
      <h2 style="margin-top:6px">Find baby names by gender, origin, style, letter, and meaning.</h2>
      <p class="sub">Name the Baby is a free one-page baby name generator built for the way families actually search. Start broad with boy, girl, or unisex names, or narrow the catalog by cultural tradition, first letter, style, syllables, length, ending sound, and recent U.S. popularity. Save the names you like and bring family or friends into the final decision.</p>
      <div class="seo-grid">
        <article class="seo-item" id="namesByGender">
          <h3>Boy, girl & unisex baby names</h3>
          <p>Choose boy names, girl names, unisex names, or leave gender open. Reviewed examples include <b>Benjamin</b> and <b>Leo</b> for boys, <b>Sophia</b> and <b>Imani</b> for girls, and <b>Rowan</b> and <b>Zion</b> as unisex options.</p>
        </article>
        <article class="seo-item" id="namesByOrigin">
          <h3>Baby names by origin or tradition</h3>
          <p>Explore reviewed traditions represented in the catalog. Examples include <b>Imani</b> (African/Swahili usage), <b>Aaliyah</b> (Arabic), <b>Benjamin</b> (Hebrew), <b>Saoirse</b> (Irish), and <b>Leo</b> (Latin). Origin labels are only shown where the catalog has reviewed support.</p>
        </article>
        <article class="seo-item" id="namesByLetter">
          <h3>Baby names starting with A–Z</h3>
          <p>Looking for baby names that start with a particular letter? Use the Starts With filter from A through Z. For example, try A for <b>Aaliyah</b>, B for <b>Benjamin</b>, I for <b>Imani</b>, R for <b>Rowan</b>, or S for <b>Sophia</b> and <b>Saoirse</b>.</p>
        </article>
        <article class="seo-item" id="namesByStyle">
          <h3>Unique, classic & distinctive baby names</h3>
          <p>Explore reviewed style tags such as classic, modern, distinctive, Southern, biblical, vintage, strong, elegant, and nature-inspired. <b>Magnolia</b> is tagged Southern, vintage and nature-inspired; <b>Willow</b> is nature-inspired and modern; <b>Zion</b> is biblical, modern and strong.</p>
        </article>
        <article class="seo-item" id="namesWithMeaning">
          <h3>Baby names with meanings</h3>
          <p>Reviewed profiles explain meanings without pretending uncertain etymologies are settled. <b>Sophia</b> comes from the Greek word for “wisdom,” <b>Leo</b> is Latin for “lion,” <b>Saoirse</b> is Irish for “freedom,” and <b>Imani</b> is a Swahili name associated with faith.</p>
        </article>
        <article class="seo-item" id="familyNamePoll">
          <h3>Baby name shortlist & family poll</h3>
          <p>Save favorites on your device, compare two finalists in Name Battle, or share a live baby-name poll so family and friends can vote without creating an account. The generator, shortlist and voting flow stay together on this one page.</p>
        </article>
      </div>
      <div class="seo-note"><b>About the data:</b> Name the Baby currently includes 1,500 names, with reviewed meaning/origin/style profiles for a growing portion of the catalog. Official U.S. Social Security Administration 2020–2025 Top 200 data is layered onto matching names. A name outside that recent Top 200 is not automatically labeled rare.</div>
    </section>

    <section class="card sponsor-panel">'''
text, count = old_section.subn(new_section, text, count=1)
if count != 1:
    raise SystemExit('SEO discovery section not found exactly once')

# Add accurate WebApplication schema alongside the existing WebSite schema. This describes visible functionality;
# it does not claim a Google rich-result feature that is not supported for this content type.
app_schema = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Name the Baby",
    "url": "https://www.namethebaby.site/",
    "applicationCategory": "LifestyleApplication",
    "operatingSystem": "Any",
    "isAccessibleForFree": true,
    "description": "A free baby name generator for exploring names by gender, origin, style, first letter, meaning and other filters, with a shortlist, name comparison and family voting tools."
  }
  </script>
'''
if '"@type": "WebApplication"' not in text:
    text = text.replace('</head>', app_schema + '</head>', 1)

marker = '<!-- V19.1 SEO: verified crawlable catalog examples + intent coverage -->'
if marker not in text:
    text = text.replace('</head>', f'  {marker}\n</head>', 1)

p.write_text(text, encoding='utf-8')
