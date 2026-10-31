#!/usr/bin/env python3
"""Synthetic engineering smoke check. Does not assess transcription quality."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[1]
CLI = REPO / "advanced-econ-note2pdf/scripts/econ_note.py"


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def run(*args, expected=0):
    proc = subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True)
    if proc.returncode != expected:
        raise RuntimeError("%s returned %s, wanted %s\n%s\n%s" % (args, proc.returncode, expected, proc.stdout, proc.stderr))
    return json.loads(proc.stdout)


def check(base):
    image = Image.new("RGB", (1900, 1400), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((200, 180, 1500, 1000), outline="navy", width=10)
    draw.text((250, 230), "Synthetic engineering fixture: x + y = 1", fill="black")
    photo = base / "board.png"
    image.save(photo)
    pdf = base / "pages.pdf"
    image.save(pdf, save_all=True, append_images=[image], resolution=300)
    root = base / "project"
    run("init", "--project", root, "--inputs", photo, pdf, "--mode", "both", "--title", "工程自检", "--domains", "math")
    run("init", "--project", root, "--inputs", photo, "--mode", "study", "--title", "refuse overwrite", expected=2)
    p = json.loads((root / "project.json").read_text())
    assert len(p["sources"]) == 3
    run("validate", "--project", root, expected=3)
    run("prepare", "--project", root, "--tile-size", "1024")
    before = (root / "project.json").read_bytes()
    run("prepare", "--project", root, "--tile-size", "1024")
    assert (root / "project.json").read_bytes() == before, "prepare must be idempotent"
    p = json.loads(before)
    assert all(len(s["tiles"]) > 1 for s in p["sources"])
    asset = run("crop", "--project", root, "--source", "s0001", "--box", ".1", ".1", ".9", ".9", "--name", "diagram")
    assert (root / asset["path"]).is_file()
    run("crop", "--project", root, "--source", "s0001", "--box", ".1", ".1", ".9", ".9", "--name", "diagram", expected=2)
    for i, source in enumerate(p["sources"], 1):
        uid, bid = "u%03d" % i, "b%03d" % i
        ref = {"source_id": source["id"], "revision": source["revision"], "box": [0, 0, 1, 1]}
        fragment = "content/%s.tex" % bid
        (root / fragment).write_text("\\[x+y=1\\]\n", encoding="utf-8")
        unit = {"id": uid, "title": "合成内容 %s" % i, "source_ids": [source["id"]],
                "coverage": [{"id": "c001", **ref, "kind": "equation", "disposition": "included", "block_ids": [bid], "reason": ""}],
                "blocks": [{"id": bid, "kind": "equation", "origin": "source", "refs": [ref], "body": {"faithful": fragment}}], "issues": []}
        write(root / "units" / (uid + ".json"), unit)
    run("validate", "--project", root)
    run("review", "--project", root, "--kind", "content", "--unit", "u001", "--note", "Synthetic state-transition check; not an OCR evaluation")
    assert run("status", "--project", root)["units"][0]["content_review_current"]
    (root / "content/b001.tex").write_text("\\[x+y=2\\]\n", encoding="utf-8")
    assert not run("status", "--project", root)["units"][0]["content_review_current"]
    run("prepare", "--project", root, "--source", "s0001", "--rotate", "90", "--tile-size", "1024")
    result = run("validate", "--project", root, expected=2)
    assert any("Stale" in e or "stale" in e for e in result["errors"])
    run("prepare", "--project", root, "--source", "s0001", "--tile-size", "1024")
    run("validate", "--project", root)
    bad = json.loads((root / "units/u001.json").read_text())
    saved = json.loads(json.dumps(bad))
    bad["blocks"][0]["body"]["faithful"] = "../outside.tex"
    write(root / "units/u001.json", bad)
    assert run("validate", "--project", root, expected=2)["errors"]
    write(root / "units/u001.json", saved)
    print("PASS: import, PDF pages, immutable originals, tiles, crop collisions, state invalidation, stale sources, path confinement")
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", type=Path, help="Keep synthetic artifacts in a new or empty directory")
    args = parser.parse_args()
    if args.keep:
        args.keep.mkdir(parents=True, exist_ok=True)
        if any(args.keep.iterdir()):
            parser.error("--keep directory must be empty")
        check(args.keep.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="econ-dev-") as tmp:
            check(Path(tmp))


if __name__ == "__main__":
    main()
