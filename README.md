# Study Buddy

An app that takes your notes and quizzes you on them, using the Claude API.

## What it does

It takes your notes and creates a knowledge tree from them, breaking them down
into branches and leaves. It generates a question for every leaf. And it
schedules those questions using the SM-2 algorithm, which decides what concept
comes back for review and when.

## Demo

```
════════════════════════════════════════════════════════════════
                           STUDY BUDDY                          
                active recall + spaced repetition               
════════════════════════════════════════════════════════════════


────────────────────────────────────────────────────────────────
  Daughter Cells  · 4 due
────────────────────────────────────────────────────────────────

  generating question...

  QUESTION

  Explain why the two daughter cells produced by mitosis are
  genetically identical to each other and to the original
  parent cell, describing the key events that ensure this
  outcome.

  Your answer
  (Press Enter on an empty line when done)

  grading...

────────────────────────────────────────────────────────────────
  SCORE  █████████░  90/100
────────────────────────────────────────────────────────────────

  YOU UNDERSTAND THIS

  WHAT YOU GOT RIGHT
  Correctly centers the explanation on semiconservative S-phase
  replication producing identical sister chromatids joined at
  the centromere, with proofreading and mismatch repair
  ensuring fidelity...

  WHAT TO IMPROVE
  Phrasing slips: at metaphase it is whole chromosomes (paired
  sister chromatids) that align single-file, not individual
  chromatids; cohesin cleavage by separase occurs at anaphase
  onset...

  next review: tomorrow (2026-09-20)

  [Enter] next question   [q] quit
```

That answer scored 90, which maps to SM-2 quality 4, so the card moved from
`repetition 0` to `repetition 1` with an interval of 1 day and its ease factor
held at 2.5.

## How it works

Notes go in at one end and a scheduled review comes out the other. Each file
does one job.

| File | Job |
|---|---|
| `ingest.py` | Reads pasted multi-line text from the terminal |
| `knowledge_tree.py` | `extract_knowledge_tree(notes)` → a `KnowledgeTree` of `Branch`es and `Leaf`s |
| `quiz.py` | `quiz(leaf)` → one open-ended question, as plain text |
| `evaluator.py` | `evaluator(leaf, question, answer)` → a `Grade` (`score` 0-100, `strengths`, `improvements`) |
| `scheduler.py` | `converter()` maps 0-100 to SM-2 quality 0-5; `scheduling()` returns the new repetition, ease factor and interval |
| `tracker.py` | `new_record()`, plus reading and writing the JSON store |
| `display.py` | All terminal output — banner, headers, score bar, verdict, menu |
| `claude_client.py` | `ask_claude()`, the shared plain-text call |
| `main.py` | `next_due()` picks the card; `lazy_generator()` runs the loop |

One record per concept, in a single JSON file (`progress.json`, gitignored
so your review history stays off GitHub):

```json
{
  "Chromosome Condensation": {
    "leaf": { "name": "...", "description": "..." },
    "question": "...",
    "repetition": 1,
    "ease_factor": 2.5,
    "interval": 1,
    "due_date": "2026-09-20"
  }
}
```

## Setup

Requires Python 3.14 and an Anthropic API key.

```bash
git clone <this repo>
cd study_buddy

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

python main.py
```

On the first run it asks for your notes. After that it loads what you saved and
goes straight to whatever is due.

## Design decisions

**SM-2 for scheduling.** SuperMemo, 1987 — still what Anki's default scheduler
is a variant of. The idea behind SM-2, and why I chose it: you forget things.
Sometimes you review too early and waste time. Review too late and you've
already forgotten, so you're relearning from scratch. SM-2 tries to schedule
your review right before you forget, and pushes that point further out every
time you get it right.

It works on three numbers. **Quality** (0-5) is how well you answered this one
time. **Ease factor** is how easy this specific concept is for you — it starts
at 2.5 and floors at 1.3, so a concept you keep fumbling ends up near 1.3 and
keeps coming back fast. **Interval** is how many days until the next review.
`scheduling()` returns all three.

**Structured outputs instead of parsing JSON out of prose.** `evaluator.py` and
`knowledge_tree.py` use `messages.parse()` with a Pydantic model as
`output_format`. What comes back isn't text, it's a class — so you don't reach
for `content[0].text`, you use `parsed_output`.

Asking for JSON in prose means the model can wrap it in a code fence, prefix it
with "Here's the JSON:", or nest a field differently, and every one of those
breaks `json.loads()` at runtime. Passing the model as `output_format` makes
the shape part of the request instead of a hope.

`quiz.py` deliberately doesn't do this. A question is different from a `Grade`
because a `Grade` is an object and a question is text — one string, nothing to
pull apart.

**Bounding what comes back, not just asking for it.** `Grade` originally had a
single `feedback` field with no length guidance and `max_tokens` at 1024. A long
answer produced long feedback, the response hit the cap mid-string, and what came
back was JSON with no closing brace — a `ValidationError` that killed the run
*after* the API call had already been paid for.

Raising the cap alone just moves the cliff further out. The real fix is asking
for a bounded answer: `strengths` and `improvements` as two fields, each capped
at 80 words in the prompt. Splitting the field turned out to be worth it on its
own — the terminal can label the two blocks instead of printing one wall of text.

**A verdict that can't drift from the scheduler.** Above the feedback is a
plain-language line: `YOU UNDERSTAND THIS`, `A LITTLE MORE REVIEW`, or
`HASN'T CLICKED YET`. The bands aren't picked by feel. The bottom one starts
below 60, which is exactly where `converter()` falls under SM-2 quality 3 and
`scheduling()` resets your repetition count to zero. What the screen says and
what the algorithm does can never disagree.

**Failing without losing the review.** Every API call goes through `with_retry`,
which gives it a second attempt before giving up, and `write_json` runs on every
exit path. A rate limit or a dropped connection now ends the session with a
message instead of a traceback, and the work already done is still on disk.

**Storing a due date, not a countdown.** Storing a date means the program
doesn't have to be running overnight. When it runs, it runs once: it checks
whether anything is due, and if it is, it pulls it up. Nothing has to decrement
a counter at midnight, so there's no cron job, no daemon, and no requirement
that the app was even open yesterday.

**Deriving instead of storing.** Every card is created with the current date, so
we filter all of them for due dates less than or equal to today. Every time you
review a question its due date updates and gets pushed forward, out of the set
we're filtering for. So we just end up with the ones we have left.

This means there's no saved position anywhere. The program never asks "where did
I leave off" — it asks "what do I have to do", and recomputes the answer from
the data every time. A bookmark can disagree with reality. A filter can't.

**`display.py` was pair-written.** Claude is good at styling terminal output if
you give it the right prompt, so I let it handle the presentation layer while I
kept the pipeline.

## Planned next

- **File upload** — PDF and DOCX, instead of pasting plain text
- **Multiple trees** — a history of the trees you've made, and switching between
  them, so you can study one subject and then another
- **Branch-level status** — a branch's status derived from its leaves. Once most
  of a branch's leaves are understood, the branch is understood; otherwise it's
  practicing, or not started if you haven't touched it. Same derive-don't-store
  logic as everything else
- **Web UI**

None of these unlock the core loop, which is why they aren't here yet. The MVP
is a working CLI: paste notes, get quizzed, get graded, come back when something
is due.
