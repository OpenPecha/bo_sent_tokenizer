
import sys 
import io 

class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._temp_out = io.StringIO()
        sys.stdout = self._temp_out
        sys.stderr = self._temp_out
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
