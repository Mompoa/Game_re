[app]
title = Flappy YOLL
package.name = flappyyoll
package.domain = org.yoll.game

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3==3.10.12,pygame==2.5.2,cython

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET,VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = 
p4a.bootstrap = sdl2
android.add_src = src/main
android.add_aar =
