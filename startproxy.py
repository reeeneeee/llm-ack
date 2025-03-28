import os
import subprocess
import sys
import platform

def check_brew_installed():
    try:
        subprocess.run(["which", "brew"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_mitmproxy():
    if not check_brew_installed():
        print("Homebrew is not installed. Please install Homebrew first:")
        print("Visit https://brew.sh/ for installation instructions")
        sys.exit(1)
    
    print("Installing mitmproxy using Homebrew...")
    try:
        subprocess.run(["brew", "install", "mitmproxy"], check=True)
        print("mitmproxy installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing mitmproxy: {e}")
        sys.exit(1)

def setup_proxy():
    # Set up the proxy server
    try:
        subprocess.run(["networksetup", "-setwebproxy", "Wi-Fi", "127.0.0.1", "8080"], check=True)
        subprocess.run(["networksetup", "-setsecurewebproxy", "Wi-Fi", "127.0.0.1", "8080"], check=True)
        print("Proxy settings configured successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up proxy: {e}")
        sys.exit(1)

def install_cert():
    # Install mitmproxy certificate
    cert_path = os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.pem")
    if not os.path.exists(cert_path):
        print("Certificate not found. Please run mitmdump at least once to generate it.")
        sys.exit(1)
    
    try:
        subprocess.run([
            'sudo', 'security', 'add-trusted-cert', '-d', '-p', 'ssl', '-p', 'basic',
            '-k', '/Library/Keychains/System.keychain', cert_path
        ], check=True)
        print("Certificate installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing certificate: {e}")
        sys.exit(1)

def generate_cert():
    print("Generating mitmproxy certificate...")
    try:
        # Run mitmdump to generate the certificate
        process = subprocess.Popen(["mitmdump", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        print("Certificate generated successfully")
    except Exception as e:
        print(f"Error generating certificate: {e}")
        sys.exit(1)

def main():
    # Check if we're on macOS
    if platform.system() != "Darwin":
        print("This script is currently only supported on macOS")
        sys.exit(1)

    # First, ensure mitmproxy is installed
    try:
        subprocess.run(["which", "mitmdump"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("mitmproxy is not installed.")
        response = input("Would you like to install it now? (y/n): ")
        if response.lower() == 'y':
            install_mitmproxy()
        else:
            print("Please install mitmproxy manually using: brew install mitmproxy")
            sys.exit(1)

    # Generate certificate if it doesn't exist
    cert_path = os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.pem")
    if not os.path.exists(cert_path):
        generate_cert()

    # Set up proxy and install certificate
    setup_proxy()
    install_cert()

    print("\nStarting mitmdump...") # note: we use mitmdump because it has no tty requirement
    print("Press Ctrl+C to stop the proxy")
    
    # Run mitmdump with the request modificationscript
    try:
        subprocess.run(["mitmdump", "-s", "llmack.py"])
    except KeyboardInterrupt:
        print("\nStopping proxy...")
        # Clean up proxy settings
        subprocess.run(["networksetup", "-setwebproxystate", "Wi-Fi", "off"])
        subprocess.run(["networksetup", "-setsecurewebproxystate", "Wi-Fi", "off"])
        print("Proxy settings cleaned up")

if __name__ == "__main__":
    main()