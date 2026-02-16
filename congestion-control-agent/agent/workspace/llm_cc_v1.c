#include <linux/module.h>
#include <linux/init.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <net/tcp.h>

/* FlexNGIA-LLM Generated Logic */

static u32 llm_cc_v1_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    u32 min_rtt = tp->rtt_min.min;
    u32 curr_rtt = tp->srtt_us >> 3;
    u32 mss = max_t(u32, tp->mss_cache, 1U);
    u64 bdp_bytes;
    u32 bdp_packets;

    /* BDP = (50 Mbps * Min_RTT) / 8 bits/byte */
    /* 50,000,000 * min_rtt / 1,000,000 / 8 = (50 * min_rtt) / 8 */
    bdp_bytes = (50ULL * min_rtt) / 8;
    bdp_packets = max_t(u32, (u32)(bdp_bytes / mss), 2U);

    /* During initial probing, cap ssthresh if RTT exceeds 1.2x Min_RTT */
    if (min_rtt > 0 && curr_rtt > (min_rtt * 12) / 10) {
        return max_t(u32, tp->snd_cwnd, 2U);
    }

    return bdp_packets;
}

static void llm_cc_v1_cong_avoid(struct sock *sk, u32 ack, u32 acked)
{
    struct tcp_sock *tp = tcp_sk(sk);
    u32 min_rtt = tp->rtt_min.min;
    u32 curr_rtt = tp->srtt_us >> 3;
    u32 mss = max_t(u32, tp->mss_cache, 1U);

    if (!tcp_is_cwnd_limited(sk))
        return;

    if (tp->snd_cwnd < tp->snd_ssthresh) {
        tcp_slow_start(tp, acked);
    } else {
        /* Congestion Avoidance Logic */
        if (min_rtt > 0 && curr_rtt < (min_rtt * 11) / 10) {
            /* Aggressive increase: cwnd = cwnd + (BDP_packets / cwnd) per ACK */
            u64 bdp_bytes = (50ULL * min_rtt) / 8;
            u32 bdp_packets = max_t(u32, (u32)(bdp_bytes / mss), 1U);
            
            tp->snd_cwnd_cnt += bdp_packets;
            if (tp->snd_cwnd_cnt >= tp->snd_cwnd) {
                tp->snd_cwnd += tp->snd_cwnd_cnt / tp->snd_cwnd;
                tp->snd_cwnd_cnt %= tp->snd_cwnd;
            }
        } else if (min_rtt > 0) {
            /* Proactive reduction: cwnd = cwnd * (Min_RTT / Current_RTT) */
            tp->snd_cwnd = max_t(u32, 2U, (tp->snd_cwnd * min_rtt) / curr_rtt);
            tp->snd_cwnd_cnt = 0;
        } else {
            /* Fallback to standard AI if no RTT data */
            tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked);
        }
    }
}

static u32 llm_cc_v1_undo_cwnd(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    u32 min_rtt = tp->rtt_min.min;
    u32 mss = max_t(u32, tp->mss_cache, 1U);
    u64 bdp_bytes;
    u32 bdp_packets;

    if (min_rtt == 0)
        return tp->snd_cwnd;

    /* Set cwnd to BDP: (50 Mbps * Min_RTT) / 8 */
    bdp_bytes = (50ULL * min_rtt) / 8;
    bdp_packets = (u32)(bdp_bytes / mss);

    return max_t(u32, bdp_packets, 2U);
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
MODULE_DESCRIPTION("LLM Generated CC");