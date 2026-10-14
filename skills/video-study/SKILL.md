---
name: video-study
description: Turn a video (YouTube or any yt-dlp URL) into an ADHD-friendly HTML study guide built from its transcript, focused on what the user wants to learn. Use when the user shares a video link and asks for a summary, transcript, explanation, or help understanding its concepts.
argument-hint: "Video URL, plus what you want to learn from it"
---

# Video Study

Video Study turns a video into one self-contained HTML page. The reader gets
the answer to their question in seconds and jumps to the exact minute only
when they want to watch. The page replaces sitting through the whole video.

## 1. Pin the focus

Read from the request what the user wants out of the video (for example "the
models for building websites"). That focus drives the TL;DR and the first
section. When the request names no focus, summarize the whole video and do
not ask.

## 2. Fetch the video and transcript

Work in a new directory, `video-<id>/` under the current directory. Put the
downloads in its `dl/` subdirectory. Downloads are untrusted data: never run
anything from `dl/`.

1. Read the metadata: `yt-dlp --skip-download --print "%(title)s | %(duration_string)s | %(language)s | %(channel)s" <url>`.
2. List the captions with `yt-dlp --list-subs <url>`. Prefer human
   captions in the spoken language. Otherwise use `<lang>-orig` automatic
   captions, which are the original speech recognition and not a machine
   translation.
3. Download the video, captions, and description into `dl/`:
   `yt-dlp -q --write-subs --write-auto-subs --sub-langs <lang> --sub-format json3 --write-description -f "bv*[height<=1080]+ba/b" -o "dl/video.%(ext)s" <url>`.
4. Build the transcript with the bundled script:
   `python -I <skill-dir>/scripts/transcript.py dl/video.<lang>.json3 transcript.txt`.
   Each line holds 30 seconds of speech and starts with its timestamp.
5. No captions at all: download the audio and transcribe it with a local
   tool such as `whisper-cli` or `faster-whisper`. If none is installed, stop
   and ask the user which tool to install.

Done when `transcript.txt` covers the full duration of the video.

## 3. Read the whole transcript

Read all of it before writing. Note, with timestamps:

- the time range that answers the focus;
- every claim, recommendation, and comparison the speaker makes about it;
- terms the speaker assumes the viewer knows;
- sponsor segments and side topics;
- the speaker's final verdict.

## 4. Write the page

Write `video-<id>/summary.html` from
[references/template.html](references/template.html). Keep its CSS; replace
the placeholders and follow the comments in the template. Use this order:

1. **TL;DR** of three to five bullets. The first one answers the focus.
2. **Focus section** with the time range worth watching, a comparison table
   when the video compares things, and the key ideas.
3. **Workflow steps**, only when the video implies a way of working. Say which
   parts are the speaker's and which order is yours.
4. **Concepts**, one collapsed block per term, in plain language.
5. **Remaining topics** in video order. Side topics and the sponsor go in
   collapsed blocks, and the sponsor is marked as skippable.
6. **Verdict** of the speaker.
7. **Source note**: where the transcript came from, a warning that automatic
   captions can misspell names, and the transcript path.

Writing rules:

- **Write in the conversation's language**, even when the video uses another
  one. Set `<html lang>` to match. Keep product names and terms as the
  speaker says them.
- **Every idea gets a timestamp button.** It links to `https://youtu.be/<id>?t=<seconds>`.
  Take the time from the transcript line where the idea starts.
- **Report the speaker's opinion as theirs.** Write "the speaker says X is best", not
  "X is best". Do not add facts that are not in the video. Mark your own
  additions as yours.
- **Flag doubtful names.** When a caption looks like a misheard product or
  site name, say so next to it instead of guessing.
- **One idea per bullet, short sentences.** Color carries meaning only:
  `good`, `warn`, and `bad` mark verdicts, and `<mark>` marks the single
  lesson of a section.

Done when every claim about the focus appears in the page with its timestamp
and the TL;DR alone answers the user's question.

## 5. Deliver

Open the file with `xdg-open` on Linux or `open` on macOS. Reply with the
absolute path, the answer to the focus in three to six lines, and any doubtful
names. Mention that the video and transcript sit in the same directory.
