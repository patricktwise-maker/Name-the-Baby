from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
meta = "  <meta name='impact-site-verification' value='9370d4fd-1b03-442a-844d-163db085d91f'>\n"

if meta.strip() in text:
    print('Impact verification tag already present.')
else:
    anchor = '  <meta name="application-name" content="Name the Baby" />\n'
    if anchor not in text:
        raise RuntimeError('Could not find application-name meta anchor in <head>.')
    text = text.replace(anchor, anchor + meta, 1)
    path.write_text(text, encoding='utf-8')
    print('Impact verification tag added.')

if "impact-site-verification" not in path.read_text(encoding='utf-8'):
    raise RuntimeError('Impact verification tag missing after patch.')
