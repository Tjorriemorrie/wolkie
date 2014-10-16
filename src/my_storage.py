import os
import logging
import cloudstorage as gcs
from google.appengine.api import app_identity


class Storage():

    BUCKET = None
    # PROJECT_ID = 231046206486
    # OWNER_ID = '00b4903a97eaff25a6aa438be6287281b081afedc1d63f087875bc9d5932690e'

    # Retry can help overcome transient urlfetch or GCS issues, such as timeouts.
    RETRY_PARAMS = gcs.RetryParams(
        initial_delay=0.2,
        max_delay=5.0,
        backoff_factor=2,
        max_retry_period=15,
    )

    def __init__(self):
        # All requests to GCS using the GCS client within current GAE request and
        # current thread will use this retry params as default. If a default is not
        # set via this mechanism, the library's built-in default will be used.
        # Any GCS client function can also be given a more specific retry params
        # that overrides the default.
        # Note: the built-in default is good enough for most cases. We override
        # retry_params here only for demo purposes.
        gcs.set_default_retry_params(self.RETRY_PARAMS)
        logging.debug('Storage: retry params set')

        self.BUCKET = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        if not self.BUCKET:
            raise Exception('Default GCS bucket not found')
        # self.BUCKET = 'oanda'
        logging.debug('Storage: bucket name retrieved: {0}'.format(self.BUCKET))


    def createFile(self, filename, data):
        logging.debug('Storage: create file...')
        file_path = '/' + self.BUCKET + filename
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(
            file_path,
            'w',
            content_type='text/plain',
            options={'x-goog-meta-foo': 'foo',
                     'x-goog-meta-bar': 'bar'},
            retry_params=write_retry_params
        )
        gcs_file.write(str(data.encode('utf-8')))
        gcs_file.close()
        logging.debug('File written to storage')
