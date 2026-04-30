# Creative: Screen Recording → Tutorial Video

**Class:** Community showcase · **Confidence:** High · **Demo status:** Verified workflow

## Pain Point

Creating tutorial content means: record a screen walkthrough, write a script, generate or record narration, produce a video with an avatar, edit it all together — then do it again for the next topic. Most creators bounce between OBS, a script doc, a TTS tool, and a video generator. The handoff friction between tools is where momentum dies.

## What It Does

@vicky_dyor documented a workflow where she gave Hermes a raw screen recording and asked it to produce a tutorial video. Hermes generated the script, produced the finished video on HeyGen using her AI avatar, and retained her preferences in memory for follow-up work.

The full loop: screen recording in → structured tutorial script → HeyGen video with avatar out. First attempt was reportedly perfect; zero iteration on script or avatar.

## Setup

1. Record your screen while performing the task you want to teach.
2. Share the recording with Hermes (file upload via Telegram, Discord, or file system).
3. Prompt: something like *"make a tutorial about [topic] for my YouTube channel — here's a screen recording"*.
4. Hermes can use browser tools to navigate HeyGen (or an equivalent video-generation platform), paste the generated script, select your avatar, and produce the video.
5. Memory captures your avatar choice, tone preferences, and format so the next video follows the same pattern.

**Tools involved:**
- Screen recorder (OBS, built-in OS tool, or mobile)
- Hermes with browser and file tools enabled
- HeyGen account with an AI avatar already created

## Prompts

**Starting from a screen recording:**
```
I recorded myself setting up X. Make a tutorial video for my YouTube channel using this screen recording. Use my HeyGen avatar.
```

**Follow-up after memory is primed:**
```
Same format as last time: screen recording attached, topic is Y.
```

## Skills Needed

- Browser / web interaction
- File tools (upload, read)
- Optional: HyperFrames or video-generation skill if available

## Notes

- This works because the heavy lifting (avatar, voice, video synthesis) is delegated to HeyGen. Hermes handles the decision-making, script generation, and orchestration. Don't expect Hermes to render video itself — it drives the service that does.
- Memory is the differentiator. If you have to re-explain your avatar and tone every time, the workflow collapses. After the first run, confirm that Hermes stored the preferences.

## Sources

- @vicky_dyor on X (verified): https://x.com/vicky_dyor/status/2036126432766636347
- Featured on ai-hermes-agent.com/use-cases
- YouTube channel: https://www.youtube.com/@vicky_dyor
