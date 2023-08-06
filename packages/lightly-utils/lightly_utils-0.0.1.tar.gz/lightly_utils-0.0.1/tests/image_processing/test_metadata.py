import json
import unittest
import tempfile
from PIL import Image
import numpy as np

from lightly_utils.image_processing import Metadata


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except Exception as e:
        return False


class TestMetadata(unittest.TestCase):

    def test_metadata_corrupted(self):
        image = None
        metadata = Metadata(image)
        metadata = metadata.to_dict()

        self.assertTrue(metadata['is_corrupted'])
        self.assertNotEqual(metadata['corruption'], 'e')
        for key, item in metadata.items():
            self.assertTrue(is_jsonable(item))

    def test_metadata(self):
        image = Image.new('RGB', (100, 100))
        metadata = Metadata(image)
        metadata = metadata.to_dict()

        self.assertFalse(metadata['is_corrupted'])
        for key, item in metadata.items():
            self.assertTrue(is_jsonable(item))

    def test_metadata_nonzero(self):
        arr = np.random.randint(0, 255, (100, 100, 3))
        image = Image.fromarray(arr, 'RGB')
        metadata = Metadata(image)
        metadata = metadata.to_dict()

        self.assertFalse(metadata['is_corrupted'])
        for key, item in metadata.items():
            self.assertTrue(is_jsonable(item))