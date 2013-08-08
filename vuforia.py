import urllib2, base64
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from urlparse import urlparse
from hashlib import sha1, md5
from hmac import new as hmac
import json

class Vuforia:
    def __init__(self, access_key, secret_key, host="https://vws.vuforia.com"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = host

    def _get_rfc1123_date(self):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)

    def _get_request_path(self, req):
        o = urlparse(req.get_full_url())
        return o.path

    def _hmac_sha1_base64(self, key, message):
        return base64.b64encode(hmac(key, message, sha1).digest())

    def _get_content_md5(self, req):
        if req.get_data():
            return md5(str(req.get_data())).hexdigest()
        return "d41d8cd98f00b204e9800998ecf8427e"

    def _get_content_type(self, req):
        if req.get_method() in ["POST", "PUT"]:
            return "application/json"
        return ""

    def _get_authenticated_response(self, req):
        rfc1123_date = self._get_rfc1123_date()
        string_to_sign =\
            req.get_method() + "\n" +\
            self._get_content_md5(req) + "\n" +\
            self._get_content_type(req) + "\n" +\
            rfc1123_date + "\n" +\
            self._get_request_path(req)
        signature = self._hmac_sha1_base64(self.secret_key, string_to_sign)

        req.add_header('Date', rfc1123_date)
        auth_header = 'VWS %s:%s' % (self.access_key, signature)
        req.add_header('Authorization', auth_header)
        # TODO: Add handler for error codes like 403 "TargetNameExist"
        return urllib2.urlopen(req)

    def get_target_by_id(self, target_id):
        url = '%s/targets/%s' % (self.host, target_id)
        req = urllib2.Request(url)
        response = self._get_authenticated_response(req)
        return json.loads(response.read())['target_record']

    def get_target_ids(self):
        url = '%s/targets' % self.host
        req = urllib2.Request(url)
        response = self._get_authenticated_response(req)
        return json.loads(response.read())['results']

    def get_summary(self):
        url = '%s/summary' % self.host
        req = urllib2.Request(url)
        response = self._get_authenticated_response(req)
        return json.loads(response.read())

    def get_targets(self):
        targets = []
        for target_id in self.get_target_ids():
            targets.append(self.get_target_by_id(target_id))
        return targets

    def add_target(self, data):
        url = '%s/targets' % self.host
        data = json.dumps(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json; charset=utf-8'})
        response = self._get_authenticated_response(req)
        return json.loads(response.read())

    def update_target(self, target_id, data):
        # Takes time to process
        url = '%s/targets/%s' % (self.host, target_id)
        data = json.dumps(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json; charset=utf-8'})
        req.get_method = lambda: 'PUT'
        response = self._get_authenticated_response(req)
        return json.loads(response.read())

    def delete_target(self, target_id):
        # Takes time to process
        url = '%s/targets/%s' % (self.host, target_id)
        req = urllib2.Request(url)
        req.get_method = lambda: 'DELETE'
        response = self._get_authenticated_response(req)
        return json.loads(response.read())

def main():
    v = Vuforia(access_key="YOUR_KEY_HERE",
                secret_key="YOUR_KEY_HERE")
    for target in v.get_targets():
        print target

    image_file = open('PATH_TO_IMAGE')
    image = base64.b64encode(image_file.read())
    metadata_file = open('PATH_TO_METADATAFILE')
    metadata = base64.b64encode(metadata_file.read())
    print v.add_target({"name": "zxczxc", "width": "320", "image": image, "application_metadata": metadata, "active_flag": 1})

if __name__ == "__main__":
    main()
