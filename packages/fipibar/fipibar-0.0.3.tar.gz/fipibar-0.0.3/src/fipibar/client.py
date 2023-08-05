import argparse
import json
import os
import pylast
import requests
import subprocess
import time

from .config_helper import FipibarConfig
from datetime import datetime


class FipibarClient():

    def __init__(self):
        '''
        TODO: Add args/kwargs here.
        '''
        self.config = FipibarConfig()
        self.unique_fip_process_string = 'fipibar_magic_constant'

        self.stations_list = self.get_stations_list()
        self.current_station = self.config.get('current_station', 0)

        self.currently_playing_trunclen = int(
            self.config.get('currently_playing_trunclen', 45)
        )

        self.lastfm_client = self.get_lastfm_client()

    def get_lastfm_client(self):
        if any(
            [
                self.config.get('lastfm_should_heart', False),
                self.config.get('lastfm_should_scrobble', False),
            ]
        ):
            try:
                return pylast.LastFMNetwork(
                    api_key=self.config.get('lastfm_api_key', None),
                    api_secret=self.config.get('lastfm_api_secret', None),
                    username=self.config.get('lastfm_username', None),
                    password_hash=self.config.get('lastfm_password_hash', None),
                )
            except Exception as e:
                print("Please configure ~/.fipibar_config.json with last.fm details.")
                print(e)

    def get_stations_list(self):
        '''
        Returns a list of dicts definining stations.
        '''
        return [
            {
                'name': 'FIP Groove',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/66',
                'stream_url': 'https://stream.radiofrance.fr/fipgroove/fipgroove_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP Radio',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/7',
                'stream_url': 'https://stream.radiofrance.fr/fip/fip_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP Rock',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/64',
                'stream_url': 'https://stream.radiofrance.fr/fiprock/fiprock_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP Jazz',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/65',
                'stream_url': 'https://stream.radiofrance.fr/fipjazz/fipjazz_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP World',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/69',
                'stream_url': 'https://stream.radiofrance.fr/fipworld/fipworld_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP Nouveautes',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/70',
                'stream_url': 'https://stream.radiofrance.fr/fipnouveautes/fipnouveautes_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP Reggae',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/71',
                'stream_url': 'https://stream.radiofrance.fr/fipreggae/fipreggae_hifi.m3u8\?id\=radiofrance'
            },
            {
                'name': 'FIP Electro',
                'details_url': 'https://api.radiofrance.fr/livemeta/pull/74',
                'stream_url': 'https://stream.radiofrance.fr/fipelectro/fipelectro_hifi.m3u8\?id\=radiofrance'
            },
        ]

    def is_currently_playing(self):
        '''
        Returns True if there is a currently playing song, False otherwise.
        '''
        try:
            return int(subprocess.check_output('ps aux | grep ' + self.unique_fip_process_string + ' | grep -v grep | grep -v python | wc -l', shell=True)) >= 1
        except Exception:
            return False

    def play(self):
        subprocess.check_output('bash -c "exec -a ' + self.unique_fip_process_string + ' ffplay -nodisp ' + self.stations_list[self.config.get('current_station', 0)]['stream_url'] + ' > /dev/null 2>&1 &"', shell=True)

    def pause(self):
        subprocess.check_output('kill $(ps aux | grep ' + self.unique_fip_process_string + ' | grep -v grep | awk -e \'{printf $2}\')', shell=True)

    def toggle_playback(self):
        '''
        Plays the current track if currently paused. Pauses current track if
        currently playing.
        '''
        if self.is_currently_playing():
            self.pause()
        else:
            self.play()

    def get_current_station_name(self):
        return self.stations_list[self.current_station]['name']

    def print_current_station_name(self):
        print(self.get_current_station_name())

    def get_currently_playing_string(self):
        '''
        Returns the string displayed in Polybar for currently playing
        track/artist.
        '''
        try:
            # Thanks to Zopieux for the gist this came from:
            # https://gist.github.com/Zopieux/ccb8d29437765083e4c80da52f2145b2
            data = requests.get(self.stations_list[self.config.get('current_station', 0)]['details_url']).json()

            level = data['levels'][0]
            uid = level['items'][level['position']]
            step = data['steps'][uid]

            currently_playing_string = f"{step['title']} - {step['authors']}"

            if self.config.get('current_track', '') != currently_playing_string:
                if self.config.get('should_notify', False):
                    subprocess.check_call(
                        [
                            'notify-send',
                            '-i',
                            'applications-multimedia',
                            self.get_current_station_name(),
                            currently_playing_string
                        ]
                    )

                if self.config.get('lastfm_should_scrobble', False):
                    self.lastfm_client.update_now_playing(
                        artist=step['authors'],
                        title=step['title']
                    )

                    self.lastfm_client.scrobble(
                        artist=step['authors'],
                        title=step['title'],
                        timestamp=datetime.utcnow()
                    )

                self.config.set('current_track', currently_playing_string)

            if len(currently_playing_string) > self.currently_playing_trunclen:
                return currently_playing_string[:self.currently_playing_trunclen - 3] + '...'
            else:
                return currently_playing_string

            return msg
        except:
            return 'Can\'t find details...'

    def next_station(self):
        '''
        Scroll to the next station in the list looping.
        '''
        self.current_station += 1
        self.current_station %= len(self.stations_list)
        self.config.set('current_station', self.current_station)

        self.pause()
        self.play()

    def previous_station(self):
        '''
        Scroll to the previous station in the list looping.
        '''
        self.current_station -= 1
        self.current_station %= len(self.stations_list)
        self.config.set('current_station', self.current_station)

        self.pause()
        self.play()


def main():
    fipibar_client = FipibarClient()

    parser = argparse.ArgumentParser(
        description='Entrypoint for Fip Radio/Polybar integration.'
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--get-currently-playing", action="store_true")
    group.add_argument("--toggle-playback", action="store_true")
    group.add_argument("--next-station", action="store_true")
    group.add_argument("--previous-station", action="store_true")
    group.add_argument("--print-current-station-name", action="store_true")

    args = parser.parse_args()

    if args.get_currently_playing:
        print(fipibar_client.get_currently_playing_string())
    elif args.toggle_playback:
        fipibar_client.toggle_playback()
    elif args.next_station:
        fipibar_client.next_station()
    elif args.previous_station:
        fipibar_client.previous_station()
    elif args.print_current_station_name:
        fipibar_client.print_current_station_name()


if __name__ == '__main__':
    main()
