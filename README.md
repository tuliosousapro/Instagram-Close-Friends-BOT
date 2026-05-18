<h1 align="center">Instagram Close Friends BOT</h1>
<p align="center"><em>Mass-add all your Instagram followers into your Close Friends list — grant visibility to your stories and boost engagement.</em></p>
<p align="center">
  <img src="https://img.shields.io/badge/Under_Development-BETA-orange">
  <img src="https://img.shields.io/badge/License-GPLv3-blue">
  <img src="https://img.shields.io/badge/Made%20with-Python-green">
  <img src="https://img.shields.io/github/issues/tuliosousapro/Instagram-Close-Friends-BOT">
  <img src="https://img.shields.io/github/stars/tuliosousapro/Instagram-Close-Friends-BOT?style=social">
</p>


## ✨ Features
- 🚀 Automatically adds all your followers to your Close Friends list.
- 🔒 Uses session settings for secure login.
- 🧠 Simple configuration via `.env` (loaded by `SRC/config.py`).
- 📦 Lightweight and fast — built with pure Python.

## ⚙️ Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/tuliosousapro/Instagram-Close-Friends-BOT.git
   cd Instagram-Close-Friends-BOT
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## ⚠️ Beta Disclaimer
> 🚧 This project is currently in BETA. That means:
> 
> Features may change or break unexpectedly.
> 
> Bugs might appear like uninvited guests at a party.
> 
> Documentation and setup instructions are still evolving.
> 
> We recommend using this bot in a test environment first. If you encounter issues, please open an issue and help us improve it!   


## 🛠️ Setup
1. Create a `.env` file in the repository root with your credentials and settings (see `.env.example`).
2. Ensure your session settings are saved in `SRC/session_settings.json` or the path configured by `SESSION_FILE`.
3. Run the bot:
   ```bash
   python SRC/close_friends.py
   ```

## 🚀 Usage
- The bot will log in using your session and begin adding followers to your Close Friends list.
- Monitor the terminal for progress and status updates.

## 🧪 Development
- **Key files**:
  - `SRC/close_friends.py`: Main bot logic.
  - `SRC/config.py`: Loads and validates user configuration from `.env`.
  - `SRC/session_settings.json`: Session data.
- **Language**: Python 3.x
- **Dependencies**: Listed in `requirements.txt`

## 🤝 Contributing <img src="https://img.shields.io/github/contributors/tuliosousapro/Instagram-Close-Friends-BOT">
We welcome contributions! To contribute:
1. Fork the repo.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push and open a pull request.

## 🔐 License
This project is licensed under the **GNU GPLv3**. See the [LICENSE](LICENSE) file for details.

## 👾 Issues
Found a bug or have a feature request? Open an issue in this repo.

## ⭐️ Support
If this bot made your Instagram life easier, give it a ⭐ and share it with your fellow social media **HACKERS💀**.

---

> #### ⚠️ Disclaimer: Please note that this is a research project. I am by no means responsible for any usage of this tool. Use it at your own risk. I'm also not responsible if your accounts get banned due to the extensive use of this tool.
