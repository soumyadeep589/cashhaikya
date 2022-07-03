# CashHaiKya

#### Project Setup
- Install `pip`, `pyenv`, `zsh`, `autoenv zsh plugin`, `postgres`
- Install python 3.8.0 if already not installed `pyenv install 3.8.0`
- Create virtual env using specific python version `pyenv virtualenv 3.8.0 cashhaikya`
- Activate virtual env if already not activated `pyenv activate cashhaikya`
- Run `pip install -r requirements.txt`
- Run `recreatedb` from terminal, It will create role and database
- Run `run_dj`, it will run django server on port 8000.