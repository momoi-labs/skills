#!/usr/bin/env python3
"""Extract screenshots from a downloaded video with ffmpeg.

  frames.py candidates <video> <outdir> [--step 20] [--start 0] [--end S]
      Save small candidate frames to <outdir>/cand/c<second>.jpg and build
      contact sheets (9 frames, 3 columns) in <outdir>/sheets/sheet<NN>.jpg.
      Prints the seconds on each sheet, left to right, top to bottom.

  frames.py final <video> <outdir> <second> [<second> ...] [--crop W:H:X:Y]
      Save final frames to <outdir>/img/<second>.jpg, about 1000 px wide,
      JPEG quality 4. --crop cuts the slide out of a full frame (speaker
      camera, logos). Use it only for conference videos. Crop a few pixels
      inside the slide edge to drop border lines.

Paths are arguments. Run with `python3 -I`. Never run anything from dl/.
"""
import argparse
import pathlib
import subprocess
import sys

COLS, PER_SHEET, THUMB_W = 3, 9, 640


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"{cmd[0]} failed: {r.stderr.strip()[-400:]}")
    return r.stdout


def duration(video):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(video)])
    return float(out.strip())


def grab(video, second, dest, vf):
    # -ss before -i seeks fast. Never ask for a second past the duration:
    # frames there can be solid green.
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(second), "-i", str(video),
         "-frames:v", "1", "-vf", vf, "-q:v", "4", str(dest)])


def candidates(a):
    out = pathlib.Path(a.outdir)
    cand, sheets = out / "cand", out / "sheets"
    cand.mkdir(parents=True, exist_ok=True)
    sheets.mkdir(parents=True, exist_ok=True)
    last = int(duration(a.video)) - 2
    end = min(a.end, last) if a.end else last
    seconds = list(range(a.start, end + 1, a.step))
    for s in seconds:
        grab(a.video, s, cand / f"c{s:05d}.jpg", f"scale={THUMB_W}:-2")
    for n, i in enumerate(range(0, len(seconds), PER_SHEET), 1):
        chunk = seconds[i:i + PER_SHEET]
        files = [cand / f"c{s:05d}.jpg" for s in chunk]
        rows = -(-len(files) // COLS)
        # Pad the last sheet with copies of the first frame so xstack fits.
        while len(files) < rows * COLS:
            files.append(files[0])
        layout = "|".join(f"{(k % COLS) * THUMB_W}_{(k // COLS) * 360}"
                          for k in range(len(files)))
        cmd = ["ffmpeg", "-y", "-v", "error"]
        for f in files:
            cmd += ["-i", str(f)]
        cmd += ["-filter_complex",
                "".join(f"[{k}:v]scale={THUMB_W}:360:force_original_aspect_ratio=decrease,"
                        f"pad={THUMB_W}:360:(ow-iw)/2:(oh-ih)/2[v{k}];"
                        for k in range(len(files)))
                + "".join(f"[v{k}]" for k in range(len(files)))
                + f"xstack=inputs={len(files)}:layout={layout}[o]",
                "-map", "[o]", "-frames:v", "1", "-q:v", "4",
                str(sheets / f"sheet{n:02d}.jpg")]
        run(cmd)
        print(f"sheet{n:02d}.jpg: " + " ".join(str(s) for s in chunk))


def final(a):
    out = pathlib.Path(a.outdir) / "img"
    out.mkdir(parents=True, exist_ok=True)
    limit = duration(a.video) - 2
    vf = (f"crop={a.crop}," if a.crop else "") + "scale=1000:-2"
    for s in a.seconds:
        if s > limit:
            sys.exit(f"second {s} is past the video duration")
        grab(a.video, s, out / f"{s:04d}.jpg", vf)
        print(out / f"{s:04d}.jpg")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("candidates")
    c.add_argument("video")
    c.add_argument("outdir")
    c.add_argument("--step", type=int, default=20)
    c.add_argument("--start", type=int, default=0)
    c.add_argument("--end", type=int, default=0)
    f = sub.add_parser("final")
    f.add_argument("video")
    f.add_argument("outdir")
    f.add_argument("seconds", type=int, nargs="+")
    f.add_argument("--crop", help="W:H:X:Y of the slide in the full frame")
    a = p.parse_args()
    candidates(a) if a.cmd == "candidates" else final(a)


if __name__ == "__main__":
    main()
