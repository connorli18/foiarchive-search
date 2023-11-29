def load_dynamic(filename):
    with open(f'sql/{filename}.dsql', 'r') as file:
        sql = file.read()
    return sql
    
def convert_daterange(dates, format):
    """Convert pair of datetime.date to string equivalents"""
    try:
        start_date = dates[0].strftime('%Y/%m/%d')
    except IndexError:
        start_date = None
        pass
    try:
        end_date = dates[1].strftime('%Y/%m/%d')
    except IndexError:
        end_date = None
        pass
    return start_date, end_date

def lov_predicate(colname, values):
    if not values:     # return empty string if no values
        return None
    lov = f"{colname} in ("
    for v in values:
        lov = lov + f"'{v}', "
    lov = lov[:-2] + ')'
    return lov

def compare_predicate(colname, operator, value):
    if value:
        return f"{colname} {operator} '{value}'"
    
def search_predicate(colname, searchstr):
    if searchstr:
        if searchstr[0] == "'":         # replace single quote with double
            searchstr = '"' + searchstr[1:-1:] + '"'
        searchstr = searchstr.replace("'", "''")
        return f"{colname} @@ websearch_to_tsquery('english', '{searchstr}')"

def add_predicate(predicates, text):
    if text:
        predicates.append(text)

def where_clause(predicates):
    if predicates:
        where = f"where {predicates[0]}"
    else:
        return ""
    for p in predicates[1:]:
        where += f" and {p}"
    return where

def query(template_name, table_name, where_clause):
    template = load_dynamic(template_name)
    return template.format(table_name=table_name, where_clause=where_clause)