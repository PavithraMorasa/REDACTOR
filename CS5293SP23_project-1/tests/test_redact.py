import pytest
import os
import tempfile
from project1.functions import redact_names, redact_genders, redact_dates, redact_phone_numbers, redact_address, redact_files_in_directory

def test_redact_names():
    # Test with sample input
    text = "Alex Johnson"
    expected_output = "████████████"
    assert redact_names(text) == expected_output

    # Test with input that contains only email addresses
    text = "johndoe@example.com, janedoe@example.com"
    expected_output = "johndoe@example.com, janedoe@example.com"
    assert redact_names(text) == expected_output
def test_redact_genders():
    sample_text = "My sister loves to watch movies. He always gets emotional during romantic scenes. The actor performed his role perfectly."
    expected_output = "My ██████ loves to watch movies. ██ always gets emotional during romantic scenes. The █████ performed ███ role perfectly."
    assert redact_genders(sample_text) == expected_output
def test_redact_dates():
    sample_text = "The dates are 15 Apr 2023"
    expected_output = "The dates are ███████████████████████████"
    assert redact_dates(sample_text) == expected_output
def test_redact_phone_numbers():
    sample_number = "Alex's number is 123-456-7890 and he tried to call the number +1 1234567890 but the call was forwarded"
    expected_output = "Alex's number is █████████████████ and he tried to call the number ████████████████ but the call was forwarded"
    assert redact_phone_numbers(sample_number) == expected_output
def test_redact_address():
    text = "John Doe,Los Angeles, CA 90001, is a new customer."
    expected_output = "John Doe,Los Angeles, CA █████, is a new customer."
    assert redact_address(text) == expected_output
def test_redact_files_in_directory():
    # create a temporary directory and files for testing
    test_dir = tempfile.mkdtemp()
    test_file1 = os.path.join(test_dir, 'test_file1.txt')
    with open(test_file1, 'w') as f1:
        f1.write('John Doe (male) called 555-1234 on 01/01/2022 from 123 Main St, San Francisco, CA 94123')
    
    # run the function on the test directory
    redact_files_in_directory(test_dir)
    
    # check that the redacted files were created with the expected content
    with open(os.path.splitext(test_file1)[0] + '.redacted', 'r') as f1r:
        redacted_content1 = f1r.read()
        expected_content1 = '████████ (████) █████████████████████-1234 on ███████████████████████ █████████████████████ Main St, San Francisco, CA █████'
        assert redacted_content1 == expected_content1
