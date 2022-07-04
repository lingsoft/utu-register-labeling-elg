import os
import sys
import unicodedata
# Available for Python < 3.12
from distutils.util import strtobool

from elg.model.base import StatusMessage


registers = {
        "HI": "How-to/Instructions",
        "ID": "Interactive discussion",
        "IN": "Informational description",
        "IP": "Informational persuasion",
        "LY": "Lyrical",
        "NA": "Narrative",
        "OP": "Opinion",
        "SP": "Spoken",
        "av": "Advice",
        "ds": "Description with intent to sell",
        "dtp": "Description of a thing or a person",
        "ed": "News & opinion blog or editorial",
        "en": "Encyclopedia article",
        "fi": "FAQ",
        "it": "Interview",
        "lt": "Legal terms and conditions",
        "nb": "Narrative blog",
        "ne": "News report",
        "ob": "Opinion blog",
        "ra": "Research article",
        "re": "Recipe",
        "rs": "Religious blog / sermon",
        "rv": "Review",
        "sr": "Sports report"
}

punct_chars = set([
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith('P') or
        ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
         (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
])

translation_table = str.maketrans({ c: ' '+c+' ' for c in punct_chars })


# Basic tokenizer from keras-bert-ner by TurkuNLP. MIT license.
def basic_tokenize(text):
    return text.translate(translation_table).split()


def validate_params_type(params):
    if isinstance(params, dict):
        return None
    else:
        warning = StatusMessage(
                code="lingsoft.parmas.invalid.type",
                text="Params should be dictionary",
                params=[])
        return warning 


def validate_threshold(params, def_threshold):
    threshold = params.get("threshold")
    if not isinstance(threshold, float):
        try:
            threshold = float(threshold)
        except Exception:
            warning = StatusMessage(
                    code="lingsoft.params.invalid.type",
                    text="Parameter threshold can't be converted to float",
                    params=[])
            return def_threshold, warning
    if 0 <= threshold <= 1:
        return threshold, None
    else:
        warning = StatusMessage(
                code="lingsoft.params.invalid.value",
                text="Parameter threshold should be in range [0,1]",
                params=[])
        return threshold, warning


def validate_sub_registers(params, def_sub_registers):
    sub_registers = params.get("sub_registers", def_sub_registers)
    if isinstance(sub_registers, bool):
        return sub_registers, None
    if isinstance(sub_registers, str):
        sub_registers = strtobool(sub_registers)
    else:
        sub_registers = bool(sub_registers)
    warning = StatusMessage(
            code="lingsoft.params.invalid.type",
            text="Parameter sub_registers was not boolean",
            params=[])
    return sub_registers, warning


def full_register_name(label):
    if label in registers:
        return label, registers[label]
    else:
        return label, "Unknown"
