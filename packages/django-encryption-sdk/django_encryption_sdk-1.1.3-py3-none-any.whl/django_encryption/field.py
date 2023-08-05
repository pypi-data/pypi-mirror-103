import django.dispatch
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from django_encryption.context import Context
from django_encryption.client import crypto_client

import logging

logger = logging.getLogger(__name__)
plain_sig = django.dispatch.Signal()


class DataKeeper(object):
    def __init__(self, plain_text=None, cipher_text=None, mask_type=None, field=None, edk_key='default') -> None:
        self._plain_text = plain_text
        self._cipher_text = cipher_text
        self._model = self._field_name = self._verbose_name = None
        if field is not None:
            self._model = field.model._meta.db_table
            self._field_name = field.column
            self._verbose_name = field.verbose_name
        self._mask_type = mask_type if mask_type is not None else ""
        self._edk_key = edk_key
        self._id = None

    def plain(self):
        """
        获取原始明文，获取增加额外记录
        """
        try:
            plain_sig.send(sender=self.__class__, model=self._model, filed_name=self._field_name,
                           verbose_name=self._verbose_name, mask_text=self.mask(), cipher_text=self.cipher(), id=self._id,
                           context=Context.get())
        except Exception as e:
            logging.warn("send plain sig error, %s" % e, )

        if self._plain_text is not None:
            return self._plain_text

        return '' if self._cipher_text is None else crypto_client(self._edk_key).decrypt(self._cipher_text)

    def cipher(self):
        """
        获取密文
        """
        if self._cipher_text is not None:
            return self._cipher_text
        if self._plain_text is not None:
            self._cipher_text = '' if self._plain_text == '' else crypto_client(self._edk_key).encrypt(self._plain_text)
            return self._cipher_text
        return None

    def mask(self, mask_type=None):
        """
        获取掩码信息
        """
        plain_info = self._plain_text if self._plain_text is not None else crypto_client(self._edk_key).decrypt(self._cipher_text)

        if plain_info == '':
            return ''

        mask_type = mask_type if mask_type is not None else self._mask_type
        # 自动判断掩码
        if mask_type == 'auto':
            """
            至少保证四位是加密的，优先后面原始显示，最多前3后4
            """
            if len(plain_info) <= 4:
                return "*"
            last_total = len(plain_info)-4
            before = 3 if last_total//2 > 3 else last_total//2
            after = 4 if last_total - before > 4 else last_total - before
            return plain_info[:before] + "****" + plain_info[len(plain_info) - after:]

        if len(mask_type) <= 1:
            return "*"

        mask_type = mask_type.split("*")
        before = int(mask_type[0]) if mask_type[0].isdigit() else 0
        after = int(mask_type[-1]) if mask_type[-1].isdigit() else 0

        if len(plain_info) <= (before + after):
            return "***"

        mask_text = "***" if mask_type.count("") == 0 else "*" * (len(plain_info) - before - after)
        return plain_info[:before] + mask_text + plain_info[len(plain_info) - after:]

    def __str__(self) -> str:
        return self.mask()

    def __repr__(self) -> str:
        return self.mask()


class DataKeeperCharField(CharField):
    description = _("Plain Data Keeper String (base CharField)")

    def __init__(self, *args, mask_type="auto", edk_key='default', **kwargs):
        """
        mask_type: [num1] (*|**) [num2]
        num1:前num1位明文显示
        (*|**): *表示固定三个*，(即***)，**表示按遮挡长度显示*
        num2: 后num2位明文显示
        """
        self.mask_type = mask_type
        self.edk_key = edk_key
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        将会在从数据库中载入的生命周期中调用，包括聚集和 values() 调用
        """
        if value is None:
            return value
        return self.to_python(value)

    def to_python(self, value):
        """
        回显python
        """
        if value is None:
            return value

        if isinstance(value, DataKeeper):
            return value

        return DataKeeper(cipher_text=value, mask_type=self.mask_type, edk_key=self.edk_key, field=self)

    def get_prep_value(self, value):
        """
        落库
        """
        if value is None:
            return ""
        if isinstance(value, DataKeeper):
            return value.cipher()

        dk = DataKeeper(plain_text=value)
        return dk.cipher()

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if self.mask_type != "auto":
            kwargs["mask_type"] = self.mask_type
        if self.edk_key != 'default':
            kwargs["edk_key"] = self.edk_key
        return name, path, args, kwargs
