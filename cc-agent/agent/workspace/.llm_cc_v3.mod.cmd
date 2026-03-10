savedcmd_llm_cc_v3.mod := printf '%s\n'   llm_cc_v3.o | awk '!x[$$0]++ { print("./"$$0) }' > llm_cc_v3.mod
