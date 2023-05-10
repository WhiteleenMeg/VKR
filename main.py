from pages.record_page import Record_page
from pages.import_page import Import_page
from pages.listen_page import Listen_page
from pages.info_page import Info_page




class Main():
    def __init__(self):
        page = Import_page()
        while page.new_page != 0:
            if page.new_page == 1:
                page = Import_page()
            if page.new_page == 2:
                page = Record_page()
            if page.new_page == 3:
                page = Listen_page()
            if page.new_page == 4:
                page = Info_page()


main = Main()

