__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import re
import sys
from math import ceil
from pathlib import Path
from time import sleep
from typing import Tuple, List, Dict, Optional

from pydub import AudioSegment
import requests
from tinytag import TinyTag

MIXCLOUD_MAX_FILESIZE = 512 * 1024 * 1024
MIXCLOUD_API_UPLOAD_URL = 'https://api.mixcloud.com/upload'
DEFAULT_CROSSFADE_MS = 1000
DEFAULT_MAX_RETRY = 100
DEFAULT_AUDIO_FILE_TYPES = ['flac', 'MP3', 'mp3', 'ogg', 'm4a']
# Mixcloud app:
# https://www.mixcloud.com/developers/Q29uc3VtZXI6MzY3Nw%253D%253D/
ACCESS_TOKEN_FILE = '.mixcloud_access_token'
MP3_KBIT_RATE = 128


def bytes_per_second(mp3_kbit_rate: int = MP3_KBIT_RATE) -> int:
    return mp3_kbit_rate // 8 * 1024 * 2


class Mix:  # pylint: disable=too-many-instance-attributes

    @classmethod
    def create(  # pylint: disable=too-many-arguments
            cls, basedir: Path, patterns: Tuple[str, ...],
            verbose: bool = False, strict: bool = False,
            crossfade_ms: int = DEFAULT_CROSSFADE_MS, title: str = None
    ) -> "Mix":
        files, length = cls.scan(basedir, patterns)
        if bytes_per_second() * length < MIXCLOUD_MAX_FILESIZE:
            return Mix(basedir, patterns, verbose, strict, crossfade_ms, title)
        return MultiMix(
            basedir, files, length, verbose, strict, crossfade_ms, title
        )

    @classmethod
    def scan(cls, basedir: Path, patterns: Tuple[str, ...]) -> Tuple[List[str], int]:
        audio_files = sorted([f for p in patterns for f in basedir.glob(p)])
        length = sum([TinyTag.get(str(audio_file)).duration for audio_file in audio_files])
        return [f.name for f in audio_files], int(length)

    @staticmethod
    def _read_access_token() -> str:
        with open(ACCESS_TOKEN_FILE, 'r') as file:
            return file.read().strip()

    def __init__(  # pylint: disable=too-many-arguments
            self, basedir: Path, patterns: Tuple[str, ...],
            verbose: bool = False, strict: bool = False,
            crossfade_ms: int = DEFAULT_CROSSFADE_MS, title: str = None
    ) -> None:
        self._basedir = basedir
        self._verbose = verbose
        self._strict = strict
        self._crossfade_ms = crossfade_ms
        self._title = title
        self._incomplete = False
        self._track_info: List[Dict] = []
        self._access_token = self._read_access_token()
        audio_files = sorted([f for p in patterns for f in self._basedir.glob(p)])
        self._audio = self._import_audio(audio_files)

    @property
    def valid(self):
        return not self._incomplete

    @property
    def tags(self) -> List[str]:
        if (self._basedir / 'tags.txt').exists():
            with (self._basedir / 'tags.txt').open() as file:
                return list(line for line in (line.strip() for line in file) if line)
        if self._strict:
            raise ValueError('No tags found')
        print('WARNING - no tags found')
        self._incomplete = True
        return ['Testing Mixcloud API']

    @property
    def title(self) -> str:
        if self._title:
            return self._title
        title = re.sub(r'^\d+ - ', '', self._basedir.resolve().name)
        return f"Test - don't bother playing ({title})" if self._incomplete else title

    @property
    def description(self) -> str:
        if (self._basedir / 'description.txt').exists():
            with (self._basedir / 'description.txt').open() as file:
                return file.read().strip()
        if self._strict:
            raise ValueError('No description found')
        print('WARNING - no description found')
        self._incomplete = True
        return 'Test test test'

    @property
    def picture(self) -> Optional[Path]:
        """Currently just returns the first JPEG or PNG. Room for improvement!"""
        try:
            return next(self._basedir.glob('*.*p*g'))
        except StopIteration as error:
            if self._strict:
                raise ValueError(f"No picture in {self._basedir}") from error
            print('WARNING - no picture found')
            self._incomplete = True
            return None

    def _import_audio(self, audio_files: List[Path]) -> AudioSegment:
        audio = AudioSegment.empty()
        for audio_file in audio_files:
            self._track_info.append(self._get_track_info(audio_file))
            if self._verbose:
                print(audio_file.name)
            track = AudioSegment.from_file(audio_file)
            track = track.normalize()
            audio = audio.append(
                track, crossfade=self._crossfade_ms if len(audio) > self._crossfade_ms else 0
            )

        return audio

    def _get_track_info(self, audio_file: Path) -> Dict:
        tags = TinyTag.get(str(audio_file))
        if tags.artist is None or tags.title is None:
            if self._strict:
                raise ValueError(f"Incomplete tags for {audio_file}")
            self._incomplete = True
            return {'artist': '???', 'title': '???', 'length': tags.duration}
        return {
            'artist': tags.artist, 'title': tags.title, 'length': tags.duration,
            'filename': audio_file.name
        }

    def export(self, name: Path = Path('mix.mp3')) -> None:
        mix_file = self._basedir / name
        audio_format = name.suffix[1:]
        if self._verbose:
            print(f'Exporting to {mix_file} with bitrate {MP3_KBIT_RATE} kbps')
        self._audio.export(
            mix_file, format=audio_format, parameters=["-q:a", "0"], bitrate=f'{MP3_KBIT_RATE}k'
        )

    def upload(self, name: Path = Path('mix.mp3'), max_retry: int = DEFAULT_MAX_RETRY) -> None:
        url = MIXCLOUD_API_UPLOAD_URL + '/?access_token=' + self._access_token
        mix_file = self._basedir / name
        files = {
            'mp3': ('mix.mp3', mix_file.open('rb'), 'audio/mpeg'),
        }
        if self.picture:
            picture_type = self.picture.suffix
            files['picture'] = (
                'picture' + picture_type, self.picture.open('rb'),
                f'image/{"png" if picture_type == ".png" else "jpeg"}'
            )

        data = {
            'name': self.title,
            'description': self.description,
            'percentage_music': 100
        }
        self._add_tags(data)
        self._add_track_info(data)
        if self._verbose:
            size = mix_file.stat().st_size + self.picture.stat().st_size
            print(
                f'Uploading {size // 1024:,d} kBytes '
                f'({len(self._audio) // 60000}:{len(self._audio) % 60000 // 1000:02} minutes) '
                f'as {self.title}'
            )

        try:
            response = requests.post(url, files=files, data=data)
        except requests.exceptions.ConnectionError as error:
            if self._verbose:
                print(self.connection_error_message(error, max_retry))
            if max_retry > 0:
                self.upload(name, max_retry=max_retry - 1)
                return
            sys.exit(1)

        if self._verbose:
            print(self.response_message(response))
        if self.is_rate_limited(response) and max_retry > 0:
            sleep(int(response.json()['error']['retry_after']))
            self.upload(name, max_retry=max_retry - 1)
        else:
            sys.exit(1)

    @staticmethod
    def is_rate_limited(response: requests.Response) -> bool:
        return response.json().get('error', {}).get('type') == 'RateLimitException'

    @staticmethod
    def response_message(response: requests.Response) -> str:
        if response.status_code == 200:
            return f"{response.status_code}: {response.json()['result']['message']}"
        return f"{response.status_code}: {response.json()['error']}"

    @staticmethod
    def connection_error_message(error: requests.exceptions.ConnectionError, max_retry: int) -> str:
        message = f"{error.args[0].args[1].args[1]}: {error.args[0].args[0]} "
        if max_retry > 0:
            message += f"Retrying {max_retry} time{'s' if max_retry > 1 else ''}."
        else:
            message += "Giving up."
        return message

    def _add_tags(self, data: Dict) -> None:
        for i, tag in enumerate(self.tags):
            data[f"tags-{i}-tag"] = tag

    def _add_track_info(self, data: Dict) -> None:
        start_time = 0
        for i, track_info in enumerate(self._track_info):
            data[f"sections-{i}-artist"] = track_info['artist']
            data[f"sections-{i}-song"] = track_info['title']
            data[f"sections-{i}-start_time"] = int(start_time)
            start_time += (track_info['length'] - self._crossfade_ms / 1000)


