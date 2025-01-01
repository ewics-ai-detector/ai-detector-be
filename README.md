
# Prereqs
make sure version 3.12.0 is installed and nothing newer. Tensor does not support the newest version
`pyenv install 3.12.0`

Create virtual environment
`python3.12 -m venv venv`

source virtual environment
`source venv/bin/activate`

install dependencies as per [hugging face docs](https://huggingface.co/docs/transformers/en/installation)
`brew install cmake`
`brew install pkg-config`

install python dependencies
`pip install -r /path/to/requirements.txt`

# How to run
simply run `make run` after completing prereqs above

Example curl request
`

