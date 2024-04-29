from bo_sent_tokenizer import tokenize

def test_bo_sentence_tokenizer():
    """clean tibetan"""
    input_string = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།"
    expected_output = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n"
    assert tokenize(input_string) == expected_output

    """ tibetan with invalid tokens"""
    input_string = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།"
    expected_output = ""
    assert tokenize(input_string) == expected_output

    input_string = "ཁྱེད་དེ་རིང་བདེམོཡིན་ནམ།"
    expected_output = ""
    assert tokenize(input_string) == expected_output


    """tibetan with english"""
    input_string = "ངའི་མིང་ལ་Thomas་ཟེར།"
    expected_output = ""
    assert tokenize(input_string) == expected_output
    
    """tibetan with other language"""
    input_string = "རྒྱ་གར་ཧིན་དྷིའི་སྐད་ཡིག་ལ་གཅིག་ནི་एकཡིན་།"
    expected_output = ""
    assert tokenize(input_string) == expected_output

    """tibetan with non tibetan symbols"""
    input_string = "ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།"
    expected_output = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n"
    assert tokenize(input_string) == expected_output