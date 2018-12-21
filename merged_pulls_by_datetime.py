# merged_pulls_by_datetime.py

import argparse
from datetime import datetime

import requests


def all_events_after(releasedatetime):
    params = {
        'base': 'master',
        'page': 0,
    }
    all_events = []

    while True:
        params['page'] += 1
        response = requests.get('https://api.github.com/repos/ansible/'
                                'ansible-lint/issues/events',
                                params=params)
        page_events = response.json()
        all_events.extend(page_events)
        page_oldest_created_at = datetime.strptime(
            page_events[29]['created_at'],
            '%Y-%m-%dT%H:%M:%SZ'
        )

        # exit only when page covers necessary timespan
        if page_oldest_created_at <= releasedatetime:
            print('Got {} pages of data from api'.format(params['page']))
            return all_events


def main():
    parser = argparse.ArgumentParser(description='List merged PRs '
                                     'since last release datetime.')
    parser.add_argument(
        '--releasedatetime',
        help='Datetime to start getting issues and PRs, '
             'use format 2018-10-29-23:30:00',
        type=lambda d: datetime.strptime(d, '%Y-%m-%d-%H:%M:%S'))
    args = parser.parse_args()

    all_events = all_events_after(args.releasedatetime)
    all_events = [
        e for e in all_events
        if datetime.strptime(e['created_at'],
                             '%Y-%m-%dT%H:%M:%SZ') >= args.releasedatetime
    ]
    all_events = [e for e in all_events if e['event'] in ('merged')]

    for event in all_events:
        print("- `%s %s <%s>`_" % (
            event['issue']['number'],
            event['issue']['title'],
            event['issue']['html_url']))


if __name__ == '__main__':
    main()
