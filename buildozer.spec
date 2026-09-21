[app]
title = NightLoad
package.name = nightload
package.domain = com.nightload.app

source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 35
android.minapi = 23
android.ndk = 27c
android.ndk_api = 23

android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
