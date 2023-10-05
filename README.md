# aicli

[![pypi](https://img.shields.io/pypi/v/samuelcolvin-aicli.svg)](https://pypi.python.org/pypi/samuelcolvin-aicli)
[![versions](https://img.shields.io/pypi/pyversions/samuelcolvin-aicli.svg)](https://github.com/samuelcolvin/aicli)
[![license](https://img.shields.io/github/license/samuelcolvin/aicli.svg)](https://github.com/samuelcolvin/aicli/blob/main/LICENSE)

## Installation

```bash
pip install samuelcolvin-aicli
```

## Usage

You'll need to set the `OPENAI_API_KEY` environment variable to use `aicli` which you can generate from
[platform.openai.com](https://platform.openai.com/), you'll have to add some credit to use the API.

```bash
export OPENAI_API_KEY='...'
```

Then usage is as simple as:

```bash
aicli
```

## Example

https://github.com/samuelcolvin/aicli/assets/4039449/15cc8127-c5fc-4cff-a9d7-3560f3b96d60


## Local Installation

Follow these steps to install the project locally

## Step 1: Clone the Repository

First, clone the repository to your local machine. You can do this by running the following command in your terminal:

```bash
git clone https://github.com/samuelcolvin/aicli.git
```

## Step 2: Install Python

The project requires Python 3.7 or higher. If you don't have Python installed, you can download it from the official website:

```bash
https://www.python.org/downloads/
```

## Step 3: Install Dependencies

Navigate to the project directory and install the required dependencies. The dependencies are listed in the `requirements/linting.txt` file and `pyproject.toml` file. You can install them using pip:

```bash
pip install -r requirements/linting.txt
```

The project also requires the following packages: `openai`, `rich`, and `prompt-toolkit`. You can install them using pip:

```bash
pip install openai rich prompt-toolkit
```

## Step 4: Run the Project

Finally, you can run the project using the provided script `aicli`:

```bash
python samuelcolvin_aicli.py
```

You should now have a functioning installation of the project.