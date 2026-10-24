from types import SimpleNamespace as NS

from godoc_rag import answer
from godoc_rag.store import Hit


def hit(i=1, sim=0.8, content="Towel calf stretch, three holds of 30 seconds. Twice a day."):
    return Hit(i, "heel-program", "Heel Program", "1", "Exercises", 3, 3, content, sim, 0.03)


class FakeClient:
    def __init__(self, content, stop_reason="end_turn"):
        self.calls = []
        self.beta = NS(messages=NS(create=self._create))
        self._response = NS(content=content, stop_reason=stop_reason)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return self._response


def cited(text, idx=0, quote="Towel calf stretch, three holds of 30 seconds."):
    return NS(type="text", text=text, citations=[NS(type="search_result_location",
                                                    search_result_index=idx, cited_text=quote)])


def plain(text):
    return NS(type="text", text=text, citations=None)


def test_patient_red_flag_stops_before_anything_else():
    result = answer.pre_checks("عندي وجع في صدري ومش قادر اتنفس", "patient")
    assert result.status == "urgent" and "123" in result.text


def test_physio_mode_has_no_red_flag_gate():
    assert answer.pre_checks("Patient reports chest pain on exertion, which tests?", "physio") is None


def test_medication_questions_get_fixed_answer():
    assert answer.pre_checks("What dose of ibuprofen for knee OA?", "physio").status == "medication"
    assert answer.pre_checks("اخد مسكن ايه للضهر؟", "patient").status == "medication"


def test_low_similarity_returns_no_source_without_calling_model():
    client = FakeClient([])
    result = answer.generate(client, "m", "q", "physio", [hit(sim=0.1)], min_similarity=0.35)
    assert result.status == "no_source" and client.calls == []


def test_request_shape_uses_search_results_citations_and_fallbacks():
    client = FakeClient([cited("Stretch the calf with a towel.")])
    answer.generate(client, "claude-opus-5-5", "Calf stretch dosage?", "physio", [hit()], 0.35)
    call = client.calls[0]
    assert call["model"] == "claude-opus-5-5"
    assert call["fallbacks"] == "default" and call["betas"] == ["server-side-fallback-2026-07-01"]
    blocks = call["messages"][0]["content"]
    assert blocks[0]["type"] == "search_result" and blocks[0]["citations"] == {"enabled": True}
    assert blocks[0]["source"] == "godoc://heel-program#chunk-1"
    assert [b["text"] for b in blocks[0]["content"]] == [
        "Towel calf stretch, three holds of 30 seconds.", "Twice a day."]
    assert blocks[-1] == {"type": "text", "text": "Calf stretch dosage?"}


def test_citations_are_numbered_and_rendered():
    client = FakeClient([plain("Use "), cited("a towel calf stretch"), plain(" twice a day.")])
    result = answer.generate(client, "m", "q", "physio", [hit()], 0.35)
    assert result.status == "answered"
    assert result.text == "Use a towel calf stretch[1] twice a day."
    assert result.citations[0].reference == "Heel Program, 1 ed., Exercises, p. 3"


def test_uncited_answer_is_treated_as_no_source():
    client = FakeClient([plain("I think you should rest.")])
    assert answer.generate(client, "m", "q", "physio", [hit()], 0.35).status == "no_source"


def test_patient_answer_with_diagnosis_is_blocked():
    client = FakeClient([cited("You have plantar fasciitis.")])
    assert answer.generate(client, "m", "q", "patient", [hit()], 0.35).status == "blocked"
    client = FakeClient([cited("حضرتك عندك التهاب في اللفافة")])
    assert answer.generate(client, "m", "سؤال", "patient", [hit()], 0.35).status == "blocked"


def test_refusal_is_handled():
    client = FakeClient([], stop_reason="refusal")
    assert answer.generate(client, "m", "q", "physio", [hit()], 0.35).status == "refusal"


def test_language_detection():
    assert answer.language("ركبتي") == "ar" and answer.language("knee") == "en"
