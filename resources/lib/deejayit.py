"""Module mainly hosting the Python clinet to https://www.deejay.it ."""
from __future__ import annotations

import logging
from collections import namedtuple
from typing import Any
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

_ITER_LIMIT = 50


class DeejayIt:
    """Python client to deejay.it API v2.

    Aim is to give the same experience in Kodi that you get via iOS/Android app.
    """

    def __init__(self) -> None:
        self.base_url = "https://www.deejay.it/api/pub/v2/all/mhub/"
        self.logger = logging.getLogger("deejay_it_client")
        self.logger.setLevel(logging.DEBUG)

    def _get_request(  # noqa: ANN202
        self,
        url_fragment: str,
        params: dict[str, str | int] | None = None,
    ):
        url = urljoin(self.base_url, url_fragment)
        req = requests.get(url, params=params, timeout=30)
        self.logger.debug("req.url: %s", req.url)
        req.raise_for_status()
        return req

    def _query_webradios(self) -> list[JsonType]:
        # https://www.deejay.it/api/pub/v2/all/mhub/webradios/deejay

        radios = self._get_request("webradios/deejay").json()
        return radios["data"]

    def _query_programs(self) -> list[JsonType]:
        results = []
        residual = 1
        idx = 1
        while residual > 0 and idx < _ITER_LIMIT:  # idx is a safety measure
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
                results.append(prog)  # noqa: PERF402

            residual = out.json()["count"] - len(results)
            idx += 1

        return results

    def _query_episodes(
        self,
        show_id: int | str,
        page_nr: int = 1,
    ) -> tuple[list[JsonType], int]:
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

    def get_radios(self) -> frozenset[WebRadio]:
        """Return the whole list of webradios.

        The webradios are NamedTuples that provide the raw, JSON, output from
        the API to provide just the information that is consumed by Kodi.

        :return: list of webradios, what else?
        :rtype: frozenset[WebRadio]
        """
        radios = self._query_webradios()
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

    def get_shows(self) -> frozenset[Show]:
        """Return the whole list of shows.

        The shows are NamedTuples that provide the raw, JSON, output from the API
        to provide just the information that is consumed by Kodi.

        This method makes more than one request to return the full list and not
        leave scrolling through the pages to the user.

        :return: set of shows
        :rtype: frozenset[Show]
        """
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

    def _safe_get_pic(self, ep_dict: JsonType, key: str) -> str | None:
        try:
            url = ep_dict["images"][key]
        except TypeError:
            url = None
        return url

    def get_show_episodes(
        self,
        show_id: int | str,
        page_nr: int | str,
    ) -> frozenset[Episode]:
        """Return one page of the list of episodes for a show.

        As there are many episodes per show, we let the users go through the
        full list via pagination.

        The episodes are NamedTuples that provide the raw, JSON, output from
        the API to provide just the information that is consumed by Kodi.

        :param show_id: show identifier, as per API database
        :type show_id: int
        :param page_nr: the number of the page to be queried
        :type page_nr: int
        :return: set of episodes
        :rtype: frozenset[Episode]
        """
        eps_raw, _ = self._query_episodes(show_id, int(page_nr))
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
        """Parse the metadata for a webradio.

        The data is implemented as NamedTuple to provide just the information
        that Kodi needs.

        :param metadata_url: url of the JSON file providing metadata updates.
        :type metadata_url: str
        :return: filtered metadata information.
        :rtype: WebRadioMetadata
        """
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
