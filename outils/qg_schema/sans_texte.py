# -*- coding: utf-8 -*-
"""Version sans légende ni écriture du plan final : retire #cartouche, <text>, <title>."""
import re, sys, cairosvg
src = "final/Plan_QG_Corresone_final.svg"; dst = sys.argv[1] if len(sys.argv) > 1 else "final/Plan_sans_texte_main_levee.svg"
s = open(src, encoding="utf-8").read()
s = re.sub(r'<g[^>]*id="cartouche".*?</g>\s*', '', s, flags=re.S)
s = re.sub(r'<text\b.*?</text>', '', s, flags=re.S)
s = re.sub(r'<title\b.*?</title>', '', s, flags=re.S)
open(dst, "w", encoding="utf-8").write(s)
cairosvg.svg2png(url=dst, write_to=dst.replace(".svg", ".png"), output_width=2600)
print("ok", dst, len(s)//1024, "Ko")
