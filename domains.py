# Init the domains
domains = {}

domains['MED'] = {
    'map': 'maps/med_mask.nc',
    'title': 'Med. Sea',
    'popup': 'html/medsea.html',
    'lat_offset': -3 * 1/12
}

domains['NS'] = {
    'map': 'maps/ns_mask.nc',
    'title': 'NS',
    'popup': 'html/ns.html',
    'config': 'csv/ns_config.csv'
}

domains['EEC'] = {
    'title': 'EEC',
    'map': 'maps/eec_mask.nc',
    'popup': 'html/eec.html'
}

domains['GOG'] = {
    'map': 'maps/gog_mask.nc',
    'title': 'GOG',
    'popup': 'html/gog.html'
}

domains['GOL'] = {
    'map': 'maps/gol_mask.nc',
    'title': 'GOL',
    'popup': 'html/gol.html'
}

domains['BEN'] = {
    'map': 'maps/ben_mask.nc',
    'title': 'BEN',
    'popup': 'html/ben.html'
}

domains['NSB'] = {
    'map': 'maps/nsb_mask.nc',
    'title': 'NSB',
    'popup': 'html/nsb.html'
}


domains['BS'] = {
    'map': 'maps/bs_mask.nc',
    'title': 'BS',
    'popup': 'html/bs.html'
}

domains['WAP'] = {
    'map': 'maps/wap_mask.nc',
    'title': 'WAP',
    'popup': 'html/bs.html'
}
