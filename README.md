# growth-heartside

The organic acquisition engine for [Heartside](https://heartside.io), gifts from
your dog. Goal: **$10,000 of Shopify net sales in a calendar month**, with low
paid acquisition cost. This is an operating target, not a revenue guarantee or
an unconfirmed Christmas delivery promise.

The engine syncs real product truth, produces native marketing media, packages
reviewable drafts, keeps creative/evidence history and makes conservative
experiment recommendations. It never publishes social posts, sends outreach,
places gifts, confirms printing, changes the store or schedules paid AI requests.

**Start with [the completion handoff](docs/HANDOFF.md).**

- [Runbook and current capability limits](docs/ENGINE.md)
- [Acquisition strategy and 30-day experiment](STRATEGY.md)
- [AI production, provider budgets and provenance](docs/PROVIDERS.md)
- [Reference corpus: dog datasets and organic growth research](knowledge/README.md)
- [Control Center brief: the growth engine protocol](docs/CONTROL-CENTER-BRIEF.md)
- [Operating instructions](AGENTS.md), [playbook](PLAYBOOK.md), [browser boundary](BROWSER.md)
- [Product handoff in heartside PR #13](https://github.com/krishanraja/heartside/pull/13)

## Produce and review

```sh
# Use Python 3.12 for the full media runtime.
python3 -m pip install -r requirements-media.txt
# Install FFmpeg and ffprobe through your system package manager.
python3 growth.py sync
python3 growth.py readiness
python3 growth.py render campaigns/waits-at-the-door.json
```

Use the printed draft path with `growth.py check`, then `growth.py bundle` to
create a review ZIP. Unzip and open `review.html` for native videos, cover,
carousel, Stories, Pins, captions, subtitles and source/revision evidence.
`growth.py post` stores an internal pack; it does not publish a social post.
Every revision needs human review. Purchase claims stay gated to the actual
public gift range. The first campaigns are price-free audience materials.

## Scheduled operation

[Heartside draft engine](https://github.com/krishanraja/growth-heartside/actions/workflows/engine.yml)
checks these seven canonical jobs every 15 minutes on GitHub Actions:

| Job | Due in America/New_York |
|---|---|
| Sync | Daily 05:45 |
| Numbers | Daily 06:00 |
| Radar | Daily 06:30 |
| Daily media pack | Daily 09:00 |
| Creators | Tuesday 07:00 |
| Store and search | Saturday 07:00 |
| Weekly report | Sunday 07:00 |

IANA timezone conversion handles daylight saving. GitHub may run late. Completed
jobs are idempotent; failures remain retryable. Checkpoints restore verified
state between machines and runs. The separate hourly product sync keeps the
public `state/HEARTSIDE-NOW.md` current.

The fallback uses reusable approved assets, imported aggregate observations and
public-source research. It has no signed-in social browser or inherited private
Shopify connector. It does not pretend that missing analytics, creator evidence
or paid provider access is available. Connected Codex/Cowork authoring sessions
can follow the richer `jobs/` prompts and use their own connected AI tools.

Download `heartside-review` from the latest successful engine run to inspect the
current bundle. Download `heartside-state` to restore the whole hot workspace.
Read the runbook for retention, privacy, recovery and exact commands. No customer
data, named creator lists or credentials belong in public-repository artifacts.

## Repository boundaries

Product and fulfillment recommendations live in the separate heartside handoff.
This build makes no further changes there. Nothing here edits, merges, migrates or
deploys Control Center. Progress reaches it through the growth engine protocol:
the [Control Center directive](https://github.com/krishanraja/growth-heartside/actions/workflows/control-center.yml)
workflow answers its daily dispatch with one report (see the runbook). Pack
delivery stays disabled by default even when `GROWTH_ENGINE_TOKEN` exists, so
central UI work does not block creative production.
