import re


def check_mail(mail):
    """
    Validates typed email and raises exception if it doesn't match to the regex
    pattern. More about this regex you can read at http://emailregex.com/
    :param mail: The user mail
    :type mail: String
    :return: Nothing
    """
    raw_mail_pattern = (
                        r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/="
                        r"?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-"
                        r"\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:("
                        r"?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0"
                        r"-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9"
                        r"][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?"
                        r"|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x2"
                        r"1-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
                        )

    if re.match(raw_mail_pattern, mail) is None:
        raise ValueError("Please, input correct email")
