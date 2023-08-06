
# 1. Generating distribution archives

    python -m pip install --upgrade build

    python -m build


# 2. Uploading the distribution archives


    python -m twine upload --repository testpypi dist/*
