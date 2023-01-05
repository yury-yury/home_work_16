import json


def load_data(file):
    """
    The function takes as an argument the name of the JSON file that contains the source data for the database,
    in the form of a string, reads the information from the opened file and returns the data in the form
    of a list of dictionaries.
    """
    with open(f'{file}', 'r', encoding='utf-8') as file:

        file_list = json.load(file)

    return file_list


if __name__ == '__main__':

    # print(type(load_data('users.json')))
    print(load_data('offers.json'))
