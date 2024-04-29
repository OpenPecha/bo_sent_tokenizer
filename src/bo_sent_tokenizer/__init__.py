import re
import botok

from bo_sent_tokenizer.vars import SYMBOLS_TO_KEEP

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
    opening_puncts = ['༁', '༂', '༃', '༄', '༅', '༆', '༇', '༈', '༉', '༊', '༑', '༒', '༺', '༼', '༿', '࿐', '࿑', '࿓', '࿔', '࿙']  # noqa: E501
    closing_puncts = ['།', '༎', '༏', '༐', '༔', '༴', '༻', '༽', '༾', '࿚']  # noqa: E501
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
        
        if any(punct in token_text for punct in opening_puncts):
            curr_sent += token_text.strip()
        elif any(punct in token_text for punct in closing_puncts):
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


if __name__ == "__main__":
    sentence= """ ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་ནམ། ཁྱེད་དེ་རིང་བདེ་མོ་ཡིན་བབབབབབབབནམ། ངའི་མིང་ལ་(Thomas)་ཟེར། དང་པོ་ནི་དཔོན་བཙན་པོ་ནས་(བཀའ་རྒྱུད་ཁོ་ན་)གུ་གེ་བློ་ལྡན་ལ་བརྒྱུད། རྒྱ་གར་ཧིན་དྷིའི་སྐད་ཡིག་ལ་གཅིག་ནི་एकཡིན་།"""
    output = tokenize(sentence)
    print(output)