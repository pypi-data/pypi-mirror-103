import difflib


class File:
    def __init__(self, path, content=None):
        self.path = path
        self.content = content

    async def __call__(self, target):
        if await target.exists(self.path):
            content = await target.read(self.path)
            if content == self.content:
                self.skipped = True
                return
            diff = difflib.ndiff(content, self.content)
            target.output.info(diff)
        self.proc = await target.write(self.path, self.content)

    def __str__(self):
        return f'File({self.path})'

    def cachekey(self):
        return self.path + self.content
