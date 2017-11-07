import time

import requests
import json
import argparse


def check_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('latitue', type=float,
                        help='Latitude of location')
    parser.add_argument('longitude', type=float,
                        help='Longtitude of location')
    parser.add_argument('radius', type=int,
                        help='Search in radius(m)')
    parser.add_argument('keyword',
                        help='Name of target need to search')
    parser.add_argument('token', help='Your google api token')
    args = parser.parse_args()

    return args.latitue, args.longitude, args.radius, args.keyword, args.token


def page_resp(args, page_token):
    resp = requests.get('https://maps.googleapis.com/'
                        'maps/api/place/nearbysearch/json?'
                        'location={},{}&radius={}&keyword={}&key={}&'
                        'pagetoken={}'.format(*args, page_token))

    return resp.json()


def solve(input_data):
    page_token = ''
    result = []

    while True:
        resp = page_resp(input_data, page_token)
        time.sleep(2)

        if 'error_message' in resp:
            print(resp['error_message'])
            break

        for i in resp['results']:
            result.append(i)

        try:
            page_token = resp['next_page_token']
        except Exception:
            break

    with open('Google.json', 'w') as f:
        json.dump(result, f)
        print('done')


def main():
    args = check_input()
    solve(args)


if __name__ == '__main__':
    main()
