#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

static u32 llm_cc_3_6_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return max_t(u32, (tp->snd_cwnd * 921) >> 10, 2U * tp->mss_cache);
}

static void llm_cc_3_6_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    u32 rtt_us;
    if (!tcp_is_cwnd_limited(sk))
        return;
    if (tp->snd_cwnd <= tp->snd_ssthresh) {
        tcp_slow_start(tp, acked);
    } else {
        rtt_us = tp->srtt_us >> 3;
        if (rtt_us > 90000) {
            tcp_cong_avoid_ai(tp, tp->snd_cwnd * 2, acked);
        } else {
            tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);
        }
    }
}

static u32 llm_cc_3_6_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_3_6 __read_mostly = {
    .name       = "llm_cc_3_6",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_3_6_ssthresh,
    .cong_avoid = llm_cc_3_6_cong_avoid,
    .undo_cwnd  = llm_cc_3_6_undo_cwnd,
};

static int __init llm_cc_3_6_register(void)
{
    return tcp_register_congestion_control(&llm_cc_3_6);
}

static void __exit llm_cc_3_6_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_3_6);
}

module_init(llm_cc_3_6_register);
module_exit(llm_cc_3_6_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("LLM Generated CC for Wi-Fi Video Streaming v3.6");