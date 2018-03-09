# ethogram <img src="https://i.imgur.com/YWMAUVL.png" alt="alt text" width="30" height="30">

Telegram bot for ethOS! Feel free to use it by adding `@ethogramBot` to a group, or chatting with it directly.

Since the bot now tracks the chat id's in a file, even if it restarts, we can alert users of downtime, or possible issues with the bot itself by sending status messages (not implemented yet).

## Getting Started

- Just add `ethogramBot` to the group, or chat it up directly.
- run `/start [PANEL_ID]` to monitor [PANEL_ID].ethosdistro.com

## Metrics

| action | alert | description |
|---|---|---|
| all_stats | :white_check_mark: | send all available stats |
| gpu_temps | :white_check_mark: | Alert range 40 - 75 C |
| hashrates | :white_check_mark: | Alert increase/decrease of +10% |
| timestamp | :white_check_mark: | Alert if t(n) > t(n+1) |

### Demo

![](https://i.imgur.com/tRs6NRr.png)

![](https://i.imgur.com/e4dpk06.png)

![](https://i.imgur.com/iq3USEv.png)
