import time

from aliyunsdkcore import client as ali_client
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkkms.request.v20160120 import GenerateDataKeyRequest, DecryptRequest
import json
import logging

from .aes import CryptoAES

logger = logging.getLogger(__name__)


def generate_data_key(clt: AcsClient, key_alias: str):
    request = GenerateDataKeyRequest.GenerateDataKeyRequest()
    request.set_accept_format('JSON')
    request.set_KeyId(key_alias)
    request.set_NumberOfBytes(32)
    response = json.loads(do_action(clt, request))

    edk = response["CiphertextBlob"]
    dk = response["Plaintext"]
    return dk, edk


def decrypt_data_key(clt: AcsClient, ciphertext: str) -> str:
    request = DecryptRequest.DecryptRequest()
    request.set_accept_format('JSON')
    request.set_CiphertextBlob(ciphertext)
    response = json.loads(do_action(clt, request))
    return response.get("Plaintext")


def do_action(clt: AcsClient, req, retry=0):
    """
    指数退避获取结果
    """
    try:
        resp = clt.do_action_with_exception(req)
        return resp
    except ServerException as e:
        logging.critical("query kms error, %s" % e, )
        if e.http_status != 200 and retry < 3:
            time.sleep(pow(2, retry))
            return do_action(clt, req, retry + 1)

        raise e


_crypto = {}


def init(kms):
    keys = {'access_id', 'access_secret', 'region_id', 'edk'} - kms.keys()

    if len(keys) > 0:
        raise KeyError("not found %s in KMS config" % ','.join(keys))

    client = ali_client.AcsClient(kms['access_id'], kms['access_secret'], kms['region_id'])
    if isinstance(kms['edk'], str):
        kms['edk'] = {'default': kms['edk']}

    global _crypto
    for k, v in kms['edk'].items():
        key = decrypt_data_key(client, v)
        _crypto[k] = CryptoAES(key)


def crypto_client(key='default') -> CryptoAES:
    return _crypto.get(key)


# if __name__ == '__main__':
#     print(generate_data_key(client, "alias/main"))
