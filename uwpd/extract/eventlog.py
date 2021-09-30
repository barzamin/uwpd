import itertools
import camelot
import pandas as pd
from tqdm import tqdm
from PyPDF2 import PdfFileReader

from ..util import chunked_pdf_read


def extract(pdf_path):
    EVT_LOG_AREAS = {
        'first': ['0,555,800,25'],
        'rest':  ['0,600,800,25'],
    }

    postprocessed_dfs = []
    with open(pdf_path, "rb") as f:
        infile = PdfFileReader(f, strict=False)
        pagecount = infile.getNumPages()

    for page in tqdm(itertools.chain(
            # handle first page separately
            chunked_pdf_read(pdf_path, '1', flavor='stream', table_areas=EVT_LOG_AREAS['first']),

            # then do the rest in chunks
            chunked_pdf_read(pdf_path, '2-end', flavor='stream', chunksize=10, table_areas=EVT_LOG_AREAS['rest'])), total=pagecount):
        postprocessed_dfs.append(postprocess(page.df))

    full_df = pd.concat(postprocessed_dfs, ignore_index=True)
    full_df.sort_values('Date & Time', ascending=False, inplace=True)

    return full_df

# clean up a page's table
def postprocess(df):
    df = df.copy()
    
    needs_loc_split = df.iloc[0,3] == 'Location\nAddress'
    df.drop(0, inplace=True)
    if needs_loc_split:
        df.rename(columns={0: 'Event #', 1: 'Date & Time', 2: 'Nature', 3: 'Location & Address', 4: 'Status'}, inplace=True)
        df[['Location', 'Address']] = df['Location & Address'].str.split('\n', 1, expand=True)
        df.drop(columns='Location & Address', inplace=True)
    else:
        df.rename(columns={0: 'Event #', 1: 'Date & Time', 2: 'Nature', 3: 'Location', 4: 'Address', 5: 'Status'}, inplace=True)
    
    # fixup last page stuff
    if '/' in df.iloc[-1,0]: # date in evt column
        df = df[:-1]

    df['Event #'] = pd.to_numeric(df['Event #'])
    # df[1] = df[1].apply(lambda dts: datetime.strptime(dts, '%m/%d/%y %H:%M %p'))
    df['Date & Time'] = pd.to_datetime(df['Date & Time'])
    return df