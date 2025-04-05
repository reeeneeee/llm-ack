# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mitmproxy",
# ]
# ///
import os
import subprocess
import sys
import platform


def compare_cert_fingerprint():
    # Get keychain cert
    keychain_proc = subprocess.run(
        ["security", "find-certificate", "-c", "mitmproxy", "-Z"],
        capture_output=True,
    )
    keychain_fingerprint = (
        keychain_proc.stdout.decode("utf-8")
        .splitlines()[0]
        .split(":")[1]
        .strip()
        .lower()
    )

    # Get mitmproxy cert
    cert_path = os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.pem")
    openssl_proc = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-fingerprint", "-sha256"],
        capture_output=True,
    )
    openssl_fingerprint = (
        openssl_proc.stdout.decode("utf-8")
        .splitlines()[0]
        .split("=")[1]
        .replace(":", "")
        .strip()
        .lower()
    )

    return keychain_fingerprint == openssl_fingerprint


def setup_proxy():
    # Set up the proxy server
    try:
        subprocess.run(
            ["networksetup", "-setwebproxy", "Wi-Fi", "127.0.0.1", "8080"], check=True
        )
        subprocess.run(
            ["networksetup", "-setsecurewebproxy", "Wi-Fi", "127.0.0.1", "8080"],
            check=True,
        )
        print("Proxy settings configured successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up proxy: {e}")
        sys.exit(1)


def install_cert():
    # Install mitmproxy certificate
    cert_path = os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.pem")
    if not os.path.exists(cert_path):
        print(
            "Certificate not found. Please run mitmdump at least once to generate it."
        )
        sys.exit(1)

    try:
        subprocess.run(
            [
                "sudo",
                "security",
                "add-trusted-cert",
                "-d",
                "-p",
                "ssl",
                "-p",
                "basic",
                "-k",
                "/Library/Keychains/System.keychain",
                cert_path,
            ],
            check=True,
        )
        print("Certificate installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing certificate: {e}")
        sys.exit(1)


def generate_cert():
    print("Generating mitmproxy certificate...")
    try:
        # Run mitmdump to generate the certificate
        process = subprocess.Popen(
            ["mitmdump", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
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

    # Generate certificate if it doesn't exist
    cert_path = os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.pem")
    if not os.path.exists(cert_path):
        generate_cert()

    # Set up proxy and install certificate
    setup_proxy()
    if not compare_cert_fingerprint():
        install_cert()

    print(
        "\nStarting mitmdump..."
    )  # note: we use mitmdump because it has no tty requirement
    print("Press Ctrl+C to stop the proxy")

    try:
        script_name = sys.argv[1]
    except IndexError:
        script_name = "response_intercept.py"

    # Run mitmdump with the request modificationscript
    try:
        subprocess.run(["mitmdump", "-s", script_name])
    except KeyboardInterrupt:
        print("\nStopping proxy...")
        # Clean up proxy settings
        subprocess.run(["networksetup", "-setwebproxystate", "Wi-Fi", "off"])
        subprocess.run(["networksetup", "-setsecurewebproxystate", "Wi-Fi", "off"])
        subprocess.run(["unset", "http_proxy"])
        subprocess.run(["unset", "https_proxy"])
        print("Proxy settings cleaned up")


if __name__ == "__main__":
    main()
