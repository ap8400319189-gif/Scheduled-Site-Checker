# Scheduled-Site-Checker

Scheduled-Site-Checker keeps a Streamlit Community Cloud app from going to sleep by visiting it in a real
headless browser every 6 hours, using GitHub Actions. Free, and no hardware of your own needed.

**App being kept awake:** https://lecture-summ-ai.streamlit.app/

## Why this exists

Streamlit Community Cloud puts apps to sleep after about 12 hours without traffic.
Uptime monitors such as UptimeRobot only send plain HTTP requests. Streamlit answers
those with a static page and never starts the app, so the app still sleeps. Waking it
needs a real browser (JavaScript plus a WebSocket connection) or a click on the
"Yes, get this app back up!" button.

## How it works

1. GitHub Actions runs the workflow on a schedule (every 6 hours).
2. `keepalive.py` opens the app in headless Chromium using Playwright.
3. If the app is asleep, the script clicks the wake-up button.
4. It waits for the Streamlit app to finish loading, then stays connected for 15 seconds.
5. If the app does not load within 2 minutes, the run fails and GitHub emails you.

## Project structure

```
.
├── keepalive.py                      # Playwright script that visits/wakes the app
├── README.md
└── .github/
    └── workflows/
        └── keepalive.yml             # Schedule and job definition
```

## Setup

1. Create a new GitHub repo (public repos get free, unlimited Actions minutes).
2. Add `keepalive.py` to the repo root.
3. Add the workflow at `.github/workflows/keepalive.yml`.
   On GitHub: **Add file > Create new file**, type `.github/workflows/keepalive.yml`
   as the file name (the slashes create the folders), and paste the contents.
4. Commit and push.
5. Open the **Actions** tab, select **Keep Streamlit app awake**, and click **Run workflow**.
6. After about 2 minutes, a green check means it works.

## Configuration

| What | Where | Default |
|------|-------|---------|
| App URL | `APP_URL` in `keepalive.py` | `https://lecture-summ-ai.streamlit.app/` |
| Schedule | `cron` in `keepalive.yml` | `0 */6 * * *` (00:00, 06:00, 12:00, 18:00 UTC) |
| Load timeout | `timeout=120_000` in `keepalive.py` | 2 minutes |

Cron times are in UTC. 00:00, 06:00, 12:00 and 18:00 UTC equal 05:30, 11:30, 17:30 and 23:30 IST.

## Run it locally (optional)

```bash
pip install playwright
playwright install chromium
python keepalive.py
```

## Troubleshooting

- **Scheduled runs are late or skipped.** GitHub can delay cron jobs at busy times.
  The 6-hour interval leaves a buffer inside Streamlit's 12-hour limit.
- **Workflow stopped running.** GitHub pauses scheduled workflows after 60 days without
  repo activity. Re-enable it from the Actions tab.
- **Run fails with "app did not load".** Check the run log, then open the app in a
  browser to see if it has an error. If the app is fine, Streamlit may have changed its
  page structure and the iframe selector (`iframe[title='streamlitApp']`) needs updating.
- **Still sleeping.** Try a shorter interval, for example `0 */4 * * *`.
