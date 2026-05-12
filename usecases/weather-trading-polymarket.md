# Weather Trading on Polymarket

**Class:** Third-party integration · **Confidence:** Medium-High · **Status:** Real-world deployment, multiple traders

## Pain Point

Predictive markets like Polymarket require constant monitoring of forecast feeds, odds movements, and position sizing under uncertainty. Human traders miss signals, overreact to single data points, and size positions emotionally. Quant shops pay $500K+ salaries for teams that build and maintain this infrastructure.

## What It Does

Hermes Agent runs as a 24/7 autonomous trading agent on a $5/month VPS. It monitors weather forecast feeds, scores each market on expected value (EV), sizes positions via Kelly Criterion, and executes self-calibrating trades on Polymarket — without emotion, without sleep, and without manual intervention.

The agent stack:
- **Hermes Agent** — agent framework driving decisions
- **Kelly Criterion** — mathematically optimal position sizing based on edge and bankroll
- **EV scoring** — expected value calculation against market odds
- **Weather forecast feeds** — real-time data ingestion
- **Self-calibrating / self-learning** — feedback loop from trade outcomes to refine future scoring

**Deployments observed:**
- One trader: **$300 → $123K in 3 months**
- Another: **$440K profit in 20 days**
- **85% win rate** reported (850 green trades out of 1,000)
- Fully on-chain, no custom smart contract code required
- Deployable in ~30 minutes from published prompt

## Setup

1. Deploy Hermes Agent on a $5/month VPS (Hetzner, DigitalOcean, or similar)
2. Configure Polymarket wallet connection and API access
3. Feed the published prompt into Hermes (see Sources)
4. Point Hermes at weather forecast data feeds (public NOAA, ECMWF, or paid APIs)
5. Set Kelly Criterion bankroll constraints as guardrails
6. Let it run 24/7

## Notes

- This is a high-variance strategy — the traders sharing results are likely the survivors of a larger population, not a representative sample
- Cloud models recommended for reliability; local models have been reported to cause cron reliability issues with Hermes
- Position sizing and risk controls are the critical layer; EV without bankroll management is not a complete strategy
- Polymarket operates in a regulatory grey area in many jurisdictions; verify legality in your region before deploying

## Sources

- **Step-by-step guide:** Moonsat (Medium) — "Hermes Agent + Polymarket — how I built self-learning weather trading bot $100 → $5,000" — full install walkthrough, prompt template, and operational notes
- **Primary prompt:** RohOnChain — "The only prompt you need to build a self-learning Polymarket weather trading agent" — step-by-step deployable guide (X/Twitter)
- **Results thread:** @antpalkin — $440K profit in 20 days, 372 likes, 63 RTs (X/Twitter)
- **Trading stack overview:** @RoundtableSpace — $500K quant stack narrative, viral thread (X/Twitter)
- **Video walkthrough:** Craig Hewitt — "Hermes Just Solved the Biggest Problem With OpenClaw" — 59,499 views, covers Hermes as "brain" for automated trading bots (YouTube)
- **Analogy:** Hermes as the brain, OpenClaw as the arms — recurring pattern across trading agent descriptions
