# Changelog

## 1.0.3 — 2026-11-26

- Skip identical billing state writes while preserving changed counters and dates.
- Declare statistics classes for numeric page and ink sensors.


## 1.0.2
- Fixed integration setup when the printer is temporarily unavailable.
- Added ConfigEntryNotReady handling during coordinator initialization.
- Home Assistant now automatically retries setup after connection failures.
- 
## 1.0.0

- First public release.
- Local reading of the printer `SubscriptionImpressions` counter.
- Monthly allowance, rollover balance, total remaining pages and cycle usage.
- Explicit initialization from the subscription account's monthly and rollover values.
- Automatic renewal handling with configurable rollover cap.
- Black, cyan, magenta and yellow ink-level sensors.
- 120-second local polling.
- Persistent billing state and cleanup when the config entry is removed.
- Diagnostics with printer host redacted.
- English and Italian translations.
- Original, vendor-neutral local branding.
