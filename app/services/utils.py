import pandas as pd

# Generate a pandas dataframe concisely; not really needed but it's here now
def produce_df(products):
    df = pd.DataFrame(products)

    return df

# Wrap text concisely so that it doesn't overflow the legend in the graph
def wrap_text(text, width):
    return "<br>".join([text[i : i + width] for i in range(0, len(text), width)])
