class MCPServerAdapter:
    def __init__(self, params):
        self.params = params
    def __enter__(self):
        return []
    def __exit__(self, exc_type, exc, tb):
        pass
