<div align="center">

## FlexNGIA 2.0: Redesigning the Internet with Agentic AI <br> Protocols, Services, and Traffic Engineering Designed, Deployed, <span style="white-space: nowrap;">and Managed</span> by AI

**Mohamed Faten Zhani**<sup>1,2</sup>, **Younes Korbi**<sup>1,2</sup> and **Yamen Mkadem**<sup>1,2</sup>  
<sup>1</sup>FlexNGIA, Tunisia 
</br><sup>2</sup>ISITCom, University of Sousse, Tunisia  
📧 {mfzhani, ykorbi, ymkadem}@FlexNGIA.net

[![Paper](https://img.shields.io/badge/📄-Paper-yellow?style=flat)](https://arxiv.org/abs/2509.02124)
[![FlexNGIA Website](https://img.shields.io/badge/🌐-flexngia.net-blue?style=flat)](https://www.flexngia.net/)

</div>

<div align="center">
    <img src="./resources/logo.webp" alt="FlexNGIA Logo" width="250">
</div>


## 📖 Overview

This repository contains the official implementation and experimental code for the paper:  
**"FlexNGIA 2.0: Redesigning the Internet with Agentic AI Protocols, Services, and Traffic Engineering Designed, Deployed, and Managed by AI"**

The project demonstrates an Agentic AI-driven Internet architecture where LLM-based AI agents autonomously design, implement, and manage:
- **Custom Congestion Control schemes**
- **Service Function Chains (SFCs)**
- **Network protocols**
- **Resource allocation strategies**

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

This section covers the design, implementation, and experiments for the **AI-Driven Congestion Control Agent**.  
It combines kernel-side extensions with LLM-based decision logic to dynamically design, select, and deploy congestion control (CC) schemes.

### 1.1 Kernel Support

To enable AI-driven CC, the Linux kernel is extended with:

- **Custom TCP Proxy CC Module**  
  A minimal congestion control algorithm (`proxy`) that delegates its logic to another CC algorithm at runtime. This enables seamless switching between algorithms without rebooting or recompilation.

- **TCP Metrics Monitoring**  
  Extended instrumentation inside the TCP stack to extract key transport-layer metrics in real time:
  - Congestion Window (CWND)  
  - Round-Trip Time (RTT)  
  - Losses and retransmissions  
  - Sending rate and throughput  

👉 Detailed kernel configuration and installation instructions are available in the [congestion-control-agent README](./congestion-control-agent/README.md).

### 1.2 AI-Driven Congestion Control Agent

The Congestion Control Agent leverages LLM reasoning to monitor network state and autonomously adapt transport behavior:

- Agent architecture and system prompts  
- Dynamic CC scheme selection and parameter tuning  
- Runtime code generation for new congestion control algorithms  
- Integration with the Linux kernel TCP stack  

👉 See the [congestion-control-agent README](./congestion-control-agent/README.md) for implementation details, agent configuration, and usage.

### 1.3 Mininet-WiFi Topology and Experiments

Experiments are conducted in **Mininet-WiFi**, where custom CC schemes are evaluated against standard algorithms under diverse conditions (e.g., wireless, lossy links).  
This section includes:
- Testbed setup and network topology  
- Experiment scripts and automation  
- Performance evaluation and visualization of results  

👉 See the [congestion-control-agent](./congestion-control-agent/) directory for implementation details, experiment code, and usage examples.

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