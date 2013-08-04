import urllib2
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
        return hmac(key, message, sha1).digest().encode('base64')

    def _get_content_md5(self, req):
        if req.data:
            return md5(req.data).hexdigest()
        return "d41d8cd98f00b204e9800998ecf8427e"

    def _get_content_type(self, req):
        if req.get_method() == "POST":
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

    def get_targets(self):
        targets = []
        for target_id in self.get_target_ids():
            targets.append(self.get_target_by_id(target_id))
        return targets

    def add_target(self, data):
        url = '%s/targets' % self.host
        data = json.dumps(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        response = self._get_authenticated_response(req)
        return json.loads(response.read())['results']

def main():
    v = Vuforia(access_key="YOUR_KEY_HERE",
                secret_key="YOU_KEY_HERE")
    for target in v.get_targets():
        print target

    image = "http://placehold.it/320x100"
    metadata = "https://dl.dropboxusercontent.com/s/p9fot1ltr92j5ex/metadata.txt?token_hash=AAHriiVFKXpnX10iekhCBaB2oBDS4bhIbxvg3Ox_Z5N41Q&dl=1"
    print v.add_target({"name": "Eyadd", "width": "320.0", "image_url": image, "application_metadata_url": metadata})

if __name__ == "__main__":
    main()
