from traitlets.config.configurable import Configurable
from traitlets import Int, Unicode, Bool
from traitlets.config import Application


class Person(Configurable):
    name = Unicode("John", help="Person's name", config=True)
    age = Int(36, help="Person's age", config = True)
    hasPet = Bool(True, help="Flag to indicate if a Person has Pets", config=True)

    def info(self):
        print(f'{self.name} is {self.age} years old')

class App(Application):
    def initialize(self, argv=None):
        super().initialize(argv=argv)
        self.load_config_file("base_config.json")

    def start(self):
        p = Person(parent=self)
        p.info()

if __name__ == "__main__":
    App.launch_instance()
