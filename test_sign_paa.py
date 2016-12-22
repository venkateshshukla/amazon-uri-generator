import sign_paa
from pytest import raises

def test_canonicalize():
        query = "Service=AWSECommerceService&AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&Operation=ItemLookup&ItemId=0679722769&ResponseGroup=Images,ItemAttributes,Offers,Reviews&Version=2013-08-01&Timestamp=2014-08-18T12:00:00Z"
        expected = "AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews&Service=AWSECommerceService&Timestamp=2014-08-18T12%3A00%3A00Z&Version=2013-08-01"
        actual = sign_paa.canonicalize(query)
        assert actual == expected

def test_sort_qv_numeric():
        q = "Amazon,Is,A,Website,For,Selling,and,buying,goods,2,0,1"
        actual = sign_paa.sort_qp_numeric(q)
        expected = "0,1,2,A,Amazon,For,Is,Selling,Website,and,buying,goods"
        assert actual == expected, "Numeric sort does not work"

def test_sign_base64_enc():
        string_to_sign = "GET\nwebservices.amazon.com\n/onca/xml\nAWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews&Service=AWSECommerceService&Timestamp=2014-08-18T12%3A00%3A00Z&Version=2013-08-01"
        key = "1234567890"
        actual = sign_paa.sign_base64_enc(key, string_to_sign)
        expected = "j7bZM0LXZ9eXeZruTqWm2DIvDYVUU3wxPPpp%2BiXxzQc%3D"
        assert actual == expected

def test_sign_base64():
        string_to_sign = "GET\nwebservices.amazon.com\n/onca/xml\nAWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews&Service=AWSECommerceService&Timestamp=2014-08-18T12%3A00%3A00Z&Version=2013-08-01"
        key = "1234567890"
        actual = sign_paa.sign_base64(key, string_to_sign)
        expected = "j7bZM0LXZ9eXeZruTqWm2DIvDYVUU3wxPPpp+iXxzQc="
        assert actual == expected

def test_sign_hex():
        string_to_sign = "GET\nwebservices.amazon.com\n/onca/xml\nAWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews&Service=AWSECommerceService&Timestamp=2014-08-18T12%3A00%3A00Z&Version=2013-08-01"
        key = "1234567890"
        actual = sign_paa.sign_hex(key, string_to_sign)
        expected = "8fb6d93342d767d797799aee4ea5a6d8322f0d8554537c313cfa69fa25f1cd07"
        assert actual == expected

def test_get_signature():
        sign_paa.HOST = "webservices.amazon.com"
        sk = "1234567890"
        qp = "Service=AWSECommerceService&AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&Operation=ItemLookup&ItemId=0679722769&ResponseGroup=Images,ItemAttributes,Offers,Reviews&Version=2013-08-01&Timestamp=2014-08-18T12:00:00Z"
        actual = sign_paa.get_signature(sk, qp)
        expected = "j7bZM0LXZ9eXeZruTqWm2DIvDYVUU3wxPPpp%2BiXxzQc%3D"
        assert actual == expected


def test_get_url_dict_cred():
        sign_paa.HOST = "webservices.amazon.com"
        sk = "1234567890"
        ak = "AKIAIOSFODNN7EXAMPLE"
        at = "mytag-20"
        fmt_date = "2014-08-18T12:00:00Z"
        qd = {}
        qd['Service'] = "AWSECommerceService"
        qd['Operation'] = "ItemLookup"
        qd["ItemId"] = "0679722769"
        qd["ResponseGroup"] = "ItemAttributes,Offers,Images,Reviews"
        qd["Version"] = "2013-08-01"
        actual = sign_paa.get_url_dict_cred(qd, ak, sk, at, fmt_date)
        expected = "http://webservices.amazon.com/onca/xml?AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&AssociateTag=mytag-20&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews&Service=AWSECommerceService&Timestamp=2014-08-18T12%3A00%3A00Z&Version=2013-08-01&Signature=j7bZM0LXZ9eXeZruTqWm2DIvDYVUU3wxPPpp%2BiXxzQc%3D"
        assert actual == expected
