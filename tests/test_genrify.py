"""
This module contains functional test cases for the genrify CLI
"""
import os
import subprocess

import pytest

GENRIFY_PATH = ["python", "-m", "genrify.genrify_run"]
MOCK_SERVER_PATH = "./mock_lastfm.py"

# relative to project root because the subprocess needs to cwd to there to
# run the module correctly
TEST_LIBRARY_PATH = "./tests/test_data/music"

songs = ["animals.mp3"]


# `cd` into tests directory if pytest is started from the project root, so
# that the paths work TODO make this better
if ".git" in os.listdir():
    os.chdir("tests")


os.environ["LASTFM_URL"] = "http://localhost:8252"
os.environ["LASTFM_API_KEY"] = "your_api_key"


@pytest.fixture(scope="module", autouse=True)
def mock_lastfm_server():
    """
    Fixture used to start the mock last.fm server before
    running any tests. Kill the server on test finish.
    """
    server = subprocess.Popen(["python", MOCK_SERVER_PATH])
    yield
    subprocess.Popen(["kill", str(server.pid)])


def run_genrify_command(args=None, input_=None, debug=False):
    """
    Runs genrify as a module with the passed args, and passes input to stdin
    when prompted.
    :param args: list of args to pass to genrify e.g. ["./album", "-i"]
    :type args: list[str]
    :param input: list of strings to be fed to genrify's stdin one by one
    :type args: list[str]
    :return: tuple containing lists of stdout and stderr lines returned
        by the process
    :rtype: tuple(list[str], list[str])
    """

    def _get_decoded(out):
        """
        Helper for decoding stdout/stderr from bytes
        """
        return [line.decode("utf-8") for line in out.splitlines()]

    args = args or []

    print_ = print if debug else lambda *args: None

    print_("=" * 40)
    print_(f"Testing command: genrify {' '.join(args)}")
    if input_:
        for i, line in enumerate(input_):
            print_(f"Input line {i}: '{line}'")

    process = subprocess.Popen(
        GENRIFY_PATH + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        cwd=".."
    )

    if input_:
        input_ = "\n".join(input_).encode()

    out, err = process.communicate(input=input_)

    out = _get_decoded(out)
    err = _get_decoded(err)

    print_(f"stdout: \n{out}")
    print_(f"stderr: \n{err}")
    print_("=" * 40)

    return out, err


def test_help():
    """
    Test for help command
    """
    args = ["-h"]
    out, _ = run_genrify_command(args)
    assert any(line for line in out if "usage" in line)


def test_library_no_flags():
    """
    Test for passing music library with no optional args
    """
    args = [TEST_LIBRARY_PATH]
    out, _ = run_genrify_command(args, debug=True)
    assert any(
        line for line in out
        if "changed" in line
        or "already" in line
    )

def test_single_song_interactive():
    """
    Test for passing single song in interactive mode
    """
    args = [
        os.path.join(TEST_LIBRARY_PATH, songs[0]),
        "-i"
    ]
    out, _ = run_genrify_command(args, input_=["2"], debug=True)
    assert any(line for line in out if "Emo" in line)


def test_single_song_interactive_custom(limit=1):
    """
    Test for passing single song in interactive mode,
    select manual genre input
    """
    args = [
        os.path.join(TEST_LIBRARY_PATH, songs[0]),
        '--limit',
        str(limit),
        '-i'
    ]
    input_ = ["2", "asdf"]
    out, _ = run_genrify_command(args, input_=input_)
    assert any(
        line for line in out
        if "genre changed" in line
        or "No action taken" in line
    )
