import sys
import pickle
import pandas as pd


def send_data_to_stdout(data):

    if isinstance(data, pd.DataFrame):
        data.to_json(sys.stdout, orient="split")
    elif isinstance(data, pd.Series):
        data = pd.DataFrame(data)
        data.to_json(sys.stdout, orient="split")
    pass

def load_data_from_stdin():

    new_df = pd.read_json(sys.stdin)
    print(new_df)
    pass


#dog = pd.DataFrame(["2","3"])
#print(dog)
#send_data_to_stdout(dog)

#load_data_from_stdin()