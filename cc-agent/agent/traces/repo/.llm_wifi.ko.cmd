savedcmd_llm_wifi.ko := ld -r -m elf_x86_64 -z noexecstack --no-warn-rwx-segments --build-id=sha1  -T /home/FlexNGIA/bbr/scripts/module.lds -o llm_wifi.ko llm_wifi.o llm_wifi.mod.o .module-common.o
