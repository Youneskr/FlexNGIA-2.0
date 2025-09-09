# Congestion Control Agent

## Overview
This directory contains the implementation and experiments for the **AI-Driven Congestion Control Agent**.

It includes:
- A custom Linux kernel with a TCP Proxy module and real-time TCP metric monitoring
- An LLM-driven agent for congestion control scheme design and switching
- Experimentation scripts using Mininet-WiFi
- Performance results and analysis


<div align="center">

[![Paper](https://img.shields.io/badge/📄-Paper-yellow?style=flat)](https://arxiv.org/abs/2509.02124)
[![FlexNGIA Website](https://img.shields.io/badge/🌐-flexngia.net-blue?style=flat)](https://www.flexngia.net/)

</div>
<div align="center">
    <img src="../resources/logo.webp" alt="FlexNGIA Logo" width="250">
</div>

---

# 1. Kernel Installation and Configuration
This section provides a comprehensive guide for setting up the kernel, including prerequisites, source acquisition, configuration, compilation, and module installation. We use a **customized Linux kernel version 5.13.12** (based on Google’s BBR kernel) that integrates the TCP Proxy Congestion Control module along with real-time TCP metric monitoring capabilities.

## 1.1 Prerequisites
Install required development tools:
```bash
sudo apt-get install build-essential libncurses-dev bison flex libssl-dev libelf-dev
```

Install the `dwarves` package (required for modern kernel builds):
```bash
sudo apt install dwarves
```

## 1.2 Kernel Source Installation
Download the **customized** Linux kernel version 5.13.12 (based on Google’s BBR kernel):  
[Download Kernel Source](https://ucf5a8c83aca9580ec1b76962f16.dl.dropboxusercontent.com/cd/0/get/CxCkxaLzP-PGRD_kDZzDFWuT6O5CfRKhbHG9jj1jFeUS5f6KiI84qq8gJsm2WzQlxYSQ8c9uDPnUXS8KWk2Nuu0pAx3TwMA5D9HG1akM2-xbiGhrDSIhKeVkLoKlyTWrTxNe26Zcmce78CkQZtCrMkcW3QpqVo-T9ZbYGLPrlbo_qg/file?_download_id=26587710815208965626527659032575300133024348866439558685271136431179&_log_download_success=1&_notify_domain=www.dropbox.com&dl=1)

After downloading, extract and enter the source directory:
```bash
unzip kernel_5.13.12.zip
cd kernel_5.13.12
```

## 1.3 First-Time Compilation Setup
To disable trusted keys and revocation keys (useful for custom kernel builds):
```bash
CONFIG_SYSTEM_TRUSTED_KEYS=""
scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
scripts/config --disable SYSTEM_REVOCATION_KEYS
```

## 1.4 Kernel Configuration
Copy your current kernel configuration to the working directory:
```bash
cp -v /boot/config-$(uname -r) .config
```

Open the kernel configuration menu to `enable the TCP Proxy module`: 
```bash
make menuconfig
```

In the menu, navigate to:
```
Networking support → Networking options → TCP: advanced congestion control
[M] TCP Proxy congestion control
```

Select the module (`[M]`), save the configuration, and exit.
## 1.5 Compilation & Installation

```bash
# Compile the kernel using all available CPU cores
make -j $(nproc)
```

```bash
# Install the kernel modules
sudo make modules_install
```

```bash
# Install the newly compiled kernel
sudo make install
```

```bash
# Reboot the system to load the new kernel
sudo reboot
```

---

# 2. TCP Proxy Congestion Control Module

## 2.1 Overview
The **TCP Proxy** is a minimal congestion control algorithm that:
- Delegates its behavior to another CC algorithm chosen at runtime.
- Allows seamless switching between algorithms.
- Forwards standard callbacks (`ssthresh()`, `cong_avoid()`, `undo_cwnd()`).
- Default delegate: `reno` (modifiable at runtime).

## 2.2 How It Works
- **Delegation model:** `delegate_cc` parameter points to target CC (e.g., `reno`, `llm_cc_v0`).
- **Lifecycle:** On load, registers as a CC algorithm, resolves delegate, and pins its module. On unload, releases reference.
- **Runtime control:** `/sys/module/tcp_proxy/parameters/delegate_cc`

## 2.3 Compatibility
- Compatible with traditional loss-based CC algorithms (e.g., `reno`).
- Not suitable for BBR-like algorithms that use `cong_control()`.

## 2.4 Usage

```bash
# Load the TCP Proxy module with the default delegate (reno)
sudo modprobe tcp_proxy delegate_cc
```

```bash
# Load the TCP Proxy module and specify a delegate CC scheme at load time (e.g., reno)
sudo modprobe tcp_proxy delegate_cc=reno
```

```bash
# Set the TCP Proxy as the active congestion control algorithm
sudo sysctl -w net.ipv4.tcp_congestion_control=proxy
```

```bash
# Check the currently active delegate CC scheme for the TCP Proxy
sudo cat /sys/module/tcp_proxy/parameters/delegate_cc
```

```bash
# Dynamically switch the delegate CC scheme at runtime (e.g., to llm_cc_v0)
echo -n "llm_cc_v0" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc
```


---

## 3. TCP Metrics Monitoring

### 3.1 Overview
The kernel is instrumented to capture and expose real-time TCP metrics from kernel space to user space, including:
- Congestion Window (CWND)
- Round-Trip Time (RTT)
- TCP throughput
- Packet losses and retransmissions
- Extendable to monitor additional TCP-related metrics

### 3.2 Monitoring Module
The header file `include/linux/track_metrics.h` defines the `track` function, which has the following prototype:

```c
track(CC_name, source_address, destination_address, source_port, destination_port, Metric_ID, Metric_value);
```

For detailed information about the `Metric_ID` corresponding to each metric, refer to the `include/linux/track_metrics.h` file. To add new `Metric_ID` values for extracting additional metrics, update this file accordingly.

By including this header (`#include <linux/track_metrics.h>`) in a kernel C file, the `track` function can be invoked at any appropriate location to extract metrics.  

Currently, this header is included in several TCP-related source files:
- `tcp_rate.c` for monitoring TCP throughput
- `tcp_input.c` for extracting RTT, losses, and retransmissions
- `tcp_cong.c` for monitoring the growth of the congestion window (CWND) for TCP Reno

For example, the kernel monitors the growth of the congestion window (CWND) for TCP Reno in `net/ipv4/tcp_cong.c`:

```c
#include <linux/track_metrics.h>

/* Slow start threshold is half the congestion window (min 2) */
u32 tcp_reno_ssthresh(struct sock *sk)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    struct inet_sock *inet = inet_sk(sk);
    __be32 saddr = inet->inet_saddr;
    __be32 daddr = inet->inet_daddr;
    unsigned short sport = ntohs(inet->inet_sport);
    unsigned short dport = ntohs(inet->inet_dport);

    track("RENO", saddr, daddr, sport, dport, CWND, tp->snd_cwnd);
    return max(tp->snd_cwnd >> 1U, 2U);
}
```

Using this approach, the `track` function can be leveraged to monitor any metric from any TCP congestion control module.

> **Note:** Currently, only communications with source IP `10.0.0.1` and destination IP `10.0.0.2` are monitored. To track other IPs, update `include/linux/track_metrics.h`, then recompile and reinstall the kernel.

All metrics for monitored TCP flows are available in user space and logged in the kernel buffer.  

### 3.3 Viewing Metrics in Real Time
1. **Via terminal log:**  
```bash
dmesg --follow
```
2. **Via system log:**  
Check `/var/log/kern.log` for all kernel messages and extracted metrics.

This monitoring module is the same as used in the study:

📘 **Reference:**  
Korbi, Younes, Mohamed Faten Zhani, and John Kaippallimalil. "Congestion Control in Wi-Fi Networks—State of the Art, Performance Evaluation, and Key Research Directions." *IEEE Access*, 2024. DOI: [10.1109/ACCESS.2024.3425271](https://doi.org/10.1109/ACCESS.2024.3425271)

---

## 4. AI-Driven Congestion Control Agent

### 4.1 Design
The agent leverages LLM-based reasoning to:
- Monitor real-time TCP metrics
- Adapt congestion control dynamically
- Generate and load new CC algorithms at runtime

### 4.2 Implementation
- Prompt templates for CC decision-making
- Python-based orchestration logic
- Kernel-space integration for runtime switching
- Support for hot-reloading custom congestion control code

---

## 5. Mininet-WiFi Topology and Experiments


---

## 📊 Results
(Figures and result summaries will be added here, e.g., throughput curves, fairness indices, CWND/RTT plots.)
