import requests
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='Aurora IP address')
    parser.add_argument('-t', '--token-file', help='File to write Aurora token in', default="key")
    parser.add_argument('-p,' '--port', help='Aurora port', type=int, default=16021)
    args = parser.parse_args()

    print("** This script has not been fully tested yet.")
    print("Press the power button on your aurora for several seconds until the light starts blinking.")

    r = requests.post(f'http://{args.ip}:{args.port}/api/v1/new')

    if not r.ok:
        print(f"Error: {r.status_code} {r.content}")
        sys.exit(1)

    with open(args.token_file, 'w') as keyfile:
        keyfile.write(r.json()['auth_token'])
    print(f"Wrote token to {args.token_file}")
