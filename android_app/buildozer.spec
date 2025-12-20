[app]
title = NTRLI AI
package.name = ntrliai
package.domain = com.ntrli
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,json
version = 1.0.0

# Minimal requirements for reliable build
requirements = python3,kivy,requests,certifi

orientation = portrait
fullscreen = 0

# Android settings
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
