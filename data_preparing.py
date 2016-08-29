import pandas as pd
import os,re



def parse_csv_dir_to_drugs_stat(dir):
    data = pd.DataFrame(columns=['Name', 'Reviews count', 'F', 'M'])
    ind = 0

    def process_drug(drug_data):  # Drug processing. remove one gendered drug
        drug_data.fillna("", inplace=True)
        ln = len(drug_data)
        female_count = len(drug_data[drug_data["Sex"] == "F"])
        return ln, female_count, ln - female_count

    for i in os.listdir(dir):
        print(i)
        drug = pd.DataFrame.from_csv(dir + i)
        data.loc[ind] = ([i] + list(process_drug(drug)))
        ind += 1
    data.sort_values('Reviews count', inplace=True, ascending=False)
    return data


def choose_drugs(drug_data):  # Drug processing. remove one gendered drug. get the top
    return drug_data['Name'].values

def parse_drugs():
    dir = "out/drugs/"
    drugs = pd.DataFrame.from_csv("drugs_stat.csv")
    data = pd.DataFrame()
    print("parsing drugs dir...")
    for i in choose_drugs(drugs):
        new_data = pd.DataFrame.from_csv(dir + i)
        data = data.append(new_data)
    return data

def prepare_data():
    data = parse_drugs()
    data = data.dropna()
    men = data[data['Sex'] == 'M']
    women = data[data['Sex'] == 'F'].sample(len(men))
    data = men.append(women).sample(frac=1)  # reshuffle reviews, just in case.

    # regex = re.compile("([^a-zA-Z']|_)")

    def numify_sex(gender):
        return 0 if gender == "F" else 1

    data['Sex'] = data['Sex'].apply(numify_sex)

    data['Review'] = data['Side Effects'] + " " + data['Comments']
    data['Review'] = data['Review'].apply(str.lower)

    def replace_non_letters(word):
        return re.sub("([^a-zA-Z']|_)", " ", word)

    data['Review'] = data['Review'].apply(replace_non_letters)
    return data


drugs_stat = parse_csv_dir_to_drugs_stat("out/drugs/")
drugs_stat.to_csv("drugs_stat.csv")
# data = pd.DataFrame.from_csv("out/data.csv")
dataset = prepare_data()
dataset.to_csv("corpus.csv")