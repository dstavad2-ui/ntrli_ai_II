# ============================================================================
# NTRLI' AI - Buildozer Specification
# ============================================================================
# Build APK: buildozer android debug
# Build release APK: buildozer android release

[app]

# Application name
title = NTRLI AI

# Package name
package.name = ntrliai

# Package domain
package.domain = ai.ntrli

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# Source files to exclude
source.exclude_exts = spec

# Application versioning
version = 1.0.0

# Application requirements
requirements = python3,kivy,requests,beautifulsoup4,jsonschema

# Supported orientations
orientation = portrait

# Fullscreen mode
fullscreen = 0

# Android specific settings
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android API levels
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33

# Android architectures
android.archs = arm64-v8a, armeabi-v7a

# Enable AndroidX
android.enable_androidx = True

# Accept Android SDK license
android.accept_sdk_license = True

# Application icon
# icon.filename = %(source.dir)s/icon.png

# Presplash image
# presplash.filename = %(source.dir)s/presplash.png

# Application log level
log_level = 2

# Build warnings
warn_on_root = 1

[buildozer]

# Buildozer log level
log_level = 2

# Display warning on root
warn_on_root = 1
