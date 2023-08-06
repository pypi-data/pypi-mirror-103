class Option:
    """
    {
        # free input
        "name": <name>
        "value": ""/null
    },
    {
        # single choice
        "name": <name>
        "options": ["<opt0>", "<opt1>", "<opt2>"]
        "single": True
    },
    {
        # multiple choice
        "name": <name>
        "options": ["<opt0>", "<opt1>", "<opt2>"]
        "single": False
    }
    """
    def __init__(self, name:str, value:str):
        self.name = name
        self.value = value
        self.options = []

    def add(self, opt:Option) -> bool:
        pass
    
    def to_json(self)->dict:
        pass

    @staticmethod
    def from_json(json:dict)->Option:
        pass