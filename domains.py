# Init the domains
domains = {}

domains['BOB'] = {
    'map': 'maps/bob_mask.nc',
    'popup': "html/template.html",
    'status': 'dev'
}

domains['BALTIC'] = {
    'map' : 'maps/med_mask.nc',
    'popup': 'html/baltic_sea.html',
    'config': 'csv/baltic_sea.csv'
}

#domains['MED'] = {
#    'map': 'maps/med_mask.nc',
#    'title': 'Med. Sea',
#    'popup': 'html/medsea.html',
#    'lat_offset': -3 * 1/12
#}

domains['NS'] = {
    'map': 'maps/ns_mask.nc',
    'popup': 'html/ns.html',
    'config': 'csv/ns_config.csv'
}

domains['EEC'] = {
    'map': 'maps/eec_mask.nc',
    'popup': 'html/eec.html'
}

domains['GOG'] = {
    'map': 'maps/gog_mask.nc',
    'popup': 'html/gog.html'
}

domains['GOL'] = {
    'map': 'maps/gol_mask.nc',
    'popup': 'html/gol.html'
}

domains['BEN'] = {
    'map': 'maps/ben_mask.nc',
    'popup': 'html/ben.html'
}

domains['NSB'] = {
    'map': 'maps/nsb_mask.nc',
    'popup': 'html/nsb.html'
}


domains['BS'] = {
    'map': 'maps/bs_mask.nc',
    'popup': 'html/bs.html',
    'config': 'csv/bs_config.csv'
}

domains['WAP'] = {
    'map': 'maps/wap_mask.nc',
    'popup': 'html/wap.html'
}
