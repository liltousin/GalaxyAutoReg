import os
from random import choice

from dotenv import load_dotenv

load_dotenv()


TG_USERNAME = os.getenv("TG_USERNAME")


def get_text():
    a = f"""П;п;n;ñ;Π;π
и;u;ú;ù;ü;ū;û;И;U;Ú;Ù;Ü;Ū;Û
ш;Ш;w;W
и;u;ú;ù;ü;ū;û;И;U;Ú;Ù;Ü;Ū;Û
*
м;М;m;M
н;Н;H
е;ё;Е;Ё;e;é;ë;ê;ē;è;E;É;Ë;Ê;Ē;È
*
в;В;B
*
Т;т;T;t
г;ґ;Г;Ґ;g;G
*
{TG_USERNAME}
*
П;п;n;ñ;Π;π
о;О;o;ó;ø;ō;ô;õ;ö;ò;O;Ó;Ø;Ō;Ô;Õ;Ö;Ò
ш;Ш;w;W
а;А;a;à;á;ã;â;å;ä;ā;A;À;Á;Ã;Â;Å;Ä;Ā
л;Л
и;u;ú;ù;ü;ū;û;И;U;Ú;Ù;Ü;Ū;Û
м;М;m;M
🔞💋; 🔞💋;💋🔞; 💋🔞""".replace(
        "*", " "
    )
    return "".join([choice(i.split(";")) for i in a.split("\n")])
