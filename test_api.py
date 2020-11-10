#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import requests
import sys
from simplejson import loads, dumps

HOST = 'http://localhost:3333'
SONG_URL = 'https://music.163.com/#/song?id=%s'


def login():
    url = HOST + '/login/cellphone'

    resp = requests.get(url, {
        'phone': '17600083957',
        'password': 'hit6886033'
    })

    data = resp.json()


def refresh_login():
    pass


def search(q):
    print 'search:' + q

    url = HOST + '/search?keywords=' + q
    resp = requests.get(url)
    data = resp.json()

    code = data.get('code')
    if code != 200:
        return

    result = data['result']
    

    song_count = result.get('songCount', 0)
    print '搜索结果数量：', song_count
    song_list = result.get('songs', [])

    privileges = batch_get_privileges([str(s['id']) for s in song_list])

    for i, s in enumerate(song_list):
        id = s['id']
        name = s['name']
        fee = s['fee']
        artists = s['artists']
        duration = s['duration']

        artists_names = ', '.join([c['name'] for c in artists])
        idx = i + 1

        copyright_id = s['copyrightId']
        vip = privileges[i]['cp'] and '免费' or '付费VIP歌曲'

        print idx, id, name, fee, 'duration:', duration_str(duration), '艺术家:', artists_names, 'copyright', copyright_id, SONG_URL % id, s['status'], vip
    
    

def duration_str(d):
    sec = d / 1000
    s = str(datetime.timedelta(seconds=int(sec)))
    ss = s.split(':')
    if len(ss) == 3:
        return ':'.join(ss[1:])
    return ss

def batch_get_privileges(ids):
    url = HOST + '/song/detail?ids=' + ','.join(ids)
    resp = requests.get(url)
    data = resp.json()

    code = data.get('code')
    if code != 200:
        return
    privileges = data['privileges']
    return privileges

def get_song(id):
    url = HOST + '/song/detail?ids=' + str(id)
    resp = requests.get(url)
    data = resp.json()

    code = data.get('code')
    if code != 200:
        return

    song_list = data.get('songs', [])
    for i, s in enumerate(song_list):
        id = s['id']
        name = s['name']
        fee = s['fee']
        artists = s['ar']
        duration = s['dt']

        artists_names = ', '.join([c['name'] for c in artists])

        idx = i + 1

        print idx, id, name, fee, 'duration:', duration_str(duration), '艺术家:', artists_names, 'copyright', s['copyright'], SONG_URL %  id, s['st']

        #print dumps(s)

# import ipdb
# ipdb.set_trace()


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        id = 168091 # 蓝莲花VIP
        get_song(id)
        id = 167908 # 有版权
        get_song(id)
        id = 25706282
        get_song(id)
        id = 185694 # 无版权
        get_song(id)
    else:
        q = sys.argv[1]
        search(q)