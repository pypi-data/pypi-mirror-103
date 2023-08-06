from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Comp:
    '''Create a Comp object'''

    def __init__(self, driver, name, css_selector, parent=None, children=None):
        self.driver = driver
        self.name = name
        self.css_selector = css_selector
        self.parent = parent
        self.children = children or {}

    def __contains__(self, comp_name):
        return comp_name in self.children

    def __iter__(self):
        yield from self.children

    def __len__(self):
        return len(self.children)

    def __getitem__(self, comp_name):
        return self.children[comp_name]

    def __setitem__(self, comp_name, comp):
        self.children[comp_name] = comp

    def __delitem__(self, comp_name):
        del self.children[comp_name]

    def __eq__(self, comp2):
        if self is comp2:
            return True
        elif self.driver != comp2.driver:
            return False
        elif self.css_selector != comp2.css_selector:
            return False
        elif self.parent != comp2.parent:
            return False
        elif self.children != comp2.children:
            return False
        return True

    def __ne__(self, comp2):
        if self is comp2:
            return True
        elif (self.driver == comp2.driver:
            and self.css_selector == comp2.css_selector
            and self.parent == comp2.parent
            and self.children == comp2.children):
            return False
        return True

    def get(self, comp_name, default=None):
        if comp_name in self.children:
            return self.children[comp_name]
        else:
            return default

    def pop(self, comp_name):
        comp = self[comp_name]
        del self[comp_name]
        return comp

    def popitem(self):
        raise NotImplementedError()

    def clear(self):
        self.children.clear()

    def update(self, comp2):
        self.children.update(comp2.children)

    def setdefault(self, key, default=None):
        self.children.setdefault(key, default=default)

    def keys(self):
        return self.children.keys()

    def values(self):
        return self.children.values()

    def items(self):
        return self.children.items()

    def path(self):
        '''Returns the comp's CSS selector'''

        parents_path = f'{self.parent.path()} ' if self.parent else None
        return f'{parents_path}{self.css_selector}'

    def add_comp(self, selector, name=None, comp_type=None):
        '''Add a child comp'''

        if name == comp_type == None:
            raise ValueError('One of name or comp_type must be set')
        elif name:
            self.comps[name] = Comp(driver, selector)
        elif comp_type:
            self.comps[comp_type.__name__] = comp_type(driver, selector)

class EntryComp(Comp):
    def __init__(self, driver, name, css_selector, entry_url, children=None, args=0, kwargs=None):
        super().__init__(driver, name, css_selector, parent=parent, children=children)
        self.entry_url = entry_url

    def enter(self, *args, **kwargs) -> Comp:
        raise NotImplementedError()

class Pom:
    def __init__(self, chrome_options=None):
        self.driver = None
        self.chrome_options = Options()
        if chrome_options:
            for arg in chrome_options:
                self.chrome_options.add_argument(arg)

    def open(self):

class Fluent:
    def __init__(self):
        self.entry_comps = {}
        self.other_comps = {}

    def add_entry(self, entry_comp, entry_url, args=0, kwargs=None):
        self.entry_comps[entry_comp.name] = entry_comp

    def start(self, initial_page, *args, **kwargs):
        return self.entry_comps[initial_page].enter()
        