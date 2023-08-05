import pytest
import unittest
from unittest.mock import patch

from requests_cache.backends import DynamoDbDict
from tests.conftest import AWS_OPTIONS, fail_if_no_connection
from tests.integration.test_backends import BaseStorageTestCase

# Run this test module last, since the DynamoDB container takes the longest to initialize
pytestmark = pytest.mark.order(-1)


@pytest.fixture(scope='module', autouse=True)
@fail_if_no_connection
def ensure_connection():
    """Fail all tests in this module if DynamoDB is not running"""
    import boto3

    client = boto3.client('dynamodb', **AWS_OPTIONS)
    client.describe_limits()


class DynamoDbDictWrapper(DynamoDbDict):
    def __init__(self, namespace, collection_name='dynamodb_dict_data', **options):
        super().__init__(namespace, collection_name, **options, **AWS_OPTIONS)


class DynamoDbTestCase(BaseStorageTestCase, unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            storage_class=DynamoDbDictWrapper,
            picklable=True,
            **kwargs,
        )


@patch('requests_cache.backends.dynamodb.boto3.resource')
def test_connection_kwargs(mock_resource):
    """A spot check to make sure optional connection kwargs gets passed to connection"""
    DynamoDbDict('test', region_name='us-east-2', invalid_kwarg='???')
    mock_resource.assert_called_with('dynamodb', region_name='us-east-2')
