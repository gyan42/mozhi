# Mozhi Test Suite

pytest flags:
- `s` #prints all logs to the terminal
- `rP` #shows the captured output of passed tests.
- `rx` #shows the captured output of failed tests (default behaviour).

```
cd /path/tp/mozhi/
export PYTHONPATH=$PYTHONPATH:$(pwd)/mozhi/
export PYTHONPATH=$PYTHONPATH:$(pwd)/tests/

pytest -s 
```