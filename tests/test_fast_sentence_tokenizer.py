from bo_sent_tokenizer import fast_tokenize

def test_fast_bo_sentence_tokenizer():
    """ main test example"""
    input_string = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ། ངའི་མིང་ལ་Thomas་ཟེར། ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།"
    expected_output = 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།\n ངའི་མིང་ལ་ ་ཟེར།\n ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།\n'
    output = fast_tokenize(input_string)
    assert output == expected_output

    """clean tibetan"""
    input_string = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།"
    expected_output = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n"
    output = fast_tokenize(input_string)
    assert output == expected_output
    
    """ tibetan with invalid tokens"""
    input_string = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།"
    expected_output = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།"
    output = fast_tokenize(input_string)
    assert output == expected_output

    input_string = "ཁྱེད་དེ་རིང་བདེམོཡིན་ནམ།"
    expected_output = "ཁྱེད་དེ་རིང་བདེམོཡིན་ནམ།"
    output = fast_tokenize(input_string)
    assert output == expected_output


    """tibetan with english"""
    input_string = "ངའི་མིང་ལ་Thomas་ཟེར།"
    expected_output = "ངའི་མིང་ལ་ ་ཟེར།"
    output = fast_tokenize(input_string)
    assert output == expected_output

    """tibetan with other language"""
    input_string = "རྒྱ་གར་ཧིན་དྷིའི་སྐད་ཡིག་ལ་གཅིག་ནི་एकཡིན་།"
    expected_output = "རྒྱ་གར་ཧིན་དྷིའི་སྐད་ཡིག་ལ་གཅིག་ནི་ ཡིན་།"
    output = fast_tokenize(input_string)
    assert output == expected_output

    """tibetan with non tibetan symbols"""
    input_string = "ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།"
    expected_output = "ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།\n"
    output = fast_tokenize(input_string)
    assert output == expected_output
    
