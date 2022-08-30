#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from ll-sdk.utils.config_api_helper.cert import SSLCertObj

shortname = "testname"
certificate = "-----BEGIN CERTIFICATE-----\n-----END CERTIFICATE-----"
private_key = "-----BEGIN RSA PRIVATE KEY-----\n-----END RSA PRIVATE KEY-----"


@pytest.fixture(scope="function")
def ssl_cert():
    """Fixture for generating default SSLCert object"""
    cert = SSLCertObj()
    cert.generate_default(shortname, certificate, private_key)
    return cert


def test_generate_default():
    """Test: Generate default SSLCert object

    Steps:
    1. Generate default SSLCert object
    2. Compare expected result with actual

    Result:
    OK: sslcert object is generated as expected
    """
    expected = {
        "body": {
            "certName": "test_name",
            "cert": certificate,
            "certKey": private_key,
            "contentType": "default"
        },
        "accounts": [
            {"shortname": shortname}
        ]
    }
    ssl_cert = SSLCertObj()
    ssl_cert.generate_default(shortname, certificate, private_key, cert_name="test_name")
    assert expected == ssl_cert


def test_cert_name(ssl_cert):
    """Test: Set name in SSLCert object

    Steps:
    1. Set name in SSLCert object
    2. Compare expected result with actual

    Result:
    OK: sslcert object is updated as expected
    """
    ssl_cert.cert_name = "updated_name"
    assert "updated_name" == ssl_cert.cert_name
    assert ssl_cert.cert_name == ssl_cert["body"]["certName"]


def test_cert(ssl_cert):
    """Test: Set cert value in SSLCert object

    Steps:
    1. Set cert value in SSLCert object
    2. Compare expected result with actual

    Result:
    OK: sslcert object is updated as expected
    """
    ssl_cert.cert = "-----BEGIN CERTIFICATE-----\nTest\n-----END CERTIFICATE-----"
    assert "-----BEGIN CERTIFICATE-----\nTest\n-----END CERTIFICATE-----" == ssl_cert.cert
    assert ssl_cert.cert == ssl_cert["body"]["cert"]


def test_cert_key(ssl_cert):
    """Test: Set certKey value in SSLCert object

    Steps:
    1. Set certKey value in SSLCert object
    2. Compare expected result with actual

    Result:
    OK: sslcert object is updated as expected
    """
    ssl_cert.cert_key = "-----BEGIN RSA PRIVATE KEY-----\nTestKey\n-----END RSA PRIVATE KEY-----"
    assert "-----BEGIN RSA PRIVATE KEY-----\nTestKey\n-----END RSA PRIVATE KEY-----" == ssl_cert.cert_key
    assert ssl_cert.cert_key == ssl_cert["body"]["certKey"]


def test_intermediate_certs(ssl_cert):
    """Test: Set intermediate certificate in SSLCert object

    Steps:
    1. Set intermediate cert in SSLCert object
    2. Compare expected result with actual

    Result:
    OK: sslcert object is updated as expected
    """
    inter_cert = "-----BEGIN CERTIFICATE-----\nIntermediateCertificate\n-----END CERTIFICATE-----"
    ssl_cert.intermediate_certs = inter_cert
    assert "{0}\n{1}".format(certificate, inter_cert) == ssl_cert["body"]["cert"]


def test_shortname(ssl_cert):
    """Test: Set shortname in SSLCert object

    Steps:
    1. Set shortname in SSLCert object
    2. Compare expected result with actual

    Result:
    OK: sslcert object is updated as expected
    """
    ssl_cert.shortname = "somename"
    assert "somename" == ssl_cert.shortname
    assert ssl_cert.shortname == ssl_cert["accounts"][0]["shortname"]


def test_fingerprint(ssl_cert):
    """Test: Get fingerprints from SSLCert object

    Steps:
    1. Get fingerprints from SSLCert object
    2. Compare expected result with actual

    Result:
    OK: retrieved value is the same as expected
    """
    ssl_cert["body"]["fingerprints"] = ["www.example.com"]
    assert ["www.example.com"] == ssl_cert.fingerprint
