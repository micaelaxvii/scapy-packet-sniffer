## Packet Sniffer

### Requirements

- Python 3.9 or later (recommended)
- Scapy
- A supported network interface


### Installation
##### 1. Clone the repository
```bash
git clone https://github.com/micaelaxvii/scapy-packet-sniffer.git
```

##### 2. Install dependencies
```bash
pip install scapy
```
Depending on your operating system, you may also need to install packet-capture support such as Npcap on Windows or libpcap on Linux.


### Command-Line Arguments

- `-n`, `--network_interface`: Network interface to monitor (**required**).
- `-d`, `--detailed_view`: Display detailed packet information.
- `-l`, `--logging`: Save captured packets to a PCAP file.
- `-h`, `--help`: Show manual.


### Example usage
```bash
python packet-sniffer.py -n eth0 -l -d
```
