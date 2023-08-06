

class Config:
    def __init__(self, **config):
        self.config = config

    async def __call__(self, target):
        await target.config(**self.config)

    def __str__(self):
        return f'Config({self.config})'
