import os

from elg import FlaskService
from elg.model import TextRequest, ClassificationResponse, Failure
from elg.model.base import StandardMessages

from ttml.predict import load_models, predict


MODEL_DIR = 'ttml/models/'
TOK_NAME = os.path.join(MODEL_DIR, "xlm-roberta-base")
FINE_TUNED = os.path.join(MODEL_DIR, "xlmr-base-en-fi-fr-se.pt")
MAX_CHAR = 10000


class RegLab(FlaskService):

    tokenizer, model = load_models(TOK_NAME, FINE_TUNED)

    def process_text(self, request: TextRequest):
        content = request.content
        if len(content) > MAX_CHAR:
            error_msg = StandardMessages.generate_elg_request_too_large()
            return Failure(errors=[error_msg])
        try:
            predictions = predict(self.tokenizer, self.model, content)
            predictions.sort(key=lambda x: x[1], reverse=True)
            classes = []
            for label, prob in predictions:
                # add threshold and label set
                classes.append({
                    "class": label,
                    "score": prob,
                })
            return ClassificationResponse(classes=classes)
        except Exception as err:
            error_msg = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error_msg])


flask_service = RegLab("RegLab")
app = flask_service.app
