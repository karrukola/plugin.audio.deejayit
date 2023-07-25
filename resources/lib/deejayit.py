from __future__ import annotations

import logging
from collections import namedtuple
from typing import Any, FrozenSet, List, Union
from urllib.parse import urljoin

import requests

JsonType = Any
WebRadio = namedtuple(
    "WebRadio",
    "name desc content_url logo_url fanart_url metadata_url",
)
Episode = namedtuple(
    "Episode",
    "title desc content_url logo_url fanart_url date speakers program",
)
Show = namedtuple(
    "Show",
    "name id desc logo_url fanart_url",
)

WebRadioMetadata = namedtuple(
    "WebRadioMetadata",
    "last_update title artist album cover_url next_date",
)


class DeejayIt:
    def __init__(self) -> None:
        self.base_url = "https://www.deejay.it/api/pub/v2/all/mhub/"
        self.logger = logging.getLogger("deejay_it_client")
        self.logger.setLevel(logging.DEBUG)

    def _get_request(self, url_fragment: str, params=None):
        url = urljoin(self.base_url, url_fragment)
        req = requests.get(url, params=params, timeout=30)
        self.logger.debug("req.url: %s", req.url)
        req.raise_for_status()
        return req

    def _query_webradios(self) -> List[JsonType]:
        # https://www.deejay.it/api/pub/v2/all/mhub/webradios/deejay

        radios = self._get_request("webradios/deejay").json()
        return radios["data"]

    def _query_programs(self) -> List[JsonType]:
        results = []
        residual = 1
        idx = 1
        while residual > 0 and idx < 50:  # idx is a safety measure
            # https://www.deejay.it/api/pub/v2/all/mhub/programs?brand_id=deejay&page=1&pagination_rows=15&sort=desc
            out = self._get_request(
                "programs",
                params={
                    "brand_id": "deejay",
                    "page": idx,
                    "pagination_rows": 15,
                    "sort": "desc",
                },
            )
            for prog in out.json()["results"]:
                results.append(prog)

            residual = out.json()["count"] - len(results)
            idx += 1

        return results

    def _query_episodes(self, show_id: int, page_nr: int = 1):
        # https://www.deejay.it/api/pub/v2/all/mhub/search?program_id=15&audio_type=episode&page=1&pagination_rows=15&sort=desc
        resp = self._get_request(
            "search",
            params={
                "program_id": show_id,
                "audio_type": "episode",
                "page": page_nr,
                "pagination_rows": 15,
                "sort": "desc",
            },
        ).json()
        return (resp["results"], resp["count"])

    def get_radios(self) -> FrozenSet[WebRadio]:
        radios = self._query_webradios()
        # print(radios[0])
        return frozenset(
            WebRadio(
                # name desc content_url logo_url fanart_url metadata
                radio["title"],
                radio["content"],
                radio["streamingUrlHLS"],
                radio["featuredImage"]["sizes"]["size_320x320"],  # logo_url
                radio["appImage"]["sizes"]["size_1200x675"],  # fanart_url
                radio["metadataUrl"],
            )
            for radio in radios
            if radio["status"] == "on"
        )

    def get_shows(self):
        shows = self._query_programs()
        # "name id desc logo_url fanart_url",
        return frozenset(
            Show(
                show["name"],
                show["id"],
                show["description"],
                show["images"]["size_320x320"],
                show["images"]["size_1200x675"],
            )
            for show in shows
        )

    def _safe_get_pic(self, ep_dict, key) -> Union[None, str]:
        try:
            url = ep_dict["images"][key]
        except TypeError:
            url = None
        return url

    def get_show_episodes(self, show_id: int, page_nr: int) -> FrozenSet[Episode]:
        eps_raw, _ = self._query_episodes(show_id, page_nr)
        self.logger.debug(eps_raw)

        return frozenset(
            # title desc content_url logo_url fanart_url date speakers program
            Episode(
                ep["name"],
                ep["description"],
                ep["hls_url"] if ep["hls_url"] else ep["mp3_url"],
                self._safe_get_pic(ep, "size_320x320"),  # logo_url
                self._safe_get_pic(ep, "size_1200x675"),  # fanart_url
                ep["datePublished"],  # dd/mm/yyyy
                " e ".join(speaker["name"] for speaker in ep["speakers"]),
                ep["program"]["name"],
            )
            for ep in eps_raw
        )

    @staticmethod
    def parse_webradio_metadata(metadata_url: str) -> WebRadioMetadata:
        # https://streamcdnb10-4c4b867c89244861ac216426883d1ad0.msvdn.net/webradio/metadata/deejaywfmlinus.json
        req = requests.get(metadata_url, timeout=10)
        req.raise_for_status()
        out = req.json()["json"]
        # "last_update title artist album cover_url next_date",
        album = out["now"]["album"].strip() if out["now"]["album"] is not None else None
        return WebRadioMetadata(
            out["time"].strip(),
            out["now"]["title"].strip(),
            out["now"]["artist"].strip(),
            album,
            out["now"]["coverUrl"].strip(),
            out["next"][0]["datePlay"].strip(),
        )


def _main() -> int:
    try:
        # just making pretty prints on PC
        from rich import print
    except ImportError:
        pass

    deejay = DeejayIt()

    # radios = deejay.get_radios()
    # print(radios)

    shows = deejay.get_shows()
    print(shows)

    # eps = deejay.get_show_episodes(15, 1)  # 15 = Cordialmente
    # print(eps)

    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
