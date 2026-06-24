# Brand assets

Drop the official Purinton Analytics brand files here, then tell Claude to wire
them in (`python3 build.py` regenerates every page).

## Expected files
- `logo.svg` — primary logo (header). Preferred: SVG.
- `logo-light.svg` *(optional)* — light/white version for dark backgrounds (footer/hero).
- `favicon.svg` or `favicon.png` *(optional)* — if different from the logo mark.

## How Claude uses them
- Header logo → `header()` in `build.py`
- Favicon / apple-touch-icon → `head()` in `build.py`
- Open Graph image → `assets/img/og-default.*`

## Getting files into this repo (the container can't read your local Mac)
1. **Paste** (best for SVG): open the `.svg` in a text editor, copy all, paste in chat.
2. **GitHub web upload**: on branch `claude/pa-expert-website-redesign-8wb1bh`,
   open `assets/img/brand/`, choose *Add file → Upload files*, commit.
3. **git**: `git add assets/img/brand/logo.svg && git commit && git push`.
