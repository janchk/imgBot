
def file_ext_checker(drive, filename, filetype):
    page_token = None
    while True:
        resp = drive.files().list(
            q="mimeType='{}' and name='{}'".format(filetype, filename),
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()
        try:
            files = resp.get('files',[])
            for file in files:
                if (filename == file['name']):
                    print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    return file.get('id')
                    # break
        except IndexError:
            return False
            # pass
        page_token = resp.get('nextPageToken', None)
        if page_token is None:
            return False
            