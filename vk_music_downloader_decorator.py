import argparse
import configparser
import os
import sys
import vk
from urllib.request import urlretrieve

# Decorator, that checks if specified artist is exist and adds some messages :)
def check_if_artist_exist(fn):
    def wrapper(*args):
        if args[0] is not None:
            flag = False
            for i in range(len(args[1]['items'])):
                if args[1]['items'][i]['artist'] == args[0][0]:
                    flag = True
            if not flag:
                sys.exit("It seems you made mistake or specified artist is absent. Try again, please!")
        if len(args) == 3:
            print()
            print("The list of your tracks:")
        fn(*args)
        if len(args) == 4:
            print("Download complete!")
        print()
        print("Have a nice day!")
    return wrapper

# Print the list of tracks sorted by artist / adding date
@check_if_artist_exist
def show_tracks(artist, tracks, sort):
    artist_title = []
    print()
    if artist is None:
        for track in tracks['items']:
            artist_title.append(track['artist'] + " - " + track['title'])
    else:
        artist = artist[0]
        for track in tracks['items']:
            if track['artist'] == artist:
                artist_title.append(track['artist'] + " - " + track['title'])
    if sort == True:
        artist_title.sort()
    print('\n'.join(artist_title))


# Download the specified tracks / all
@check_if_artist_exist
def download_tracks(artist, tracks, title, path):
    if not os.path.exists(path):
        os.makedirs(path)
    if artist is None and title is None:
        confirm = input("It seems you want to DOWNLOAD ALL THE TRACKS! Are you SURE? (Y / N) ")
        if confirm.lower() == 'y':
            print()
            for track in tracks['items']:
                url = track['url']
                print('Downloading: {} - {}'.format(track['artist'], track['title']))
                urlretrieve(url, path + '/' + track['artist'] + ' - ' + track['title'] + ".mp3")
        if confirm.lower() == 'n':
            sys.exit("Please, specify the arguments and try again!")
        else:
            sys.exit("It seems like you didn't choose YES.\nPlease, specify the arguments and try again!")
    elif artist is not None:
        artist = artist[0]
        if title is None:
            print()
            for track in tracks['items']:
                if track['artist'] == artist:
                    url = track['url']
                    print('Downloading: {} - {}'.format(track['artist'], track['title']))
                    urlretrieve(url, path + '/' + track['artist'] + ' - ' + track['title'] + ".mp3")
        else:
            title = title[0]
            print()
            for track in tracks['items']:
                if track['artist'] == artist and track['title'] == title:
                    url = track['url']
                    print('Downloading: {} - {}'.format(track['artist'], track['title']))
                    urlretrieve(url, path + '/' + track['artist'] + ' - ' + track['title'] + ".mp3")
    elif artist is None:
        title = title[0]
        print()
        for track in tracks['items']:
            if track['title'] == title:
                url = track['url']
                print('Downloading: {} - {}'.format(track['artist'], track['title']))
                urlretrieve(url, path + '/' + track['artist'] + ' - ' + track['title'] + ".mp3")

def main():
    # Read the auth-conf file
    conf = configparser.ConfigParser()
    conf.read('vk_music_downloader_auth.cfg')
    appid = conf.get('AUTH', 'app_id')
    login = conf.get('AUTH', 'user_login')
    passw = conf.get('AUTH', 'user_password')

    # VK authorization
    auth = vk.AuthSession(app_id=appid, user_login=login, \
                          user_password=passw, scope='audio')
    api = vk.API(auth, v='5.53', lang='en')
    tracks = api.audio.get()

    # Parse the command-line arguments
    pars = argparse.ArgumentParser(description='VK Downloader parameters.')
    pars.add_argument('-path', metavar='PATH', type=str, nargs=1,
                      help='Path of download folder. Default: "Download"')
    pars.add_argument('-artist', metavar='ARTIST', type=str, nargs=1,
                      help='Download the track(s) with specified Artist')
    pars.add_argument('-title', metavar='TITLE', type=str, nargs=1,
                      help='Download the track(s) with specified Title')
    pars.add_argument('-show', action="store_true", default=False,
                      help='Show the track(s) without downloading')
    pars.add_argument('--sort', action="store_true", default=False,
                      help='Sort the track(s) by Artist')
    args = pars.parse_args()

    path = args.path
    if path is None:
        path = "Downloads" # Default path

    artist = args.artist # Artist
    title = args.title # Title
    sort = args.sort # Sort

    # Check the mode: show / download
    if args.show == True:
        show_tracks(artist, tracks, sort)
    else:
        download_tracks(artist, tracks, title, path)

if __name__ == '__main__':
    main()