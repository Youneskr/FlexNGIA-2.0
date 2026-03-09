savedcmd_llm_cc_v3.o := gcc -Wp,-MMD,./.llm_cc_v3.o.d -nostdinc -I/home/younes/bbr/arch/x86/include -I/home/younes/bbr/arch/x86/include/generated -I/home/younes/bbr/include -I/home/younes/bbr/include -I/home/younes/bbr/arch/x86/include/uapi -I/home/younes/bbr/arch/x86/include/generated/uapi -I/home/younes/bbr/include/uapi -I/home/younes/bbr/include/generated/uapi -include /home/younes/bbr/include/linux/compiler-version.h -include /home/younes/bbr/include/linux/kconfig.h -include /home/younes/bbr/include/linux/compiler_types.h -D__KERNEL__ -std=gnu11 -fshort-wchar -funsigned-char -fno-common -fno-PIE -fno-strict-aliasing -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx -fcf-protection=none -m64 -falign-jumps=1 -falign-loops=1 -mno-80387 -mno-fp-ret-in-387 -mpreferred-stack-boundary=3 -mskip-rax-setup -mtune=generic -mno-red-zone -mcmodel=kernel -Wno-sign-compare -fno-asynchronous-unwind-tables -mindirect-branch=thunk-extern -mindirect-branch-register -mindirect-branch-cs-prefix -mfunction-return=thunk-extern -fno-jump-tables -mharden-sls=all -fpatchable-function-entry=16,16 -fno-delete-null-pointer-checks -O2 -fno-allow-store-data-races -fstack-protector-strong -fno-omit-frame-pointer -fno-optimize-sibling-calls -ftrivial-auto-var-init=zero -fno-stack-clash-protection -fzero-call-used-regs=used-gpr -pg -mrecord-mcount -mfentry -DCC_USING_FENTRY -falign-functions=16 -fstrict-flex-arrays=3 -fno-strict-overflow -fno-stack-check -fconserve-stack -Wall -Wundef -Werror=implicit-function-declaration -Werror=implicit-int -Werror=return-type -Werror=strict-prototypes -Wno-format-security -Wno-trigraphs -Wno-frame-address -Wno-address-of-packed-member -Wmissing-declarations -Wmissing-prototypes -Wframe-larger-than=1024 -Wno-main -Wno-dangling-pointer -Wvla -Wno-pointer-sign -Wcast-function-type -Wno-stringop-overflow -Wno-array-bounds -Wno-alloc-size-larger-than -Wimplicit-fallthrough=5 -Werror=date-time -Werror=incompatible-pointer-types -Werror=designated-init -Wenum-conversion -Wextra -Wunused -Wno-unused-but-set-variable -Wno-unused-const-variable -Wno-packed-not-aligned -Wno-format-overflow -Wno-format-truncation -Wno-stringop-truncation -Wno-override-init -Wno-missing-field-initializers -Wno-type-limits -Wno-shift-negative-value -Wno-maybe-uninitialized -Wno-sign-compare -Wno-unused-parameter -g -gdwarf-5  -fsanitize=bounds-strict -fsanitize=shift -fsanitize=bool -fsanitize=enum  -fsanitize=signed-integer-overflow  -DMODULE  -DKBUILD_BASENAME='"llm_cc_v3"' -DKBUILD_MODNAME='"llm_cc_v3"' -D__KBUILD_MODNAME=kmod_llm_cc_v3 -c -o llm_cc_v3.o llm_cc_v3.c   ; /home/younes/bbr/tools/objtool/objtool --hacks=jump_label --hacks=noinstr --hacks=skylake --retpoline --rethunk --sls --stackval --static-call --uaccess --prefix=16   --module llm_cc_v3.o

source_llm_cc_v3.o := llm_cc_v3.c

