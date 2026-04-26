#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

static u32 llm_cc_3_8_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    /* Wi-Fi optimization: Reduce CWND to 85% instead of 50% to maintain throughput */
    return max_t(u32, (tp->snd_cwnd * 870) >> 10, 2U * tp->mss_cache);
}

static void llm_cc_3_8_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    u32 rtt_ms;

    if (!tcp_is_cwnd_limited(sk))
        return;

    if (tp->snd_cwnd <= tp->snd_ssthresh) {
        tcp_slow_start(tp, acked);
    } else {
        rtt_ms = (tp->srtt_us >> 3) / 1000;
        if (rtt_ms < 90) {
            /* Aggressive: RTT is within target, push for 12Mbps */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd >> 2, acked);
        } else if (rtt_ms > 130) {
            /* Conservative: RTT is too high, slow down growth to mitigate bufferbloat */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd << 1, acked);
        } else {
            /* Standard Reno-like growth */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);
        }
    }
}

static u32 llm_cc_3_8_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_3_8 __read_mostly = {
    .name       = "llm_cc_3_8",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_3_8_ssthresh,
    .cong_avoid = llm_cc_3_8_cong_avoid,
    .undo_cwnd  = llm_cc_3_8_undo_cwnd,
};

static int __init llm_cc_3_8_register(void)
{
    return tcp_register_congestion_control(&llm_cc_3_8);
}

static void __exit llm_cc_3_8_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_3_8);
}

module_init(llm_cc_3_8_register);
module_exit(llm_cc_3_8_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("LLM Generated CC for Wi-Fi Video Streaming v3.8");