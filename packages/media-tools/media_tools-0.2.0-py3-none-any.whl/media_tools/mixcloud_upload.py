__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

from media_tools.util.mixcloud import (
    Mix, DEFAULT_CROSSFADE_MS, DEFAULT_MAX_RETRY, DEFAULT_AUDIO_FILE_TYPES
)


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="Creates a mix from audio files and uploads it to Mixcloud"
    )
    parser.add_argument(
        '-d', '--directory', type=str, required=True, help='Directory containing the mix'
    )
    parser.add_argument(
        '-e', '--extensions', nargs='+', default=DEFAULT_AUDIO_FILE_TYPES,
        help='List of extensions considered for the mix'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true'
    )
    parser.add_argument(
        '-s', '--strict', action='store_true', help='Fail if any required data are missing'
    )
    parser.add_argument(
        '-c', '--crossfade-ms', type=int, default=DEFAULT_CROSSFADE_MS,
        help='Milliseconds overlap between tracks'
    )
    parser.add_argument(
        '-r', '--max-retry', type=int, default=DEFAULT_MAX_RETRY,
        help='Maximum number of retries for failing uploads'
    )
    return parser.parse_args(args)


def main() -> None:
    args: List[str] = sys.argv[1:]
    opts = parse_commandline(args)
    mix = Mix.create(
        Path(opts.directory), tuple(f'?? - *.{ext}' for ext in opts.extensions),
        crossfade_ms=opts.crossfade_ms, verbose=not opts.quiet, strict=opts.strict
    )
    mix.export()
    mix.upload(max_retry=opts.max_retry)


if __name__ == '__main__':
    main()
