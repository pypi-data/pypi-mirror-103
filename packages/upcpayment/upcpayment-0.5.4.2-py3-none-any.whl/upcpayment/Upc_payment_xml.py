import datetime, random, string
import errno
import os
from OpenSSL import crypto
import base64
import xml.etree.ElementTree as ET
from io import BytesIO

class FileNotPrivateKey(Exception):
    def __init__(self, message="You have to use private key(*.pem)"):
        self.message = message
        super().__init__(self.message)

class AltCurrencyAmountNullException(Exception):
    def __init__(self, message="Currency or amount is null"):
        self.message = message
        super().__init__(self.message)

class MPIEnrolRequest(object):
    def __init__(self, merchantId, terminalid, total_amount, currency, order_id, purchase_desc, card_num, exp_year, exp_month, **kwargs):
        self.version = 1
        self.merchantId = merchantId
        self.terminalid = terminalid
        self.total_amount = total_amount
        self.currency = currency
        self.order_id = order_id
        self.signature = ''
        self.purchase_desc = purchase_desc
        self.card_num = card_num
        self.exp_year = exp_year
        self.exp_month = exp_month
        self.device_category = kwargs.get('device_category', 0)

    def generate_xml(self):
        ECommerceConnect = ET.Element('ECommerceConnect')
        ECommerceConnect.set('xmlns:xenc', 'http://www.w3.org/2001/04/xmlenc#')
        ECommerceConnect.set('xmlns:ds', 'http://www.w3.org/2000/09/xmldsig#')
        ECommerceConnect.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ECommerceConnect.set('xsi:noNamespaceSchemaLocation', 'https://secure.upc.ua/go/pub/schema/xmlpay-1.2.xsd')
        Message = ET.SubElement(ECommerceConnect, 'Message')
        Message.set('id', self.order_id)
        Message.set('version', '1.0')
        XMLMPIRequest = ET.SubElement(Message, 'XMLMPIRequest')
        MerchantID = ET.SubElement(XMLMPIRequest, 'MerchantID')
        MerchantID.text = self.merchantId
        TerminalID = ET.SubElement(XMLMPIRequest, 'TerminalID')
        TerminalID.text = self.terminalid
        MPIRequest = ET.SubElement(XMLMPIRequest, 'MPIRequest')
        MPIRequest.set('id', self.order_id)
        MPIEnrolRequest_node = ET.SubElement(MPIRequest, 'MPIEnrolRequest')
        CardNum = ET.SubElement(MPIEnrolRequest_node, 'CardNum')
        CardNum.text = self.card_num
        ExpYear = ET.SubElement(MPIEnrolRequest_node, 'ExpYear')
        ExpYear.text = self.exp_year
        ExpMonth = ET.SubElement(MPIEnrolRequest_node, 'ExpMonth')
        ExpMonth.text = self.exp_month
        TotalAmount = ET.SubElement(MPIEnrolRequest_node, 'TotalAmount')
        TotalAmount.text = self.total_amount
        Currency = ET.SubElement(MPIEnrolRequest_node, 'Currency')
        Currency.text = self.currency
        Description = ET.SubElement(MPIEnrolRequest_node, 'Description')
        Description.text = self.purchase_desc
        DeviceCategory = ET.SubElement(MPIEnrolRequest_node, 'DeviceCategory')
        DeviceCategory.text = self.device_category

        Signature = ET.SubElement(ECommerceConnect, 'Signature')

        return ElementTree.tostring(ECommerceConnect, encoding='utf8', method='xml')

    def generate_signature(self, private_key):
        data = "{};{};{};".format(self.merchantId, self.terminalid, self.purchase_time)
        if self.delay != '':
            data += "{},{};".format(self.order_id, self.delay)
        else:
            data += "{};".format(self.order_id)
        
        if self.alt_currency != '' and self.alt_total_amount != '':
            data += "{},{};{},{};".format(self.currency, self.alt_currency, self.total_amount, self.alt_total_amount)
        elif self.alt_currency == '' and self.alt_total_amount == '':
            data += "{};{};".format(self.currency, self.total_amount)
        else:
            raise AltCurrencyAmountNullException()

        data += "{};".format(self.sd)

        if self.ref3 != '':
            data += "{};".format(self.ref3)

        if os.path.exists(private_key): 
            key_id = open(private_key).read();
            if key_id.startswith('-----BEGIN RSA PRIVATE KEY'):
                priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_id)
                signature_bin_str = crypto.sign(priv_key, data, 'sha1')
                base64_bytes = base64.b64encode(signature_bin_str)
                base64_message = base64_bytes.decode('ascii')
                self.signature = base64_message
            else:
                raise FileNotPrivateKey()
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), private_key)
        