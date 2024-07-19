
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

Important Note: If speed is essential, prioritize sentence segmentation over sentence tokenization.


### 1.Sentence tokenization

```py
from bo_sent_tokenizer import tokenize

text = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ། ངའི་མིང་ལ་Thomas་ཟེར། ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།"

tokenized_text = tokenize(text)
print(tokenized_text) #Output:> 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\nཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n'


```

### Explanation
code is refered from [op_mt_tools](https://github.com/OpenPecha/mt-training-data-prep-tools/blob/main/src/op_mt_tools/tokenizers.py) and
made minor changes to get the following desired output.

### Output Explanation
The text 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།' is clean Tibetan text.

The text 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།' contains an illegal token 'བབབབབབབབནམ'.

The text 'ངའི་མིང་ལ་Thomas་ཟེར།' includes characters from another language.

The text 'ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།' contains non-Tibetan symbols '(', and ')'.

If the text is clean, it is retained. If a sentence contains an illegal token or characters from another language, that sentence is excluded. If a sentence contains non-Tibetan symbols, these symbols are filtered out, and the sentence is retained.

### 2.Sentence segmentation

```py
from bo_sent_tokenizer import segment

text = "ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\n ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ། ངའི་མིང་ལ་Thomas་ཟེར། ཁྱེད་དེ་རིང་(བདེ་མོ་)ཡིན་ནམ།"

segmented_text = segment(text)
print(segmented_text) #Output:> 'ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ།\nཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ།\nངའི་མིང་ལ་ ་ཟེར།\nཁྱེད་དེ་རིང(བདེ་མོ་)ཡིན་ནམ།\n'

```

### Terms:

**Closing Punctuation**: Characters in the Tibetan language that symbolize the end of a sentence, similar to a full stop in English.

**Opening Punctuation**: Characters in the Tibetan language that symbolize the start of a sentence.

### How Sentence Segmentation Works:

1. **Preprocessing**: All carriage returns and new lines are removed from the string.

2. **Splitting into Parts**: The preprocessed text is then split by closing punctuation using a regular expression.

3. **Joining the Parts**:
   - Empty parts are ignored.
   - In some cases, closing punctuation appears immediately after opening punctuation, so care is taken not to split these instances.
    Example of a valid Tibetan sentence: ༄༅།།བོད་ཀྱི་གསོ་བ་རིག་པའི་གཞུང་ལུགས་དང་དེའི་སྐོར་གྱི་དཔྱད་བརྗོད།
     - ༄༅ = opening punctuation
     - །། = closing punctuation

4. **Filtering Text**: Only Tibetan characters and a few predefined symbols are retained; all other characters are removed.

**Note:**
- Closing punctuation, opening punctuation, and predefined symbols are defined in the file `vars.py`
- To have a better understanding of the code, refer to the test cases in `test_segmenter.py`
