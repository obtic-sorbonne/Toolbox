def cc_licence_link(licence, version="4.0"):
    l = licence.lower()

    if l.startswith("cc ") or l.startswith("cc-"):
        l = l[3:]

    return f"https://creativecommons.org/licenses/{l}/{version}/"
