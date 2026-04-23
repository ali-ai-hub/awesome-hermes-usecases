# Android Device Control

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Community repo

## Pain Point

Your Android phone has apps and state (Maps, banking, messaging, 2FA codes) that aren't easily accessible from a VPS-side agent. You want to let Hermes do things *on your phone* — check a notification, read a screen, tap a button — from wherever the agent lives.

## What It Does

The `hermes-android` community plugin ships a Hermes-side plugin and an Android app. The Android app acts as a relay and exposes 36 `android_*` tools to the agent: take screenshots, tap coordinates, swipe, type text, read the current screen's accessibility tree, and more. The phone holds an outbound WebSocket to a small relay server, which sidesteps NAT and keeps the phone reachable even on mobile data.

The agent drives the phone the way a human would — screenshot, decide, tap — with the reasoning happening in Hermes.

## Setup

1. Install the Android app from the repo and grant it accessibility permission (required for reading screen content and simulating input).
2. Install the Hermes plugin on your Hermes host:
   ```
   ~/.hermes/plugins/hermes-android/
   ```
   Follow the repo's install instructions for exact layout.
3. Run the relay server (also in the repo) somewhere both the phone and the Hermes host can reach.
4. Pair the phone with the plugin using the pairing flow in the app.
5. Verify the tools show up:
   ```bash
   hermes tools    # look for the android_* group
   ```

## Prompts

Once paired, the phone is just another tool surface:

```
Open Google Maps on my phone, search for coffee shops near me,
and tell me the top 3 with their ratings.
```

```
Read the latest 2FA code from my authenticator app and come back
with just the number.
```

```
Take a screenshot of my home screen so I can see what's on it.
```

## Skills Needed

- Android app installed and accessibility permission granted
- Hermes plugin in `~/.hermes/plugins/`
- Relay server reachable from both sides

## Security Notes

- Accessibility permission is powerful — the app can read anything on screen. Treat the Hermes instance controlling the phone with the same trust you give your phone itself.
- A compromised Hermes can drain your banking app. If you're running Hermes on a VPS, think hard about whether that VPS should have remote control of your phone.
- This is a community extension, not an official Nous repo. Review the code before installing.

## Sources

- Community repo: <https://github.com/raulvidis/hermes-android>
