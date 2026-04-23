# Voice Assistant Workflows

**Class:** First-party demo · **Confidence:** High · **Demo status:** Docs + runbook

## Pain Point

Typing to your agent is fine at a desk, but not when you're cooking, driving, or walking around the house. You want to speak to Hermes and have it speak back — without wiring up a separate voice stack, a wake-word engine, and TTS plumbing.

## What It Does

Hermes ships with three distinct voice modes out of the box:

1. **CLI microphone loop.** Hold-to-talk or push-to-talk from the terminal. Transcription happens locally or via a provider; the agent's reply is spoken back through TTS.
2. **Voice replies in messaging gateways.** Send a Telegram or Discord voice note to your bot; Hermes transcribes it, processes normally, and can reply with a synthesized voice message.
3. **Discord voice-channel bot.** Join a voice channel and have the agent listen and respond in real time — for standups, co-working sessions, or hands-free team workflows.

Same agent, same memory, same skills. The voice layer is input/output only.

## Setup

Voice is enabled through `hermes tools` and provider config. The fast path:

```bash
hermes setup       # the wizard offers voice configuration
hermes tools       # enable the Voice & TTS toolset explicitly
```

Provider options include xAI TTS (auto-wired when using an xAI endpoint), ElevenLabs, and other TTS backends configured in `config.yaml`. For transcription, Whisper (local or API) is the typical pick.

Specific messaging platforms need their gateway enabled (Telegram, Discord). The Discord voice-channel bot mode has its own docs section — join the channel manually or have the agent join on a trigger word.

## Prompts

Voice is mostly transparent to prompting — you speak the same way you'd type. Useful patterns:

- Short spoken tasks that would be annoying to type: "add milk and coffee to the grocery list"
- Hands-free status checks: "what's on my calendar tomorrow?"
- Driving/walking: "send a Telegram to my partner saying I'll be 20 minutes late"

## Skills Needed

- Voice & TTS toolset enabled (`hermes tools`)
- A TTS provider (xAI TTS, ElevenLabs, or compatible)
- Transcription (Whisper local or API)
- Messaging gateway for the platform you're using (Telegram, Discord)

## Notes

- Latency is dominated by transcription and TTS, not the model turn. For responsiveness, a fast local Whisper and a streaming TTS provider make the biggest difference.
- Voice-channel mode in Discord is the most finicky — it needs persistent voice permissions on the bot and a VPS with outbound UDP unimpeded.
- Termux on Android has voice limitations noted in the official repo — the `.[termux]` extra deliberately skips some voice deps.

## Sources

- Official docs (platform/messaging): <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>
- Voice & TTS / provider docs: <https://hermes-agent.nousresearch.com/docs/integrations/providers/>
