# cli_count_galaxy_scores.py

import requests


def main():
    '''Provides count of galaxy quality and community scores.'''

    base_url = 'https://galaxy.ansible.com/api/v1/'
    collection_endpoint = 'repositories/'
    content_endpoint = 'content/'
    params = '?{0}__gte={1}&{0}__lt={2}'
    # other count option: '?community_score__isnull=0'

    r = requests.get(base_url + collection_endpoint)
    total_collections = r.json()['count']

    r = requests.get(base_url + content_endpoint + '?content_type__id=11')
    total_roles = r.json()['count']

    collection_quality = []
    collection_community = []
    content_quality = []

    for start, end in [(0.0, 2.0), (2.0, 4.0), (4.0, 5.1)]:
        filter = params.format('quality_score', start, end)
        url = base_url + collection_endpoint + filter
        r = requests.get(url)
        collection_quality.append(r.json()['count'])

        filter = params.format('community_score', start, end)
        url = base_url + collection_endpoint + filter
        r = requests.get(url)
        collection_community.append(r.json()['count'])

        filter = params.format('quality_score', start, end)
        url = base_url + content_endpoint + filter
        r = requests.get(url)
        content_quality.append(r.json()['count'])

    num_scored = sum(collection_quality)
    msg = 'Quality scored collections out of total: {}/{}'
    print(msg.format(num_scored, total_collections))
    msg = 'Quality Score: 0-1.9: {:.0f}%, 2.0-3.9: {:.0f}%, 4.0-5.0: {:.0f}%'
    percents = [100*float(x)/num_scored for x in collection_quality]
    print(msg.format(*percents))

    num_scored = sum(collection_community)
    msg = 'Community scored collections out of total: {}/{}'
    print(msg.format(num_scored, total_collections))
    msg = 'Community Score: 0-1.9: {:.0f}%, 2.0-3.9: {:.0f}%, 4.0-5.0: {:.0f}%'
    percents = [100*float(x)/num_scored for x in collection_community]
    print(msg.format(*percents))

    num_scored = sum(content_quality)
    msg = 'Quality scored content(roles) out of total: {}/{}'
    print(msg.format(num_scored, total_roles))
    msg = 'Quality Score: 0-1.9: {:.0f}%, 2.0-3.9: {:.0f}%, 4.0-5.0: {:.0f}%'
    percents = [100*float(x)/num_scored for x in content_quality]
    print(msg.format(*percents))


if __name__ == '__main__':
    main()
