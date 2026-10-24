import pytest

from godoc_rag import redflags

URGENT = [
    ("bladder_bowel", "Since yesterday I can't control my bladder and my back hurts"),
    ("bladder_bowel", "مش قادر اتحكم في البول من امبارح"),
    ("bladder_bowel", "البول بينزل لوحده"),
    ("bladder_bowel", "mesh 2ader at7akem fel bol"),
    ("saddle_numbness", "I have numbness between my legs"),
    ("saddle_numbness", "عندي تنميل في المنطقة الحساسة"),
    ("chest_pain_breathing", "chest pain when I walk"),
    ("chest_pain_breathing", "عندي وجع في صدري وانا بطلع السلم"),
    ("chest_pain_breathing", "مش قادر اتنفس"),
    ("chest_pain_breathing", "waga3 fe sedri"),
    ("stroke_signs", "suddenly my right arm went weak and my speech is slurred"),
    ("stroke_signs", "بوقي اتعوج والكلام تقيل"),
    ("stroke_signs", "فجأة ضعف في ايدي الشمال"),
    ("severe_headache", "worst headache of my life"),
    ("progressive_weakness", "my foot is dropping when I walk"),
    ("progressive_weakness", "رجليا الاتنين بتضعف"),
    ("fall_cannot_bear_weight", "I fell yesterday and now I can't walk"),
    ("fall_cannot_bear_weight", "وقعت امبارح ومش قادر ادوس على رجلي"),
    ("fever_with_pain", "fever and back pain since Monday"),
    ("fever_with_pain", "عندي سخونية ووجع في ضهري"),
    ("calf_swelling", "my calf is swollen and hot"),
    ("calf_swelling", "بطن رجلي وارمة وسخنة"),
    ("weight_loss", "I lost a lot of weight without trying"),
    ("weight_loss", "خسيت كتير من غير سبب"),
    # Arabic و/ف/ب attached to the key word
    ("fever_with_pain", "عندي سخونية وورم في ركبتي"),
    ("fall_cannot_bear_weight", "وقعت ومقدرش امشي"),
    ("saddle_numbness", "تنميل وبين الرجلين"),
]

ROUTINE = [
    "My knee hurts when I go down stairs",
    "ركبتي بتوجعني على السلم",
    "Pain under my heel in the morning",
    "كتفي واجعني لما ارفع ايدي",
    "How long should I hold the calf stretch?",
    "ضهري بيوجعني بعد الشغل على الكمبيوتر",
]


@pytest.mark.parametrize("flag,text", URGENT)
def test_red_flags_detected(flag, text):
    result = redflags.check(text)
    assert result.urgent and flag in result.flags, (text, result.flags)


@pytest.mark.parametrize("text", ROUTINE)
def test_routine_messages_pass(text):
    assert redflags.check(text).flags == []


def test_urgent_message_language():
    assert "123" in redflags.urgent_message("ar") and "الإسعاف" in redflags.urgent_message("ar")
    assert "ambulance" in redflags.urgent_message("en")
