# Streak Saver

This Python program is designed to help you maintain your GitHub contribution heatmap streak. It runs automatically when your system starts up and makes a small, harmless commit to a designated GitHub repository to ensure your streak remains unbroken.

## How it Works

When executed, the script performs the following actions:

1.  Checks if it's the first run of the day (to avoid unnecessary commits).
2.  Creates a new commit with a simple message like 'Streak Saver: Daily Check-in'.
3.  Pushes this commit to your GitHub repository.

## Setup

### 1. Prerequisites

*   **Python 3:** Ensure you have Python 3 installed on your system.
*   **Git:** Git must be installed and configured on your system.
*   **GitHub Repository:** You'll need a GitHub repository where you want to make these commits. This can be a new repository or an existing one. For simplicity, it's recommended to create a dedicated repository for streak saving.
*   **GitHub Personal Access Token:** You will need a Personal Access Token (PAT) with `repo` scope to authenticate with GitHub.

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/streak-saver.git
    cd streak-saver
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

1.  **Create a configuration file:** Create a file named `config.ini` in the root of the `streak-saver` directory with the following structure:

    ```ini
    [github]
    username = your_github_username
    repo_name = your_repository_name
    token = your_github_personal_access_token
    ```

    *   Replace `your_github_username` with your actual GitHub username.
    *   Replace `your_repository_name` with the name of the repository you want to contribute to.
    *   Replace `your_github_personal_access_token` with your generated Personal Access Token.

    **Important:** Treat your Personal Access Token like a password. Do not commit it to your repository. Ensure your `config.ini` file is added to the `.gitignore` file.

### 4. Automating Startup

To ensure the script runs every time you open your system, you need to add it to your system's startup applications.

*   **Windows:**
    *   Press `Win + R`, type `shell:startup`, and press Enter. This will open the Startup folder.
    *   Create a shortcut to your Python script (e.g., `run_streak_saver.bat`) that activates the virtual environment and runs the `streak_saver.py` script.

    Example `run_streak_saver.bat`:
    ```batch
    @echo off
    call venv\Scripts\activate
    python streak_saver.py
    exit
    ```
    Place this `.bat` file shortcut in the Startup folder.

*   **macOS:**
    *   You can use `launchd` to schedule the script to run at login. Create a `.plist` file in `~/Library/LaunchAgents/`.

    Example `com.user.streaksavetask.plist`:
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.user.streaksavetask</string>
        <key>ProgramArguments</key>
        <array>
            <string>/path/to/your/venv/bin/python</string>
            <string>/path/to/your/streak-saver/streak_saver.py</string>
        </array>
        <key>StartCalendarInterval</key>
        <dict>
            <key>Minute</key>
            <integer>0</integer>
            <key>Hour</key>
            <integer>9</integer>
        </dict>
        <key>RunAtLoad</key>
        <true/>
        <key>StandardOutPath</key>
        <string>/tmp/streak_saver.log</string>
        <key>StandardErrorPath</key>
        <string>/tmp/streak_saver.log</string>
    </dict>
    </plist>
    ```
    Replace `/path/to/your/venv/bin/python` and `/path/to/your/streak-saver/streak_saver.py` with the actual paths. Load it using `launchctl load ~/Library/LaunchAgents/com.user.streaksavetask.plist`.

*   **Linux:**
    *   You can use `cron` or systemd timers. For startup, systemd timers are generally preferred.

    Create a service file (e.g., `/etc/systemd/system/streak-saver.service`):
    ```ini
    [Unit]
    Description=GitHub Streak Saver
    After=network.target

    [Service]
    ExecStart=/path/to/your/venv/bin/python /path/to/your/streak-saver/streak_saver.py
    WorkingDirectory=/path/to/your/streak-saver
    User=your_username
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target
    ```
    Replace paths and `your_username`. Then run `sudo systemctl enable streak-saver.service`.

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
