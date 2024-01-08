#!/usr/bin/python3
import pep8 as pycodestyle


def test_pep8_conformance():
    """Test that models/base_model.py conforms to PEP8."""
    for path in ['models/base_model.py',
                    'tests/test_models/test_base_model.py']:
        errors = pycodestyle.Checker(path, show_source=True).check_all()
        print(errors)
            
test_pep8_conformance()