import sys
import os
import base64
import datetime
import hashlib
import hmac
import urllib

METHOD = 'GET'
HOST = 'webservices.amazon.in'
URI = '/onca/xml'
SERVICE = 'AWSECommerceService'
OPERATION = 'ItemSearch'

def sign_hex(key, string_to_sign):
	"Get the HEX encoded HMAC signature."
        if not key or not string_to_sign:
            raise ValueError("key or string_to_sign cannot be blank")
	return hmac.new(key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def sign_base64(key, string_to_sign):
        "Return base64 encoded HMAC signature"
        val_hex = sign_hex(key, string_to_sign)
	return val_hex.decode("hex").encode("base64").strip()

def sign_base64_enc(key, string_to_sign):
        "Return Base64 URL Encoded HMAC Signature"
        val_base64 = sign_base64(key, string_to_sign)
        return urllib.quote(val_base64)

def sort_qp_numeric(qp):
	"Return a comma separated string of numerically sorted data from a CSV String"
        if not qp:
            raise ValueError("qp cannot be blank")
	tok = qp.split(',')
	tok.sort(key=str.encode)
	return ','.join(tok)

def canonicalize(query_param):
	"Return a canonical string of query parameters."
        if not query_param:
	    raise ValueError("query_param cannot be blank")
	qps = query_param.split('&')
	qp_map = {}
	qp_keys = []
	qp_val = []
	for qp in qps:
		tok = qp.split('=')
		k = tok[0].strip()
		v = tok[1].strip()
		vl = sort_qp_numeric(v)
                vlq = urllib.quote(vl)
		qp_map[k] = vlq
		qp_keys.append(k)

	qp_keys.sort(key=str.encode)

	cans = ''
	for k in qp_keys:
		q = '{}={}'.format(k, qp_map[k])
		if not cans:
                        cans = q
                else:
			cans = cans + '&' + q
	return cans

def canonicalize_dict(query_dict):
        "Given a dictionary, get the corresponding canonical query params"
        if not query_dict:
            raise ValueError("Cannot canonicalize empty dictionary")
        can_qp = ''
        sk = sorted(query_dict.keys(), key=str.encode)
        for k in sk:
            if can_qp:
                can_qp += "&"
            v = query_dict[k]
            vs = sort_qp_numeric(v)
            vse = urllib.quote(vs)
            can_qp += "{}={}".format(k, vse)
        return can_qp

def get_signature(secret_key, query_param):
	"For the given query parameter, get the HMAC signature"
        if not secret_key or not query_param:
            raise ValueError("secret_key or query_param cannot be blank")
	canonical_qp = canonicalize(query_param)
        return get_signature_can(secret_key, canonical_qp)

def get_signature_can(secret_key, canonical_qp):
        "For the given canonical_qp, get the HMAC signature using the given key"
        if not secret_key or not canonical_qp:
            raise ValueError("secret_key or query_param cannot be blank")
	string_to_sign = string_to_sign = '{}\n{}\n{}\n{}'.format(METHOD, HOST, URI, canonical_qp).strip()
	signature = sign_base64_enc(secret_key, string_to_sign)
	return signature

def get_url_dict(secret_key, query_dict):
        "Get the complete url from the given dict and secret_key"
        if not query_dict:
            raise ValueError("Cannot get blank URL")
        if not secret_key:
            raise ValueError("secret_key cannot be blank")
        can_qp = canonicalize_dict(query_dict)
        sign = get_signature_can(secret_key, can_qp)
        return "http://{}{}?{}&Signature={}".format(HOST, URI, can_qp, sign)

def get_url_dict_cred(query_dict, access_key=None, secret_key=None, associate_tag=None, fmt_date=None):
        "Given a dict of query paramters, get the complete URL"
        if not query_dict:
            raise ValueError("query_dict cannot be None or empty")

        if not access_key:
            access_key = os.environ.get('AWS_ACCESS_KEY_ID')

        if not secret_key:
            secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        if not associate_tag:
            associate_tag = os.environ.get('AWS_ASSOCIATE_TAG')

        if not access_key or not secret_key or not associate_tag:
            raise ValueError("Blank credentials not allowed. Either pass them or export them.")

        if not fmt_date:
            t = datetime.datetime.utcnow()
            fmt_date = t.strftime('%Y-%m-%dT%H:%M:%SZ')

        ak = access_key.strip()
        sk = secret_key.strip()
        at = associate_tag.strip()

        qd = query_dict.copy()
        qd['AWSAccessKeyId'] = ak
        qd['AssociateTag'] = at
        qd['Timestamp'] = fmt_date

        return get_url_dict(sk, qd)

def get_url_defaults(category, keywords, access_key, secret_key, associate_tag, fmt_date):
        "Given the category, keywords and credentials, get the amazon URL"
        # If keywords or category is None, return.
        if not keywords or not category:
            raise ValueError("category/keywords cannot be blank")

        # If access_key is None or secret_key is None or associate_tag is None:
        if not access_key or not secret_key or not associate_tag:
            raise ValueError("Blank credentials.")

        qp = {}
        qp['Service'] = SERVICE
        qp['Operation'] = OPERATION
        qp['SearchIndex'] = category
        qp['Keywords'] = keywords

        return get_url_dict_cred(qp, access_key, secret_key, associate_tag, fmt_date)


def get_complete_url(category, keywords):
        "Get the complete url for given category and keywords. Fetch credentials from environ"
        if not keywords or not category:
            raise ValueError("category/keywords cannot be blank")

        # Get the access credentials from the environment
        access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        associate_tag = os.environ.get('AWS_ASSOCIATE_TAG')

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        fmt_date = t.strftime('%Y-%m-%dT%H:%M:%SZ')

        return get_url_defaults(category, keywords, access_key, secret_key, associate_tag, fmt_date)

if __name__ == '__main__':
        category = raw_input("Enter the SearchIndex [Books]: ")
        if not category:
            category = 'Books'
        keywords = raw_input("Enter the search keywords : ")
        print get_complete_url("Books", keywords)