deps_llm_cc_v3.o := \
  /home/younes/bbr/include/linux/compiler-version.h \
    $(wildcard include/config/CC_VERSION_TEXT) \
  /home/younes/bbr/include/linux/kconfig.h \
    $(wildcard include/config/CPU_BIG_ENDIAN) \
    $(wildcard include/config/BOOGER) \
    $(wildcard include/config/FOO) \
  /home/younes/bbr/include/linux/compiler_types.h \
    $(wildcard include/config/DEBUG_INFO_BTF) \
    $(wildcard include/config/PAHOLE_HAS_BTF_TAG) \
    $(wildcard include/config/FUNCTION_ALIGNMENT) \
    $(wildcard include/config/CC_HAS_SANE_FUNCTION_ALIGNMENT) \
    $(wildcard include/config/X86_64) \
    $(wildcard include/config/ARM64) \
    $(wildcard include/config/LD_DEAD_CODE_DATA_ELIMINATION) \
    $(wildcard include/config/LTO_CLANG) \
    $(wildcard include/config/HAVE_ARCH_COMPILER_H) \
    $(wildcard include/config/CC_HAS_COUNTED_BY) \
    $(wildcard include/config/UBSAN_SIGNED_WRAP) \
    $(wildcard include/config/CC_HAS_ASM_INLINE) \
  /home/younes/bbr/include/linux/compiler_attributes.h \
  /home/younes/bbr/include/linux/compiler-gcc.h \
    $(wildcard include/config/MITIGATION_RETPOLINE) \
    $(wildcard include/config/ARCH_USE_BUILTIN_BSWAP) \
    $(wildcard include/config/SHADOW_CALL_STACK) \
    $(wildcard include/config/KCOV) \
  /home/younes/bbr/include/linux/module.h \
    $(wildcard include/config/MODULES) \
    $(wildcard include/config/SYSFS) \
    $(wildcard include/config/MODULES_TREE_LOOKUP) \
    $(wildcard include/config/LIVEPATCH) \
    $(wildcard include/config/STACKTRACE_BUILD_ID) \
    $(wildcard include/config/ARCH_USES_CFI_TRAPS) \
    $(wildcard include/config/MODULE_SIG) \
    $(wildcard include/config/GENERIC_BUG) \
    $(wildcard include/config/KALLSYMS) \
    $(wildcard include/config/SMP) \
    $(wildcard include/config/TRACEPOINTS) \
    $(wildcard include/config/TREE_SRCU) \
    $(wildcard include/config/BPF_EVENTS) \
    $(wildcard include/config/DEBUG_INFO_BTF_MODULES) \
    $(wildcard include/config/JUMP_LABEL) \
    $(wildcard include/config/TRACING) \
    $(wildcard include/config/EVENT_TRACING) \
    $(wildcard include/config/FTRACE_MCOUNT_RECORD) \
    $(wildcard include/config/KPROBES) \
    $(wildcard include/config/HAVE_STATIC_CALL_INLINE) \
    $(wildcard include/config/KUNIT) \
    $(wildcard include/config/PRINTK_INDEX) \
    $(wildcard include/config/MODULE_UNLOAD) \
    $(wildcard include/config/CONSTRUCTORS) \
    $(wildcard include/config/FUNCTION_ERROR_INJECTION) \
    $(wildcard include/config/DYNAMIC_DEBUG_CORE) \
    $(wildcard include/config/ARCH_HAS_EXECMEM_ROX) \
  /home/younes/bbr/include/linux/list.h \
    $(wildcard include/config/LIST_HARDENED) \
    $(wildcard include/config/DEBUG_LIST) \
  /home/younes/bbr/include/linux/container_of.h \
  /home/younes/bbr/include/linux/build_bug.h \
  /home/younes/bbr/include/linux/compiler.h \
    $(wildcard include/config/TRACE_BRANCH_PROFILING) \
    $(wildcard include/config/PROFILE_ALL_BRANCHES) \
    $(wildcard include/config/OBJTOOL) \
    $(wildcard include/config/64BIT) \
  /home/younes/bbr/arch/x86/include/generated/asm/rwonce.h \
  /home/younes/bbr/include/asm-generic/rwonce.h \
  /home/younes/bbr/include/linux/kasan-checks.h \
    $(wildcard include/config/KASAN_GENERIC) \
    $(wildcard include/config/KASAN_SW_TAGS) \
  /home/younes/bbr/include/linux/types.h \
    $(wildcard include/config/HAVE_UID16) \
    $(wildcard include/config/UID16) \
    $(wildcard include/config/ARCH_DMA_ADDR_T_64BIT) \
    $(wildcard include/config/PHYS_ADDR_T_64BIT) \
    $(wildcard include/config/ARCH_32BIT_USTAT_F_TINODE) \
  /home/younes/bbr/include/uapi/linux/types.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/types.h \
  /home/younes/bbr/include/uapi/asm-generic/types.h \
  /home/younes/bbr/include/asm-generic/int-ll64.h \
  /home/younes/bbr/include/uapi/asm-generic/int-ll64.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/bitsperlong.h \
  /home/younes/bbr/include/asm-generic/bitsperlong.h \
  /home/younes/bbr/include/uapi/asm-generic/bitsperlong.h \
  /home/younes/bbr/include/uapi/linux/posix_types.h \
  /home/younes/bbr/include/linux/stddef.h \
  /home/younes/bbr/include/uapi/linux/stddef.h \
  /home/younes/bbr/arch/x86/include/asm/posix_types.h \
    $(wildcard include/config/X86_32) \
  /home/younes/bbr/arch/x86/include/uapi/asm/posix_types_64.h \
  /home/younes/bbr/include/uapi/asm-generic/posix_types.h \
  /home/younes/bbr/include/linux/kcsan-checks.h \
    $(wildcard include/config/KCSAN) \
    $(wildcard include/config/KCSAN_WEAK_MEMORY) \
    $(wildcard include/config/KCSAN_IGNORE_ATOMICS) \
  /home/younes/bbr/include/linux/poison.h \
    $(wildcard include/config/ILLEGAL_POINTER_VALUE) \
  /home/younes/bbr/include/linux/const.h \
  /home/younes/bbr/include/vdso/const.h \
  /home/younes/bbr/include/uapi/linux/const.h \
  /home/younes/bbr/arch/x86/include/asm/barrier.h \
  /home/younes/bbr/arch/x86/include/asm/alternative.h \
    $(wildcard include/config/CALL_THUNKS) \
  /home/younes/bbr/include/linux/stringify.h \
  /home/younes/bbr/arch/x86/include/asm/asm.h \
  /home/younes/bbr/arch/x86/include/asm/extable_fixup_types.h \
  /home/younes/bbr/arch/x86/include/asm/nops.h \
  /home/younes/bbr/include/asm-generic/barrier.h \
  /home/younes/bbr/include/linux/stat.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/stat.h \
  /home/younes/bbr/include/uapi/linux/stat.h \
  /home/younes/bbr/include/linux/time.h \
    $(wildcard include/config/POSIX_TIMERS) \
  /home/younes/bbr/include/linux/cache.h \
    $(wildcard include/config/ARCH_HAS_CACHE_LINE_SIZE) \
  /home/younes/bbr/include/uapi/linux/kernel.h \
  /home/younes/bbr/include/uapi/linux/sysinfo.h \
  /home/younes/bbr/arch/x86/include/asm/cache.h \
    $(wildcard include/config/X86_L1_CACHE_SHIFT) \
    $(wildcard include/config/X86_INTERNODE_CACHE_SHIFT) \
    $(wildcard include/config/X86_VSMP) \
  /home/younes/bbr/include/linux/linkage.h \
    $(wildcard include/config/ARCH_USE_SYM_ANNOTATIONS) \
  /home/younes/bbr/include/linux/export.h \
    $(wildcard include/config/MODVERSIONS) \
  /home/younes/bbr/arch/x86/include/asm/linkage.h \
    $(wildcard include/config/CALL_PADDING) \
    $(wildcard include/config/MITIGATION_RETHUNK) \
    $(wildcard include/config/MITIGATION_SLS) \
    $(wildcard include/config/FUNCTION_PADDING_BYTES) \
    $(wildcard include/config/UML) \
  /home/younes/bbr/arch/x86/include/asm/ibt.h \
    $(wildcard include/config/X86_KERNEL_IBT) \
  /home/younes/bbr/include/linux/math64.h \
    $(wildcard include/config/ARCH_SUPPORTS_INT128) \
  /home/younes/bbr/include/linux/math.h \
  /home/younes/bbr/arch/x86/include/asm/div64.h \
  /home/younes/bbr/include/asm-generic/div64.h \
    $(wildcard include/config/CC_OPTIMIZE_FOR_PERFORMANCE) \
  /home/younes/bbr/include/vdso/math64.h \
  /home/younes/bbr/include/linux/time64.h \
  /home/younes/bbr/include/vdso/time64.h \
  /home/younes/bbr/include/uapi/linux/time.h \
  /home/younes/bbr/include/uapi/linux/time_types.h \
  /home/younes/bbr/include/linux/time32.h \
  /home/younes/bbr/include/linux/timex.h \
  /home/younes/bbr/include/uapi/linux/timex.h \
  /home/younes/bbr/include/uapi/linux/param.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/param.h \
  /home/younes/bbr/include/asm-generic/param.h \
    $(wildcard include/config/HZ) \
  /home/younes/bbr/include/uapi/asm-generic/param.h \
  /home/younes/bbr/arch/x86/include/asm/timex.h \
    $(wildcard include/config/X86_TSC) \
  /home/younes/bbr/arch/x86/include/asm/processor.h \
    $(wildcard include/config/X86_VMX_FEATURE_NAMES) \
    $(wildcard include/config/X86_IOPL_IOPERM) \
    $(wildcard include/config/STACKPROTECTOR) \
    $(wildcard include/config/VM86) \
    $(wildcard include/config/X86_USER_SHADOW_STACK) \
    $(wildcard include/config/USE_X86_SEG_SUPPORT) \
    $(wildcard include/config/PARAVIRT_XXL) \
    $(wildcard include/config/CPU_SUP_AMD) \
    $(wildcard include/config/XEN) \
  /home/younes/bbr/arch/x86/include/asm/processor-flags.h \
    $(wildcard include/config/MITIGATION_PAGE_TABLE_ISOLATION) \
  /home/younes/bbr/arch/x86/include/uapi/asm/processor-flags.h \
  /home/younes/bbr/include/linux/mem_encrypt.h \
    $(wildcard include/config/ARCH_HAS_MEM_ENCRYPT) \
    $(wildcard include/config/AMD_MEM_ENCRYPT) \
  /home/younes/bbr/arch/x86/include/asm/mem_encrypt.h \
    $(wildcard include/config/X86_MEM_ENCRYPT) \
  /home/younes/bbr/include/linux/init.h \
    $(wildcard include/config/MEMORY_HOTPLUG) \
    $(wildcard include/config/HAVE_ARCH_PREL32_RELOCATIONS) \
  /home/younes/bbr/include/linux/cc_platform.h \
    $(wildcard include/config/ARCH_HAS_CC_PLATFORM) \
  /home/younes/bbr/arch/x86/include/asm/math_emu.h \
  /home/younes/bbr/arch/x86/include/asm/ptrace.h \
    $(wildcard include/config/PARAVIRT) \
    $(wildcard include/config/IA32_EMULATION) \
    $(wildcard include/config/X86_DEBUGCTLMSR) \
  /home/younes/bbr/arch/x86/include/asm/segment.h \
    $(wildcard include/config/XEN_PV) \
  /home/younes/bbr/arch/x86/include/asm/page_types.h \
    $(wildcard include/config/PHYSICAL_START) \
    $(wildcard include/config/PHYSICAL_ALIGN) \
    $(wildcard include/config/DYNAMIC_PHYSICAL_MASK) \
  /home/younes/bbr/include/vdso/page.h \
    $(wildcard include/config/PAGE_SHIFT) \
  /home/younes/bbr/arch/x86/include/asm/page_64_types.h \
    $(wildcard include/config/KASAN) \
    $(wildcard include/config/DYNAMIC_MEMORY_LAYOUT) \
    $(wildcard include/config/X86_5LEVEL) \
    $(wildcard include/config/RANDOMIZE_BASE) \
  /home/younes/bbr/arch/x86/include/asm/kaslr.h \
    $(wildcard include/config/RANDOMIZE_MEMORY) \
  /home/younes/bbr/arch/x86/include/uapi/asm/ptrace.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/ptrace-abi.h \
  /home/younes/bbr/arch/x86/include/asm/paravirt_types.h \
    $(wildcard include/config/PGTABLE_LEVELS) \
    $(wildcard include/config/ZERO_CALL_USED_REGS) \
    $(wildcard include/config/PARAVIRT_DEBUG) \
  /home/younes/bbr/arch/x86/include/asm/desc_defs.h \
  /home/younes/bbr/arch/x86/include/asm/pgtable_types.h \
    $(wildcard include/config/X86_INTEL_MEMORY_PROTECTION_KEYS) \
    $(wildcard include/config/X86_PAE) \
    $(wildcard include/config/MEM_SOFT_DIRTY) \
    $(wildcard include/config/HAVE_ARCH_USERFAULTFD_WP) \
    $(wildcard include/config/PROC_FS) \
  /home/younes/bbr/arch/x86/include/asm/pgtable_64_types.h \
    $(wildcard include/config/KMSAN) \
    $(wildcard include/config/DEBUG_KMAP_LOCAL_FORCE_MAP) \
  /home/younes/bbr/arch/x86/include/asm/sparsemem.h \
    $(wildcard include/config/SPARSEMEM) \
  /home/younes/bbr/arch/x86/include/asm/nospec-branch.h \
    $(wildcard include/config/CALL_THUNKS_DEBUG) \
    $(wildcard include/config/MITIGATION_CALL_DEPTH_TRACKING) \
    $(wildcard include/config/NOINSTR_VALIDATION) \
    $(wildcard include/config/MITIGATION_UNRET_ENTRY) \
    $(wildcard include/config/MITIGATION_SRSO) \
    $(wildcard include/config/MITIGATION_IBPB_ENTRY) \
  /home/younes/bbr/include/linux/static_key.h \
  /home/younes/bbr/include/linux/jump_label.h \
    $(wildcard include/config/HAVE_ARCH_JUMP_LABEL_RELATIVE) \
  /home/younes/bbr/arch/x86/include/asm/jump_label.h \
    $(wildcard include/config/HAVE_JUMP_LABEL_HACK) \
  /home/younes/bbr/include/linux/objtool.h \
    $(wildcard include/config/FRAME_POINTER) \
  /home/younes/bbr/include/linux/objtool_types.h \
  /home/younes/bbr/arch/x86/include/asm/cpufeatures.h \
  /home/younes/bbr/arch/x86/include/asm/required-features.h \
    $(wildcard include/config/X86_MINIMUM_CPU_FAMILY) \
    $(wildcard include/config/MATH_EMULATION) \
    $(wildcard include/config/X86_CMPXCHG64) \
    $(wildcard include/config/X86_CMOV) \
    $(wildcard include/config/X86_P6_NOP) \
    $(wildcard include/config/MATOM) \
  /home/younes/bbr/arch/x86/include/asm/disabled-features.h \
    $(wildcard include/config/X86_UMIP) \
    $(wildcard include/config/ADDRESS_MASKING) \
    $(wildcard include/config/INTEL_IOMMU_SVM) \
    $(wildcard include/config/X86_SGX) \
    $(wildcard include/config/INTEL_TDX_GUEST) \
    $(wildcard include/config/X86_FRED) \
    $(wildcard include/config/KVM_AMD_SEV) \
  /home/younes/bbr/arch/x86/include/asm/msr-index.h \
  /home/younes/bbr/include/linux/bits.h \
  /home/younes/bbr/include/vdso/bits.h \
  /home/younes/bbr/include/uapi/linux/bits.h \
  /home/younes/bbr/arch/x86/include/asm/unwind_hints.h \
  /home/younes/bbr/arch/x86/include/asm/orc_types.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/byteorder.h \
  /home/younes/bbr/include/linux/byteorder/little_endian.h \
  /home/younes/bbr/include/uapi/linux/byteorder/little_endian.h \
  /home/younes/bbr/include/linux/swab.h \
  /home/younes/bbr/include/uapi/linux/swab.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/swab.h \
  /home/younes/bbr/include/linux/byteorder/generic.h \
  /home/younes/bbr/arch/x86/include/asm/percpu.h \
    $(wildcard include/config/X86_64_SMP) \
    $(wildcard include/config/CC_HAS_NAMED_AS) \
  /home/younes/bbr/include/asm-generic/percpu.h \
    $(wildcard include/config/DEBUG_PREEMPT) \
    $(wildcard include/config/HAVE_SETUP_PER_CPU_AREA) \
  /home/younes/bbr/include/linux/threads.h \
    $(wildcard include/config/NR_CPUS) \
    $(wildcard include/config/BASE_SMALL) \
  /home/younes/bbr/include/linux/percpu-defs.h \
    $(wildcard include/config/DEBUG_FORCE_WEAK_PER_CPU) \
  /home/younes/bbr/arch/x86/include/asm/current.h \
  /home/younes/bbr/arch/x86/include/asm/asm-offsets.h \
  /home/younes/bbr/include/generated/asm-offsets.h \
  /home/younes/bbr/arch/x86/include/asm/GEN-for-each-reg.h \
  /home/younes/bbr/arch/x86/include/asm/spinlock_types.h \
  /home/younes/bbr/include/asm-generic/qspinlock_types.h \
  /home/younes/bbr/include/asm-generic/qrwlock_types.h \
  /home/younes/bbr/arch/x86/include/asm/proto.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/ldt.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/sigcontext.h \
  /home/younes/bbr/arch/x86/include/asm/cpuid.h \
  /home/younes/bbr/arch/x86/include/asm/string.h \
  /home/younes/bbr/arch/x86/include/asm/string_64.h \
    $(wildcard include/config/ARCH_HAS_UACCESS_FLUSHCACHE) \
  /home/younes/bbr/arch/x86/include/asm/paravirt.h \
    $(wildcard include/config/PARAVIRT_SPINLOCKS) \
    $(wildcard include/config/DEBUG_ENTRY) \
  /home/younes/bbr/include/linux/bug.h \
    $(wildcard include/config/BUG_ON_DATA_CORRUPTION) \
  /home/younes/bbr/arch/x86/include/asm/bug.h \
    $(wildcard include/config/DEBUG_BUGVERBOSE) \
  /home/younes/bbr/include/linux/instrumentation.h \
  /home/younes/bbr/include/asm-generic/bug.h \
    $(wildcard include/config/BUG) \
    $(wildcard include/config/GENERIC_BUG_RELATIVE_POINTERS) \
  /home/younes/bbr/include/linux/once_lite.h \
  /home/younes/bbr/include/linux/panic.h \
    $(wildcard include/config/PANIC_TIMEOUT) \
  /home/younes/bbr/include/linux/printk.h \
    $(wildcard include/config/MESSAGE_LOGLEVEL_DEFAULT) \
    $(wildcard include/config/CONSOLE_LOGLEVEL_DEFAULT) \
    $(wildcard include/config/CONSOLE_LOGLEVEL_QUIET) \
    $(wildcard include/config/EARLY_PRINTK) \
    $(wildcard include/config/PRINTK) \
    $(wildcard include/config/DYNAMIC_DEBUG) \
  /home/younes/bbr/include/linux/stdarg.h \
  /home/younes/bbr/include/linux/kern_levels.h \
  /home/younes/bbr/include/linux/ratelimit_types.h \
  /home/younes/bbr/include/linux/spinlock_types_raw.h \
    $(wildcard include/config/DEBUG_SPINLOCK) \
    $(wildcard include/config/DEBUG_LOCK_ALLOC) \
  /home/younes/bbr/include/linux/lockdep_types.h \
    $(wildcard include/config/PROVE_RAW_LOCK_NESTING) \
    $(wildcard include/config/LOCKDEP) \
    $(wildcard include/config/LOCK_STAT) \
  /home/younes/bbr/include/linux/dynamic_debug.h \
  /home/younes/bbr/include/linux/cpumask.h \
    $(wildcard include/config/FORCE_NR_CPUS) \
    $(wildcard include/config/HOTPLUG_CPU) \
    $(wildcard include/config/DEBUG_PER_CPU_MAPS) \
    $(wildcard include/config/CPUMASK_OFFSTACK) \
  /home/younes/bbr/include/linux/cleanup.h \
  /home/younes/bbr/include/linux/kernel.h \
    $(wildcard include/config/PREEMPT_VOLUNTARY_BUILD) \
    $(wildcard include/config/PREEMPT_DYNAMIC) \
    $(wildcard include/config/HAVE_PREEMPT_DYNAMIC_CALL) \
    $(wildcard include/config/HAVE_PREEMPT_DYNAMIC_KEY) \
    $(wildcard include/config/PREEMPT_) \
    $(wildcard include/config/DEBUG_ATOMIC_SLEEP) \
    $(wildcard include/config/MMU) \
    $(wildcard include/config/PROVE_LOCKING) \
  /home/younes/bbr/include/linux/align.h \
  /home/younes/bbr/include/linux/array_size.h \
  /home/younes/bbr/include/linux/limits.h \
  /home/younes/bbr/include/uapi/linux/limits.h \
  /home/younes/bbr/include/vdso/limits.h \
  /home/younes/bbr/include/linux/bitops.h \
  /home/younes/bbr/include/linux/typecheck.h \
  /home/younes/bbr/include/asm-generic/bitops/generic-non-atomic.h \
  /home/younes/bbr/arch/x86/include/asm/bitops.h \
  /home/younes/bbr/arch/x86/include/asm/rmwcc.h \
  /home/younes/bbr/include/linux/args.h \
  /home/younes/bbr/include/asm-generic/bitops/sched.h \
  /home/younes/bbr/arch/x86/include/asm/arch_hweight.h \
  /home/younes/bbr/include/asm-generic/bitops/const_hweight.h \
  /home/younes/bbr/include/asm-generic/bitops/instrumented-atomic.h \
  /home/younes/bbr/include/linux/instrumented.h \
  /home/younes/bbr/include/linux/kmsan-checks.h \
  /home/younes/bbr/include/asm-generic/bitops/instrumented-non-atomic.h \
    $(wildcard include/config/KCSAN_ASSUME_PLAIN_WRITES_ATOMIC) \
  /home/younes/bbr/include/asm-generic/bitops/instrumented-lock.h \
  /home/younes/bbr/include/asm-generic/bitops/le.h \
  /home/younes/bbr/include/asm-generic/bitops/ext2-atomic-setbit.h \
  /home/younes/bbr/include/linux/hex.h \
  /home/younes/bbr/include/linux/kstrtox.h \
  /home/younes/bbr/include/linux/log2.h \
    $(wildcard include/config/ARCH_HAS_ILOG2_U32) \
    $(wildcard include/config/ARCH_HAS_ILOG2_U64) \
  /home/younes/bbr/include/linux/minmax.h \
  /home/younes/bbr/include/linux/sprintf.h \
  /home/younes/bbr/include/linux/static_call_types.h \
    $(wildcard include/config/HAVE_STATIC_CALL) \
  /home/younes/bbr/include/linux/instruction_pointer.h \
  /home/younes/bbr/include/linux/wordpart.h \
  /home/younes/bbr/include/linux/bitmap.h \
  /home/younes/bbr/include/linux/errno.h \
  /home/younes/bbr/include/uapi/linux/errno.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/errno.h \
  /home/younes/bbr/include/uapi/asm-generic/errno.h \
  /home/younes/bbr/include/uapi/asm-generic/errno-base.h \
  /home/younes/bbr/include/linux/find.h \
  /home/younes/bbr/include/linux/string.h \
    $(wildcard include/config/BINARY_PRINTF) \
    $(wildcard include/config/FORTIFY_SOURCE) \
  /home/younes/bbr/include/linux/err.h \
  /home/younes/bbr/include/linux/overflow.h \
  /home/younes/bbr/include/uapi/linux/string.h \
  /home/younes/bbr/include/linux/fortify-string.h \
    $(wildcard include/config/CC_HAS_KASAN_MEMINTRINSIC_PREFIX) \
    $(wildcard include/config/GENERIC_ENTRY) \
  /home/younes/bbr/include/linux/bitfield.h \
  /home/younes/bbr/include/linux/bitmap-str.h \
  /home/younes/bbr/include/linux/cpumask_types.h \
  /home/younes/bbr/include/linux/atomic.h \
  /home/younes/bbr/arch/x86/include/asm/atomic.h \
  /home/younes/bbr/arch/x86/include/asm/cmpxchg.h \
  /home/younes/bbr/arch/x86/include/asm/cmpxchg_64.h \
  /home/younes/bbr/arch/x86/include/asm/atomic64_64.h \
  /home/younes/bbr/include/linux/atomic/atomic-arch-fallback.h \
    $(wildcard include/config/GENERIC_ATOMIC64) \
  /home/younes/bbr/include/linux/atomic/atomic-long.h \
  /home/younes/bbr/include/linux/atomic/atomic-instrumented.h \
  /home/younes/bbr/include/linux/gfp_types.h \
    $(wildcard include/config/KASAN_HW_TAGS) \
    $(wildcard include/config/SLAB_OBJ_EXT) \
  /home/younes/bbr/include/linux/numa.h \
    $(wildcard include/config/NODES_SHIFT) \
    $(wildcard include/config/NUMA_KEEP_MEMINFO) \
    $(wildcard include/config/NUMA) \
    $(wildcard include/config/HAVE_ARCH_NODE_DEV_GROUP) \
  /home/younes/bbr/arch/x86/include/asm/frame.h \
  /home/younes/bbr/arch/x86/include/asm/page.h \
  /home/younes/bbr/arch/x86/include/asm/page_64.h \
    $(wildcard include/config/DEBUG_VIRTUAL) \
    $(wildcard include/config/X86_VSYSCALL_EMULATION) \
  /home/younes/bbr/include/linux/range.h \
  /home/younes/bbr/include/asm-generic/memory_model.h \
    $(wildcard include/config/FLATMEM) \
    $(wildcard include/config/SPARSEMEM_VMEMMAP) \
  /home/younes/bbr/include/linux/pfn.h \
  /home/younes/bbr/include/asm-generic/getorder.h \
  /home/younes/bbr/arch/x86/include/asm/special_insns.h \
  /home/younes/bbr/include/linux/irqflags.h \
    $(wildcard include/config/TRACE_IRQFLAGS) \
    $(wildcard include/config/PREEMPT_RT) \
    $(wildcard include/config/IRQSOFF_TRACER) \
    $(wildcard include/config/PREEMPT_TRACER) \
    $(wildcard include/config/DEBUG_IRQFLAGS) \
    $(wildcard include/config/TRACE_IRQFLAGS_SUPPORT) \
  /home/younes/bbr/include/linux/irqflags_types.h \
  /home/younes/bbr/arch/x86/include/asm/irqflags.h \
  /home/younes/bbr/arch/x86/include/asm/fpu/types.h \
  /home/younes/bbr/arch/x86/include/asm/vmxfeatures.h \
  /home/younes/bbr/arch/x86/include/asm/vdso/processor.h \
  /home/younes/bbr/arch/x86/include/asm/shstk.h \
  /home/younes/bbr/include/linux/personality.h \
  /home/younes/bbr/include/uapi/linux/personality.h \
  /home/younes/bbr/arch/x86/include/asm/tsc.h \
  /home/younes/bbr/arch/x86/include/asm/cpufeature.h \
  /home/younes/bbr/arch/x86/include/asm/msr.h \
  /home/younes/bbr/arch/x86/include/asm/cpumask.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/msr.h \
  /home/younes/bbr/include/uapi/linux/ioctl.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/ioctl.h \
  /home/younes/bbr/include/asm-generic/ioctl.h \
  /home/younes/bbr/include/uapi/asm-generic/ioctl.h \
  /home/younes/bbr/arch/x86/include/asm/shared/msr.h \
  /home/younes/bbr/include/linux/percpu.h \
    $(wildcard include/config/MEM_ALLOC_PROFILING) \
    $(wildcard include/config/RANDOM_KMALLOC_CACHES) \
    $(wildcard include/config/PAGE_SIZE_4KB) \
    $(wildcard include/config/NEED_PER_CPU_PAGE_FIRST_CHUNK) \
  /home/younes/bbr/include/linux/alloc_tag.h \
    $(wildcard include/config/MEM_ALLOC_PROFILING_DEBUG) \
    $(wildcard include/config/MEM_ALLOC_PROFILING_ENABLED_BY_DEFAULT) \
  /home/younes/bbr/include/linux/codetag.h \
    $(wildcard include/config/CODE_TAGGING) \
  /home/younes/bbr/include/linux/preempt.h \
    $(wildcard include/config/PREEMPT_COUNT) \
    $(wildcard include/config/TRACE_PREEMPT_TOGGLE) \
    $(wildcard include/config/PREEMPTION) \
    $(wildcard include/config/PREEMPT_NOTIFIERS) \
    $(wildcard include/config/PREEMPT_NONE) \
    $(wildcard include/config/PREEMPT_VOLUNTARY) \
    $(wildcard include/config/PREEMPT) \
    $(wildcard include/config/PREEMPT_LAZY) \
  /home/younes/bbr/arch/x86/include/asm/preempt.h \
  /home/younes/bbr/include/linux/smp.h \
    $(wildcard include/config/UP_LATE_INIT) \
    $(wildcard include/config/CSD_LOCK_WAIT_DEBUG) \
  /home/younes/bbr/include/linux/smp_types.h \
  /home/younes/bbr/include/linux/llist.h \
    $(wildcard include/config/ARCH_HAVE_NMI_SAFE_CMPXCHG) \
  /home/younes/bbr/include/linux/thread_info.h \
    $(wildcard include/config/THREAD_INFO_IN_TASK) \
    $(wildcard include/config/ARCH_HAS_PREEMPT_LAZY) \
    $(wildcard include/config/HAVE_ARCH_WITHIN_STACK_FRAMES) \
    $(wildcard include/config/HARDENED_USERCOPY) \
    $(wildcard include/config/SH) \
  /home/younes/bbr/include/linux/restart_block.h \
  /home/younes/bbr/arch/x86/include/asm/thread_info.h \
    $(wildcard include/config/COMPAT) \
  /home/younes/bbr/arch/x86/include/asm/smp.h \
    $(wildcard include/config/DEBUG_NMI_SELFTEST) \
  /home/younes/bbr/include/linux/mmdebug.h \
    $(wildcard include/config/DEBUG_VM) \
    $(wildcard include/config/DEBUG_VM_IRQSOFF) \
    $(wildcard include/config/DEBUG_VM_PGFLAGS) \
  /home/younes/bbr/include/linux/sched.h \
    $(wildcard include/config/VIRT_CPU_ACCOUNTING_NATIVE) \
    $(wildcard include/config/SCHED_INFO) \
    $(wildcard include/config/SCHEDSTATS) \
    $(wildcard include/config/SCHED_CORE) \
    $(wildcard include/config/FAIR_GROUP_SCHED) \
    $(wildcard include/config/RT_GROUP_SCHED) \
    $(wildcard include/config/RT_MUTEXES) \
    $(wildcard include/config/UCLAMP_TASK) \
    $(wildcard include/config/UCLAMP_BUCKETS_COUNT) \
    $(wildcard include/config/KMAP_LOCAL) \
    $(wildcard include/config/SCHED_CLASS_EXT) \
    $(wildcard include/config/CGROUP_SCHED) \
    $(wildcard include/config/BLK_DEV_IO_TRACE) \
    $(wildcard include/config/PREEMPT_RCU) \
    $(wildcard include/config/TASKS_RCU) \
    $(wildcard include/config/TASKS_TRACE_RCU) \
    $(wildcard include/config/MEMCG_V1) \
    $(wildcard include/config/LRU_GEN) \
    $(wildcard include/config/COMPAT_BRK) \
    $(wildcard include/config/CGROUPS) \
    $(wildcard include/config/BLK_CGROUP) \
    $(wildcard include/config/PSI) \
    $(wildcard include/config/PAGE_OWNER) \
    $(wildcard include/config/EVENTFD) \
    $(wildcard include/config/ARCH_HAS_CPU_PASID) \
    $(wildcard include/config/X86_BUS_LOCK_DETECT) \
    $(wildcard include/config/TASK_DELAY_ACCT) \
    $(wildcard include/config/ARCH_HAS_SCALED_CPUTIME) \
    $(wildcard include/config/VIRT_CPU_ACCOUNTING_GEN) \
    $(wildcard include/config/NO_HZ_FULL) \
    $(wildcard include/config/POSIX_CPUTIMERS) \
    $(wildcard include/config/POSIX_CPU_TIMERS_TASK_WORK) \
    $(wildcard include/config/KEYS) \
    $(wildcard include/config/SYSVIPC) \
    $(wildcard include/config/DETECT_HUNG_TASK) \
    $(wildcard include/config/IO_URING) \
    $(wildcard include/config/AUDIT) \
    $(wildcard include/config/AUDITSYSCALL) \
    $(wildcard include/config/DEBUG_MUTEXES) \
    $(wildcard include/config/UBSAN) \
    $(wildcard include/config/UBSAN_TRAP) \
    $(wildcard include/config/COMPACTION) \
    $(wildcard include/config/TASK_XACCT) \
    $(wildcard include/config/CPUSETS) \
    $(wildcard include/config/X86_CPU_RESCTRL) \
    $(wildcard include/config/FUTEX) \
    $(wildcard include/config/PERF_EVENTS) \
    $(wildcard include/config/NUMA_BALANCING) \
    $(wildcard include/config/RSEQ) \
    $(wildcard include/config/SCHED_MM_CID) \
    $(wildcard include/config/FAULT_INJECTION) \
    $(wildcard include/config/LATENCYTOP) \
    $(wildcard include/config/FUNCTION_GRAPH_TRACER) \
    $(wildcard include/config/MEMCG) \
    $(wildcard include/config/UPROBES) \
    $(wildcard include/config/BCACHE) \
    $(wildcard include/config/VMAP_STACK) \
    $(wildcard include/config/SECURITY) \
    $(wildcard include/config/BPF_SYSCALL) \
    $(wildcard include/config/GCC_PLUGIN_STACKLEAK) \
    $(wildcard include/config/X86_MCE) \
    $(wildcard include/config/KRETPROBES) \
    $(wildcard include/config/RETHOOK) \
    $(wildcard include/config/ARCH_HAS_PARANOID_L1D_FLUSH) \
    $(wildcard include/config/RV) \
    $(wildcard include/config/USER_EVENTS) \
  /home/younes/bbr/include/uapi/linux/sched.h \
  /home/younes/bbr/include/linux/pid_types.h \
  /home/younes/bbr/include/linux/sem_types.h \
  /home/younes/bbr/include/linux/shm.h \
  /home/younes/bbr/arch/x86/include/asm/shmparam.h \
  /home/younes/bbr/include/linux/kmsan_types.h \
  /home/younes/bbr/include/linux/mutex_types.h \
    $(wildcard include/config/MUTEX_SPIN_ON_OWNER) \
  /home/younes/bbr/include/linux/osq_lock.h \
  /home/younes/bbr/include/linux/spinlock_types.h \
  /home/younes/bbr/include/linux/rwlock_types.h \
  /home/younes/bbr/include/linux/plist_types.h \
  /home/younes/bbr/include/linux/hrtimer_types.h \
  /home/younes/bbr/include/linux/timerqueue_types.h \
  /home/younes/bbr/include/linux/rbtree_types.h \
  /home/younes/bbr/include/linux/timer_types.h \
  /home/younes/bbr/include/linux/seccomp_types.h \
    $(wildcard include/config/SECCOMP) \
  /home/younes/bbr/include/linux/nodemask_types.h \
  /home/younes/bbr/include/linux/refcount_types.h \
  /home/younes/bbr/include/linux/resource.h \
  /home/younes/bbr/include/uapi/linux/resource.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/resource.h \
  /home/younes/bbr/include/asm-generic/resource.h \
  /home/younes/bbr/include/uapi/asm-generic/resource.h \
  /home/younes/bbr/include/linux/latencytop.h \
  /home/younes/bbr/include/linux/sched/prio.h \
  /home/younes/bbr/include/linux/sched/types.h \
  /home/younes/bbr/include/linux/signal_types.h \
    $(wildcard include/config/OLD_SIGACTION) \
  /home/younes/bbr/include/uapi/linux/signal.h \
  /home/younes/bbr/arch/x86/include/asm/signal.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/signal.h \
  /home/younes/bbr/include/uapi/asm-generic/signal-defs.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/siginfo.h \
  /home/younes/bbr/include/uapi/asm-generic/siginfo.h \
  /home/younes/bbr/include/linux/syscall_user_dispatch_types.h \
  /home/younes/bbr/include/linux/mm_types_task.h \
    $(wildcard include/config/ARCH_WANT_BATCHED_UNMAP_TLB_FLUSH) \
  /home/younes/bbr/arch/x86/include/asm/tlbbatch.h \
  /home/younes/bbr/include/linux/netdevice_xmit.h \
    $(wildcard include/config/NET_EGRESS) \
  /home/younes/bbr/include/linux/task_io_accounting.h \
    $(wildcard include/config/TASK_IO_ACCOUNTING) \
  /home/younes/bbr/include/linux/posix-timers_types.h \
  /home/younes/bbr/include/uapi/linux/rseq.h \
  /home/younes/bbr/include/linux/seqlock_types.h \
  /home/younes/bbr/include/linux/kcsan.h \
  /home/younes/bbr/include/linux/rv.h \
    $(wildcard include/config/RV_REACTORS) \
  /home/younes/bbr/include/linux/livepatch_sched.h \
  /home/younes/bbr/include/linux/uidgid_types.h \
  /home/younes/bbr/arch/x86/include/generated/asm/kmap_size.h \
  /home/younes/bbr/include/asm-generic/kmap_size.h \
    $(wildcard include/config/DEBUG_KMAP_LOCAL) \
  /home/younes/bbr/include/linux/sched/ext.h \
    $(wildcard include/config/EXT_GROUP_SCHED) \
  /home/younes/bbr/include/linux/rhashtable-types.h \
  /home/younes/bbr/include/linux/mutex.h \
  /home/younes/bbr/include/linux/lockdep.h \
    $(wildcard include/config/DEBUG_LOCKING_API_SELFTESTS) \
  /home/younes/bbr/include/linux/debug_locks.h \
  /home/younes/bbr/include/linux/workqueue_types.h \
  /home/younes/bbr/include/linux/spinlock.h \
  /home/younes/bbr/include/linux/bottom_half.h \
  /home/younes/bbr/arch/x86/include/generated/asm/mmiowb.h \
  /home/younes/bbr/include/asm-generic/mmiowb.h \
    $(wildcard include/config/MMIOWB) \
  /home/younes/bbr/arch/x86/include/asm/spinlock.h \
  /home/younes/bbr/arch/x86/include/asm/qspinlock.h \
  /home/younes/bbr/include/asm-generic/qspinlock.h \
  /home/younes/bbr/arch/x86/include/asm/qrwlock.h \
  /home/younes/bbr/include/asm-generic/qrwlock.h \
  /home/younes/bbr/include/linux/rwlock.h \
  /home/younes/bbr/include/linux/spinlock_api_smp.h \
    $(wildcard include/config/INLINE_SPIN_LOCK) \
    $(wildcard include/config/INLINE_SPIN_LOCK_BH) \
    $(wildcard include/config/INLINE_SPIN_LOCK_IRQ) \
    $(wildcard include/config/INLINE_SPIN_LOCK_IRQSAVE) \
    $(wildcard include/config/INLINE_SPIN_TRYLOCK) \
    $(wildcard include/config/INLINE_SPIN_TRYLOCK_BH) \
    $(wildcard include/config/UNINLINE_SPIN_UNLOCK) \
    $(wildcard include/config/INLINE_SPIN_UNLOCK_BH) \
    $(wildcard include/config/INLINE_SPIN_UNLOCK_IRQ) \
    $(wildcard include/config/INLINE_SPIN_UNLOCK_IRQRESTORE) \
    $(wildcard include/config/GENERIC_LOCKBREAK) \
  /home/younes/bbr/include/linux/rwlock_api_smp.h \
    $(wildcard include/config/INLINE_READ_LOCK) \
    $(wildcard include/config/INLINE_WRITE_LOCK) \
    $(wildcard include/config/INLINE_READ_LOCK_BH) \
    $(wildcard include/config/INLINE_WRITE_LOCK_BH) \
    $(wildcard include/config/INLINE_READ_LOCK_IRQ) \
    $(wildcard include/config/INLINE_WRITE_LOCK_IRQ) \
    $(wildcard include/config/INLINE_READ_LOCK_IRQSAVE) \
    $(wildcard include/config/INLINE_WRITE_LOCK_IRQSAVE) \
    $(wildcard include/config/INLINE_READ_TRYLOCK) \
    $(wildcard include/config/INLINE_WRITE_TRYLOCK) \
    $(wildcard include/config/INLINE_READ_UNLOCK) \
    $(wildcard include/config/INLINE_WRITE_UNLOCK) \
    $(wildcard include/config/INLINE_READ_UNLOCK_BH) \
    $(wildcard include/config/INLINE_WRITE_UNLOCK_BH) \
    $(wildcard include/config/INLINE_READ_UNLOCK_IRQ) \
    $(wildcard include/config/INLINE_WRITE_UNLOCK_IRQ) \
    $(wildcard include/config/INLINE_READ_UNLOCK_IRQRESTORE) \
    $(wildcard include/config/INLINE_WRITE_UNLOCK_IRQRESTORE) \
  /home/younes/bbr/include/linux/tracepoint-defs.h \
  /home/younes/bbr/include/vdso/time32.h \
  /home/younes/bbr/include/vdso/time.h \
  /home/younes/bbr/include/linux/uidgid.h \
    $(wildcard include/config/MULTIUSER) \
    $(wildcard include/config/USER_NS) \
  /home/younes/bbr/include/linux/highuid.h \
  /home/younes/bbr/include/linux/buildid.h \
    $(wildcard include/config/VMCORE_INFO) \
  /home/younes/bbr/include/linux/kmod.h \
  /home/younes/bbr/include/linux/umh.h \
  /home/younes/bbr/include/linux/gfp.h \
    $(wildcard include/config/HIGHMEM) \
    $(wildcard include/config/ZONE_DMA) \
    $(wildcard include/config/ZONE_DMA32) \
    $(wildcard include/config/ZONE_DEVICE) \
    $(wildcard include/config/CONTIG_ALLOC) \
  /home/younes/bbr/include/linux/mmzone.h \
    $(wildcard include/config/ARCH_FORCE_MAX_ORDER) \
    $(wildcard include/config/CMA) \
    $(wildcard include/config/MEMORY_ISOLATION) \
    $(wildcard include/config/ZSMALLOC) \
    $(wildcard include/config/UNACCEPTED_MEMORY) \
    $(wildcard include/config/IOMMU_SUPPORT) \
    $(wildcard include/config/SWAP) \
    $(wildcard include/config/HUGETLB_PAGE) \
    $(wildcard include/config/TRANSPARENT_HUGEPAGE) \
    $(wildcard include/config/LRU_GEN_STATS) \
    $(wildcard include/config/LRU_GEN_WALKS_MMU) \
    $(wildcard include/config/MEMORY_FAILURE) \
    $(wildcard include/config/PAGE_EXTENSION) \
    $(wildcard include/config/DEFERRED_STRUCT_PAGE_INIT) \
    $(wildcard include/config/HAVE_MEMORYLESS_NODES) \
    $(wildcard include/config/SPARSEMEM_EXTREME) \
    $(wildcard include/config/HAVE_ARCH_PFN_VALID) \
  /home/younes/bbr/include/linux/list_nulls.h \
  /home/younes/bbr/include/linux/wait.h \
  /home/younes/bbr/include/linux/seqlock.h \
  /home/younes/bbr/include/linux/nodemask.h \
  /home/younes/bbr/include/linux/random.h \
    $(wildcard include/config/VMGENID) \
  /home/younes/bbr/include/uapi/linux/random.h \
  /home/younes/bbr/include/linux/irqnr.h \
  /home/younes/bbr/include/uapi/linux/irqnr.h \
  /home/younes/bbr/include/linux/pageblock-flags.h \
    $(wildcard include/config/HUGETLB_PAGE_SIZE_VARIABLE) \
  /home/younes/bbr/include/linux/page-flags-layout.h \
  /home/younes/bbr/include/generated/bounds.h \
  /home/younes/bbr/include/linux/mm_types.h \
    $(wildcard include/config/HAVE_ALIGNED_STRUCT_PAGE) \
    $(wildcard include/config/HUGETLB_PMD_PAGE_TABLE_SHARING) \
    $(wildcard include/config/USERFAULTFD) \
    $(wildcard include/config/ANON_VMA_NAME) \
    $(wildcard include/config/PER_VMA_LOCK) \
    $(wildcard include/config/HAVE_ARCH_COMPAT_MMAP_BASES) \
    $(wildcard include/config/MEMBARRIER) \
    $(wildcard include/config/AIO) \
    $(wildcard include/config/MMU_NOTIFIER) \
    $(wildcard include/config/SPLIT_PMD_PTLOCKS) \
    $(wildcard include/config/IOMMU_MM_DATA) \
    $(wildcard include/config/KSM) \
    $(wildcard include/config/CORE_DUMP_DEFAULT_ELF_HEADERS) \
  /home/younes/bbr/include/linux/auxvec.h \
  /home/younes/bbr/include/uapi/linux/auxvec.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/auxvec.h \
  /home/younes/bbr/include/linux/kref.h \
  /home/younes/bbr/include/linux/refcount.h \
  /home/younes/bbr/include/linux/rbtree.h \
  /home/younes/bbr/include/linux/rcupdate.h \
    $(wildcard include/config/TINY_RCU) \
    $(wildcard include/config/RCU_STRICT_GRACE_PERIOD) \
    $(wildcard include/config/RCU_LAZY) \
    $(wildcard include/config/TASKS_RCU_GENERIC) \
    $(wildcard include/config/RCU_STALL_COMMON) \
    $(wildcard include/config/KVM_XFER_TO_GUEST_WORK) \
    $(wildcard include/config/RCU_NOCB_CPU) \
    $(wildcard include/config/TASKS_RUDE_RCU) \
    $(wildcard include/config/TREE_RCU) \
    $(wildcard include/config/DEBUG_OBJECTS_RCU_HEAD) \
    $(wildcard include/config/PROVE_RCU) \
    $(wildcard include/config/ARCH_WEAK_RELEASE_ACQUIRE) \
  /home/younes/bbr/include/linux/context_tracking_irq.h \
    $(wildcard include/config/CONTEXT_TRACKING_IDLE) \
  /home/younes/bbr/include/linux/rcutree.h \
  /home/younes/bbr/include/linux/maple_tree.h \
    $(wildcard include/config/MAPLE_RCU_DISABLED) \
    $(wildcard include/config/DEBUG_MAPLE_TREE) \
  /home/younes/bbr/include/linux/rwsem.h \
    $(wildcard include/config/RWSEM_SPIN_ON_OWNER) \
    $(wildcard include/config/DEBUG_RWSEMS) \
  /home/younes/bbr/include/linux/completion.h \
  /home/younes/bbr/include/linux/swait.h \
  /home/younes/bbr/include/linux/uprobes.h \
  /home/younes/bbr/include/linux/timer.h \
    $(wildcard include/config/DEBUG_OBJECTS_TIMERS) \
  /home/younes/bbr/include/linux/ktime.h \
  /home/younes/bbr/include/linux/jiffies.h \
  /home/younes/bbr/include/vdso/jiffies.h \
  /home/younes/bbr/include/generated/timeconst.h \
  /home/younes/bbr/include/vdso/ktime.h \
  /home/younes/bbr/include/linux/timekeeping.h \
    $(wildcard include/config/GENERIC_CMOS_UPDATE) \
  /home/younes/bbr/include/linux/clocksource_ids.h \
  /home/younes/bbr/include/linux/debugobjects.h \
    $(wildcard include/config/DEBUG_OBJECTS) \
    $(wildcard include/config/DEBUG_OBJECTS_FREE) \
  /home/younes/bbr/arch/x86/include/asm/uprobes.h \
  /home/younes/bbr/include/linux/notifier.h \
  /home/younes/bbr/include/linux/srcu.h \
    $(wildcard include/config/TINY_SRCU) \
    $(wildcard include/config/NEED_SRCU_NMI_SAFE) \
  /home/younes/bbr/include/linux/workqueue.h \
    $(wildcard include/config/DEBUG_OBJECTS_WORK) \
    $(wildcard include/config/FREEZER) \
    $(wildcard include/config/WQ_WATCHDOG) \
  /home/younes/bbr/include/linux/rcu_segcblist.h \
  /home/younes/bbr/include/linux/srcutree.h \
  /home/younes/bbr/include/linux/rcu_node_tree.h \
    $(wildcard include/config/RCU_FANOUT) \
    $(wildcard include/config/RCU_FANOUT_LEAF) \
  /home/younes/bbr/include/linux/percpu_counter.h \
  /home/younes/bbr/arch/x86/include/asm/mmu.h \
    $(wildcard include/config/MODIFY_LDT_SYSCALL) \
  /home/younes/bbr/include/linux/page-flags.h \
    $(wildcard include/config/PAGE_IDLE_FLAG) \
    $(wildcard include/config/ARCH_USES_PG_ARCH_2) \
    $(wildcard include/config/ARCH_USES_PG_ARCH_3) \
    $(wildcard include/config/HUGETLB_PAGE_OPTIMIZE_VMEMMAP) \
  /home/younes/bbr/include/linux/local_lock.h \
  /home/younes/bbr/include/linux/local_lock_internal.h \
  /home/younes/bbr/include/linux/zswap.h \
    $(wildcard include/config/ZSWAP) \
  /home/younes/bbr/include/linux/memory_hotplug.h \
    $(wildcard include/config/ARCH_HAS_ADD_PAGES) \
    $(wildcard include/config/MEMORY_HOTREMOVE) \
  /home/younes/bbr/arch/x86/include/generated/asm/mmzone.h \
  /home/younes/bbr/include/asm-generic/mmzone.h \
  /home/younes/bbr/include/linux/topology.h \
    $(wildcard include/config/USE_PERCPU_NUMA_NODE_ID) \
    $(wildcard include/config/SCHED_SMT) \
  /home/younes/bbr/include/linux/arch_topology.h \
    $(wildcard include/config/GENERIC_ARCH_TOPOLOGY) \
  /home/younes/bbr/arch/x86/include/asm/topology.h \
    $(wildcard include/config/X86_LOCAL_APIC) \
    $(wildcard include/config/SCHED_MC_PRIO) \
  /home/younes/bbr/arch/x86/include/asm/mpspec.h \
    $(wildcard include/config/EISA) \
    $(wildcard include/config/X86_MPPARSE) \
  /home/younes/bbr/arch/x86/include/asm/mpspec_def.h \
  /home/younes/bbr/arch/x86/include/asm/x86_init.h \
  /home/younes/bbr/arch/x86/include/asm/apicdef.h \
  /home/younes/bbr/include/asm-generic/topology.h \
  /home/younes/bbr/include/linux/cpu_smt.h \
    $(wildcard include/config/HOTPLUG_SMT) \
  /home/younes/bbr/include/linux/sysctl.h \
    $(wildcard include/config/SYSCTL) \
  /home/younes/bbr/include/uapi/linux/sysctl.h \
  /home/younes/bbr/include/linux/elf.h \
    $(wildcard include/config/ARCH_HAVE_EXTRA_ELF_NOTES) \
    $(wildcard include/config/ARCH_USE_GNU_PROPERTY) \
    $(wildcard include/config/ARCH_HAVE_ELF_PROT) \
  /home/younes/bbr/arch/x86/include/asm/elf.h \
    $(wildcard include/config/X86_X32_ABI) \
  /home/younes/bbr/arch/x86/include/asm/ia32.h \
  /home/younes/bbr/include/linux/compat.h \
    $(wildcard include/config/ARCH_HAS_SYSCALL_WRAPPER) \
    $(wildcard include/config/COMPAT_OLD_SIGACTION) \
    $(wildcard include/config/ODD_RT_SIGACTION) \
  /home/younes/bbr/include/linux/sem.h \
  /home/younes/bbr/include/uapi/linux/sem.h \
  /home/younes/bbr/include/linux/ipc.h \
  /home/younes/bbr/include/uapi/linux/ipc.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/ipcbuf.h \
  /home/younes/bbr/include/uapi/asm-generic/ipcbuf.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/sembuf.h \
  /home/younes/bbr/include/linux/socket.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/socket.h \
  /home/younes/bbr/include/uapi/asm-generic/socket.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/sockios.h \
  /home/younes/bbr/include/uapi/asm-generic/sockios.h \
  /home/younes/bbr/include/uapi/linux/sockios.h \
  /home/younes/bbr/include/linux/uio.h \
    $(wildcard include/config/ARCH_HAS_COPY_MC) \
  /home/younes/bbr/include/uapi/linux/uio.h \
  /home/younes/bbr/include/uapi/linux/socket.h \
  /home/younes/bbr/include/uapi/linux/if.h \
  /home/younes/bbr/include/uapi/linux/libc-compat.h \
  /home/younes/bbr/include/uapi/linux/hdlc/ioctl.h \
  /home/younes/bbr/include/linux/fs.h \
    $(wildcard include/config/READ_ONLY_THP_FOR_FS) \
    $(wildcard include/config/FS_POSIX_ACL) \
    $(wildcard include/config/CGROUP_WRITEBACK) \
    $(wildcard include/config/IMA) \
    $(wildcard include/config/FILE_LOCKING) \
    $(wildcard include/config/FSNOTIFY) \
    $(wildcard include/config/FS_ENCRYPTION) \
    $(wildcard include/config/FS_VERITY) \
    $(wildcard include/config/EPOLL) \
    $(wildcard include/config/UNICODE) \
    $(wildcard include/config/QUOTA) \
    $(wildcard include/config/FS_DAX) \
    $(wildcard include/config/BLOCK) \
  /home/younes/bbr/include/linux/wait_bit.h \
  /home/younes/bbr/include/linux/kdev_t.h \
  /home/younes/bbr/include/uapi/linux/kdev_t.h \
  /home/younes/bbr/include/linux/dcache.h \
  /home/younes/bbr/include/linux/rculist.h \
    $(wildcard include/config/PROVE_RCU_LIST) \
  /home/younes/bbr/include/linux/rculist_bl.h \
  /home/younes/bbr/include/linux/list_bl.h \
  /home/younes/bbr/include/linux/bit_spinlock.h \
  /home/younes/bbr/include/linux/lockref.h \
    $(wildcard include/config/ARCH_USE_CMPXCHG_LOCKREF) \
  /home/younes/bbr/include/linux/stringhash.h \
    $(wildcard include/config/DCACHE_WORD_ACCESS) \
  /home/younes/bbr/include/linux/hash.h \
    $(wildcard include/config/HAVE_ARCH_HASH) \
  /home/younes/bbr/include/linux/path.h \
  /home/younes/bbr/include/linux/list_lru.h \
  /home/younes/bbr/include/linux/shrinker.h \
    $(wildcard include/config/SHRINKER_DEBUG) \
  /home/younes/bbr/include/linux/xarray.h \
    $(wildcard include/config/XARRAY_MULTI) \
  /home/younes/bbr/include/linux/sched/mm.h \
    $(wildcard include/config/MMU_LAZY_TLB_REFCOUNT) \
    $(wildcard include/config/ARCH_HAS_MEMBARRIER_CALLBACKS) \
  /home/younes/bbr/include/linux/sync_core.h \
    $(wildcard include/config/ARCH_HAS_SYNC_CORE_BEFORE_USERMODE) \
    $(wildcard include/config/ARCH_HAS_PREPARE_SYNC_CORE_CMD) \
  /home/younes/bbr/arch/x86/include/asm/sync_core.h \
  /home/younes/bbr/include/linux/sched/coredump.h \
  /home/younes/bbr/include/linux/radix-tree.h \
  /home/younes/bbr/include/linux/pid.h \
  /home/younes/bbr/include/linux/capability.h \
  /home/younes/bbr/include/uapi/linux/capability.h \
  /home/younes/bbr/include/linux/semaphore.h \
  /home/younes/bbr/include/linux/fcntl.h \
    $(wildcard include/config/ARCH_32BIT_OFF_T) \
  /home/younes/bbr/include/uapi/linux/fcntl.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/fcntl.h \
  /home/younes/bbr/include/uapi/asm-generic/fcntl.h \
  /home/younes/bbr/include/uapi/linux/openat2.h \
  /home/younes/bbr/include/linux/migrate_mode.h \
  /home/younes/bbr/include/linux/percpu-rwsem.h \
  /home/younes/bbr/include/linux/rcuwait.h \
  /home/younes/bbr/include/linux/sched/signal.h \
    $(wildcard include/config/SCHED_AUTOGROUP) \
    $(wildcard include/config/BSD_PROCESS_ACCT) \
    $(wildcard include/config/TASKSTATS) \
    $(wildcard include/config/STACK_GROWSUP) \
  /home/younes/bbr/include/linux/signal.h \
    $(wildcard include/config/DYNAMIC_SIGFRAME) \
  /home/younes/bbr/include/linux/sched/jobctl.h \
  /home/younes/bbr/include/linux/sched/task.h \
    $(wildcard include/config/HAVE_EXIT_THREAD) \
    $(wildcard include/config/ARCH_WANTS_DYNAMIC_TASK_STRUCT) \
    $(wildcard include/config/HAVE_ARCH_THREAD_STRUCT_WHITELIST) \
  /home/younes/bbr/include/linux/uaccess.h \
    $(wildcard include/config/ARCH_HAS_SUBPAGE_FAULTS) \
  /home/younes/bbr/include/linux/fault-inject-usercopy.h \
    $(wildcard include/config/FAULT_INJECTION_USERCOPY) \
  /home/younes/bbr/include/linux/nospec.h \
  /home/younes/bbr/arch/x86/include/asm/uaccess.h \
    $(wildcard include/config/CC_HAS_ASM_GOTO_OUTPUT) \
    $(wildcard include/config/CC_HAS_ASM_GOTO_TIED_OUTPUT) \
    $(wildcard include/config/X86_INTEL_USERCOPY) \
  /home/younes/bbr/include/linux/mmap_lock.h \
  /home/younes/bbr/arch/x86/include/asm/smap.h \
  /home/younes/bbr/arch/x86/include/asm/extable.h \
    $(wildcard include/config/BPF_JIT) \
  /home/younes/bbr/arch/x86/include/asm/tlbflush.h \
  /home/younes/bbr/include/linux/mmu_notifier.h \
  /home/younes/bbr/include/linux/interval_tree.h \
  /home/younes/bbr/arch/x86/include/asm/invpcid.h \
  /home/younes/bbr/arch/x86/include/asm/pti.h \
  /home/younes/bbr/arch/x86/include/asm/pgtable.h \
    $(wildcard include/config/DEBUG_WX) \
    $(wildcard include/config/HAVE_ARCH_TRANSPARENT_HUGEPAGE_PUD) \
    $(wildcard include/config/ARCH_HAS_PTE_DEVMAP) \
    $(wildcard include/config/ARCH_SUPPORTS_PMD_PFNMAP) \
    $(wildcard include/config/ARCH_SUPPORTS_PUD_PFNMAP) \
    $(wildcard include/config/HAVE_ARCH_SOFT_DIRTY) \
    $(wildcard include/config/ARCH_ENABLE_THP_MIGRATION) \
    $(wildcard include/config/PAGE_TABLE_CHECK) \
  /home/younes/bbr/arch/x86/include/asm/pkru.h \
  /home/younes/bbr/arch/x86/include/asm/fpu/api.h \
    $(wildcard include/config/X86_DEBUG_FPU) \
  /home/younes/bbr/arch/x86/include/asm/coco.h \
  /home/younes/bbr/include/asm-generic/pgtable_uffd.h \
  /home/younes/bbr/include/linux/page_table_check.h \
  /home/younes/bbr/arch/x86/include/asm/pgtable_64.h \
  /home/younes/bbr/arch/x86/include/asm/fixmap.h \
    $(wildcard include/config/PROVIDE_OHCI1394_DMA_INIT) \
    $(wildcard include/config/X86_IO_APIC) \
    $(wildcard include/config/PCI_MMCONFIG) \
    $(wildcard include/config/ACPI_APEI_GHES) \
    $(wildcard include/config/INTEL_TXT) \
  /home/younes/bbr/arch/x86/include/uapi/asm/vsyscall.h \
  /home/younes/bbr/include/asm-generic/fixmap.h \
  /home/younes/bbr/arch/x86/include/asm/pgtable-invert.h \
  /home/younes/bbr/arch/x86/include/asm/uaccess_64.h \
  /home/younes/bbr/arch/x86/include/asm/runtime-const.h \
  /home/younes/bbr/include/asm-generic/access_ok.h \
    $(wildcard include/config/ALTERNATE_USER_ADDRESS_SPACE) \
  /home/younes/bbr/include/linux/cred.h \
  /home/younes/bbr/include/linux/key.h \
    $(wildcard include/config/KEY_NOTIFICATIONS) \
    $(wildcard include/config/NET) \
  /home/younes/bbr/include/linux/assoc_array.h \
    $(wildcard include/config/ASSOCIATIVE_ARRAY) \
  /home/younes/bbr/include/linux/sched/user.h \
    $(wildcard include/config/VFIO_PCI_ZDEV_KVM) \
    $(wildcard include/config/IOMMUFD) \
    $(wildcard include/config/WATCH_QUEUE) \
  /home/younes/bbr/include/linux/ratelimit.h \
  /home/younes/bbr/include/linux/posix-timers.h \
  /home/younes/bbr/include/linux/alarmtimer.h \
    $(wildcard include/config/RTC_CLASS) \
  /home/younes/bbr/include/linux/hrtimer.h \
    $(wildcard include/config/HIGH_RES_TIMERS) \
    $(wildcard include/config/TIME_LOW_RES) \
    $(wildcard include/config/TIMERFD) \
  /home/younes/bbr/include/linux/hrtimer_defs.h \
  /home/younes/bbr/include/linux/timerqueue.h \
  /home/younes/bbr/include/linux/rcuref.h \
  /home/younes/bbr/include/linux/rcu_sync.h \
  /home/younes/bbr/include/linux/delayed_call.h \
  /home/younes/bbr/include/linux/uuid.h \
  /home/younes/bbr/include/linux/errseq.h \
  /home/younes/bbr/include/linux/ioprio.h \
  /home/younes/bbr/include/linux/sched/rt.h \
  /home/younes/bbr/include/linux/iocontext.h \
    $(wildcard include/config/BLK_ICQ) \
  /home/younes/bbr/include/uapi/linux/ioprio.h \
  /home/younes/bbr/include/linux/fs_types.h \
  /home/younes/bbr/include/linux/mount.h \
  /home/younes/bbr/include/linux/mnt_idmapping.h \
  /home/younes/bbr/include/linux/slab.h \
    $(wildcard include/config/FAILSLAB) \
    $(wildcard include/config/KFENCE) \
    $(wildcard include/config/SLUB_TINY) \
    $(wildcard include/config/SLUB_DEBUG) \
    $(wildcard include/config/SLAB_FREELIST_HARDENED) \
    $(wildcard include/config/SLAB_BUCKETS) \
  /home/younes/bbr/include/linux/percpu-refcount.h \
  /home/younes/bbr/include/linux/kasan.h \
    $(wildcard include/config/KASAN_STACK) \
    $(wildcard include/config/KASAN_VMALLOC) \
  /home/younes/bbr/include/linux/kasan-enabled.h \
  /home/younes/bbr/include/linux/kasan-tags.h \
  /home/younes/bbr/include/linux/rw_hint.h \
  /home/younes/bbr/include/linux/file_ref.h \
  /home/younes/bbr/include/linux/unicode.h \
  /home/younes/bbr/include/uapi/linux/fs.h \
  /home/younes/bbr/include/linux/quota.h \
    $(wildcard include/config/QUOTA_NETLINK_INTERFACE) \
  /home/younes/bbr/include/uapi/linux/dqblk_xfs.h \
  /home/younes/bbr/include/linux/dqblk_v1.h \
  /home/younes/bbr/include/linux/dqblk_v2.h \
  /home/younes/bbr/include/linux/dqblk_qtree.h \
  /home/younes/bbr/include/linux/projid.h \
  /home/younes/bbr/include/uapi/linux/quota.h \
  /home/younes/bbr/include/uapi/linux/aio_abi.h \
  /home/younes/bbr/include/uapi/linux/unistd.h \
  /home/younes/bbr/arch/x86/include/asm/unistd.h \
  /home/younes/bbr/arch/x86/include/uapi/asm/unistd.h \
  /home/younes/bbr/arch/x86/include/generated/uapi/asm/unistd_64.h \
  /home/younes/bbr/arch/x86/include/generated/asm/unistd_64_x32.h \
  /home/younes/bbr/arch/x86/include/generated/asm/unistd_32_ia32.h \
  /home/younes/bbr/arch/x86/include/asm/compat.h \
  /home/younes/bbr/include/linux/sched/task_stack.h \
    $(wildcard include/config/DEBUG_STACK_USAGE) \
  /home/younes/bbr/include/uapi/linux/magic.h \
  /home/younes/bbr/arch/x86/include/asm/user32.h \
  /home/younes/bbr/include/asm-generic/compat.h \
    $(wildcard include/config/COMPAT_FOR_U64_ALIGNMENT) \
  /home/younes/bbr/arch/x86/include/asm/syscall_wrapper.h \
  /home/younes/bbr/arch/x86/include/asm/user.h \
  /home/younes/bbr/arch/x86/include/asm/user_64.h \
  /home/younes/bbr/arch/x86/include/asm/fsgsbase.h \
  /home/younes/bbr/arch/x86/include/asm/vdso.h \
  /home/younes/bbr/include/uapi/linux/elf.h \
  /home/younes/bbr/include/uapi/linux/elf-em.h \
  /home/younes/bbr/include/linux/kobject.h \
    $(wildcard include/config/UEVENT_HELPER) \
    $(wildcard include/config/DEBUG_KOBJECT_RELEASE) \
  /home/younes/bbr/include/linux/sysfs.h \
  /home/younes/bbr/include/linux/kernfs.h \
    $(wildcard include/config/KERNFS) \
  /home/younes/bbr/include/linux/idr.h \
  /home/younes/bbr/include/linux/kobject_ns.h \
  /home/younes/bbr/include/linux/moduleparam.h \
    $(wildcard include/config/ALPHA) \
    $(wildcard include/config/PPC64) \
  /home/younes/bbr/include/linux/rbtree_latch.h \
  /home/younes/bbr/include/linux/error-injection.h \
  /home/younes/bbr/include/asm-generic/error-injection.h \
  /home/younes/bbr/arch/x86/include/asm/module.h \
    $(wildcard include/config/UNWINDER_ORC) \
  /home/younes/bbr/include/asm-generic/module.h \
    $(wildcard include/config/HAVE_MOD_ARCH_SPECIFIC) \
    $(wildcard include/config/MODULES_USE_ELF_REL) \
    $(wildcard include/config/MODULES_USE_ELF_RELA) \

llm_cc_v3.o: $(deps_llm_cc_v3.o)

$(deps_llm_cc_v3.o):

llm_cc_v3.o: $(wildcard /home/younes/bbr/tools/objtool/objtool)
