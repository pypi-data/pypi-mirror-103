import requests
import simplebot
from simplebot.bot import Replies

__version__ = "1.1.0"
tv_emoji, cal_emoji, aster_emoji = "📺", "📆", "✳"
channels = {
    "cv": "Cubavisión",
    "cvi": "Cubavisión Internacional",
    "cvplus": "Cubavisión Plus",
    "tr": "Tele Rebelde",
    "edu": "Educativo",
    "edu2": "Educativo 2",
    "mv": "Multivisión",
    "clave": "Clave",
    "caribe": "Caribe",
    "chabana": "Canal Habana",
}


@simplebot.command
def cartv(replies: Replies) -> None:
    """Muestra la cartelera de todos los canales de la TV cubana."""
    replies.add(text="\n\n".join(_get_channel(chan) for chan in channels.keys()))


@simplebot.command
def cartvcv(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión."""
    replies.add(text=_get_channel("cv"))


@simplebot.command
def cartvcvi(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión Internacional."""
    replies.add(text=_get_channel("cvi"))


@simplebot.command
def cartvcvp(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión Plus."""
    replies.add(text=_get_channel("cvplus"))


@simplebot.command
def cartvtr(replies: Replies) -> None:
    """Muestra la cartelera del canal Tele Rebelde."""
    replies.add(text=_get_channel("tr"))


@simplebot.command
def cartved(replies: Replies) -> None:
    """Muestra la cartelera del canal Educativo."""
    replies.add(text=_get_channel("edu"))


@simplebot.command
def cartved2(replies: Replies) -> None:
    """Muestra la cartelera del canal Educativo 2."""
    replies.add(text=_get_channel("edu2"))


@simplebot.command
def cartvmv(replies: Replies) -> None:
    """Muestra la cartelera del canal Multivisión."""
    replies.add(text=_get_channel("mv"))


@simplebot.command
def cartvcl(replies: Replies) -> None:
    """Muestra la cartelera del canal Clave."""
    replies.add(text=_get_channel("clave"))


@simplebot.command
def cartvca(replies: Replies) -> None:
    """Muestra la cartelera del canal Caribe."""
    replies.add(text=_get_channel("caribe"))


@simplebot.command
def cartvha(replies: Replies) -> None:
    """Muestra la cartelera del canal Habana."""
    replies.add(text=_get_channel("chabana"))


def _get_channel(chan) -> str:
    url = "https://www.tvcubana.icrt.cu/cartv/{}/hoy.php".format(chan)
    with requests.get(url) as req:
        req.raise_for_status()
        programs = req.json()

    text = "{} {}\n".format(tv_emoji, channels[chan])
    date = None
    for prog in programs:
        date2, time = prog["eventInitialDateTime"].split("T")
        time = time[:-3]
        if date != date2:
            date = date2
            text += "{} {}\n".format(cal_emoji, date)
        title = " ".join(prog["title"].split())
        desc = " ".join(prog["description"].split())
        trans = prog["transmission"].strip()
        text += "{} {} {}\n".format(
            aster_emoji, time, "/".join(e for e in (title, desc, trans) if e)
        )

    if not programs:
        text += "Cartelera no disponible."

    return text


class TestPlugin:
    def test_cartv(self, mocker, requests_mock) -> None:
        for chan in channels.keys():
            self._requests_mock(requests_mock, chan)
        msg = mocker.get_one_reply("/cartv")
        for chan in channels.keys():
            assert channels[chan] in msg.text

    def test_cartvcv(self, mocker, requests_mock) -> None:
        chan = "cv"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcv").text

    def test_cartvcvi(self, mocker, requests_mock) -> None:
        chan = "cvi"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcvi").text

    def test_cartvcvp(self, mocker, requests_mock) -> None:
        chan = "cvplus"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcvp").text

    def test_cartvtr(self, mocker, requests_mock) -> None:
        chan = "tr"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvtr").text

    def test_cartved(self, mocker, requests_mock) -> None:
        chan = "edu"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartved").text

    def test_cartved2(self, mocker, requests_mock) -> None:
        chan = "edu2"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartved2").text

    def test_cartvmv(self, mocker, requests_mock) -> None:
        chan = "mv"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvmv").text

    def test_cartvcl(self, mocker, requests_mock) -> None:
        chan = "clave"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcl").text

    def test_cartvca(self, mocker, requests_mock) -> None:
        chan = "caribe"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvca").text

    def test_cartvha(self, mocker, requests_mock) -> None:
        chan = "chabana"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvha").text

    def _requests_mock(self, requests_mock, chan) -> None:
        data = [
            {
                "title": "Example program",
                "description": "Example description",
                "eventInitialDateTime": "2021-04-25T00:19:00",
                "transmission": "Estreno",
            },
            {
                "title": "Example program 2",
                "description": "Example description 2",
                "eventInitialDateTime": "2021-04-26T00:10:00",
                "transmission": "",
            },
        ]
        url = "https://www.tvcubana.icrt.cu/cartv/{}/hoy.php"
        requests_mock.get(url.format(chan), json=data)
