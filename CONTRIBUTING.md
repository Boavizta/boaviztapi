Check this points if you want to do a pull request :

 * [ ] Is my code written in [PEP8](https://www.python.org/dev/peps/pep-0008/)?
 * [ ] Are the tests passing?
 * [ ] Is my feature or bug fix unit tested?
 * [ ] Does each of my commits represent an atomic functionality or bug fix?
 * [ ] Is my feature or bug fix related to an issue?
 * [ ] Is my code compatible with the minimum Python version? You can run `make test-compat-min` to check
 * [ ] Is my code compatible with the maximum Python version? You can run `make test-compat-max` to check
 * [ ] Have I installed and configured [pre-commit](https://pre-commit.com/) hooks? You can install it by running `pip install pre-commit` and set it up with `pre-commit install`.
 * [ ] Have I ensured that all pre-commit hooks pass before committing my changes? You can run `pre-commit run --all-files` to check.
