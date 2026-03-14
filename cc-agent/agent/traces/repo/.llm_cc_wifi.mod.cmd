savedcmd_llm_cc_wifi.mod := printf '%s\n'   llm_cc_wifi.o | awk '!x[$$0]++ { print("./"$$0) }' > llm_cc_wifi.mod
