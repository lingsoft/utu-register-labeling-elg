import os

from elg import FlaskService
from elg.model import TextRequest, ClassificationResponse, Failure
from elg.model.base import StandardMessages
from elg.model.base import StatusMessage

from ttml.predict import load_models, predict
from utils import basic_tokenize


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
        threshold = 0.4
        all_labels = True

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

        # TODO Add parameter handling

        try:
            predictions = predict(self.tokenizer, self.model, content)
            predictions.sort(key=lambda x: x[1], reverse=True)
            classes = []
            for label, prob in predictions:
                if prob > threshold:
                    if all_labels or label.isupper():
                        classes.append({
                            "class": label,  ## TODO Full names
                            "score": prob,
                        })
            return ClassificationResponse(classes=classes)
        except Exception as err:
            error = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error])


flask_service = RegLab("RegLab")
app = flask_service.app
