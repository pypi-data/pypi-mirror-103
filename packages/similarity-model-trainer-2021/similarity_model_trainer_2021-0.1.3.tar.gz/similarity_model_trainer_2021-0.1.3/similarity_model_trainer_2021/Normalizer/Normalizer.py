"""
‫با توجه به استفاده این فایل دو تا تابع داره که یکی برای نرمال کردن پرس‌وجو است و دیگری برای نرمال کردن متن
"""
import re
import pandas as pd
import pathlib

# جداولی که آقای جمال در اختیارمون گذاشتن
charTable = pd.read_csv('{}/'.format(pathlib.Path(__file__).parent.absolute()) + 'tables/chars.csv', delimiter=',')
SW = pd.read_csv('{}/'.format(pathlib.Path(__file__).parent.absolute()) + 'tables/specialWords.csv', delimiter=',')

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))
compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]


# ‫این کلاس تمامی به هنجارسازی های گفته شده در readme را انجام می‌دهد
class Normalizer(object):
    def __init__(self, remove_extra_spaces=True, persian_numbers=True, unicode=True, word_refine=True,
                 persian_style=True, punctuation_spacing=True, affix_spacing=True, remove_emoji=True,
                 remove_diacritics=True, remove_extra_char=True, remove_punctuation=False, remove_repeated_word=False):
        self._punctuation_spacing = punctuation_spacing
        self._affix_spacing = affix_spacing
        self._remove_emoji = remove_emoji
        self._remove_extra_char = remove_extra_char
        # ‫تبدیل اعدادفارسی  به انگلیسی
        translation_src, translation_dst = ' ىكي“”', ' یکی""'
        if persian_numbers:
            translation_src += '۰۱۲۳۴۵۶۷۸۹٪'
            translation_dst += '0123456789%'
        if unicode:
            unicode_chars = ''.join(list(charTable['unicode']))
            translation_src += unicode_chars
            original_chars = ''.join(list(charTable['orginal']))
            translation_dst += original_chars
        self.translations = maketrans(translation_src, translation_dst)

        self.character_refinement_patterns = []

        if remove_diacritics:
            self.character_refinement_patterns.append(
                ('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),
                # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
            )

        if word_refine:
            self.character_refinement_patterns.extend(list(zip(SW['before'], SW['after'])))
        if persian_style:
            self.character_refinement_patterns.extend([
                ('"([^\n"]+)"', r'«\1»'),  # replace quotation with gyoome
                ('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
                (r' ?\.\.\.', ' …'),  # replace 3 dots
            ])
        if remove_extra_spaces:
            self.character_refinement_patterns.extend([
                (r' +', ' '),  # remove extra spaces
                (r'\n\n+', '\n'),  # remove extra newlines
                (r'\r\n+', '\r\n'),  # remove extra newlines
                (r'[ـ\r]', ''),  # remove keshide, carriage returns
                (r'\s+\n', '\n'),  # end of the paragraph delete space before \n
                (r'(\w)(\1{2,})', r'\1'),  # remove repeating of a chars
            ])
        if remove_punctuation:
            self.character_refinement_patterns.extend([
                (r'[^\w\s]', '')  # remove punctuations
            ])
        if remove_repeated_word:
            self.character_refinement_patterns.extend([
                (r'\b(\w+)( \1\b)+', r'\1')
            ])
        self.character_refinement_patterns = compile_patterns(self.character_refinement_patterns)

        punc_after, punc_before = r'\.:!،abcdefghijklmnopqrstuvwxyz؛؟»\]\)\}0123456789', r'«\[\(\{abcdefghijklmnopqrstuvwxyz0123456789'
        if punctuation_spacing:
            self.punctuation_spacing_patterns = compile_patterns([
                ('" ([^\n"]+) "', r'"\1"'),  # remove space before and after quotation
                (' ([' + punc_after + '])', r'\1'),  # remove space before
                ('([' + punc_before + ']) ', r'\1'),  # remove space after
                ('([' + punc_after[:3] + '])([^ ' + punc_after + '\d0123456789])', r'\1 \2'),
                # put space after . and :
                ('([' + punc_after[3:] + '])([^ ' + punc_after + '])', r'\1 \2'),  # put space after
                ('([^ ' + punc_before + '])([' + punc_before + '])', r'\1 \2'),  # put space before
            ])

        if affix_spacing:
            self.affix_spacing_patterns = compile_patterns([
                (r'([^ ]ه) ی ', r'\1‌ی '),  # fix ی space
                (r'(^| )(ن?می) ', r'\1\2'),  # put zwnj after می, نمی
                (
                    r'(?<=[^\n\d ' + punc_after + punc_before + ']{2}) (تر(ین?)?|گری?|های?)(?=[ \n' + punc_after + punc_before + ']|$)',
                    r'\1'),  # put zwnj before تر, تری, ترین, گر, گری, ها, های
                (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n' + punc_after + ']|$)', r'\1‌\2'),
                # join ام, ایم, اش, اند, ای, اید, ات

            ])

    def character_refinement(self, text):
        text = text.translate(self.translations)
        for pattern, repl in self.character_refinement_patterns:
            text = pattern.sub(repl, text)
        return text

    # ‫حذف اموجی‌ها
    def deEmojify(self, text):
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            u"\U00002500-\U00002BEF"  # chinese char
                                            u"\U00002702-\U000027B0"
                                            u"\U00002702-\U000027B0"
                                            u"\U000024C2-\U0001F251"
                                            u"\U0001f926-\U0001f937"
                                            u"\U00010000-\U0010ffff"
                                            u"\u2640-\u2642"
                                            u"\u2600-\u2B55"
                                            u"\u200d"
                                            u"\u23cf"
                                            u"\u23e9"
                                            u"\u231a"
                                            u"\ufe0f"  # dingbats
                                            u"\u3030"
                                            "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r' ', text)

    # ‫این تابع برای قرار دادن space بعد از punctuation هاست
    def punctuation_spacing(self, text):
        for pattern, repl in self.punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    # این تابع برای اصلاح نیم‌فاصله‌هاست
    def affix_spacing(self, text):
        for pattern, repl in self.affix_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    # تابع اصلی برای نرمال کردن متن
    def normalizeText(self, text):
        if self._remove_emoji:
            text = self.deEmojify(text).strip()
        text = self.character_refinement(text)
        if self._punctuation_spacing:
            text = self.punctuation_spacing(text)
        if self._affix_spacing:
            text = self.affix_spacing(text)
        return text