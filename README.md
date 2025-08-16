# SDN Performance Analysis

This project uses Mininet to simulate SDN topologies and analyze network performance using Ryu controller and D-ITG traffic generator.

## Overview

Software Defined Networking (SDN) performance analysis framework that provides comprehensive testing and evaluation of network topologies. The project combines Mininet's network simulation capabilities with Ryu's SDN controller framework and D-ITG's traffic generation tools.

## Technologies Used

- **Mininet**: Network emulator for creating virtual networks
- **Ryu**: SDN framework for topology management and control
- **D-ITG**: Distributed Internet Traffic Generator for network flows
- **Python**: Custom topology and controller implementation

## Quick Start

### Prerequisites

```bash
sudo apt-get install mininet python3-ryu python3-pip
```

Install D-ITG following the official documentation.

### Usage

**Note**: The controller application and Mininet topology must be running on separate terminals.

#### Controller

Start the controller by executing the `run_controller.sh` script:

```bash
bash run_controller.sh [-f <controller-file>]
```

- Default controller: `controller1.py` (located in `controllers` directory)
- Implements shortest-path routing with equal link weights

#### Mininet Topology

Run the topology test using the `test_topo.sh` script:

```bash
bash test_topo.sh [-f <topology-file>] [--start <lambda-rate>] [--stop <lambda-rate>] [--step <lambda-rate>]
```

**Default parameters:**
- Topology: `topology2.py` (located in `topologies` directory)
- Start: 2 packets/second
- Stop: 200 packets/second  
- Step: 2 packets/second

#### Generate Performance Plots

Create graphs and analysis reports:

```bash
bash plot_graphs.sh [-f <topology-file>] [--start <lambda-rate>] [--stop <lambda-rate>] [--step <lambda-rate>]
```

**Default parameters:**
- Same as topology testing
- Generates plots for the specified topology and lambda rate range

## Network Topologies

### Topology v1

**Configuration:**
- 4 hosts (H₁, H₂, H₃, H₄)
- 3 switches (S₁, S₂, S₃)
- Link properties: 20 Mbps bandwidth, 20ms delay, max queue size = 10

**Traffic flows (unidirectional):**
- H₁ → H₃
- H₁ → H₄  
- H₂ → H₃
- H₂ → H₄

**Test parameters:**
- Lambda rate: 2-200 packets/second (Poisson distribution)
- Observation time: 20 seconds per measurement
- Protocol: UDP packets

## Performance Metrics

The framework measures and analyzes:

- **End-to-end delay**: Packet transmission times across network paths
- **Packet loss**: Network reliability under varying load conditions
- **Bandwidth utilization**: Link capacity usage monitoring
- **Throughput**: Per-flow and aggregate network performance

## Controller Features

The SDN controller (`controller1.py`) provides:

- Shortest-path routing algorithm
- Dynamic flow table management
- OpenFlow 1.3 compatibility
- Automatic topology discovery
- Multi-path support capabilities

## Data Collection

Performance data is extracted using:
- **Ryu**: Bandwidth utilization statistics
- **D-ITG**: End-to-end delay and packet loss measurements
- **Custom scripts**: Automated data processing and visualization

## Output

The analysis generates:
- Performance graphs and charts
- Statistical analysis reports
- Network utilization data
- Comparative topology studies

## Research Findings and Analysis

This project conducted comprehensive performance analysis comparing two network topologies under varying traffic conditions. The research provides valuable insights into SDN behavior, bottleneck identification, and network optimization strategies.

### Topology v1 Analysis

**Network Structure:**
- Linear topology: H₁-S₁-S₂-S₃ with H₂ connected to S₂, H₃ and H₄ connected to S₃
- Traffic flows: (H₁→H₃), (H₁→H₄), (H₂→H₃), (H₂→H₄)
- All flows follow shortest path routing with equal link weights

**Key Findings:**

**Bottleneck Identification:**
- Link (S₂, S₃) identified as primary bottleneck, carrying 4 distinct flows vs. 2 flows on other links
- Bottleneck saturation occurs at **60 packets/second** lambda rate
- Link utilization grows twice as fast for (S₂, S₃) compared to other links

**Path-Length Impact on Latency:**
- H₁ packets experience **33% longer delay** than H₂ packets due to extended path length
- H₁ path: 4 hops (H₁→S₁→S₂→S₃→destination)
- H₂ path: 3 hops (H₂→S₂→S₃→destination)

**Packet Loss Behavior:**
- Linear packet drop growth begins at **lambda rates > 100 packets/second**
- Links (H₃, S₃) and (H₄, S₃) reach maximum utilization slower due to upstream packet drops

### Topology v2 Analysis

**Network Enhancement:**
- Added direct link (S₁, S₃) to eliminate bottleneck from Topology v1
- Maintains same link characteristics (20 Mbps, 20ms delay, queue size 10)

**Routing Optimization:**
- New shortest paths: H₁ traffic now uses direct S₁→S₃ link
- Eliminated bottleneck: maximum 2 flows per link across entire topology
- Link (S₁, S₂) becomes unused in optimal routing

**Performance Improvements:**

**Enhanced Throughput:**
- Bottleneck saturation improved to **120 packets/second** (2x improvement)
- All active links show uniform, linear utilization growth
- No preferential bottleneck formation

**Latency Equalization:**
- **Equal latency** for all packet flows (H₁ and H₂ packets)
- Path length normalization: all flows now traverse 3 hops

**Packet Loss Reduction:**
- Negligible packet drop in standard testing range (2-200 pkt/s)
- Extended testing shows packet drop threshold at **240 packets/second**
- 2.4x improvement in sustainable traffic load

### Comparative Performance Summary

| Metric | Topology v1 | Topology v2 | Improvement |
|--------|-------------|-------------|-------------|
| Bottleneck Saturation | 60 pkt/s | 120 pkt/s | **2x** |
| Packet Drop Threshold | 100 pkt/s | 240 pkt/s | **2.4x** |
| H₁ vs H₂ Latency | 33% difference | Equal | **Eliminated** |
| Max Flows per Link | 4 | 2 | **50% reduction** |

### Technical Insights

**Network Design Principles:**
- Single additional link can eliminate bottlenecks and double network capacity
- Shortest-path routing automatically exploits topology improvements
- Equal path lengths critical for latency consistency

**Traffic Engineering Observations:**
- Flow distribution analysis enables bottleneck prediction
- Link cost calculation methodology validated through empirical testing
- Poisson traffic distribution provides realistic performance evaluation

**SDN Controller Validation:**
- Shortest-path algorithm correctly adapts to topology changes
- Dynamic flow table management handles route optimization automatically

- OpenFlow integration enables real-time performance monitoring
