def run_function_call_parallely_for_list(data_list, call_function, connections=5):
    """
    This function is used to call the given function parallely

    data_list: list of elements which should be sent to the call function
    call_function: The function which will be executed for every element of data list, first arg: element, second arg:
     str i.e. queue number of the element.
    connections: Number of parallel calls
    """
    import concurrent.futures
    import requests
    import time

    out = []
    CONNECTIONS = connections
    TIMEOUT = 10

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (
        executor.submit(call_function, data, f"{index + 1} of {len(data_list)} executed.") for
        index, data in enumerate(data_list))
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.append(data)

                print(str(len(out)), end="\r")

        time2 = time.time()

    print(f'Took {time2 - time1:.2f} s')


def convert_list_of_dicts_to_csv_stringio(data):
    from io import StringIO
    import csv

    stream = StringIO()

    # Make list same
    keys_set = set()
    for d in data:
        for key, value in d.items():
            keys_set.add(key)
    for d in data:
        for key in keys_set:
            if key not in d:
                d[key] = ""

    fc = csv.DictWriter(stream,
                        fieldnames=data[0].keys(),
                        )
    fc.writeheader()
    fc.writerows(data)

    return stream


def is_list_a_subset(data, superset, match_type='all'):
    """
    match_type: String: 'all' -> All elements of data must be present in superset
                        'any' -> Any element of data must be present in superset
    """
    if match_type == 'all':
        return all(x in superset for x in data)
    elif match_type == 'any':
        return any(x in superset for x in data)
    else:
        raise Exception('Invalid match type. Valid choices: all/any')


def group_by(data, key_lambda, multiple=False):
    """
    Convert list of data to a dictionary
    data: List of values
    key_lambda: A function which returns the key when called on a item of data
    multiple: Boolean: If key can have multiple values
    """
    from collections import defaultdict
    result_dict = defaultdict(list) if multiple else dict()
    for value in data:
        if multiple:
            result_dict[key_lambda(value)].append(value)
        else:
            result_dict[key_lambda(value)] = value

    return result_dict


def break_list_into_chunks(data_list, chunk_size):
    """
    Divides one big list into chunks of smaller lists
    """
    chunked_list = []
    for i in range(0, len(data_list), chunk_size):
        chunked_list.append(data_list[i:i + chunk_size])
    return chunked_list


def read_file_from_url(url):
    import urllib.request
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')