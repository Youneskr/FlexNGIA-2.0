savedcmd_wifi.mod := printf '%s\n'   wifi.o | awk '!x[$$0]++ { print("./"$$0) }' > wifi.mod
