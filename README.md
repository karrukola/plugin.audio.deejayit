# plugin.audio.deejayit

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[IT]
_Reloaded_, _podcast_ e _webradio_ di Radio DeeJay su Kodi. Da Deejay Chiama Italia a
Tropical Pizza, da Asganaway al Deejay Time, i programmi di
[Radio Deejay](http://www.deejay.it) da riascoltare quando e dove vuoi.

[EN]
A Kodi plugin that lets you access [Radio Deejay](http://www.deejay.it)'s ondemand archive.

Radio DeeJay is an Italian radio station. It was founded on 1 February 1982 by the
Italian radio and television personality Claudio Cecchetto and was acquired by the
Gruppo Editoriale L'Espresso in 1989 (which also owns DeeJay TV, Repubblica Radio TV,
m2o and Radio Capital). [source: Wikipedia]

## Why does this exist?

So I am able to access all episodes of [**Cordialmente**](https://www.deejay.it/programmi/cordialmente/)
and play them on long road trips.

## Technical details

Version 2 of this plugin relies on the API used by the official mobile apps, sniffed
using [Fiddler Classic](https://www.telerik.com/fiddler).
The JSON output is then parsed and used to present data on screen.

## List of API calls

### Home page

[Reloaded list](https://www.deejay.it/api/pub/v2/all/mhub/programs?brand_id=deejay&page=1&pagination_rows=15&sort=desc)

[Podcasts](https://www.deejay.it/api/pub/v2/all/mhub/series?brand_id=deejay&page=1&pagination_rows=15&sort=desc)

[Webradios](https://www.deejay.it/api/pub/v2/all/mhub/webradios/deejay)

### Get latest episode(s)

Once you know the `program_id` you can query for its latest episodes.

[Show's episodes: Cordialmente](https://www.deejay.it/api/pub/v2/all/mhub/search?program_id=15&audio_type=episode&page=1&pagination_rows=15&sort=desc)
