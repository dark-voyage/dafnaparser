def get_links() -> list:
    from weblinks import Web
    web = Web('https://mebel.dafna.uz/category/index', '/category/view')
    lst = web.get_links()
    return lst
