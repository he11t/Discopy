# 🚀 Discopy - Professional Discord Server Cloner

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-proprietary-red.svg?style=for-the-badge)
[![Contact](https://img.shields.io/badge/contact-sns2mhd%40gmail.com-orange.svg?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sns2mhd@gmail.com)

<img src="https://raw.githubusercontent.com/shalanv/discopy/main/assets/banner.png" alt="Discopy Banner" width="600"/>

**The Most Advanced Discord Server Cloning Tool**

[Features](#✨-features) • [Installation](#🔧-installation) • [Usage](#📚-usage) • [Security](#🔒-security) • [Support](#💬-support)

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **Complete Server Copying**
  - Roles & Permissions
  - Channels & Categories
  - Emojis & Stickers
  - Server Settings & Icon
  - Webhooks & Integrations

### 📊 Advanced Features
- **Real-time Progress Tracking**
  - Visual Progress Bars
  - Detailed Status Updates
  - Error Reporting
  - Time Estimates

### 🛡️ Security Features
- **Enterprise-grade Protection**
  - Anti-tampering System
  - Integrity Verification
  - Copyright Protection
  - Secure Token Handling

### 🎨 User Experience
- **Professional Interface**
  - Rich Console UI
  - Color-coded Output
  - Interactive Menus
  - Detailed Logging

---

## 🔧 Installation

### 📋 Requirements

#### System Requirements
- Windows 10/11 or Linux/macOS
- Python 3.8 or higher
- 2GB RAM minimum
- Stable internet connection

#### Discord Requirements
- Discord account with valid token
- Administrator permissions in source server
- Administrator permissions in target server (if copying to existing)
- 2FA enabled (for certain Discord actions)

#### Python Dependencies
- aiohttp>=3.8.0
- python-dotenv>=0.19.0
- rich>=10.0.0
- colorama>=0.4.4
- discord.py>=2.0.0

### 🚀 Installation Guide

#### Step 1: Python Setup
1. Download Python 3.8 or higher from [python.org](https://python.org)
2. During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"

#### Step 2: Download Discopy
```bash
# Clone the repository
git clone https://github.com/yourusername/discopy.git

# Navigate to directory
cd discopy

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import aiohttp, dotenv, rich, colorama, discord"
```

#### Step 4: Configuration
1. Create `.env` file in the project root:
```env
# Discord token (required)
DISCORD_TOKEN=your_token_here

# Optional settings
LOG_LEVEL=INFO
RATE_LIMIT_DELAY=1.5
```

2. Verify `config.json` exists and contains default settings:
```json
{
    "version": "2.0",
    "settings": {
        "rate_limit_delay": 1.5,
        "max_retries": 3,
        "timeout": 30,
        "log_level": "INFO"
    }
}
```

#### Step 5: Security Verification
```bash
# Run the verification check
python discopy.py --verify

# Expected output:
✅ Security verification passed
✅ Copyright verification passed
✅ Configuration valid
```

#### Step 6: Test Run
```bash
# Start Discopy
python discopy.py

# You should see the main menu:
# ╔════════════════════════════╗
# ║      Discopy Menu         ║
# ╚════════════════════════════╝
```

#### Troubleshooting

##### Common Issues
1. **"Python not found" error**
   - Ensure Python is added to PATH
   - Try running `py` instead of `python`

2. **Dependencies installation fails**
   ```bash
   # Try updating pip first
   python -m pip install --upgrade pip
   # Then install dependencies
   pip install -r requirements.txt
   ```

3. **Token verification fails**
   - Ensure token is valid and not expired
   - Check Discord account status
   - Verify network connection

4. **Security verification fails**
   ```bash
   # Reset configuration
   cp config.json.example config.json
   # Try running again
   python discopy.py
   ```

##### Getting Help
If you encounter any issues:
1. Check the [Common Issues](#common-issues) section
2. Review the logs in `logs/discopy.log`
3. Contact support with error details:
   - Email: sns2mhd@gmail.com
   - Include log files
   - Describe your system setup

---

## 📚 Usage

### 🚀 Quick Start

1. **Launch Discopy**
   ```bash
   python discopy.py
   ```

2. **Main Menu Options**
   - `Copy Server` - Create new server with content
   - `Clean Server` - Remove all content
   - `Copy to Existing` - Copy to existing server

### 💡 Best Practices

- Always verify source server permissions
- Backup important data before cleaning servers
- Use rate limiting for large servers
- Keep your token secure

---

## 🔒 Security

### 🛡️ Protection Features

- **File Integrity**
  - Checksum verification
  - Runtime protection
  - Anti-debugging measures

- **Copyright Protection**
  - Legal safeguards
  - Tampering detection
  - Unauthorized use prevention

### ⚠️ Important Notes

- Keep your Discord token private
- Don't share modified versions
- Report security issues
- Regular updates recommended

---

## 💬 Support

### 📧 Contact

- **Email**: sns2mhd@gmail.com
- **Discord**: shalan.v
- **GitHub**: @shalanv

### 🆘 Common Issues

<details>
<summary>Token Validation Failed</summary>
Ensure you're using a valid user token, not a bot token.
</details>

<details>
<summary>Rate Limiting</summary>
Adjust RATE_LIMIT_DELAY in .env for your needs.
</details>

<details>
<summary>Permission Errors</summary>
Verify you have administrator permissions in both servers.
</details>

---

## ⚖️ Legal

### 📜 License
```
Copyright (c) 2024 shalan.v
All Rights Reserved

Discopy is proprietary and confidential software.
Unauthorized copying, modification, distribution, or use is strictly prohibited.
```

### ⚠️ Disclaimer

This tool is for personal use only. Users are responsible for compliance with Discord's Terms of Service.

---

<div align="center">

**Made with ❤️ by shalan.v**

[🔝 Back to Top](#-discopy---professional-discord-server-cloner)

</div>

```
╔══════════════════════════════════════════════════╗
║             SECURITY & COPYRIGHT NOTICE           ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  ⚠️ This software is protected by copyright law   ║
║  and includes anti-tampering security measures.   ║
║                                                  ║
║  • Modification of ANY files is prohibited       ║
║  • Removal of copyright notices is prohibited    ║
║  • Unauthorized redistribution is prohibited     ║
║                                                  ║
║  Violations will result in immediate software    ║
║  termination and potential legal action.         ║
║                                                  ║
║  By using this software, you agree to these     ║
║  terms and conditions.                          ║
║                                                  ║
║  © 2024 shalan.v - All Rights Reserved          ║
╚══════════════════════════════════════════════════╝

```
╔══════════════════════════════════════════════════╗
║               LEGAL DISCLAIMER                    ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  1. This software is protected by copyright law  ║
║     and international treaties.                  ║
║                                                  ║
║  2. ANY unauthorized modification, including:    ║
║     • Editing any files                         ║
║     • Removing copyright notices                 ║
║     • Disabling security features               ║
║     • Redistributing the code                   ║
║     Is STRICTLY PROHIBITED and will result in   ║
║     immediate termination of your right to use  ║
║     this software.                              ║
║                                                  ║
║  3. Violations may result in legal action.      ║
║                                                  ║
║  By using this software, you agree to these     ║
║  terms and conditions.                          ║
║                                                  ║
║  © 2024 shalan.v - All Rights Reserved          ║
╚══════════════════════════════════════════════════╝
