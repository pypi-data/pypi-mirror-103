# TODO: Better name
class CountingContextManager(object):
    def __init__(self):
        self._context_count = 0

    def _initial_context_enter(self):
        pass

    def __enter__(self):
        result = None
        if self._context_count == 0:
            result = self._initial_context_enter()
        self._context_count += 1

        if result is None:
            return self
        else:
            return result

    def _final_context_exit(self, exc_type, exc_value, traceback):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self._context_count -= 1
        if self._context_count == 0:
            return self._final_context_exit(exc_type, exc_value, traceback)
