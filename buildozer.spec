[app]
title = Mychelle Beauty
package.name = mychellebeauty
package.domain = org.mychelle
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1

# Versão mínima do Android suportada
android.api = 33
# Versão do NDK usada pelo Buildozer
android.ndk = 25b
# Versão mínima do Android para rodar o app
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
