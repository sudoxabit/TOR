import subprocess
import time

def change_ip(interface, new_ip):
    try:
        # Disable the network interface
        subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
        # Change the IP address
        subprocess.run(['sudo', 'ifconfig', interface, new_ip], check=True)
        # Enable the network interface
        subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error changing IP: {e}")

def create_banner(text, font='standard'):
    result = subprocess.run(['figlet', '-f', font, text], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def main(interface, base_ip, interval, count):
    # Create and print the figlet banner and additional text
    banner_text = create_banner("XABIT - TOR")
    additional_text = "telegram : nightmarewashere\nig : xabit___\n"

    print("\033[91m" + banner_text + "\033[0m")  # Red color for banner
    print("\033[92m" + additional_text + "\033[0m")  # Green color for additional text

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
    # Example usage:
    # Network interface: 'eth0'
    # Base IP address: '192.168.1.100'
    # Interval between changes: 60 seconds
    # Number of changes: 5 or '00' for infinite
    interface = 'eth0'
    base_ip = '192.168.1.100'
    interval = 60  # in seconds
    count = '00'  # or specify a number like '5'
    
    main(interface, base_ip, interval, count)