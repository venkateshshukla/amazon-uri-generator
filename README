Amazon Product Ad APIs URI Generator
===================================

Amazon Product Ad APIs uses HMAC Authentication for user authentication.

HMAC is `Keyed-Hash Message Authentication Code` and requires a secret key beforehand.
More can be read in the official [RFC2104](https://tools.ietf.org/html/rfc2104).

Assuming, you have the

1. Amazon Access Key
2. Amazon Secret Key
3. Amazon Associates Tag

Steps to use
============

1. Edit the `amazonKeys.sh` to add the above three information.
2. Source this file by `source amazonKeys.sh`. This will ensure that you have proper environmental variables.
3. If needed, edit the sign_paa.py file to set the appropriate hosts.
4. Run the `sign_paa.py` file, by using this command `python sign_paa.py`. Enter the SearchIndex and the Keywords.
5. The URL returned is the signed URL, that can be used to fetch the data using the Amazon Product Ad APIs.
6. List of SearchIndices can be found [here](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/localevalues.html)

Extensible
==========

There are many methods available in the sign_paa.py which can be used to sign any kind of requests.

Most notable of these are `get_url_dict_cred(query_dict, access_key=None, secret_key=None, associate_tag=None, fmt_date=None)`

Just pass a dictionary of the query parameters that need signing, along with credentials. The method would canonicalize the query params, sign them using the secret_key and return the complete url.

If the optional params are not passed, they are inferred from the environmental variables. If still not present, a `ValueError` is thrown.

Tests
=====

Test cases are present which are taken from the Amazon Docs [here](http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html#rest_detailedexample).
