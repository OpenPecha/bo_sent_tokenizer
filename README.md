
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">tibetan sentence tokenizer.</h3>

## Description

Tibetan sentence tokenizer designed specifically for data preparation.

## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@tenzin3](https://github.com/tenzin3)

## Installation 

```py
pip install git+https://github.com/OpenPecha/bo_sent_tokenizer.git
```

## Usage
```py
from bo_sent_tokenizer import tokenize

text = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ། ངའི་མིང་ལ་Thomas་ཟེར། ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།"

tokenized_text = tokenize(text)
print(tokenized_text) #Output:> 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\nཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n'


```

## Explanation 
The text 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།' is clean Tibetan text.

The text 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།' contains an illegal token 'བབབབབབབབནམ'.

The text 'ངའི་མིང་ལ་Thomas་ཟེར།' includes characters from another language.

The text 'ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།' contains non-Tibetan symbols '(', and ')'.

If the text is clean, it is retained. If a sentence contains an illegal token or characters from another language, that sentence is excluded. If a sentence contains non-Tibetan symbols, these symbols are filtered out, and the sentence is retained.
