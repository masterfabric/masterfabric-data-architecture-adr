"""Compose docs/hero.png (1600x900) from real charts and measured numbers.

Every number on the hero is read from evidence/claims.json, which tools/check_claims.py verifies.
"""

from __future__ import annotations

import json

from PIL import Image, ImageDraw, ImageFilter

from mfviz import BG, BG2, DOCS, GREEN, GREY, ICE, IMG, ORANGE, PURPLE, RED, ROOT, WHITE, YELLOW, font

W, H = 1600, 900



def background():
    im = Image.new("RGB", (W, H), BG)
    px = im.load()
    for y in range(H):
        for x in range(W):
            t = min(1.0, (x / W) * 0.75 + (y / H) * 0.35)
            px[x, y] = tuple(int(BG[i] * (1 - t) + BG2[i] * t) for i in range(3))
    return im


def card(base, path, box, label, color, crop=None):
    x0, y0, x1, y1 = box
    shot = Image.open(path).convert("RGB")
    if crop:
        shot = shot.crop(crop)
    shot = shot.resize((x1 - x0, round(shot.height * (x1 - x0) / shot.width)), Image.LANCZOS)
    shot = shot.crop((0, 0, x1 - x0, min(shot.height, y1 - y0)))
    shadow = Image.new("RGBA", (shot.width + 40, shot.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((20, 20, shot.width + 20, shot.height + 20), radius=16, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    base.paste(shadow, (x0 - 20, y0 - 12), shadow)
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, shot.width, shot.height), radius=14, fill=255)
    base.paste(shot, (x0, y0), mask)
    d = ImageDraw.Draw(base)
    f = font(20, 800)
    w = d.textlength(label, font=f)
    d.rounded_rectangle((x0 - 10, y0 - 22, x0 + w + 18, y0 + 14), radius=18, fill=color)
    d.text((x0 + 4, y0 - 18), label, font=f, fill=(255, 255, 255))


def main():
    data = json.loads((ROOT / "evidence" / "claims.json").read_text(encoding="utf-8"))
    C = {c["id"]: c["values"] for c in data["claims"]}
    adrs = len(list((DOCS / "adr").glob("0*.md")))
    im = background()
    card(im, IMG / "platform.png", (960, 70, 1570, 450), "Reference platform", ICE)
    card(im, IMG / "evidence.png", (960, 520, 1570, 860), "Each decision, measured", GREEN)
    d = ImageDraw.Draw(im)
    d.text((80, 70), "MASTERFABRIC", font=font(36, 800), fill=WHITE)
    d.text((76, 120), "Data Architecture", font=font(80, 800), fill=WHITE)
    x, y = 80, 238
    for word, col in ((f"{len(data['repos'])} labs", ICE), (" · ", GREY), (f"{adrs} ADRs", GREEN), (" · ", GREY),
                      (f"{len(data['claims'])} verified numbers", YELLOW)):
        f = font(38, 800)
        d.text((x, y), word, font=f, fill=col)
        x += d.textlength(word, font=f)
    d.text((80, 318), "A data and AI platform for a mobile operator, decided with evidence:", font=font(26, 500), fill=GREY)
    d.text((80, 352), "every figure is checked against the lab that measured it.", font=font(26, 500), fill=GREY)
    facts = [
        (f"Iceberg compaction: {C['lh_query']['before']} → {C['lh_query']['after']} ms",
         f"one-day query · streaming aggregate {C['rt_maint']['before']} → {C['rt_maint']['after']} ms", ICE),
        (f"Adaptive alerts: {C['rt_static']['false_alerts']} → {C['rt_detect']['false_alerts']} false",
         f"precision {C['rt_static']['precision']} → {C['rt_detect']['precision']} · gated retraining AUC "
         f"{C['af_auc']['never']} → {C['af_auc']['auto']:.3f}", GREEN),
        (f"Governed RAG: {C['sd_rag']['before_pct']}% → 0% unauthorised chunks",
         f"PII leaks {C['sd_llm02']['before']}/8 → 0/8 · on-prem RAG hit@4 {C['op_hit']['hit4']}", RED),
        (f"Small jobs: {C['sr_sum']['pyspark']} s → {C['sr_sum']['polars']} s",
         f"PySpark vs Polars, same SQL, 200M rows · CPU Q8_0 {C['sv_q8']['cpu']} vs Q4 {C['sv_q4']['cpu']} tok/s", YELLOW),
    ]
    y = 430
    for title, sub, col in facts:
        d.rounded_rectangle((80, y + 6, 88, y + 62), radius=4, fill=col)
        d.text((106, y), title, font=font(29, 750), fill=WHITE)
        d.text((106, y + 38), sub, font=font(20, 450), fill=GREY)
        y += 92
    d.text((80, 820), "github.com/masterfabric/masterfabric-data-architecture-adr", font=font(28, 700), fill=WHITE)
    im.save(DOCS / "hero.png", optimize=True)
    print("docs/hero.png written")


if __name__ == "__main__":
    main()
