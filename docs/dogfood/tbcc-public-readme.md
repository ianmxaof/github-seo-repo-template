# Telegram Bot Command Center (TBCC)

A self-hosted command center for Telegram channel operators: schedule posts, organize media pools, and run checkout from a FastAPI backend, Celery workers, and a React ops dashboard.

## What this project provides

- Scheduler for one-off and recurring channel posts, campaigns, and caption HTML
- Media library with pools, tags, URL import, and an optional Chrome extension
- Celery plus Redis workers for posting, scrape jobs, and subscriptions
- React dashboard for media, scheduler, commerce, and system health
- Admin, scraper, and payment bots that talk to the same API

## Who should use this

Operators who already post to Telegram channels and want a local or VPS-hosted control plane. Not a hosted SaaS and not a growth-hacking kit.

## Quick start

1. Copy `tbcc/.env.example` to `tbcc/.env` and set Telegram API credentials.
2. From `tbcc/`, run the documented start script (dashboard on localhost).
3. Open the React dashboard and connect a channel plus a media pool.
4. For scheduled sending, run Redis and Celery (see `tbcc/README.md` in the checkout).

## Usage

Import media into a pool, approve it, attach a caption, then schedule a post or campaign. Optional: Chrome extension Send to TBCC from a normal https page.

## License

See the repository license file. Secrets and production hosts stay out of git.
