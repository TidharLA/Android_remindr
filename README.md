# AndroidReminderKivyApp

A clean Android Kivy reminder app folder you can push to GitHub.

## What it does
- Save memories like: `I put the key in drawer`
- Look up and auto-delete: `Where is the key?`
- Stores data locally in SQLite on the phone

## Files
- `main.py` - Kivy app UI
- `logic.py` - parsing + SQLite logic
- `buildozer.spec` - Android packaging config
- `requirements.txt` - Python dependency list
- `run_desktop.py` - optional desktop launcher
- `tests/test_logic_unittest.py` - quick logic test
- `.github/workflows/build-android-apk.yml` - GitHub Actions APK build

## Windows-friendly use
You can edit this folder on Windows and push it to GitHub.
Build the APK in GitHub Actions or later with Linux/WSL.

## Local test on Windows
```powershell
cd AndroidReminderKivyApp
python -m unittest tests.test_logic_unittest -v
```

## GitHub Actions build
Use the workflow file in `.github/workflows/build-android-apk.yml` to build an APK on GitHub's Linux runner.

## Install on Android
After the APK is built:
1. Download the artifact
2. Copy APK to your phone
3. Tap it in Files
4. Allow unknown apps if prompted
5. Install

