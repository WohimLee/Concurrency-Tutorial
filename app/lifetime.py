
_db_client = None


def set_models(m):
    global _models
    _models = m

def get_models():
    return _models
