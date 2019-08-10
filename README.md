# plugin.audio.deejayit
![Build Status](https://travis-ci.org/karrukola/plugin.audio.deejayit.svg?branch=master)

[IT]
I reloaded di Radio DeeJay su Kodi. Da Deejay Chiama Italia a Tropical Pizza, da Asganaway al Deejay Time, i programmi di [Radio Deejay](http://www.deejay.it) da riascoltare quando e dove vuoi.

[EN]
A Kodi plugin that lets you access [Radio Deejay](http://www.deejay.it)'s ondemand archive.

Radio DeeJay is an Italian radio station. It was founded on 1 February 1982 by the Italian radio and television personality Claudio Cecchetto and was acquired by the Gruppo Editoriale L'Espresso in 1989 (which also owns DeeJay TV, Repubblica Radio TV, m2o and Radio Capital). [source: Wikipedia]

# Technical details

Version 2 of this plugin relies on the API used by the official mobile apps, sniffed using [Fiddler](https://www.telerik.com/fiddler). The JSON output is then parsed and used to present data on screen.

## List of API calls
## Get list of Reloaded
http://www.deejay.it/api/pub/v1/programs_ondemand?section=radio
## Get latest episode(s)
http://www.deejay.it/api/pub/v1/archive_ondemand?last_day=1&pid=225196&rid=225228
