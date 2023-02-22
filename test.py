import pandas as pd

def get_header_row(file):
    data = pd.read_csv(file, on_bad_lines='skip')
    return len(data) + 1

# with open('./report_TOPICS.csv') as f:

index = get_header_row('./report_TOPICS.csv')
# print(type(index))

new_df = pd.read_csv('./report_TOPICS.csv', skiprows=index)
print(new_df)