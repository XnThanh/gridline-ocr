"""
Test suite for gridline OCR main processing.

Run all tests:              pytest tests/test.py -v
Run specific set:           pytest tests/test.py::TestSetA -v
Run specific image:         pytest tests/test.py::TestSetA::test[A1] -v
Run by keyword:             pytest tests/test.py -k "A1" -v

Flags:
--save-profiles: Save projection profile plots (default is False)
-s: show print statements in test output if test passed
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
        ("C2", "setC/vocab-page-C2", None),
        ("C3", "setC/vocab-page-C3", None),
        ("C4", "setC/vocab-page-C4", None),
        ("C5", "setC/vocab-page-C5", None),
    ],
    "SetD": [
        ("D1", "setD/vocab-page-D1", 16),
        ("D2", "setD/vocab-page-D2", None),
        ("D3", "setD/vocab-page-D3", None),
        ("D4", "setD/vocab-page-D4", None),
        ("D5", "setD/vocab-page-D5", None),
        ("D6", "setD/vocab-page-D6", None),
        ("D7", "setD/vocab-page-D7", None),
    ],
    "SetE": [
        ("E1", "setE/vocab-page-E1", 12),
        ("E2", "setE/vocab-page-E2", None),
        ("E3", "setE/vocab-page-E3", None),
        ("E4", "setE/vocab-page-E4", None),
        ("E5", "setE/vocab-page-E5", None),
        ("E6", "setE/vocab-page-E6", None),
        ("E7", "setE/vocab-page-E7", None),
        ("E8", "setE/vocab-page-E8", None),
        ("E9", "setE/vocab-page-E9", None),
        ("E10", "setE/vocab-page-E10", None),
    ],
    "SetF": [
        ("F1", "setF/vocab-page-F1", 17),
        ("F2", "setF/vocab-page-F2", None),
        ("F3", "setF/vocab-page-F3", None),
        ("F4", "setF/vocab-page-F4", None),
        ("F5", "setF/vocab-page-F5", None),
        ("F6", "setF/vocab-page-F6", None),
        ("F7", "setF/vocab-page-F7", None),
        ("F8", "setF/vocab-page-F8", None),
    ],
    "SetG": [
        ("G1", "setG/vocab-page-G1", 20),
        ("G2", "setG/vocab-page-G2", 33),
    ],
    "SetH": [
        ("H1", "setH/vocab-page-H1", 26),
        ("H2", "setH/vocab-page-H2", None),
        ("H3", "setH/vocab-page-H3", None),
    ],
    "SetI": [
        ("I1", "setI/vocab-page-I1", 14),
        ("I2", "setI/vocab-page-I2", None),
        ("I4", "setI/vocab-page-I4", None),
        ("I3", "setI/vocab-page-I3", None),
        ("I5", "setI/vocab-page-I5", None),
        ("I6", "setI/vocab-page-I6", None),
        ("I7", "setI/vocab-page-I7", None),
        ("I8", "setI/vocab-page-I8", None),
        ("I9", "setI/vocab-page-I9", None),
        # ("I10", "setI/vocab-page-I10", None),
        # ("I11", "setI/vocab-page-I11", None),
    ],
}


class TestSetA:
    """Tests for setA images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetA"],
        ids=[item[0] for item in TEST_DATA["SetA"]]
    )
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetA"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
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
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetB"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
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
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetC"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
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
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetD"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetE:
    """Tests for setE images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetE"],
        ids=[item[0] for item in TEST_DATA["SetE"]]
    )
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetE"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetF:
    """Tests for setF images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetF"],
        ids=[item[0] for item in TEST_DATA["SetF"]]
    )
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetF"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetG:
    """Tests for setG images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetG"],
        ids=[item[0] for item in TEST_DATA["SetG"]]
    )
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetG"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetH:
    """Tests for setH images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetH"],
        ids=[item[0] for item in TEST_DATA["SetH"]]
    )
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetH"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

class TestSetI:
    """Tests for setI images - parametrized for all images in the set"""
    
    @pytest.mark.parametrize(
        "image_id,image_path,expected_slices",
        TEST_DATA["SetI"],
        ids=[item[0] for item in TEST_DATA["SetI"]]
    )
    def test(self, image_id, image_path, expected_slices, save_profiles):
        """Dynamically run tests for each image in SetI"""
        row_slices = process_image(image_path, save_profiles=save_profiles)
        actual_slices = len(row_slices) if row_slices is not None else 0
        
        if expected_slices is None:
            raise Exception(f"{image_id}: No expected slice count provided. Please update TEST_DATA with the expected number of slices.")

        assert actual_slices == expected_slices, \
            f"{image_id}: Expected {expected_slices} slices, got {actual_slices}"
        
        print(f"✓ {image_id} passed: {actual_slices} row slices generated")

if __name__ == "__main__":
    # Allow running this file directly
    pytest.main([__file__, "-v"])

