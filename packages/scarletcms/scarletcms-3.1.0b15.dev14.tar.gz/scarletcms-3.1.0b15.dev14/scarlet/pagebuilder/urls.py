class SlashSlugConverter:
    regex = "[-a-zA-Z0-9_/]+"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)
