import os

from elg import FlaskService
from elg.model import TextRequest, ClassificationResponse, Failure

from ttml.predict import load_models, predict
from utils import basic_tokenize, full_register_name
from utils import validate_content
from utils import validate_threshold, validate_sub_registers


MODEL_DIR = 'ttml/models/'
TOK_NAME = os.path.join(MODEL_DIR, "xlm-roberta-base")
FINE_TUNED = os.path.join(MODEL_DIR, "xlmr-base-en-fi-fr-se.pt")
MAX_TOKENS = 512
MAX_TOKEN_LENGTH = 100
MAX_CHAR = 10000


class RegLab(FlaskService):

    tokenizer, model = load_models(TOK_NAME, FINE_TUNED)

    def process_text(self, request: TextRequest):

        content = request.content
        error = validate_content(
                content, MAX_CHAR, MAX_TOKENS, MAX_TOKEN_LENGTH)
        if error is not None:
            return Failure(errors=[error])

        threshold = 0.4
        sub_registers = True
        warnings = []

        params = request.params or {}
        threshold, warning = validate_threshold(params, threshold)
        if warning is not None:
            warnings.append(warning)
        sub_registers, warning = validate_sub_registers(params, sub_registers)
        if warning is not None:
             warnings.append(warning)

        try:
            predictions = predict(self.tokenizer, self.model, content)
            predictions.sort(key=lambda x: x[1], reverse=True)
            classes = []
            for label, prob in predictions:
                if prob > threshold:
                    # General registers are in uppercase.
                    if sub_registers or label.isupper():
                        label, name = full_register_name(label)
                        full_name = label + " - " + name
                        # TODO Add warning if Unknown
                        classes.append({
                            "class": full_name,
                            "score": prob,
                        })
            return ClassificationResponse(classes=classes, warnings=warnings)
        except Exception as err:
            error = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error])


flask_service = RegLab("RegLab")
app = flask_service.app
