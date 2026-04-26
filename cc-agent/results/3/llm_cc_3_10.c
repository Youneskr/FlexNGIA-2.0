#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

/* FlexNGIA-LLM Generated Logic: llm_cc_3_10 */

static u32 llm_cc_3_10_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    /* Wi-Fi 2.4GHz Optimization: Retain 90% of CWND (922/1024) to handle non-congestive interference loss */
    return max_t(u32, (tp->snd_cwnd * 922) >> 10, 2U * tp->mss_cache);
}

static void llm_cc_3_10_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    u32 rtt_ms;

    if (!tcp_is_cwnd_limited(sk))
        return;

    if (tp->snd_cwnd <= tp->snd_ssthresh) {
        tcp_slow_start(tp, acked);
    } else {
        /* Convert SRTT to milliseconds */
        rtt_ms = (tp->srtt_us >> 3) / 1000;

        if (rtt_ms < 90) {
            /* Target met: Very aggressive growth (4x Reno) */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd >> 2, acked);
        } else if (rtt_ms < 150) {
            /* Target not met but RTT manageable: Aggressive growth (2x Reno) to hit 12Mbps */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd >> 1, acked);
        } else {
            /* High Latency: Standard Reno growth to avoid worsening bufferbloat */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);
        }
    }
}

static u32 llm_cc_3_10_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    return tp->snd_cwnd;
}

static struct tcp_congestion_ops llm_cc_3_10 __read_mostly = {
    .name       = "llm_cc_3_10",
    .owner      = THIS_MODULE,
    .ssthresh   = llm_cc_3_10_ssthresh,
    .cong_avoid = llm_cc_3_10_cong_avoid,
    .undo_cwnd  = llm_cc_3_10_undo_cwnd,
};

static int __init llm_cc_3_10_register(void)
{
    return tcp_register_congestion_control(&llm_cc_3_10);
}

static void __exit llm_cc_3_10_unregister(void)
{
    tcp_unregister_congestion_control(&llm_cc_3_10);
}

module_init(llm_cc_3_10_register);
module_exit(llm_cc_3_10_unregister);

MODULE_AUTHOR("FlexNGIA Agent");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("LLM Generated CC for Wi-Fi Video Streaming v3.10");