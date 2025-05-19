import os
import sys
import json
import time
import requests
from xml.etree import ElementTree as ET

# Parámetro de búsqueda
query = " ".join(sys.argv[1:]) or "CTCF TADs"
max_results = 500
batch_size = 200
output_dir_meta = "data/papers_raw"
output_dir_text = "data/papers_fulltext"
os.makedirs(output_dir_meta, exist_ok=True)
os.makedirs(output_dir_text, exist_ok=True)

# Archivo resumen
summary_path = "data/descarga_resumen.json"
resumen_articulos = []

# Paso 1: Buscar IDs de artículos con ESearch
search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
search_params = {
    "db": "pubmed",
    "term": query,
    "retmax": max_results,
    "retmode": "json"
}

search_resp = requests.get(search_url, params=search_params)
ids = search_resp.json().get("esearchresult", {}).get("idlist", [])
print(f"🔍 Se encontraron {len(ids)} artículos en PubMed para el término '{query}'")

# Paso 2: Recuperar detalles por lotes con EFetch
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

for i in range(0, len(ids), batch_size):
    batch_ids = ids[i:i + batch_size]
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(batch_ids),
        "retmode": "xml"
    }

    fetch_resp = requests.get(fetch_url, params=fetch_params)
    if fetch_resp.status_code != 200 or not fetch_resp.text.strip():
        print(f"⚠️ Error al recuperar lote {i // batch_size + 1}: código {fetch_resp.status_code}")
        continue

    try:
        root = ET.fromstring(fetch_resp.text)
    except ET.ParseError as e:
        print(f"⚠️ Error de parseo XML en lote {i // batch_size + 1}: {e}")
        continue

    for j, article in enumerate(root.findall(".//PubmedArticle")):
        try:
            medline = article.find("MedlineCitation")
            article_data = medline.find("Article")

            title = article_data.findtext("ArticleTitle", default="Sin título")
            abstract = " ".join([a.text.strip() for a in article_data.findall("Abstract/AbstractText") if a.text])
            authors = ", ".join(
                f"{a.findtext('LastName', '')} {a.findtext('Initials', '')}".strip()
                for a in article_data.findall("AuthorList/Author")
                if a.find("LastName") is not None
            )
            journal = article_data.findtext("Journal/Title", default="Desconocido")
            year = article_data.findtext("Journal/JournalIssue/PubDate/Year", default="Desconocido")
            pmid = medline.findtext("PMID")
            pmcid = None
            fulltext = None

            # Buscar en Europe PMC si tiene PMCID y texto completo
            epmc_search = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params={
                "query": f"EXT_ID:{pmid} AND SRC:MED",
                "format": "json"
            })
            result_list = epmc_search.json().get("resultList", {}).get("result", [])
            if result_list:
                pmcid = result_list[0].get("pmcid")
                if pmcid:
                    fulltext_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
                    fulltext_resp = requests.get(fulltext_url)
                    if fulltext_resp.status_code == 200:
                        try:
                            fulltree = ET.fromstring(fulltext_resp.text)
                            paras = [p.text.strip() for p in fulltree.findall(".//body//p") if p.text]
                            fulltext = "\n\n".join(paras)
                        except ET.ParseError:
                            pass

            # Si no hay texto completo, saltar
            if not fulltext:
                continue

            # Guardar metadatos
            record = {
                "id": pmid,
                "title": title,
                "doi": None,
                "authors": authors,
                "journal": journal,
                "year": year,
                "abstract": abstract,
                "source": "PubMed",
                "pmcid": pmcid
            }

            safe_title = title.strip().replace(" ", "_")[:80]
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in ("_", "-"))

            with open(f"{output_dir_meta}/{safe_title}.json", "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)

            with open(f"{output_dir_text}/{safe_title}.txt", "w", encoding="utf-8") as f:
                f.write(fulltext)

            # Agregar al resumen
            resumen_articulos.append({
                "id": pmid,
                "title": title,
                "pmcid": pmcid,
                "filename": f"{safe_title}"
            })

        except Exception as e:
            print(f"⚠️ Error procesando artículo {j + 1} del lote {i // batch_size + 1}: {e}")

    print(f"✅ Lote {i // batch_size + 1} procesado")
    time.sleep(0.5)

# Guardar resumen global
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(resumen_articulos, f, indent=2, ensure_ascii=False)

print(f"📁 Guardado completo en {output_dir_meta} y {output_dir_text}")
print(f"🗂️  Resumen guardado en {summary_path}")