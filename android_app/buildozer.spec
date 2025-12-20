[app]
title = NTRLI AI
package.name = ntrliai
package.domain = com.ntrli
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,json
version = 1.0.0

# Requirements for Android build - comprehensive list
requirements = python3==3.10.13,kivy==2.2.1,requests==2.31.0,certifi==2023.7.22,charset-normalizer==3.3.0,idna==3.4,urllib3==2.0.7

orientation = portrait
fullscreen = 0

# Android settings
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.skip_update = False
android.release_artifact = apk

# Buildozer settings
[buildozer]
log_level = 2
warn_on_root = 0
