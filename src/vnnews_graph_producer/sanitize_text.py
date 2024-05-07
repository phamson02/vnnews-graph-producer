import re


def remove_accents(input_str: str) -> str:
    s1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
    s0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"

    s = ""
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def clean_plo_text(text: str) -> str:
    # Remove the last line
    text = text.rsplit("\n", 1)[0]

    # Remove any 'PLO'
    text = text.replace("(PLO)-", "")

    return text


def clean_vtc_text(text: str) -> str:
    if "\n" not in text:
        return text

    # Remove the first line
    text = text.split("\n", 1)[1]

    # Remove the last line
    text = text.rsplit("\n", 1)[0]

    return text


def clean_laodong_text(text: str) -> str:
    if "\n" not in text:
        return text

    # Remove the first line
    text = text.split("\n", 1)[1]

    return text


def clean_vtv_text(text: str) -> str:
    if "\n" not in text:
        return text

    # Remove the first line
    text = text.split("\n", 1)[1]

    # Remove the last line
    text = text.rsplit("\n", 1)[0]

    # Remove any 'VTV.vn'
    text = text.replace("VTV.vn", "")

    return text


def clean_unnecessary_text(text: str) -> str:
    """Unnecessary text can be author, image source, etc."""
    # List of patterns of image source to remove
    patterns = [
        r"\(Ảnh:.*?\)",  # (Ảnh: VTV)
        r"\(Ảnh minh hoạ:.*?\)",  # (Ảnh minh hoạ: VTV)
        r"\(Ảnh minh họa:.*?\)",
        r"\(Nguồn:.*?\)",
        r"\(Nguồn ảnh:.*?\)",
        r"\(Nguồn video:.*?\)",
        r"Ảnh: [AĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴA-Z\s\\/-]*\b",  # Ảnh: PHƯƠNG UYÊN
        r"Đồ họa: [AĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴA-Z\s\\/-]*\b",
        r"ẢNH CHỤP MÀN HÌNH [AĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴAĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐEÊÉẾÈỀẺỂẼỄẸỆIÍÌỈĨỊOÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢUƯÚỨÙỪỦỬŨỮỤỰYÝỲỶỸỴA-Z\s\\/-]*\b",
    ]

    for pattern in patterns:
        text = re.sub(pattern, "", text)
    # Remove image source sentences, which start with "Ảnh: " or "Đồ họa: ", etc.
    sentences = text.split(". ")
    patterns = [
        r"Ảnh:.*",
        r"Đồ họa:.*",
        r"Ảnh minh hoạ:.*",
        r"Ảnh minh họa:.*",
        r"Video:.*",
        r"Nguồn:.*",
        r"Bài viết tham khảo nguồn:.*",
        r"\*Nguồn:.*",
        r"Tham khảo:.*",
    ]
    for pattern in patterns:
        sentences = [
            sentence for sentence in sentences if not re.match(pattern, sentence)
        ]
    text = ". ".join(sentences)

    # Clean sentences with all uppercase characters (usually author)
    sentences = text.split(".")
    sentences = [sentence for sentence in sentences if not sentence.isupper()]
    text = ".".join(sentences)

    # Clean sentences with 2 or less words, excluding words inside parentheses (usually author)
    sentences = text.split(".")
    clean_sentences = []
    for sentence in sentences:
        if len(re.sub(r"\(.*?\)", "", sentence).split()) > 3:
            clean_sentences.append(sentence)

    text = ".".join(clean_sentences)

    return text


def clean_text(text: str) -> str:
    """Clean scraped text"""
    text = text.replace("BNEWS", " ")

    # Remove line breaks, check if the line before line break is a full stop, if not, add a full stop
    lines = text.splitlines(True)  # keep line breaks in list
    lines = [line for line in lines if line.strip()]  # remove empty lines
    for i, line in enumerate(lines):
        line = line.strip()
        if not line.endswith("."):
            line += "."
        lines[i] = line
    text = " ".join(lines)

    # Clean image source
    text = clean_unnecessary_text(text)

    # Remove any words that contains "/TTXVN"
    words = text.split(" ")
    words = [word for word in words if "/TTXVN" not in word]
    text = " ".join(words)

    # Strip leading and trailing spaces
    text = text.strip()

    return text
