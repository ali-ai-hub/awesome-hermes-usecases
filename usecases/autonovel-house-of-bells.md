# Autonovel — House of Bells

**Class:** Official production · **Confidence:** High · **Demo status:** Full pipeline repo

## Pain Point

"Can an agent actually produce a finished creative work end-to-end, not just a draft?" is the benchmark question for autonomous long-form content. Most demos stop at "chapter 1 looks good." Producing a coherent novel, illustrating it, type-setting it, and turning it into an audiobook — without a human stitching the pieces together — is a much higher bar.

## What It Does

Nous Research used Hermes as the engine for a full autonomous book production pipeline. The result was *House of Bells*: a 19-chapter, 79,456-word novel, generated, reviewed, illustrated, type-set in LaTeX, and produced as an audiobook. Six automated revision passes and six Opus-driven review rounds ran before the text was frozen. The audiobook was cut into 4,179 segments.

The repo is public and runnable. It's the clearest evidence to date that a Hermes-driven pipeline can ship a polished creative artifact, not just a demo.

## What's in the Pipeline

- Writing and revision (multi-stage, with automated review rounds)
- LaTeX type-setting of the final manuscript
- Art generation for the cover and illustrations (FAL)
- Audiobook production with voice synthesis (ElevenLabs)

## Setup

Not a lightweight demo — this is a production repo with real API costs. Treat it as a case study you can run end-to-end if you want to.

```bash
git clone https://github.com/NousResearch/autonovel
cd autonovel
cp .env.example .env
# fill in ANTHROPIC_API_KEY, and optionally FAL_KEY and ELEVENLABS_API_KEY
uv sync
# follow the repo's run instructions
```

## Reported Metrics

- 19 chapters, 79,456 words
- 6 automated revision passes
- 6 Opus review rounds
- 4,179 audiobook segments

## Skills Needed

- Anthropic API key (Opus for reviews)
- Optional: FAL for art, ElevenLabs for audio
- `uv` for environment management
- Substantial wall-clock time and non-trivial API spend for a full run

## Sources

- Blog post (includes the finished artifacts): <https://nousresearch.com/bells>
- Pipeline repo: <https://github.com/NousResearch/autonovel>
