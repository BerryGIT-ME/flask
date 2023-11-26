def valid_data(data):
    is_list = isinstance(data, list)
    if not is_list: return False

    test_results = [test_item(item) for item in data]
    passesed = all(test_results)
    return passesed

def test_item(item):
    try:
        chat = item['chat']
        content = chat['content']
        role = chat['role']
        suggestions = item['suggestions']

        content_is_str = isinstance(content, str)
        role_is_str = isinstance(role, str)
        suggestions_is_list = isinstance(suggestions, list)
        

        return content_is_str and role_is_str and suggestions_is_list
    except:
        return False