# Custom TCP Kernel Modules

<div align="center">
<div align="center">
    <img src="../resources/logo.webp" alt="FlexNGIA Logo" width="250">
</div>

[![FlexNGIA Website](https://img.shields.io/badge/🌐-flexngia.net-blue?style=flat)](https://www.flexngia.net/)

</div>


## 📑 Table of Contents

- [Part 1: High-Precision Event-Driven TCP Monitoring](#part-1-high-precision-event-driven-tcp-monitoring)
  - [📖 Introduction \& Motivation](#-introduction--motivation)
  - [1. Modifying the TCP Socket Implementation](#1-modifying-the-tcp-socket-implementation)
  - [2. The Control Interface: setsockopt](#2-the-control-interface-setsockopt)
  - [3. Creating the Tracepoint (The Hook)](#3-creating-the-tracepoint-the-hook)
  - [4. Installing the Tracepoint](#4-installing-the-tracepoint)
  - [🚀 Execution \& Reading the Data](#-execution--reading-the-data)
- [Part 2: TCP Proxy — Runtime-Switchable Congestion Control](#part-2-tcp-proxy--runtime-switchable-congestion-control)
  - [📌 Overview](#-overview)
  - [⚙️ How It Works](#️-how-it-works)
  - [🛠 Compatibility and Limitations](#-compatibility-and-limitations)
  - [🏗 Build and Install](#-build-and-install)
  - [🚀 Usage](#-usage)
  - [🔍 Verification and Troubleshooting](#-verification-and-troubleshooting)

---

Reference Publication
> This report serves as a reference for the custom TCP Monitoring module in the Linux Kernel, which was utilized in the survey paper:

"Y. Korbi, M. F. Zhani and J. Kaippallimalil, "Congestion Control in Wi-Fi Networks—State of the Art, Performance Evaluation, and Key Research Directions," in IEEE Access, vol. 12, pp. 94972-94989, 2024, doi: 10.1109/ACCESS.2024.3425271"

DOI: https://doi.org/10.1109/ACCESS.2024.3425271

If you use this implementation in your research, please cite the following paper:

```bibtex
@ARTICLE{10589468,
  author={Korbi, Younes and Zhani, Mohamed Faten and Kaippallimalil, John},
  journal={IEEE Access}, 
  title={Congestion Control in Wi-Fi Networks—State of the Art, Performance Evaluation, and Key Research Directions}, 
  year={2024},
  volume={12},
  number={},
  pages={94972-94989},
  doi={10.1109/ACCESS.2024.3425271}
}
```

---

# Part 1: High-Precision Event-Driven TCP Monitoring

## 📖 Introduction & Motivation

The Goal: To monitor TCP performance indicators (like Congestion Window, Round-Trip Time, and Throughput) in real-time with microsecond precision.

Standard Linux tools (like polling with ss or netstat) operate in "User Space" and only take periodic snapshots of the network. Because TCP reacts to network changes in milliseconds (especially during phases like Slow Start), these standard tools miss crucial, transient events. To get true, high-precision data, we must monitor the connections directly from inside the operating system's core: the Linux Kernel.

How We Achieved This (High-Level Overview):
To build this zero-latency monitoring system, we executed four main steps:

1. Modify the TCP Socket Structure: We appended new fields to the kernel's internal socket representation, including a boolean flag. When activated, it tells the kernel that this specific socket should be monitored (Selectivity).
2. Create a User/Kernel Interface: We modified setsockopt, a system call that acts as a bridge. This allows a standard User Space application (like an iperf client) to securely tell the Kernel to turn monitoring ON or OFF for its connection.
3. Create a Tracepoint (The Hook): We defined a custom, low-overhead kernel event (a tracepoint) designed to cleanly extract and format the TCP metrics without slowing down the system.
4. Install the Tracepoint: We injected this hook directly into the kernel's packet-processing path so that it fires exactly when the network state changes.

The following sections break down each of these steps, explaining both the underlying operating system concepts and the actual C code implementation.

## 1. Modifying the TCP Socket Implementation

### 🧠 Concept: The tcp_sock Structure

In Linux, every active network connection is represented by a massive data structure called struct tcp_sock. It holds the "State Machine" of the connection (how many packets are lost, the current congestion window, etc.). However, it does not permanently store the "Current Sending Rate," nor does it know if we want to monitor it.

### 💻 Implementation

We modified the header file include/linux/tcp.h to append two custom fields to this structure:

- sending_rate_mbps: To store our calculated real-time throughput.
- is_monitored: A boolean flag to ensure we only trace the connections we care about. Tracing every connection on a server would cause severe performance degradation.

```c
struct tcp_sock {
    struct inet_connection_sock inet_conn; /* Inherited Inet Socket */
    
    /* --- CUSTOM MONITORING FIELDS --- */
    u64 sending_rate_mbps;  /* Storage for calculated Throughput */
    bool is_monitored;      /* Control Flag: Is this socket being tracked? */
    /* -------------------------------- */

    /* ... existing kernel members ... */
    u16 tcp_header_len;
    /* ... */
};
```

## 2. The Control Interface: setsockopt

### 🧠 Concept: What is setsockopt?

Operating systems are divided into User Space (where your normal apps run) and Kernel Space (where the core OS and hardware drivers run). User apps cannot directly alter Kernel memory.

To allow an app to configure its network connection safely, Linux provides a system call named setsockopt (Set Socket Option). By adding a custom option to this interface, we give user-space applications a remote control to toggle the is_monitored flag inside the kernel.

### 💻 Implementation

We reserved Option 150 in net/ipv4/tcp.c. When an application calls setsockopt(fd, IPPROTO_TCP, 150, &val, sizeof(val)), the kernel executes the following logic. We also implement a "Snapshot" here: the exact moment monitoring is turned on, we log the initial state.

```c
/* Inside do_tcp_setsockopt() in net/ipv4/tcp.c */
case 150:
    /* 'val' is the integer passed from user space (1=ON, 0=OFF) */
    if (val == 1) {
        tp->is_monitored = true;
        
        /* SNAPSHOT: Log the initial state immediately */
        trace_tcp_monitor_log(sk); 
        
    } else {
        tp->is_monitored = false;
    }
    return 0;
```

## 3. Creating the Tracepoint (The Hook)

### 🧠 Concept: What is a Tracepoint?

If you want to print a message in standard C, you use printf. In the kernel, developers historically used printk. However, writing text to a log buffer is extremely slow. If we used printk for every network packet, the network speed would collapse.

A Tracepoint is a modern, static hook tied to the Linux ftrace subsystem.

When disabled, it acts as a NOP (No Operation) instruction, taking 0 CPU cycles.

When enabled, it securely packs binary data (integers, IP addresses) into a ring buffer incredibly fast, to be read by the user later.

### 💻 Implementation

We defined a new trace event called tcp_monitor_log in include/trace/events/tcp.h. This defines exactly what data we are extracting from the socket.

```c
TRACE_EVENT(tcp_monitor_log,
    TP_PROTO(struct sock *sk),
    TP_ARGS(sk),
    TP_STRUCT__entry(
        /* Identity */
        __field(u32, saddr)
        __field(u16, sport)
        __field(u32, daddr)
        __field(u16, dport)
        
        /* Metrics */
        __field(u64, sending_rate_mbps)
        __field(u32, srtt_ms)
        __field(u32, cwnd)
    ),
    TP_fast_assign(
        struct tcp_sock *tp = tcp_sk(sk);
        struct inet_sock *inet = inet_sk(sk);
        
        /* Extract Identity and Metrics */
        __entry->saddr = inet->inet_saddr;
        __entry->sport = ntohs(inet->inet_sport);
        __entry->sending_rate_mbps = tp->sending_rate_mbps;
        __entry->cwnd = tp->snd_cwnd;
        __entry->srtt_ms = (tp->srtt_us >> 3) / 1000;
    ),
    TP_printk("id=%pI4:%u->%pI4:%u srate=%llu Mbps cwnd=%u",
              &__entry->saddr, __entry->sport, &__entry->daddr, 
              __entry->dport, __entry->sending_rate_mbps, __entry->cwnd)
);
```

## 4. Installing the Tracepoint

### 🧠 Concept: Where do we put the hook?

A hook is only useful if it is placed in the right location. TCP dynamically updates its metrics (like Congestion Window) when it receives an Acknowledgement (ACK) from the receiver.

Therefore, we place our tracepoint at the very end of the tcp_ack() function. This ensures we capture the Final Verdict—the exact state of the connection immediately after the kernel has processed the ACK and updated its metrics. Additionally, we calculate the real-time throughput right before the hook fires.

### 💻 Implementation

First, we calculate the rate in tcp_rate_gen() (located in net/ipv4/tcp_rate.c):

```c
/* Calculate Sending Rate */
if (tp->is_monitored && rs->snd_interval_us > 0) {
    u64 bits_sent = (u64)rs->delivered * tp->mss_cache * 8;
    tp->sending_rate_mbps = div64_u64(bits_sent, rs->snd_interval_us);
}
```

Next, we trigger the event inside tcp_ack() (located in net/ipv4/tcp_input.c):

```c
static int tcp_ack(struct sock *sk, const struct sk_buff *skb, int flag)
{
    /* ... [Standard ACK processing logic] ... */
    tcp_rate_gen(sk, ...);     /* Rate is calculated here */
    tcp_cong_control(sk, ...); /* CWND is updated here */

    /* --- EVENT TRIGGER --- */
    if (tp->is_monitored) {
        /* Fire the tracepoint with the fresh data */
        trace_tcp_monitor_log(sk);
    }
    /* --------------------- */

    return 1;
}
```

## 🚀 Execution & Reading the Data

To use this system, you must instruct the Linux ftrace subsystem to arm the tracepoint. The order of operations is critical to avoid system noise.

### 1. Arming the Tracepoint (Run as Root)

```bash
TRACE_DIR="/sys/kernel/debug/tracing"

# 1. PAUSE: Stop recording globally to perform maintenance
echo 0 > $TRACE_DIR/tracing_on

# 2. CLEAR: Wipe the ring buffer
echo > $TRACE_DIR/trace

# 3. ENABLE: Activate our specific custom TCP event
echo 1 > $TRACE_DIR/events/tcp/tcp_monitor_log/enable

# 4. START: Globally arm the tracing system
echo 1 > $TRACE_DIR/tracing_on
```

### 2. Reading the Real-Time Stream

Once an application (like an iperf client) activates option 150 via setsockopt, you can view the high-precision logs streaming in real-time:

```bash
cat /sys/kernel/debug/tracing/trace_pipe
```

Sample Output:

```text
# Initial Snapshot (Triggered by setsockopt)
tcp_monitor: id=10.0.0.1->10.0.0.2 srate=0 Mbps cwnd=10

# Traffic Begins (Triggered by tcp_ack)
tcp_monitor: id=10.0.0.1->10.0.0.2 srate=5 Mbps cwnd=11
tcp_monitor: id=10.0.0.1->10.0.0.2 srate=12 Mbps cwnd=12
tcp_monitor: id=10.0.0.1->10.0.0.2 srate=48 Mbps cwnd=24
```

---

# Part 2: TCP Proxy — Runtime-Switchable Congestion Control

A minimal TCP congestion control (CC) proxy that delegates all congestion behavior to another CC algorithm chosen at runtime. The proxy itself implements no control logic—it simply forwards the kernel's CC callbacks to the selected delegate.

---

## 📌 Overview

- **Purpose:** Enables rapid switching between congestion control algorithms at runtime for experimentation, or orchestrated trials—without requiring a kernel reboot or recompilation.
- **Name:** `proxy` (as a TCP CC algorithm).
- **Default Delegate:** `reno` (modifiable at runtime).
- **Forwarded Callbacks:** `ssthresh()`, `cong_avoid()`, `undo_cwnd()`.
- **Runtime Control:** `/sys/module/tcp_proxy/parameters/delegate_cc`.

> 💡 Use `proxy` as the system-wide CC algorithm and switch the delegate dynamically to compare CC algorithms. The `tcp_proxy` module is perceived by the kernel as a standard congestion control module. It should be set as the active congestion control algorithm in the Linux system by configuring `proxy` as the default congestion control. The kernel and the system remain unaware of the delegation mechanism itself, as all delegation is handled internally.

---

## ⚙️ How It Works

- **Delegation Model:**  
  The module exposes a parameter, `delegate_cc`, which holds the name of the target CC algorithm (e.g., `reno`, `llm_cc_v0`). On load or when the parameter changes, the proxy resolves the delegate using `tcp_ca_find()`, pins its module with `try_module_get()`, and forwards CC callbacks to the delegate.

- **Forwarded Callbacks:**  
  - `ssthresh()` → Delegate's slow-start threshold function.  
  - `cong_avoid()` → Delegate's congestion avoidance function.  
  - `undo_cwnd()` → Delegate's cwnd undo function.

- **Module Parameter:**  
  - **Name:** `delegate_cc`.  
  - **Path:** `/sys/module/tcp_proxy/parameters/delegate_cc`.  
  - **Read/Write:** Yes (requires root privileges).  
  - **Default Value:** `reno`.

- **Lifecycle:**  
  On load, the `proxy` registers as a CC algorithm, resolves the default delegate, and pins it. On unload, it releases the delegate's module reference and unregisters itself.

---

## 🛠 Compatibility and Limitations

- **Delegate Requirements:**  
  The delegate must implement the following callbacks:
  - `ssthresh()`.
  - `cong_avoid()`.
  - `undo_cwnd()`.

- **Compatible With:**  
  Traditional loss-based CC algorithms such as `reno`.

- **Not Suitable For:**  
  Algorithms like **BBR**, which use `cong_control()` instead of `cong_avoid()`.

---

## 🏗 Build and Install

### In-Tree Integration

1. **Place the Source File:**  
   Copy the source file to `net/ipv4/tcp_proxy.c`.

2. **Update Kbuild (`net/ipv4/Makefile`):**  
   - Open: `net/ipv4/Makefile`.  
   - Add this line after other TCP congestion modules:  
     ```make
     obj-$(CONFIG_TCP_CONG_PROXY) += tcp_proxy.o
     ```

3. **Add Kconfig Entry (`net/ipv4/Kconfig`):**  
   - Open: `net/ipv4/Kconfig`.  
   - Add this at the end (below other CC configs):  
     ```make
     config TCP_CONG_PROXY
           tristate "TCP Proxy congestion control"
           default y
           help
             A TCP congestion control module that delegates control to another algorithm.
             You can select the delegate at runtime via /sys/module/tcp_proxy/parameters/delegate_cc.
     ```

4. **Enable in `menuconfig`:**  
   - From the root of the kernel source directory, run:  
     ```bash
     make menuconfig
     ```
   - Navigate to:  
     `Networking support → Networking options → TCP: advanced congestion control`.
   - Enable the option:  
     `[M] TCP Proxy congestion control`.

5. **Build and Install:**
   ```bash
   make -j"$(nproc)"
   sudo make modules_install
   sudo make install
   sudo reboot
   ```

---

## 🚀 Usage

### Load the Module

- **With Default Delegate (`reno`):**
  ```bash
  sudo modprobe tcp_proxy
  ```

- **With a Specific Delegate:**
  ```bash
  sudo modprobe tcp_proxy delegate_cc=reno
  ```

### Set Proxy as the Active CC Algorithm

```bash
sudo sysctl -w net.ipv4.tcp_congestion_control=proxy
```

### Verify the Configuration

- **Available CC Algorithms:**
  ```bash
  sysctl net.ipv4.tcp_available_congestion_control
  ```

- **Active CC Algorithm:**
  ```bash
  cat /proc/sys/net/ipv4/tcp_congestion_control
  ```

### Switch Delegate at Runtime

- **Switch to a Custom CC Algorithm:**
  ```bash
  echo -n "llm_cc_v0" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc
  ```

- **Switch to `reno`:**
  ```bash
  echo -n "reno" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc
  ```

### Unload the Module

```bash
sudo modprobe -r tcp_proxy
```

---

## 🔍 Verification and Troubleshooting

- **Check Available CC Algorithms:**
  ```bash
  sysctl net.ipv4.tcp_available_congestion_control
  ```

- **Confirm Active CC Algorithm:**
  ```bash
  cat /proc/sys/net/ipv4/tcp_congestion_control
  ```

- **Read Current Delegate:**
  ```bash
  cat /sys/module/tcp_proxy/parameters/delegate_cc
  ```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## 📧 Contact

For questions or collaborations, please contact:  
[mfzhani@flexNGIA.net](mailto:mfzhani@flexNGIA.net)  
Website: [www.FlexNGIA.net](https://www.flexngia.net/)