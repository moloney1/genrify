import os
import subprocess

from mock_lastfm import start_server

GENRIFY_PATH = "../genrify/genrify.py"
TEST_LIBRARY_PATH = "./test_data/music"
MOCK_SERVER_PATH = "./mock_lastfm.py"
songs = ["animals.mp3"]


os.environ["LASTFM_URL"] = "http://localhost:8252"
os.environ["LASTFM_API_KEY"] = "your_api_key"

def start_mock_lastfm_server():
    cmd = ["python", MOCK_SERVER_PATH]
    return subprocess.Popen(cmd)

def stop_mock_lastfm_server(server):
    subprocess.Popen(["kill", str(server.pid)])

def ping():
    print("=" * 40)
    cmd = [
        GENRIFY_PATH,
        "-h"
    ]
    print("Testing cmd: {cmd}")
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE
    )
    out, _ = p.communicate()
    decoded = get_decoded_out(out)
    print(decoded)
    assert any(line for line in decoded if "usage" in line)
    print("=" * 40)


def library_no_flags():
    print("=" * 40)
    cmd = [GENRIFY_PATH, TEST_LIBRARY_PATH]
    print("Testing cmd: ", cmd)
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE
    )
    out, _ = p.communicate()
    decoded = get_decoded_out(out)
    print(decoded)
    assert any(
        line for line in decoded
        if "changed" in line
        or "already" in line
    )
    print("=" * 40)


def single_song_interactive(limit=3):
    print("=" * 40)
    cmd = [
        GENRIFY_PATH,
        os.path.join(TEST_LIBRARY_PATH, songs[0]),
        "-i"
    ]
    print("Testing cmd: ", cmd)
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE
    )
    out, _ = p.communicate(input=b"2")
    decoded = get_decoded_out(out)
    print(decoded)
    assert any([line for line in decoded if "Emo" in line])
    print("=" * 40)


def single_song_interactive_custom(limit=1):
    print("=" * 40)
    cmd = [
        GENRIFY_PATH,
        os.path.join(TEST_LIBRARY_PATH, songs[0]),
        '-i',
        '--limit',
        str(limit)
    ]
    print("Testing cmd: ", cmd)
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE
    )
    out, _ = p.communicate(input=b"2\nasdf")
    decoded = get_decoded_out(out)
    print(decoded)
    assert any([line for line in decoded if "genre changed" in line])
    print("=" * 40)


def get_decoded_out(out):
    return [line.decode("utf-8") for line in out.splitlines()]


if __name__ == '__main__':
    server = start_mock_lastfm_server()
    ping()
    library_no_flags()
    single_song_interactive_custom()
    single_song_interactive(limit=3)
    stop_mock_lastfm_server(server)
