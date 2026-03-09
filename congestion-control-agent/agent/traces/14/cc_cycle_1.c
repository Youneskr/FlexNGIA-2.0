#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

#define TARGET_RTT_US 90000

static u32 llm_cc_v1_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    /* Gentler reduction for Wi-Fi: 75% of CWND instead of 50% */
    return max_t(u32, (tp->snd_cwnd * 3) >> 2, 2U * tp->mss_cache);
}

static void llm_cc_v1_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    u32 rtt = tp->srtt_us >> 3;

    if (!tcp_is_cwnd_limited(sk))
        return;

    if (tcp_in_slow_start(tp)) {
        tcp_slow_start(tp, acked);
    } else {
        /* If RTT is below target, grow normally. If above, grow very slowly. */
        if (rtt < TARGET_RTT_US) {
            tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);
        } else {
            /* Delay-constrained growth: 1 MSS per 2 RTTs approx */
            if (tp->snd_cwnd_cnt >= tp->snd_cwnd * 2) {
                tp->snd_cwnd++;
                tp->snd_cwnd_cnt = 0;
            } else {
                tp->snd_cwnd_cnt += acked;
            }
        }
    }
}

static u32 llm_cc_v1_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_v1 __read_mostly = {
    .name       = "llm_cc_v1",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_v1_ssthresh,
    .cong_avoid = llm_cc_v1_cong_avoid,
    .undo_cwnd  = llm_cc_v1_undo_cwnd,
};

static int __init llm_cc_v1_register(void)
{
    return tcp_register_congestion_control(&llm_cc_v1);
}

static void __exit llm_cc_v1_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_v1);
}

module_init(llm_cc_v1_register);
module_exit(llm_cc_v1_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Delay-Aware Wi-Fi Optimized CC");