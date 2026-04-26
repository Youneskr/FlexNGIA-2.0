#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

static u32 llm_cc_2_1_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    /* Reduce CWND to 70% instead of 50% to handle Wi-Fi noise better */
    return max_t(u32, (tp->snd_cwnd * 716) >> 10, 2U * tp->mss_cache);
}

static void llm_cc_2_1_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    if (!tcp_is_cwnd_limited(sk))
        return;
    if (tcp_in_slow_start(tp))
        tcp_slow_start(tp, acked);
    else
        tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);
}

static u32 llm_cc_2_1_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_2_1 __read_mostly = {
    .name       = "llm_cc_2_1",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_2_1_ssthresh,
    .cong_avoid = llm_cc_2_1_cong_avoid,
    .undo_cwnd  = llm_cc_2_1_undo_cwnd,
};

static int __init llm_cc_2_1_register(void)
{
    return tcp_register_congestion_control(&llm_cc_2_1);
}

static void __exit llm_cc_2_1_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_2_1);
}

module_init(llm_cc_2_1_register);
module_exit(llm_cc_2_1_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("LLM Generated CC for Wi-Fi Video Streaming");