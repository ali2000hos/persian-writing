# Bundled fonts

Persian fonts shipped with this skill (all SIL Open Font License — free for
commercial use and embedding):

- **Vazirmatn** — default body/document font (github.com/rastikerdar/vazirmatn)
- **Lalezar** — display/headline font (fonts.google.com/specimen/Lalezar)

Before converting any document to PDF, install them into the environment:

```bash
bash ../../scripts/install_fonts.sh
```

More families (Shabnam, Sahel, Samim, Parastoo, Tanha, Gandom):
`python3 ../../scripts/download_fonts.py --all` — needs GitHub access;
in sandboxed environments ask the user to add TTFs here manually.
