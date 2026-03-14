#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xb8e8c0af, "tcp_slow_start" },
	{ 0x77f7ac44, "tcp_unregister_congestion_control" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0x5fbe28b0, "tcp_register_congestion_control" },
	{ 0xbe4b0980, "tcp_cong_avoid_ai" },
	{ 0x7be76ff5, "module_layout" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "8B9C2F6D5DBE055136DD9F5");
