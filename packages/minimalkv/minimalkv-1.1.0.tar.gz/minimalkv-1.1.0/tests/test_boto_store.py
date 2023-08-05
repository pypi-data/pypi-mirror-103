#!/usr/bin/env python

import os

import pytest

boto = pytest.importorskip("boto")
from basic_store import BasicStore
from bucket_manager import boto_bucket, boto_credentials
from conftest import ExtendedKeyspaceTests
from url_store import UrlStore

from minimalkv._compat import BytesIO
from minimalkv.contrib import ExtendedKeyspaceMixin
from minimalkv.net.botostore import BotoStore


@pytest.fixture(
    params=boto_credentials, ids=[c["access_key"] for c in boto_credentials]
)
def credentials(request):
    return request.param


@pytest.yield_fixture()
def bucket(credentials):
    with boto_bucket(**credentials) as bucket:
        yield bucket


class TestBotoStorage(BasicStore, UrlStore):
    @pytest.fixture(params=[True, False])
    def reduced_redundancy(self, request):
        return request.param

    @pytest.fixture
    def storage_class(self, reduced_redundancy):
        return "REDUCED_REDUNDANCY" if reduced_redundancy else "STANDARD"

    @pytest.fixture(params=["", "/test-prefix"])
    def prefix(self, request):
        return request.param

    @pytest.fixture
    def store(self, bucket, prefix, reduced_redundancy):
        return BotoStore(bucket, prefix, reduced_redundancy=reduced_redundancy)

    # Disable max key length test as it leads to problems with minio
    test_max_key_length = None

    def test_get_filename_nonexistant(self, store, key, tmp_path):
        # NOTE: boto misbehaves here and tries to erase the target file
        # the parent tests use /dev/null, which you really should not try
        # to os.remove!
        with pytest.raises(KeyError):
            store.get_file(key, os.path.join(str(tmp_path), "a"))

    def test_key_error_on_nonexistant_get_filename(self, store, key, tmp_path):
        with pytest.raises(KeyError):
            store.get_file(key, os.path.join(str(tmp_path), "a"))

    def test_storage_class_put(self, store, prefix, key, value, storage_class, bucket):
        store.put(key, value)

        keyname = prefix + key

        if storage_class != "STANDARD":
            pytest.xfail("boto does not support checking the storage class?")

        assert bucket.lookup(keyname).storage_class == storage_class

    def test_storage_class_putfile(
        self, store, prefix, key, value, storage_class, bucket
    ):
        store.put_file(key, BytesIO(value))

        keyname = prefix + key

        if storage_class != "STANDARD":
            pytest.xfail("boto does not support checking the storage class?")
        assert bucket.lookup(keyname).storage_class == storage_class


class TestExtendedKeyspaceBotoStore(TestBotoStorage, ExtendedKeyspaceTests):
    @pytest.fixture
    def store(self, bucket, prefix, reduced_redundancy):
        class ExtendedKeyspaceStore(ExtendedKeyspaceMixin, BotoStore):
            pass

        return ExtendedKeyspaceStore(
            bucket, prefix, reduced_redundancy=reduced_redundancy
        )
