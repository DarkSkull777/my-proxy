import requests
import argparse
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

def cek_proxy(proxy):
    try:
        response = requests.get("http://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return f"{proxy} -> {colored('Working', 'light_green')}", True
    except:
        pass
    return f"{proxy} -> {colored('Not Working', 'light_red')}", False

def cek_proxy_massal(file_list, output_file=None, show_all=False):
    try:
        with open(file_list, "r") as file:
            daftar_proxy = file.read().splitlines()
    except FileNotFoundError:
        print(colored("File not found.", 'red'))
        return

    results = []

    def process_proxy(proxy):
        result, is_working = cek_proxy(proxy)
        if show_all or is_working:
            print(result)
            if output_file and is_working:
                results.append(proxy)

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(process_proxy, daftar_proxy)

    if output_file and results:
        with open(output_file, "w") as f:
            for proxy in results:
                f.write(f"{proxy}\n")
        print(colored(f"\nResult saved in {output_file}", 'cyan'))

def cek_proxy_target(target):
    result, _ = cek_proxy(target)
    print(result)

if __name__ == "__main__":
    print("# Dymles Ganz 1337\n")
    parser = argparse.ArgumentParser(description="Proxy Checker - tools for checking proxy working or not.")
    parser.add_argument("-l", "--list", help="Filename list of proxy.")
    parser.add_argument("-o", "--output", help="Filename to save working proxies.")
    parser.add_argument("-t", "--target", help="Single checker (ex. -t 127.0.0.1:8008).")
    parser.add_argument("-a", "--all", action="store_true", help="Show all statuses (working and not working).")

    args = parser.parse_args()

    if args.list:
        cek_proxy_massal(args.list, args.output, args.all)
    elif args.target:
        cek_proxy_target(args.target)
    else:
        parser.print_help()
