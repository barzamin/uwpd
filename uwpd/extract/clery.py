import camelot
import pandas as pd

def extract(pdf_path):
    tables = camelot.read_pdf(pdf_path, flavor='stream', pages='all',
                              table_areas=['0,530,760,0'],
                              columns=['100,180,280,330,465,637'],
                              split_text=True)

    return pd.concat((postprocess(t.df) for t in tables), ignore_index=True)

def postprocess(df):
    df = df.copy()

    df.drop(0, inplace=True)
    if any(['END OF REPORT' in x for x in df.iloc[-1]]):
        df = df[:-1]
    df.columns = ['Event #', 'Time Reported', 'Time Occurred', 'Report #', 'Location', 'Offense', 'Disposition']
    df['Time Reported'] = pd.to_datetime(df['Time Reported'].str.replace(r'\s+(?=[a-zA-Z])', '', regex=True))

    return df