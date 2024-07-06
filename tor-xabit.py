import subprocess
import time

def change_ip(interface, new_ip):
    try:
        # Bring the interface down
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
        # Assign the new IP address
        subprocess.run(['sudo', 'ip', 'addr', 'add', new_ip + '/24', 'dev', interface], check=True)
        # Bring the interface up
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
        # Remove the old IP address (assuming the base IP is on the same subnet)
        subprocess.run(['sudo', 'ip', 'addr', 'flush', 'dev', interface], check=True)
        print(f"IP changed to {new_ip} on {interface}")
    except subprocess.CalledProcessError as e:
        print(f"Error changing IP: {e}")

def create_banner(text, font='standard'):
    result = subprocess.run(['figlet', '-f', font, text], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def main(interface, base_ip, interval, count):
    # Create and print the figlet banner and additional text
    banner_text = create_banner("XABIT - TOR")
    additional_text = "telegram : nightmarewashere\nig : xabit___\n"
    instructions = "Number of IP changes (default infinite): '00'\nChange interval in seconds (default 30): '30'\n"

    print("\033[91m" + banner_text + "\033[0m")  # Red color for banner
    print("\033[92m" + additional_text + "\033[0m")  # Green color for additional text
    print("\033[93m" + instructions + "\033[0m")  # Yellow color for instructions

    i = 0
    while count == "00" or i < int(count):
        # Generate the new IP address (incrementing the last octet)
        new_ip = base_ip.split('.')
        new_ip[-1] = str((int(new_ip[-1]) + i) % 255)  # Loop back after 255
        new_ip = '.'.join(new_ip)
        
        print(f"Changing IP to {new_ip}")
        change_ip(interface, new_ip)
        
        # Wait for the given interval before changing the IP again
        time.sleep(interval)
        
        i += 1

if __name__ == "__main__":
    # Input from user for interface, base IP, interval, and count
    interface = input("Enter network interface (e.g., 'eth0'): ")
    base_ip = input("Enter base IP address (e.g., '192.168.1.100'): ")
    interval = input("Enter interval in seconds (default 30): ") or "30"
    count = input("Enter number of IP changes (default infinite, enter '00' for infinite): ") or "00"

    # Convert interval to integer
    interval = int(interval)
    
    main(interface, base_ip, interval, count)