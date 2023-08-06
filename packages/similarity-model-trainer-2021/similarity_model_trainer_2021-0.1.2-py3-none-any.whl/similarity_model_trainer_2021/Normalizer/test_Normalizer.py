from NLP.Normalizer import Normalizer
normalizer = Normalizer()


def test_1():
    assert "من به بازار میروم" == normalizer.normalizeText("من به بازار می   روم")


def test_2():
    assert "مهدی بابایی کلا کارهای سخت دوست دارد" == normalizer.normalizeText(
        "مهدیِ بابایی کُلاً کار های سخت دوست دارد")


def test_3():
    assert "شدت عملش زیاد بود" == normalizer.normalizeText("شدّت عملش زیاد بود")



def test_5():
    assert "او گفت «سلام» و رفت" == normalizer.normalizeText("او گفت “ سلام ” و رفت")


def test_6():
    assert "کتاب هنر جنگ بسیار عالی است" == normalizer.normalizeText("کتاب هنر جنگ بسیار عاااااالی است")


def test_7():
    assert "این یک تست است\nاین یک تست است\nاین یک تست است" == normalizer.normalizeText("این یک تست است\n\nاین یک تست "
                                                                                        "است\n\nاین یک تست است")

def test_8():
    assert "واقعا مطلب سنگینی بود من خیلی لذت بردم" == normalizer.normalizeText(
        "واقعا مطلب سنگینی بود😂😂😂😂من خیلی لذت بردم")


def test_9():
    assert "امروز استقلال برنده است" == normalizer.normalizeText(
        "💙💙🌟🌟💙💙امروز استقلال برنده است 🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿")


def test_10():
    assert "فاتح اعداد لنگ شاه شاهان عدد الانم همیشه باعث سوزشی مرسی که هستی" == normalizer.normalizeText(
        "فاتح اعداد لنگ شاه شاهان 😍😍😍💙💙💙💙 عدد ✌✌ الانم ✌✌✌ همیشه باعث سوزشی مرسی که هستی😍😍💙💙💙")
