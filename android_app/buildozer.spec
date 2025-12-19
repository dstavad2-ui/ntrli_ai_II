# ============================================================================
# NTRLI' AI - Buildozer Specification (Production Ready)
# ============================================================================
# Build debug APK:   buildozer android debug
# Build release APK: buildozer android release
# Deploy to device:  buildozer android deploy run

[app]

# Application name
title = NTRLI AI

# Package name (no special characters, lowercase)
package.name = ntrliai

# Package domain (reverse DNS)
package.domain = com.ntrli

# Source code directory
source.dir = .

# Source files to include (only what we need)
source.include_exts = py,png,jpg,jpeg,ttf,json

# Source files to exclude
source.exclude_exts = spec,md,txt,rst

# Exclude directories
source.exclude_dirs = tests,bin,.buildozer,__pycache__,.git

# Application versioning
version = 1.0.0

# Requirements - MINIMAL set for fast builds and small APK
# requests: HTTP client for API calls
# certifi: SSL certificates for HTTPS
requirements = python3,kivy==2.3.0,requests,certifi,charset-normalizer,idna,urllib3

# Supported orientations
orientation = portrait

# Fullscreen mode (0 = windowed)
fullscreen = 0

# Android specific settings
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android API levels (API 24 = Android 7.0, good compatibility)
android.api = 33
android.minapi = 24

# Android NDK version (use stable version)
android.ndk = 25b

# Android SDK version
android.sdk = 33

# Target Android architectures (arm64 for modern, armeabi for older)
android.archs = arm64-v8a,armeabi-v7a

# Enable AndroidX (required for modern Android)
android.enable_androidx = True

# Accept Android SDK license automatically
android.accept_sdk_license = True

# Gradle dependencies (none needed - using pure Python)
# android.gradle_dependencies =

# Use AAB format for Play Store (set to 1 for release)
android.release_artifact = apk

# Optimize Kivy
android.add_aars =

# Presplash color
android.presplash_color = #1a1a2e

# Application icon (create 512x512 icon.png)
# icon.filename = %(source.dir)s/icon.png

# Presplash image (create 512x512 presplash.png)
# presplash.filename = %(source.dir)s/presplash.png

# Whitelist pattern for python files
android.whitelist =

# Blacklist pattern (exclude test files)
android.blacklist = .*test.*,.*spec.*

# Copy files to assets
# android.add_src =

# Enable adb debug
android.logcat_filters = *:S python:D

# Meta-data for AndroidManifest.xml
# android.meta_data =

# Additional Java packages
# android.add_jars =

# Wakelock (keep screen on)
android.wakelock = False

# Enable billing
android.billing = False

# Application log level
log_level = 2

# Warn on root
warn_on_root = 1

[buildozer]

# Buildozer log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning on root
warn_on_root = 1

# Build directory
# build_dir = .buildozer

# Bin directory
# bin_dir = bin
