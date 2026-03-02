#include <linux/module.h>
#include <linux/init.h>
#include <linux/string.h>
#include <linux/param.h>
#include <net/tcp.h>

#define DEFAULT_CC "reno"

static char *delegate_cc = DEFAULT_CC;
static const struct tcp_congestion_ops *delegate_ca;
static struct module *delegate_owner;

/* Setter: verify & switch delegate */
static int delegate_cc_set(const char *val, const struct kernel_param *kp)
{
	const struct tcp_congestion_ops *ca;
	char *buf = kstrndup(val, TCP_CA_NAME_MAX, GFP_KERNEL);
	int ret;

	if (!buf)
		return -ENOMEM;

	strim(buf);

	/* If new value is same as current, skip update */
	if (strcmp(buf, delegate_cc) == 0) {
		kfree(buf);
		return 0;
	}

	/* Look up new CC */
	rcu_read_lock();
	ca = tcp_ca_find(buf);
	rcu_read_unlock();
	if (!ca) {
		kfree(buf);
		return -ENOENT;
	}

	/* Pin the CC module */
	if (!try_module_get(ca->owner)) {
		kfree(buf);
		return -ENODEV;
	}

	/* Store the new string into the param */
	ret = param_set_charp(buf, kp);
	kfree(buf);
	if (ret) {
		module_put(ca->owner);
		return ret;
	}

	/* Drop old ref, swap delegate */
	if (delegate_owner)
		module_put(delegate_owner);
	delegate_ca = ca;
	delegate_owner = ca->owner;

	pr_info("tcp_proxy: delegate set to '%s'\n", ca->name);
	return 0;
}

static int delegate_cc_get(char *buffer, const struct kernel_param *kp)
{
    return param_get_charp(buffer, kp);
}

static const struct kernel_param_ops delegate_cc_ops = {
	.set = delegate_cc_set,
	.get = delegate_cc_get,
};

module_param_cb(delegate_cc, &delegate_cc_ops, &delegate_cc, 0644);
MODULE_PARM_DESC(delegate_cc, "Delegate congestion control algorithm (default: reno)");

/* TCP CC callbacks */
static u32 proxy_ssthresh(struct sock *sk){	return delegate_ca->ssthresh(sk); }
static void proxy_cong_avoid(struct sock *sk, u32 ack, u32 acked){ delegate_ca->cong_avoid(sk, ack, acked); }
static u32 proxy_undo_cwnd(struct sock *sk){ return delegate_ca->undo_cwnd(sk); }

static struct tcp_congestion_ops tcp_proxy __read_mostly = {
	.flags		= TCP_CONG_NON_RESTRICTED,
	.name		= "proxy",
	.owner		= THIS_MODULE,
	.ssthresh	= proxy_ssthresh,
	.cong_avoid	= proxy_cong_avoid,
	.undo_cwnd	= proxy_undo_cwnd,
};

static int __init tcp_proxy_register(void)
{
	const struct tcp_congestion_ops *ca;

	/* Register our CC first */
	if (tcp_register_congestion_control(&tcp_proxy))
		return -EINVAL;

	/* Resolve default delegate */
	rcu_read_lock();
	ca = tcp_ca_find(delegate_cc);
	rcu_read_unlock();
	if (!ca || !try_module_get(ca->owner)) {
		pr_err("tcp_proxy: default delegate '%s' not available\n", delegate_cc);
		tcp_unregister_congestion_control(&tcp_proxy);
		return -ENOENT;
	}

	delegate_ca = ca;
	delegate_owner = ca->owner;
	pr_info("tcp_proxy: loaded, delegate = '%s'\n", ca->name);

	return 0;
}

static void __exit tcp_proxy_unregister(void)
{
	if (delegate_owner)
		module_put(delegate_owner);
	tcp_unregister_congestion_control(&tcp_proxy);
	pr_info("tcp_proxy: unloaded\n");
}

module_init(tcp_proxy_register);
module_exit(tcp_proxy_unregister);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("FlexNGIA");
MODULE_DESCRIPTION("TCP Proxy Congestion Control");
