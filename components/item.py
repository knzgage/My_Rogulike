class Item:
    def __init__(self, use_function=None, targeting=False, target_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.target_message = target_message
        self.function_kwargs = kwargs