# noinspection PyMissingConstructor
class MultiMix(Mix):

    def __init__(  # pylint: disable=super-init-not-called, too-many-arguments
            self, basedir: Path, files: List[str], total_length: int,
            verbose: bool = False, strict: bool = False,
            crossfade_ms: int = DEFAULT_CROSSFADE_MS, title: str = None
    ) -> None:
        self._basedir = basedir
        self._title = title
        self._incomplete = False
        self._mix_parts: List[Mix] = []
        self._part_paths: List[Path] = []
        oversize_factor = ceil(total_length * bytes_per_second() / MIXCLOUD_MAX_FILESIZE)
        chunk_size = len(files) // oversize_factor
        for i in range(oversize_factor):
            part_files = tuple(files[i * chunk_size:(i + 1) * chunk_size])
            part_name = f"{self.title} Part {i + 1}"
            if verbose:
                print(part_name)
            mix_part = Mix(
                basedir, part_files, verbose=verbose, strict=strict, crossfade_ms=crossfade_ms,
                title=part_name
            )
            self._mix_parts.append(mix_part)

    @property
    def parts(self):
        return self._mix_parts

    def upload(self, name: Path = Path('mix.mp3'), max_retry: int = DEFAULT_MAX_RETRY) -> None:
        for mix_part, part_path in zip(self._mix_parts, self._part_paths):
            mix_part.upload(part_path, max_retry)

    def export(self, name: Path = Path('mix.mp3')) -> None:
        for i, mix_part in enumerate(self._mix_parts):
            part_path = Path(f"{name.stem}_{i + 1}{name.suffix}")
            mix_part.export(part_path)
            self._part_paths.append(part_path)
