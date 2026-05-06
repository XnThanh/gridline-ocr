"""
Test suite for gridline OCR main processing.

Run all tests:              pytest tests/test.py -v
Run specific set:           pytest tests/test.py::TestSetA -v
Run specific image:         pytest tests/test.py::TestSetA::test[A1] -v
Run by keyword:             pytest tests/test.py -k "A1" -v
"""
import sys
import os
import pytest

# Add parent directory to path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import process_image


# Test data: maps image_id to (image_path, expected_slice_count)
# Format: "X#" -> ("setX/vocab-page-X#", expected_slices)
TEST_DATA = {
    "SetA": [
        ("A1", "setA/vocab-page-A1", 25),
        ("A2", "setA/vocab-page-A2", None),
        ("A3", "setA/vocab-page-A3", None),
        ("A4", "setA/vocab-page-A4", None),
        ("A5", "setA/vocab-page-A5", None),
        ("A6", "setA/vocab-page-A6", None),
    ],
    "SetB": [
        ("B1", "setB/vocab-page-B1", 13),
        ("B2", "setB/vocab-page-B2", None),
        ("B3", "setB/vocab-page-B3", None),
        ("B4", "setB/vocab-page-B4", None),
        ("B5", "setB/vocab-page-B5", None),
        ("B6", "setB/vocab-page-B6", None),
    ],
    "SetC": [
        ("C1", "setC/vocab-page-C1", 23),
    ],
    "SetD": [
        ("D1", "setD/vocab-page-D1", 16),
    ],
}


class TestSetA:
    """Tests for setA images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetA"],
        ids=[item[0] for item in TEST_DATA["SetA"]]
    )
    def test(self, image_id, image_path, expected_slices):
        """Dynamically run tests for each image in SetA"""
        row_slices = process_image(image_path, test=True)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetB:
    """Tests for setB images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetB"],
        ids=[item[0] for item in TEST_DATA["SetB"]]
    )
    def test(self, image_id, image_path, expected_slices):
        """Dynamically run tests for each image in SetB"""
        row_slices = process_image(image_path, test=True)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")


class TestSetC:
    """Tests for setC images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetC"],
        ids=[item[0] for item in TEST_DATA["SetC"]]
    )
    def test(self, image_id, image_path, expected_slices):
        """Dynamically run tests for each image in SetC"""
        row_slices = process_image(image_path, test=True)
        actual_slices = len(row_slices) if row_slices is not None else 0

        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetD:
    """Tests for setD images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetD"],
        ids=[item[0] for item in TEST_DATA["SetD"]]
    )
    def test(self, image_id, image_path, expected_slices):
        """Dynamically run tests for each image in SetD"""
        row_slices = process_image(image_path)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")


if __name__ == "__main__":
    # Allow running this file directly
    pytest.main([__file__, "-v"])

