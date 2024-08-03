type_to_ext = {
    'text/html':                             'html',
    'text/css':                              'css',
    'text/xml':                              'xml',
    'image/gif':                             'gif',
    'image/jpeg':                           'jpeg',
    'application/x-javascript':              'js',
    'application/atom+xml':                  'atom',
    'application/rss+xml':                   'rss',

    'text/mathml':                           'mml',
    'text/plain':                            'txt',
    'text/vnd.sun.j2me.app-descriptor':      'jad',
    'text/vnd.wap.wml':                      'wml',
    'text/x-component':                      'htc',

    'image/png':                             'png',
    'image/tiff':                            'tif',
    'image/vnd.wap.wbmp':                    'wbmp',
    'image/x-icon':                          'ico',
    'image/x-jng':                           'jng',
    'image/x-ms-bmp':                        'bmp',
    'image/svg+xml':                         'svg',
    'image/webp':                            'webp',

    'application/java-archive':              'jar',
    'application/mac-binhex40':            'hqx',
    'application/msword':                    'doc',
    'application/pdf':                       'pdf',
    'application/postscript':                'ps',
    'application/rtf':                       'rtf',
    'application/vnd.ms-excel':              'xls',
    'application/vnd.ms-powerpoint':         'ppt',
    'application/vnd.wap.wmlc':              'wmlc',
    'application/vnd.google-earth.kml+xml':  'kml',
    'application/vnd.google-earth.kmz':      'kmz',
  

    'audio/midi':                           'mid',
    'audio/mpeg':                        'mp3',
  
    'video/3gpp':                        '3gpp',
    'video/mpeg':                          'mpeg',
    'video/quicktime':                    'mov',
    'video/x-flv':                        'flv',
    'video/x-mng':                        'mng',
    'video/x-ms-asf':                      'asx',
    'video/x-ms-wmv':                      'wmv',
    'video/x-msvideo':                      'avi',
    'video/mp4':                            'mp4',
}

def convert_mime_type_to_file_ext(mimetype: str):
    """
    Returns the file extension corresponding to the mimetype
    """

    if mimetype not in type_to_ext.keys():
        raise Exception('Mimetype not recognized')

    return type_to_ext[mimetype]


def convert_file_extenstion_to_mimetype(file_ext: str):
    for mimetype, ext in type_to_ext.items():
        if ext == file_ext:
            return mimetype
        
    raise Exception('File extenstion not recognized')