import os

from elg import FlaskService
from elg.model import TextRequest, ClassificationResponse, Failure
from elg.model.base import StandardMessages
from elg.model.base import StatusMessage

from ttml.predict import load_models, predict
from utils import basic_tokenize, full_register_name
from utils import validate_params_type, validate_threshold, validate_sub_registers


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

        if len(content) > MAX_CHAR:
            error = StandardMessages.generate_elg_request_too_large()
            return Failure(errors=[error])

        if len(basic_tokenize(content)) > MAX_TOKENS:
            error = StatusMessage(
                    code="lingsoft.token.too.many",
                    text="Given text contains too many tokens",
                    params=[])
            return Failure(errors=[error])

        longest = 0
        if content:
            longest = max(len(token) for token in content.split())
        if longest > MAX_TOKEN_LENGTH:
            error = StatusMessage(
                    code="lingsoft.token.too.long",
                    text="Given text contains too long tokens",
                    params=[])
            return Failure(errors=[error])

        threshold = 0.4
        sub_registers = True
        warnings = []

        params = request.params
        if params: 
            params_warning = validate_params_type(params) 
            if params_warning is None:
                threshold, warning = validate_threshold(params, threshold)
                if warning is not None:
                    warnings.append(warning)
                sub_registers, warning = validate_sub_registers(
                        params, sub_registers)
                if warning is not None:
                    warnings.append(warning)
            else:
                warnings.append(params_warning)

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
