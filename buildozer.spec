[app]
title = Memory Reminder
package.name = memoryreminder
package.domain = org.tidharla
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = RECORD_AUDIO
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.build_tools_version = 33.0.0
android.accept_sdk_license = True
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653

