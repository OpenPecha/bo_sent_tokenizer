import re
import botok

from bo_sent_tokenizer.vars import SYMBOLS_TO_KEEP, OPENING_PUNCTS, CLOSING_PUNCTS, PREDIFENED_SYMBOLS
from bo_sent_tokenizer.utils import SuppressOutput

SENT_PER_LINE_STR = str  # sentence per line string
bo_word_tokenizer = None


def get_bo_word_tokenizer():
    global bo_word_tokenizer
    if bo_word_tokenizer is None:
        bo_word_tokenizer = botok.WordTokenizer()
    return bo_word_tokenizer


def bo_preprocess(text: str) -> str:
    text = text.replace("\r", "").replace("\n", "")
    return text


def tokenize(text: str) -> SENT_PER_LINE_STR:
    """Tokenize a text into sentences."""
    print("[INFO] Tokenizing Tibetan text...")

    def get_token_text(token):
        if hasattr(token, "text_cleaned") and token.text_cleaned:
            return token.text_cleaned
        else:
            return token.text

    # fmt: off
    
    skip_chunk_types = [botok.vars.CharMarkers.CJK.name, botok.vars.CharMarkers.LATIN.name, botok.vars.CharMarkers.OTHER.name]   # noqa: E501
    # fmt: on

    # Regex to improve the chunking of shunits, this will be replaced by a better sentence segmentation in botok
    r_replace = [
        (r"༼༼[༠-༩]+[བན]༽", r""),  # delete source image numbers `ས་༼༤བ༽མེད་བ`
        (
            r"([^ང])་([༔།])",
            r"\1\2",
        ),  # delete spurious spaces added by botok in the cleantext values
        (
            r"([།གཤ]{1,2})\s+(།{1,2})",
            r"\1\2 ",
        ),  # Samdong Rinpoche style double shad. This needs to be applied on inference input
        # (r"", r""),
    ]

    text = bo_preprocess(text)

    sents_text = ""
    curr_sent = ""

    found_other_lang, found_invalid_token = False, False

    """ suppressing the outputs and warnings of the botok tokenizer"""
    with SuppressOutput():
        tokenizer = get_bo_word_tokenizer()
        tokens = tokenizer.tokenize(text, split_affixes=False)
        for token in tokens:
            token_text = get_token_text(token)

            if token_text in SYMBOLS_TO_KEEP:
                continue
            """ if there are other language text, we dont need that sentence"""
            if token.chunk_type in skip_chunk_types:
                found_other_lang = True
                continue
            """ if a token is invalid such as, we dont need that sentence"""
            if token.pos == "NON_WORD":
                found_invalid_token = True
                continue
            
            if any(punct in token_text for punct in OPENING_PUNCTS):
                curr_sent += token_text.strip()
            elif any(punct in token_text for punct in CLOSING_PUNCTS):
                curr_sent += token_text.strip()
                curr_sent += "\n"
                """add the current sentence to the sents_text"""
                """reset the curr_sent to empty string"""
                if not found_other_lang and not found_invalid_token:
                    sents_text += curr_sent
                found_other_lang, found_invalid_token = False, False
                curr_sent = ""
            else:
                curr_sent += token_text


        for fr, to in r_replace:
            sents_text = re.sub(fr, to, sents_text)

        return sents_text


def filter_tibetan_and_symbols(text):
    """ Create a regex character set for the Tibetan range and the additional symbols"""
    allowed_characters = ''.join(PREDIFENED_SYMBOLS) + '\u0F00-\u0FFF'
    """ Compile a regular expression that matches characters not in the allowed set"""
    pattern = '[^' + allowed_characters + ']+'
    """ Replace characters not in the allowed set with an empty string"""
    cleaned_text = re.sub(pattern, ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text



def segment(text: str, keep_non_bo_and_symbols:bool=False) -> SENT_PER_LINE_STR:
    """
    Input arguments: 
        -text: str: The input text to be segmented into sentences.
        -keep_non_bo_and_symbols: bool: If True, the output will contain non-Tibetan characters and symbols.
    """
    text = bo_preprocess(text)
    PUNCTS = OPENING_PUNCTS + CLOSING_PUNCTS
    """ Create a regular expression pattern from the list of punctuation marks """
    pattern = '[' + ''.join(re.escape(p) for p in PUNCTS) + ']' 
    """ Split the text using the pattern"""
    parts = re.split('({})'.format(pattern), text)
    
    """ Merge the parts to form the sentences."""
    sentences = []
    current_sentence = []

    for idx, part in enumerate(parts):
        if not part.strip():
            continue
        
        if idx != 0 and part not in CLOSING_PUNCTS:
            current_sentence_text = "".join(current_sentence)
            if not any(current_sentence_text.startswith(punct) for punct in OPENING_PUNCTS):
                current_sentence_text += "\n"
            sentences.append(current_sentence_text)
            current_sentence = []
        
        if keep_non_bo_and_symbols:
            current_sentence.append(part.strip())
        else:
            current_sentence.append(filter_tibetan_and_symbols(part).strip())

    if current_sentence:
        sentences.append(f"{''.join(current_sentence)}\n")

    """ Join all sentences into a single string"""
    segmented_text = ''.join(sentences)
    return segmented_text

if __name__ == "__main__":
    text = "ང་ཚོ་ཚང་མས་མཉམ་དུ་བང་སོ་དེ་ཉིད་སྔོག་འདོན་བྱེད་པའི་ཉིན་མོ་ཞིག་འཆར་རྒྱུའི་རེ་སྨོན་ཞུ་བཞིན་ཡོད་༄༅།།བོད་ཀྱི་གསོ་བ་རིག་པའི་གཞུང་ལུགས་དང་དེའི་སྐོར་གྱི་དཔྱད་བརྗོད།"
    output = segment(text)
    print(output)
    