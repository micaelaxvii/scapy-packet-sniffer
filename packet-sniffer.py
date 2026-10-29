from scapy.all import AsyncSniffer, wrpcap
import argparse
import datetime
import time
import os


def user_input():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--network_interface', type=str, help="Network interface to monitor.", required=True)
    parser.add_argument('-l', '--logging', action='store_true', help="[Optional] Enable logging to a .pcap file.")
    parser.add_argument('-d', '--detailed_view', action='store_true', help="[Optional] Enable detailed view of packets.")

    args = parser.parse_args()
    packet_capture(args)


def show_packet(packet, args):
    timestamp = datetime.datetime.fromtimestamp(float(packet.time))

    if args.detailed_view:
        print("Timestamp:", timestamp, "Size:", len(packet), "bytes")
        packet.show()

    else:
        print(timestamp, packet.summary(), len(packet), "bytes")


def packet_capture(args):

    print("Starting capture... Press ENTER to stop capture. (Ctrl + C to force stop.)")
    time.sleep(2)
    sniffer = AsyncSniffer(iface=args.network_interface, prn=lambda packet: show_packet(packet, args), store=True)
    
    try:
        sniffer.start()
        print(f"Capturing packets on {args.network_interface}...")
        input("Press ENTER to stop capturing and continue...\n")
        
    except KeyboardInterrupt:
        print("\nForce stopping capture...")

    finally:
        if sniffer.running:
            capture = sniffer.stop()
            print(f"Capture stopped. Total packets: {len(capture)}")

        else:
            capture = sniffer.results
            print(f"\nCapture stopped. Total packets: {len(capture)}")
            
        if args.logging:
            capture_logging(capture)


def capture_logging(capture):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    captures_dir = os.path.join(current_dir, "captures")
    os.makedirs(captures_dir, exist_ok=True)

    print("\nSaving as a .pcap file (Q to quit)")

    while True:
        filename = input("Name of the file: ").strip()

        if filename.upper() == "Q":
            print("Program terminated.")
            return False

        if not filename:
            print("Filename cannot be empty.")
            continue

        pcap_file = os.path.join(captures_dir, f"{filename}.pcap")

        if not os.path.exists(pcap_file):
            wrpcap(pcap_file, capture)
            print(f"Saved in {pcap_file}")
            return False

        else:
            while True:
                c = input("File already exists. Overwrite it (O) or choose a new filename (N)? (Q to quit): ").strip().upper()

                if c == "O":
                    wrpcap(pcap_file, capture)
                    print(f"Saved in {pcap_file}")
                    return False

                elif c == "N":
                    break

                elif c == "Q":
                    print("Program terminated.")
                    return False

                else:
                    print("Invalid choice. Enter O, N, or Q.")  


if __name__ == "__main__":
    user_input()
