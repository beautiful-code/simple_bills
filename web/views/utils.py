import cloudstorage as gcs
import uuid

import settings

def isFileUploaded(handler, file_field):
    file_data = handler.request.POST[file_field]
    return True if file_data != u'' else False

def listToStringMessages(items):
    json = []
    if items:
        for item in items:
            json.append({'data': item})
    return json

def stringMessagesToList(msg_json):
    items = []
    if msg_json:
        for data_item in msg_json:
            if data_item['data']:
                items.append(data_item['data'])
    return items


def uploadBillImageToStaging(file_data):
    filename = file_data.filename
    file_type = file_data.type
    data = file_data.value

    staging_filepath= '/' + str(uuid.uuid4()) + '/' + filename
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(
        '/' + settings.STAGING_FILE_BUCKET + staging_filepath,
        'w',
        content_type=file_type,
        options={},
        retry_params=write_retry_params
        )
    gcs_file.write(data)
    gcs_file.close()

    return staging_filepath
