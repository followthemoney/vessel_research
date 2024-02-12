# Vessel research

The goal of this repository is to collect code, tools and documentation on how to investigate vessel information. This means information on vessel travel history, ownership, inspections and all other information that could be relevant for investigations. 

## Global Fishing Watch

A very useful source is [Global Fishing Watch](https://globalfishingwatch.org), an NGO/platform with AIS data, SAR imagery and information on vessel ownership and events (like loitering, encounters, port visits, AIS gaps). There are some helpful functions available in [gwf.py](src/gfw.py) to query the GFW API (documentation). You need to [get an API key](https://globalfishingwatch.org/our-apis/) and add that to an environment file (e.g. .env file in the root folder) in order for it to work. This code is work in progress and will - hopefully - result in a full-fledged Python library.

There are a few functions available for now:
1. get_vessels: finds vessels based on MMSI, name or IMO
2. get_events: finds events by vessel. Events are fishing, port_vitits, loitering, encounters (possible transshipment) and AIS gaps (not available for crowded marine environments because of signals cancelling each other out).
3. get_events by region: find events by region (administrative or polygon)

## Data sources

Many of the sources mentioned here are sourced from SaraL at the Maritime Osint Resources thread on [Bellingcat's Discord channel](https://discord.gg/bellingcat) and are re-used here with her permission.

### Vessel tracking

**Vessel tracking sites**

There are many websites for tracking shipping movements, with limited historical data (even in paid tiers). The most important are:
1. [MarineTraffic](https://marinetraffic.com)
2. [VesselFinder](https://vesselfinder.com)
3. [FleetMon](https://fleetmon.com)
4. [Global Fishing Watch](https://globalfishingwatch.org)
5. [AISHub](https://aishub.net)

There are also some fully paid services - without a free tier - that might help with investigations:
1. [Spire](https://spire.com)
2. [TankerTrackers](https://tankertrackers.com)

**Digital Selective Calling**

Digital Selective Calling is a protocol for using specific frequencies to call other ships and coast stations using encoded radio transmissions, these calls are encoded to ping (the REQ call) specific targets using their MMSIs, all ships in a certain area or all ships in general. When picked up, the receiving station pings an encoded radio transmission back (the ACK call), so both sides of the conversation know who they are talking to, and when archived, this leaves a digital trace of those radio calls.

[YaDDNet DSC Logs](http://www.yaddnet.org/index.php)

**Navtex**

Navtex, or NAVigational TEleX, is an automated system onboard ships that allows the transmission and direct printing of navigational, weather, search and rescue, and other information to ships by coast stations.

Every message is given a four character code (B₁ + B₂ + B₃ + B₄). Each station in a region is identified by a transmitter identity (B₁), the nature of the information also identified by the second letter (B₂). The last two characters (B₃ and B₄) are numbers counting from 01 - 99 based on the order of the message. More information on B₂ can be found [here](https://www.icselectronics.co.uk/support/info/gmdss/navtex_message) 

- [NAVTEX LIVE](http://navtex.lv/)
- [Frisnit Navtex Decoder](http://www.frisnit.com/cgi-bin/navtex/view.cgi)
- [Navtex Archive](https://www.navtex.net/navtex-archive.html)

**MF and HF Radio Nerds**

Super niche, but in the vein of YaDDNet recording and decoding the DSC signals, there are enthusiasts who spend their free time listening out on MF and HF nets for communications, typically weather reports, and reporting on them as a hobby. As MF/HF communications are especially used by Russian naval vessels, it's a good method of tracking them. 

te3ej - https://twitter.com/te3ej
Olga Honcharenko - https://twitter.com/olga_pp98
Twente313 - https://twitter.com/Twente313
Gerry Agnew - https://twitter.com/gerryagnew30
Geoff McMaw - https://twitter.com/geoff_mcmaw
Roland - https://twitter.com/DF3LZ
Latitude 67N SIGINT - https://twitter.com/Sigint67n
Eddy Tanoca - https://twitter.com/EddyTanoca
AvScanNZ - https://twitter.com/NZ_Trav

### Ownership & Identity

**Equasis**

Equasis is a website operated by the French Transport Ministry which collates information sources into one place. It shows the name of the ship owner and management company, classification society and links to their regular survey reports, reports on Port State Control inspections and detentions from all MOU areas, has an archive of the areas that the vessel sailed in, identifies previous identities of the ship.

[Equasis](https://www.equasis.org/)

**GISIS**

GISIS, or the Global Integrated Shipping Information System, is a portal operated by the International Maritime Organization. In the ship and company particulars, you can find additional information on ships, including a section for ships identified as operating illegally. Other tabs include information on illegal migrant smuggling and piracy, data on ports, organizations and marine accidents. The tabs available can be seen below.

[GISIS](https://gisis.imo.org/)

**Ship and Coast Station List**

The International Telecommunications Union (ITU) maintains a portal that allows you to search by name, MMSI, radio callsigns and other things for ships and coast stations, providing additional information on the vessel.

- [Ship Station List](https://www.itu.int/mmsapp/shipstation/list)
- ]Coast Station List](https://www.itu.int/mmsapp/CoastStation/list)

**Classification Societies**

In additional to national regulations which would be enforced by flag state control (on your own flag's ships) and port state control (on any ship within your country), the second element in maritime regulation in classification societies.

Classification societies, in some sense are like industry regulation bodies. As each country is going to struggle to maintain the requisite expertise to cover every element of ship operation - design, construction, operation, safety surveys, scrapping - the classification societies fill this role with experts (naval architects, maritime officers, lawyers) who draft requirements, inspect ships and provide certification.

Being "classed" is a requirement under maritime regulations for any ship, so despite it being regulations imposed by a private entity, they are like any other regulations that you must follow, with the same surveys that a national maritime administration would carry out, just by private entity.

Whilst there is many of them, the International Association of Classification Societies (IACS) has 11 members which are the primary ones.

- [IACS](https://iacs.org.uk/)
- [American Bureau of Shipping](https://ww2.eagle.org/en.html)
- [Bureau Veritas](https://group.bureauveritas.com/)
- [China Classification Society](https://www.ccs.org.cn/ccswzen/)
- [Croatian Register of Shipping](https://crs.hr/)
- [Det Norske Veritas](https://www.dnv.com/)
- [Indian Register of Shipping](https://www.irclass.org/)
- [Korean Register of Shipping](https://www.krs.co.kr/eng/)
- [Lloyds Register](https://www.lr.org/)
- [Nippon Kaiji Kyokai](https://www.classnk.com/hp/en/index.html)
- [Polish Register of Shipping](https://www.prs.pl/home)
- [Registro Italiano Navale](https://www.rina.org/en)

Expelled from IACS, there is also.

[Russian Maritime Register of Shipping](https://rs-class.org/en/)

### Remote sensing

- [Global Fishing Watch](https://globalfishingwatch.org/map)
- [SentinelHub](https://www.sentinel-hub.com/)
- [Soar](https://soar.earth/)
- [ICEEYE](https://iceeye.com) (paid)
- [Bellingcat/Ollie Ballinger's Ship Detection Tool](https://ollielballinger.users.earthengine.app/view/ship-detection-tool)
- SATIM Inc. - https://twitter.com/SatimMonitoring
- Ines_Satim - https://twitter.com/Ines_Satim
- Radex_satim - https://twitter.com/radex_satim
- stassia_satim - https://twitter.com/stassia_satim

### Events

**Maritime Safety Information**

Maritime Safety Information are snippets of information that provide ships at sea information on different goings-on at sea. This can range from buoys being inoperative, firing practice areas in operation, hydrographic surveys and details on ongoing search and rescue operations. These are then broadcast on the radio and Navtex as "radio navigation warnings."

These are divided into twenty-one NAVAREAs, each with a specific country assigned as the coordinator for that area.

- [Navigation Warnings on the Web](https://iho.int/en/navigation-warnings-on-the-web)
- [NAVAREA Links](https://navarea.info/)

Additionally, most countries operate their own websites for activities in their areas of responsibility, best to search for Notice to Mariners or Marine Notice plus the countries name, to find these websites.

**Sailing Directions**

Sailing Directions are guides that provide sailors with helpful information for seafarers at sea to assist with navigation, passage planning and contact information. Whilst the Admiralty Sailing Directions are only available if you pay for them, the US government (National Geospatial-Intelligence Agency) is required to publish such information into the public domain, can be found here, and cover the entire world.

- [Sailing Directions Enroute](https://msi.nga.mil/Publications/SDEnroute)
- [Sailing Directions Planning Guide](https://msi.nga.mil/Publications/SDPGuides)

**Office of Naval Intelligence**

The United States Office of Naval Intelligence produces open source reports on the navies of Russia, People's Republic of China and Iran, this includes ship identification guides (with silhouettes), shipbuilding forecasts, fleet assignments in addition to reporting on the command structure and officers within their navies, it can be found there.

[Office of Naval Intelligence](https://www.oni.navy.mil/)

**Threats to Shipping**

In addition to the ONI's focus on naval affairs, they also produce weekly reporting on threats to merchant vessels and shipping companies, these can be found here.

[Worldwide Threat to Shipping](https://www.oni.navy.mil/ONI-Reports/Shipping-Threat-Reports/Worldwide-Threat-to-Shipping/)

As the coordinator of anti-piracy in the Indian Ocean, the UK Maritime Trade Operations (UKMTO) office publishes reports on incidents, including suspicious approaches to merchant vessels, these can be found here.

[UKMTO](https://www.ukmto.org/indian-ocean/recent-incidents)
[Twitter](https://twitter.com/UK_MTO)

For piracy incidents in the Gulf of Guinea, the Maritime Domain Awareness for Trade – Gulf of Guinea (MDAT-GoG) office publishes reports for their area of responsibility, these can be found here.

[MDAT-GoG](https://gog-mdat.org/home)
[Twitter](https://twitter.com/MDAT_GoG)

In Asia, the Regional Cooperation Agreement on Combating Piracy and Armed Robbery against Ships in Asia (ReCAAP) publishes reports for their area of responsibility, these can be found here.

[ReCAAP](https://www.recaap.org/)
[Twitter](https://twitter.com/recaapisc)

Lastly, the International Maritime Bureau Piracy Reporting Centre publishes reports about recent incidents worldwide, these can be found here.

[IMBPRC Live Piracy Report](https://icc-ccs.org/piracy-reporting-centre/live-piracy-report)

**United States Naval Institute News Fleet and Marine Tracker**

The USNI carries out a weekly report on the positions of U.S. naval assets using open source DVIDS content descriptions and other reporting, it can be found here.

[USNI News Fleet and Marine Tracker](https://news.usni.org/category/fleet-tracker)

**Seafarer Abandonment**

The International Labour Organization maintains a database of seafarers abandoned by their employers at ports around the world, who refuse to pay the seafarers their wages or repatriate them to their home country.

[Abandonment of Seafarers database](https://www.ilo.org/dyn/seafarers/seafarersBrowse.list)

**Navigational Charts**

Ships at sea navigate using navigational charts. Whilst their routes may look haphazard, a merchant ship on its route can in most cases be predictable, its passage plan going from traffic separation scheme to traffic separation scheme, giving dangers to navigation (offshore infrastructure, rocks, shallow areas) a wide berth. A navigational charts detail provides context that might not be otherwise readily apparent, a spy ship hovering over underwater infrastructure, a ship at anchor in a designated anchorage, certain berths in ports being fuel berths, and so on.

- [NOAA ENC Viewer](https://www.nauticalcharts.noaa.gov/enconline/enconline.html) (US/associated waters)
- [Kystverket](https://a3.kystverket.no/kystinfo) (Norway) (note: change basemap to nautical map/ENC)

In addition to the above resources, there's also navigational maps with worldwide/broader coverage, albeit somewhat worse quality.

- [i-Boating](https://fishing-app.gpsnauticalcharts.com/i-boating-fishing-web-app/fishing-marine-charts-navigation.html)
- [Navionics](https://webapp.navionics.com/)
- [OpenSeaMap])https://map.openseamap.org/)

For help with deciphering the meaning of different symbols, please see Chart No. 1.

[Chart No. 1](https://msi.nga.mil/Publications/Chart1)


## Social media

**X**

- Yörük Işık - https://twitter.com/YorukIsik (Bosphorus)
- Ryan Chan - https://twitter.com/ryankakiuchan (Indo-Pacific)
- Frederik Van Lokeren - https://twitter.com/KaptainLOMA/ (Russian Navy)
- FauteuilColbert -  https://twitter.com/FauteuilColbert (French Navy)
- Michael J. Sanchez - https://twitter.com/key2med (Gibraltar)
- Ray Powell - https://twitter.com/GordianKnotRay (South China Sea)
- NZDF Liaison Officer, Singapore IFC - https://twitter.com/NZ_ILO_IFC_SING (South-East Asia)
- TankerTrackers.com - https://twitter.com/TankerTrackers (Tanker Tracking)
- MT Anderson - https://twitter.com/MT_Anderson (Satellite imagery)
- The Lookout - https://twitter.com/The_Lookout_N (Norwegian/Barents Sea)
- Damien Symon - https://twitter.com/detresfa_ (Indo-Pacific)
- Chris Cavas - https://twitter.com/CavasShips (U.S. Navy)
- Straits Sights - https://twitter.com/StraitsSights (Singapore and Johor)
- H.I. Sutton - https://twitter.com/covertshores/ (Submarines)
- WarshipCam - https://twitter.com/WarshipCam (Warships on online webcams)
- Wondersmith_rae - https://twitter.com/wondersmith_rae (tips for maritime OSINT)

## Tutorials and knowledge bases

- Discord
