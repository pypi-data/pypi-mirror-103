# coding: utf-8

"""
    MailSlurp API

    MailSlurp is an API for sending and receiving emails from dynamically allocated email addresses. It's designed for developers and QA teams to test applications, process inbound emails, send templated notifications, attachments, and more.   ## Resources - [Homepage](https://www.mailslurp.com) - Get an [API KEY](https://app.mailslurp.com/sign-up/) - Generated [SDK Clients](https://www.mailslurp.com/docs/) - [Examples](https://github.com/mailslurp/examples) repository   # noqa: E501

    The version of the OpenAPI document: 6.5.2
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from mailslurp_client.configuration import Configuration


class DNSLookupOptions(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'hostname': 'str',
        'omit_final_dns_dot': 'bool',
        'record_types': 'list[str]'
    }

    attribute_map = {
        'hostname': 'hostname',
        'omit_final_dns_dot': 'omitFinalDNSDot',
        'record_types': 'recordTypes'
    }

    def __init__(self, hostname=None, omit_final_dns_dot=None, record_types=None, local_vars_configuration=None):  # noqa: E501
        """DNSLookupOptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._hostname = None
        self._omit_final_dns_dot = None
        self._record_types = None
        self.discriminator = None

        if hostname is not None:
            self.hostname = hostname
        if omit_final_dns_dot is not None:
            self.omit_final_dns_dot = omit_final_dns_dot
        if record_types is not None:
            self.record_types = record_types

    @property
    def hostname(self):
        """Gets the hostname of this DNSLookupOptions.  # noqa: E501

        List of record types you wish to query such as MX, DNS, TXT, NS, A etc.  # noqa: E501

        :return: The hostname of this DNSLookupOptions.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """Sets the hostname of this DNSLookupOptions.

        List of record types you wish to query such as MX, DNS, TXT, NS, A etc.  # noqa: E501

        :param hostname: The hostname of this DNSLookupOptions.  # noqa: E501
        :type: str
        """

        self._hostname = hostname

    @property
    def omit_final_dns_dot(self):
        """Gets the omit_final_dns_dot of this DNSLookupOptions.  # noqa: E501

        Optionally control whether to omit the final dot in full DNS name values.  # noqa: E501

        :return: The omit_final_dns_dot of this DNSLookupOptions.  # noqa: E501
        :rtype: bool
        """
        return self._omit_final_dns_dot

    @omit_final_dns_dot.setter
    def omit_final_dns_dot(self, omit_final_dns_dot):
        """Sets the omit_final_dns_dot of this DNSLookupOptions.

        Optionally control whether to omit the final dot in full DNS name values.  # noqa: E501

        :param omit_final_dns_dot: The omit_final_dns_dot of this DNSLookupOptions.  # noqa: E501
        :type: bool
        """

        self._omit_final_dns_dot = omit_final_dns_dot

    @property
    def record_types(self):
        """Gets the record_types of this DNSLookupOptions.  # noqa: E501

        List of record types you wish to query such as MX, DNS, TXT, NS, A etc.  # noqa: E501

        :return: The record_types of this DNSLookupOptions.  # noqa: E501
        :rtype: list[str]
        """
        return self._record_types

    @record_types.setter
    def record_types(self, record_types):
        """Sets the record_types of this DNSLookupOptions.

        List of record types you wish to query such as MX, DNS, TXT, NS, A etc.  # noqa: E501

        :param record_types: The record_types of this DNSLookupOptions.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTR", "HINFO", "MINFO", "MX", "TXT", "RP", "AFSDB", "X25", "ISDN", "RT", "NSAP", "NSAP_PTR", "SIG", "KEY", "PX", "GPOS", "AAAA", "LOC", "NXT", "EID", "NIMLOC", "SRV", "ATMA", "NAPTR", "KX", "CERT", "A6", "DNAME", "SINK", "OPT", "APL", "DS", "SSHFP", "IPSECKEY", "RRSIG", "NSEC", "DNSKEY", "DHCID", "NSEC3", "NSEC3PARAM", "TLSA", "SMIMEA", "HIP", "NINFO", "RKEY", "TALINK", "CDS", "CDNSKEY", "OPENPGPKEY", "CSYNC", "ZONEMD", "SVCB", "HTTPS", "SPF", "UINFO", "UID", "GID", "UNSPEC", "NID", "L32", "L64", "LP", "EUI48", "EUI64", "TKEY", "TSIG", "IXFR", "AXFR", "MAILB", "MAILA", "ANY", "URI", "CAA", "AVC", "DOA", "AMTRELAY", "TA", "DLV"]  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                not set(record_types).issubset(set(allowed_values))):  # noqa: E501
            raise ValueError(
                "Invalid values for `record_types` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(record_types) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._record_types = record_types

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DNSLookupOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DNSLookupOptions):
            return True

        return self.to_dict() != other.to_dict()
