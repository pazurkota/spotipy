import argparse
from api.authorization import Authorization
from api.player import SpotifyPlayer

def main():
    parser = argparse.ArgumentParser(description='Spotify CLI Player')
    parser.add_argument('command', choices=['play', 'stop', 'next', 'previous', 'seek', 'volume', 'repeat', 'shuffle'])
    parser.add_argument('--seconds', type=int, help='Seconds to seek to')
    parser.add_argument('--volume', type=int, help='Volume percentage')
    parser.add_argument('--repeat', type=str, help='Repeat mode')
    parser.add_argument('--shuffle', type=bool, help='Shuffle mode')

    args = parser.parse_args()

    auth = Authorization()
    auth.authenticate()
    player = SpotifyPlayer(auth)

    if args.command == 'play':
        print(player.play_playback())
    elif args.command == 'stop':
        print(player.stop_playback())
    elif args.command == 'next':
        print(player.skip_to_next())
    elif args.command == 'previous':
        print(player.skip_to_previous())
    elif args.command == 'seek':
        if args.seconds is not None:
            print(player.seek_to_position(args.seconds))
        else:
            print('Please provide the number of seconds to seek to.')
    elif args.command == 'volume':
        if args.volume is not None:
            print(player.set_volume(args.volume))
        else:
            print('Please provide the volume percentage.')
    elif args.command == 'repeat':
        if args.repeat is not None:
            print(player.set_repeat_mode(args.repeat))
        else:
            print('Please provide the repeat mode.')
    elif args.command == 'shuffle':
        if args.shuffle is not None:
            print(player.set_shuffle_mode(args.shuffle))
        else:
            print('Please provide the shuffle mode.')

if __name__ == '__main__':
    main()
