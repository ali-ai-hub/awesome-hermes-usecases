# Home Assistant Control

**Class:** Official integration · **Confidence:** High · **Demo status:** Docs + runbook

## Pain Point

Home Assistant's dashboards are powerful but dense. "What's the temperature in the kitchen?" or "turn off every light downstairs" is faster to say than to find in a UI. You want a conversational layer in front of Home Assistant that can reason about state and call services, not a canned voice assistant that only knows a few phrases.

## What It Does

Hermes ships four built-in Home Assistant tools: `ha_list_entities`, `ha_get_state`, `ha_list_services`, and `ha_call_service`. Given a long-lived Home Assistant token, the agent can discover your devices, read state, and call any service Home Assistant exposes. That covers lights, climate, media players, scenes, automations — anything exposed through HA's service registry.

You ask it things the way you'd ask a person, and it resolves entity IDs and service calls itself.

## Setup

1. In Home Assistant → your user profile → Long-Lived Access Tokens → create a token.
2. Configure Hermes:
   ```bash
   hermes config set homeassistant.url "http://homeassistant.local:8123"
   hermes config set homeassistant.token "YOUR_LONG_LIVED_TOKEN"
   ```
   Or in `.env`:
   ```
   HASS_URL=http://homeassistant.local:8123
   HASS_TOKEN=YOUR_LONG_LIVED_TOKEN
   ```
3. Enable the HA tool group:
   ```bash
   hermes tools         # interactive: enable the home-assistant group
   ```
4. Test:
   ```bash
   hermes
   > What's the temperature in the living room?
   > Turn off all downstairs lights.
   > What scenes are available?
   ```

## Prompts

Exploration first — let the agent discover what it's working with:

```
List every entity in the "climate" and "light" domains so I can see
what's controllable. Then tell me which lights are currently on.
```

Automation-style:

```
If the living room temperature drops below 19°C after sunset, turn on
the fireplace scene. Check current state and confirm whether this is
already active.
```

## Skills Needed

- Home Assistant tools (built-in, enabled via `hermes tools`)
- Long-lived access token from HA

## Notes

- The agent has full control — treat the HA token like any other secret. Revoke it in HA's UI if the Hermes host is compromised.
- For voice, pair this with the Telegram or Discord gateway so you can message "turn off the lights" from your phone without opening the HA app.

## Sources

- Official docs: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant/>
