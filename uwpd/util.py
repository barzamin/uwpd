import camelot

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def chunked_pdf_read(pdf_path, pages, chunksize=50, **kwargs):
    pdfh = camelot.handlers.PDFHandler(pdf_path)
    pagelist = pdfh._get_pages(pages) # index list

    for chunk in chunks(pagelist, chunksize):
        pages_desc = ','.join(map(str, chunk))
        tables = camelot.read_pdf(pdf_path, pages=pages_desc, **kwargs)
        for table in tables:
            yield table

