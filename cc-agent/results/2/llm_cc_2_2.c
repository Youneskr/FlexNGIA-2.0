#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

static u32 llm_cc_2_2_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    /* Keep 80% of CWND (819/1024) to mitigate impact of Wi-Fi noise/interference */
    return max_t(u32, (tp->snd_cwnd * 819) >> 10, 2U * tp->mss_cache);
}

static void llm_cc_2_2_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    if (!tcp_is_cwnd_limited(sk))
        return;
    if (tcp_in_slow_start(tp)) {
        tcp_slow_start(tp, acked);
    } else {
        /* Accelerated Additive Increase: Increase by ~2 segments per RTT */
        /* to reach the 12Mbps target faster in 802.11g environments */
        tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked * 2);
    }
}

static u32 llm_cc_2_2_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_2_2 __read_mostly = {
    .name       = "llm_cc_2_2",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_2_2_ssthresh,
    .cong_avoid = llm_cc_2_2_cong_avoid,
    .undo_cwnd  = llm_cc_2_2_undo_cwnd,
};

static int __init llm_cc_2_2_register(void)
{
    return tcp_register_congestion_control(&llm_cc_2_2);
}

static void __exit llm_cc_2_2_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_2_2);
}

module_init(llm_cc_2_2_register);
module_exit(llm_cc_2_2_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("LLM Generated CC for Wi-Fi Video Streaming Optimization");