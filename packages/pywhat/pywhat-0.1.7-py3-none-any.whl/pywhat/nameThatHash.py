from name_that_hash import runner


class Nth:
    def __init__(self):
        pass

    def get_hashes(self, text: str) -> dict:
        to_ret = runner.api_return_hashes_as_dict(text)
        import pprint

        pprint.pprint(to_ret)
        return to_ret
