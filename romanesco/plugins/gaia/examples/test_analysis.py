from classes import Table, Output

def main(a, b):
    c = {'fields': a['fields'], 'rows': a['rows'] + b['rows']}
    return c

# our name will be "custom" if run from romanesco, not __main__
if __name__ == "custom":
    c = Output(main(Table(a, format="rows"), Table(b, format="rows")),
               type="table", format="rows")
