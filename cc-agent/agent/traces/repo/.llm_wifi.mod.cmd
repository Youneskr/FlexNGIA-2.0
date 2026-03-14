savedcmd_llm_wifi.mod := printf '%s\n'   llm_wifi.o | awk '!x[$$0]++ { print("./"$$0) }' > llm_wifi.mod
