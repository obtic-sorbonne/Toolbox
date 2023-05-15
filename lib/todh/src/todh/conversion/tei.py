"""description:
    Des méthodes pour transformer un texte en XML-TEI.
"""

__author__ = "Yoann Dupont"
__license__ = "MIT"


import uuid
import pathlib
from datetime import date

from lxml import etree
from lxml.builder import ElementMaker

from pyexcel_ods import get_data

from todh.conversion.utils import cc_licence_link


def text_to_tei(
    text,
    author,
    publisher,
    toptitle,
    title=None,
    project=None,
    responsibility=None,
    editor=None,
    edition=None,
    pub_date=None,
    lang="fr",
    licence="by-nc-sa",
):
    """Convertit un fichier texte en XML-TEI."""

    today = date.today()

    E = ElementMaker(
        namespace="http://www.tei-c.org/ns/1.0", nsmap={None: "http://www.tei-c.org/ns/1.0"}
    )

    title = title or ""
    project = project or "{project}"
    responsibility = responsibility or "{responsibility}"
    editor = edition or "{editor}"
    edition = edition or "{edition}"

    if pub_date:
        pub_date = f"{'-'.join(pub_date.split('/')[::-1])}"
    else:
        pub_date = "inconnue"

    if lang == "français":
        lang = "fre"  # WARNING: why "fre"? Should be "fr"

    teifile = E.TEI(
        E.teiHeader(
            E.fileDesc(
                E.titleStmt(E.title(f"{toptitle}"), E.author(f"{author}")),
                E.editionStmt(
                    E.edition(edition or "{edition}"),  # formerly: "Thèse de doctorat"
                    E.respStmt(E.resp(), E.name(responsibility or "{responsibility}")),  # formerly: FirstName LastName
                ),
                E.publicationStmt(
                    E.publisher(editor or "{editor}"),  # formerly: "OBVIL"
                    E.date(when=str(today.year)),
                    E.idno(),
                    E.availability(
                        E.licence(
                            f"Licence {licence}", target=cc_licence_link(licence)
                        ),
                        status="restricted",
                    ),
                ),
                E.sourceDesc(E.bibl()),
            ),
            E.profileDesc(
                E.creation(E.date(when=pub_date)),
                E.langUsage(E.language(ident=f"{lang}")),
                E.textClass(
                    E.keywords(
                        E.term(f"{toptitle}", type="topTitle"),
                        E.term(f"{project}", type="project"),
                        E.term(f"{uuid.uuid4().hex}", type="id"),
                        E.term(
                            f"{title}", type="title"
                        ),
                        E.term(editor or "{editor}", type="edition"),  # formerly: "OBVIL"
                        E.term(f"{publisher}", type="publisher"),
                        E.term(f"{author}", type="author"),
                        E.term(type="recipient"),
                        E.term(f"{pub_date}", type="date"),
                        scheme="indexation",
                    )
                ),
            ),
        ),
        E.text(E.body(E.div(*[E.p(t.strip()) for t in text.split("\n") if t.strip()]))),
    )

    return teifile
