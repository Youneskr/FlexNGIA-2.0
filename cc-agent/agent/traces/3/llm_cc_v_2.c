#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

/* FlexNGIA-LLM Generated Logic */

static u32 llm_cc_v2_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    
    /* >>> IMPLEMENTATION HERE <<< */
    /* Implement the Slow Start Threshold logic based on the design. */
    /* Default fallback: */
    return max_t(u32, tp->snd_cwnd >> 1, 2U * tp->mss_cache);
}

static void llm_cc_v2_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    
    /* >>> IMPLEMENTATION HERE <<< */
    /* Implement the Congestion Avoidance logic based on the design. */
    /* Use: tcp_slow_start(tp, acked) and tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked) */
    tcp_cong_avoid_ai(tp, tp->snd_cwnd + 10, acked);
}

static u32 llm_cc_v2_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    /* >>> IMPLEMENTATION HERE <<< */
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_v2 __read_mostly = {
    .name       = "llm_cc_v2",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_v2_ssthresh,
    .cong_avoid = llm_cc_v2_cong_avoid,
    .undo_cwnd  = llm_cc_v2_undo_cwnd,
};

static int __init llm_cc_v2_register(void)
{
    return tcp_register_congestion_control(&llm_cc_v2);
}

static void __exit llm_cc_v2_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_v2);
}

module_init(llm_cc_v2_register);
module_exit(llm_cc_v2_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("LLM Generated CC");