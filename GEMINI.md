# Instagram Close Friends BOT

Automates mass-adding Instagram followers to your Close Friends list using Selenium and mobile emulation.

## Project Overview

- **Purpose**: Mass-add followers to the Close Friends list to increase story visibility and engagement.
- **Technology Stack**: 
  - **Language**: Python 3.x
  - **Automation**: Selenium WebDriver (with mobile emulation for Pixel 2).
  - **Dependencies**: `selenium`, `chromedriver_autoinstaller`, `instagrapi` (optional/integrated), `Pillow`.
- **Architecture**:
  - `SRC/close_friends.py`: Main entry point and automation logic.
  - `SRC/config.py`: User-defined credentials and target account settings.
  - `SRC/session_settings.json`: Persisted session data for session-based login (to avoid frequent login challenges).
  - `SRC/log/`, `SRC/extractions/`, `SRC/trace_out/`: Operational directories for logs, data extraction, and tracing.

## Building and Running

### Prerequisites
- Python 3.x installed.
- Google Chrome installed.

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution
1. Configure credentials in `SRC/config.py`:
   - `USERNAME`: Your Instagram handle.
   - `PASSWORD`: Your Instagram password.
   - `TARGET`: The target account for operations.
2. Run the bot:
   ```bash
   python SRC/close_friends.py
   ```

## Development Conventions

- **Environment**: All operations are focused within the `SRC/` directory.
- **Login Strategy**: Uses Selenium with mobile emulation (`Pixel 2`) to mimic mobile behavior. Handles 2FA/Security Codes via terminal input (`CHALLENGE_WAIT_TIME`).
- **Safety**: Includes a beta disclaimer and warning about potential account bans. Use with caution and preferably on test accounts.
- **Code Style**: Standard Python script structure. Selenium wait patterns (`WebDriverWait`) are preferred over hard `time.sleep` (though some sleeps are present for UI stability).

## Task Management & Memory

- **TODOs**: 
  - Refine `session_settings.json` integration (ensure it persists properly between runs).
  - Implement follower extraction logic (currently `close_friends.py` handles login but the full mass-add loop is under development).
  - Add robust logging to `SRC/log/`.

## Key Files
- `SRC/close_friends.py`: Main logic for Instagram interaction.
- `SRC/config.py`: Central configuration for credentials.
- `requirements.txt`: Project dependencies.
