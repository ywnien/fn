from pprint import pprint

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select


class Browser(webdriver.Chrome):
    def __init__(self, url: str, headless=False):
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.headless = headless
    
    def __enter__(self):
        super().__init__(options=self.options)
        self.get(self.url)
        #sleep(10)
        return self
    
    def __exit__(self, *args):
        self.close()

    def ls_tag(self, tag_name: str, show=True, *args: str):
        results = self.find_elements_by_tag_name(tag_name)
        all_info = []        

        for result in results:
            info = []

            for arg in args:
                info.append(result.get_attribute(arg))
            
            info.append(result.text)
            all_info.append(info)
        
        if show == True:
            pprint(all_info)
            print(f"{len(results)} elements of {tag_name}")
        else:
            return all_info
    
    def frame(self, name: str):
        self.switch_to.default_content()
        self.switch_to.frame(name)
    
    def find(self, keyword: str, by="id") -> list:
        switch = {
            "css": self.find_elements_by_css_selector,
            "tag": self.find_elements_by_tag_name,
            "class": self.find_elements_by_class_name,
            "name": self.find_elements_by_name,
            "id": self.find_elements_by_id,
            "link": self.find_elements_by_link_text,
            "partial_link": self.find_elements_by_partial_link_text,
            "xpath": self.find_elements_by_xpath,
        }

        return switch.get(by, self.find_elements_by_id)(keyword)

    def find_one(self, by="id"):
        """
        Returns `Webdriver.find_element` methods

        """
        switch = {
            "css": self.find_element_by_css_selector,
            "tag": self.find_element_by_tag_name,
            "class": self.find_element_by_class_name,
            "name": self.find_element_by_name,
            "id": self.find_element_by_id,
            "link": self.find_element_by_link_text,
            "partial_link": self.find_element_by_partial_link_text,
            "xpath": self.find_element_by_xpath,
        }

        return switch.get(by, self.find_elements_by_id)
        
    
class Menu(Select):
    def __init__(self, find_one, key: str):
        super().__init__(find_one(key))
        self.find = find_one
        self.key = key

    def now(self):
        return self.first_selected_option.text
    
    def opts(self, info="value"):
        """
        Gets informations from option elements.

        args:

        - info - attributes ("id", "name"...) or plain text ("text")

        """
        elements = self.options

        if info == "text":
            return [element.text for element in elements]
        else:
            return [element.get_attribute(info) for element in elements]
            
    def select(self, value, by="value"):
        switch = {
            "value": self.select_by_value,
            "index": self.select_by_index,
            "text": self.select_by_visible_text,
        }

        _err_msg = ("Invalid value. Select by:\n"
                    "'value': value\n"
                    "'index': index\n"
                    "'text': visible text")
                    
        return switch.get(by, _err_msg)(value)
    
    def reattach(self): # wrong 
        self = self.__init__(self.find, self.key)