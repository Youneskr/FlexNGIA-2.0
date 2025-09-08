<style>
  h1, h2 {
    border-bottom: none !important;
  }
</style>

<div align="center">

<h1>FlexNGIA 2.0: Redesigning the Internet with Agentic AI</h1> 
<h2>Protocols, Services, and Traffic Engineering Designed, Deployed, and Managed by AI</h2> 

**Mohamed Faten Zhani**<sup>1,2</sup>, **Younes Korbi**<sup>1,2</sup> and **Yamen Mkadem**<sup>1,2</sup>  
<sup>1</sup>FlexNGIA, Tunisia 
</br><sup>2</sup>ISITCom, University of Sousse, Tunisia  
📧 {mfzhani, ykorbi, ymkadem}@FlexNGIA.net

[![Paper](https://img.shields.io/badge/📄-Paper-yellow?style=flat)](https://arxiv.org/abs/2509.02124)
[![FlexNGIA Website](https://img.shields.io/badge/🌐-flexngia.net-blue?style=flat)](https://www.flexngia.net/)

</div>

<div align="center">
    <img src="./resources/logo.webp" alt="FlexNGIA Logo" width="300">
</div>

---

## 📖 Overview

This repository contains the official implementation and experimental code for the paper:  
**"FlexNGIA 2.0: Redesigning the Internet with Agentic AI Protocols, Services, and Traffic Engineering Designed, Deployed, and Managed by AI"**

The project demonstrates an Agentic AI-driven Internet architecture where LLM-based AI agents autonomously design, implement, and manage:
- **Custom Congestion Control schemes** 🚦
- **Service Function Chains (SFCs)** ⛓️  
- **Network protocols** 📡
- **Resource allocation strategies** 📊

This repository serves as both the codebase and comprehensive documentation for reproducing all experiments and results presented in the paper.

---

## 📚 Table of Contents

- [Congestion Control Agent](#1-congestion-control-agent)
- [SFC & Protocol Agent](#2-sfc--protocol-agent)
- [Getting Started](#-getting-started)
- [Citation](#-citation)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 1. Congestion Control Agent

This section includes the implementation and experiments for the AI-Driven Congestion Control Agent, including the required kernel-side implementations for custom TCP functionality.

### 1.1 Kernel Installation and Configuration

This subsection focuses on kernel-side implementations including kernel source installation, configuration, building, and module insertion. The final custom kernel will include TCP metrics monitoring and a TCP proxy module for seamless Congestion Control scheme switching.

#### Prerequisites

Install required development tools:
```bash
sudo apt-get install build-essential libncurses-dev bison flex libssl-dev libelf-dev
```

Install `dwarves` package (required for modern kernel builds):
```bash
sudo apt install dwarves
```

#### Kernel Source Installation

This customized Linux kernel version 5.13.12 (based on Google's BBR kernel) includes additional capabilities:

- **TCP Metric Monitoring**: A module integrated into TCP Congestion Control modules that extracts real-time TCP metrics transparently, including:
  - Congestion Window (CWND)
  - Round-Trip Time (RTT)
  - TCP rate
  - Losses and retransmissions
  - Extensible to capture additional TCP-related metrics

- **TCP Proxy**: A minimal TCP congestion control proxy that:
  - Delegates all congestion behavior to another CC algorithm chosen at runtime
  - Implements no control logic—forwards kernel's CC callbacks to selected delegate
  - Enables rapid switching between congestion control algorithms at runtime
  - **Name**: `proxy` (as a TCP CC algorithm)
  - **Default Delegate**: `reno` (modifiable at runtime)
  - **Forwarded Callbacks**: `ssthresh()`, `cong_avoid()`, `undo_cwnd()`
  - **Runtime Control**: `/sys/module/tcp_proxy/parameters/delegate_cc`

#### How TCP Proxy Works

- **Delegation Model:**  
  The module exposes a parameter, `delegate_cc`, which holds the name of the target CC algorithm (e.g., `reno`, `llm_cc_v0`). On load or when the parameter changes, the proxy resolves the delegate using `tcp_ca_find()`, pins its module with `try_module_get()`, and forwards CC callbacks to the delegate.

- **Forwarded Callbacks:**  
  - `ssthresh()` → Delegate's slow-start threshold function  
  - `cong_avoid()` → Delegate's congestion avoidance function  
  - `undo_cwnd()` → Delegate's cwnd undo function

- **Module Parameter:**  
  - **Name:** `delegate_cc`  
  - **Path:** `/sys/module/tcp_proxy/parameters/delegate_cc`  
  - **Read/Write:** Yes (requires root privileges)  
  - **Default Value:** `reno`

- **Lifecycle:**  
  On load, the `proxy` registers as a CC algorithm, resolves the default delegate, and pins it. On unload, it releases the delegate's module reference and unregisters itself.

#### TCP Proxy Compatibility and Limitations

- **Delegate Requirements:**  
  The delegate must implement the following callbacks:
  - `ssthresh()`
  - `cong_avoid()`
  - `undo_cwnd()`

- **Compatible With:**  
  Traditional loss-based CC algorithms such as `reno`

- **Not Suitable For:**  
  Algorithms like **BBR**, which use `cong_control()` instead of `cong_avoid()`

> 💡 Set the congestion control `proxy` as the system-wide CC algorithm and switch the delegate dynamically to compare CC algorithms. The `tcp_proxy` module is perceived by the kernel as a standard congestion control module.

#### Download and Setup

Download the kernel source: 
```bash
wget https://tinyurl.com/zsmvdabt
unzip kernel_5.13.12.zip
cd kernel_5.13.12
```

#### First-Time Compilation Setup

Execute the following commands in the terminal:
```bash
CONFIG_SYSTEM_TRUSTED_KEYS=""
scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
scripts/config --disable SYSTEM_REVOCATION_KEYS
```

#### Kernel Configuration

Copy your current kernel configuration:
```bash
cp -v /boot/config-$(uname -r) .config
```

**Enable TCP Proxy in `menuconfig`:**  
```bash
make menuconfig
```
Navigate to:  
`Networking support → Networking options → TCP: advanced congestion control`  
Enable the option:  
`[M] TCP Proxy congestion control`

#### Compile and Install the Kernel

```bash
# Compile the entire kernel
make -j $(nproc)

# Install the Linux Kernel Modules
sudo make modules_install

# Install the Linux Kernel
sudo make install

# Reboot to use the new kernel
sudo reboot
```

#### Usage: Setting and Activating TCP Proxy as Default Congestion Control

**Load the Module:**
```bash
# With Default Delegate (reno)
sudo modprobe tcp_proxy

# With Specific Delegate
sudo modprobe tcp_proxy delegate_cc=reno
```

**Set Proxy as Active CC Algorithm:**
```bash
sudo sysctl -w net.ipv4.tcp_congestion_control=proxy
```

**Verify Configuration:**
```bash
# Available CC Algorithms
sysctl net.ipv4.tcp_available_congestion_control

# Active CC Algorithm
cat /proc/sys/net/ipv4/tcp_congestion_control
```

**Switch Delegate at Runtime:**
```bash
# Switch to custom CC algorithm
echo -n "llm_cc_v0" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc

# Switch to reno
echo -n "reno" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc
```

**Unload the Module:**
```bash
sudo modprobe -r tcp_proxy
```

#### Verification and Troubleshooting

```bash
# Check available CC algorithms
sysctl net.ipv4.tcp_available_congestion_control

# Confirm active CC algorithm
cat /proc/sys/net/ipv4/tcp_congestion_control

# Read current delegate
cat /sys/module/tcp_proxy/parameters/delegate_cc
```

### 1.2 AI-Driven Congestion Control Agent

This subsection includes the implementation and experiments for the AI-Driven Congestion Control Agent:

- Agent architecture and prompt design
- Dynamic CC scheme selection and code generation
- Integration with the Linux kernel TCP stack
- Mininet-WiFi topology and experiment scripts
- Performance results and visualizations

See the [`congestion-control-agent/`](./congestion-control-agent/) directory for details.

---

## 2. SFC & Protocol Agent

This section includes the implementation and experiments for the AI-Driven SFC & Protocol Agent:

- Agent architecture and prompt design
- Dynamic SFC and protocol generation
- Custom header design and UDP-based protocol implementation
- Network Function Catalog and custom NF code generation
- Mininet-WiFi topology and experiment scripts
- Performance comparison with TCP and UDP

See the [`sfc-protocol-agent/`](./sfc-protocol-agent/) directory for details.

---

## 🚀 Getting Started

### Prerequisites

- Ubuntu 18.04+
- Mininet-WiFi
- Python 3.8+

**Highly Recommended:** Download the Mininet-WiFi VM image that has Mininet-WiFi and Python pre-installed:  
[`Download Link`](https://drive.google.com/file/d/1R8n4thPwV2krFa6WNP0Eh05ZHZEdhw4W/view)  
Login: `wifi`  
Password: `wifi`

### Installation

Clone the repository:

```bash
git clone https://github.com/Youneskr/FlexNGIA-2.0.git
cd FlexNGIA-2.0
```

Follow the instructions in each section's `README.md` to set up the kernel, agents, and experiments.

---

## 📫 Citation

If you use this code or refer to this work, please cite the original paper:

```bibtex
@misc{zhani2025flexngia20redesigninginternet,
      title={FlexNGIA 2.0: Redesigning the Internet with Agentic AI -- Protocols, Services, and Traffic Engineering Designed, Deployed, and Managed by AI}, 
      author={Mohamed Faten Zhani and Younes Korbi and Yamen Mkadem},
      year={2025},
      eprint={2509.02124},
      archivePrefix={arXiv},
      primaryClass={cs.NI},
      url={https://arxiv.org/abs/2509.02124}, 
}
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## 📧 Contact

For questions or collaborations, please contact:  
[mfzhani@flexNGIA.net](mailto:mfzhani@flexNGIA.net)  
Website: [flexngia.net](https://www.flexngia.net/)