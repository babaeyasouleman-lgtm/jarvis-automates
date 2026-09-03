"""
Injecte un filigrane diagonal dans un .docx, comme le fait Word via Création > Filigrane.

    python filigrane.py document.docx "S-WEB AGENCY"

La librairie docx de npm n'a pas d'API pour ça. Word attend une forme VML WordArt placée
dans l'en-tête de chaque section. Deux pièges qui font échouer une injection naive :

  1. les préfixes v: et o: doivent être déclarés sur la balise <w:hdr>, sinon Word signale
     un document illisible et propose de le réparer ;
  2. chaque forme doit avoir un o:spid distinct, sinon un seul filigrane s'affiche quand il
     y a plusieurs en-têtes.

Modifie le fichier sur place. Ne touche à rien d'autre dans le document.
"""
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

NS_V = 'xmlns:v="urn:schemas-microsoft-com:vml"'
NS_O = 'xmlns:o="urn:schemas-microsoft-com:office:office"'

SHAPETYPE = (
    '<v:shapetype id="_x0000_t136" coordsize="21600,21600" o:spt="136" adj="10800" '
    'path="m@7,l@8,m@5,21600l@6,21600e">'
    '<v:formulas><v:f eqn="sum #0 0 10800"/><v:f eqn="prod #0 2 1"/>'
    '<v:f eqn="sum 21600 0 @1"/><v:f eqn="sum 0 0 @2"/><v:f eqn="sum 21600 0 @3"/>'
    '<v:f eqn="if @0 @3 0"/><v:f eqn="if @0 21600 @1"/><v:f eqn="if @0 0 @2"/>'
    '<v:f eqn="if @0 @4 21600"/><v:f eqn="mid @5 @6"/><v:f eqn="mid @8 @5"/>'
    '<v:f eqn="mid @7 @8"/><v:f eqn="mid @6 @7"/><v:f eqn="sum @6 0 @5"/></v:formulas>'
    '<v:path textpathok="t" o:connecttype="custom" '
    'o:connectlocs="@9,0;@10,10800;@11,21600;@12,10800" o:connectangles="270,180,90,0"/>'
    '<v:textpath on="t" fitshape="t"/></v:shapetype>'
)


def shape(text, spid, opacity, color, size_pt):
    return (
        '<v:shape id="PowerPlusWaterMarkObject%d" o:spid="_x0000_s%d" type="#_x0000_t136" '
        'style="position:absolute;margin-left:0;margin-top:0;width:%.1fpt;height:%.1fpt;'
        'rotation:315;z-index:-251654144;mso-position-horizontal:center;'
        'mso-position-horizontal-relative:margin;mso-position-vertical:center;'
        'mso-position-vertical-relative:margin" o:allowincell="f" fillcolor="#%s" stroked="f">'
        '<v:fill opacity="%s"/>'
        '<v:textpath style="font-family:&quot;Georgia&quot;;font-size:1pt" string="%s"/>'
        '</v:shape>'
        % (spid, 2049 + spid, size_pt, size_pt * 0.4, color, opacity, text)
    )


def paragraph(text, spid, opacity, color, size_pt):
    return (
        '<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:rPr><w:noProof/></w:rPr>'
        '<w:pict>' + SHAPETYPE + shape(text, spid, opacity, color, size_pt) +
        '</w:pict></w:r></w:p>'
    )


def inject(docx_path, text="S-WEB AGENCY", opacity=".28", color="C8C4BE", size_pt=430.0):
    docx_path = Path(docx_path)
    tmp = Path(tempfile.mkdtemp())
    out = tmp / "out.docx"
    touched = []

    with zipfile.ZipFile(docx_path) as zin:
        names = zin.namelist()
        headers = [n for n in names if re.match(r"word/header\d*\.xml$", n)]
        if not headers:
            print("aucun en-tete trouve, filigrane non pose")
            return False
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
            for i, name in enumerate(names):
                data = zin.read(name)
                if name in headers:
                    xml = data.decode("utf-8")
                    # 1. declarer les prefixes VML sur <w:hdr ...>
                    m = re.search(r"<w:hdr\b[^>]*>", xml)
                    if m:
                        tag = m.group(0)
                        newtag = tag
                        if NS_V not in newtag:
                            newtag = newtag[:-1] + " " + NS_V + ">"
                        if NS_O not in newtag:
                            newtag = newtag[:-1] + " " + NS_O + ">"
                        if newtag != tag:
                            xml = xml.replace(tag, newtag, 1)
                        # 2. inserer le filigrane juste apres l'ouverture
                        spid = headers.index(name) + 1
                        xml = xml.replace(
                            newtag, newtag + paragraph(text, spid, opacity, color, size_pt), 1)
                        touched.append(name)
                    data = xml.encode("utf-8")
                zout.writestr(name, data)

    shutil.move(str(out), str(docx_path))
    shutil.rmtree(tmp, ignore_errors=True)
    print("filigrane pose dans: " + ", ".join(touched))
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    inject(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "S-WEB AGENCY")
