Since we have two copies of the code, we'd like for the contents of `td_submission/sub1/` to be our official submission.

The dockerfile is `td_submission/sub1/Dockerfile`, and it is working so y'all can just use that.

The agent is in the file `td_submission/sub1/sf_agent.py`. It depends on the existence of the `stockfish` file.
This file may need to be built by running `make clean && make -j build` (possibly with options to specify architecture, etc.) 
inside `td_submission/sub1/Fairy-Stockfish/src/`, then the built `stockfish` file should be moved into `td_submission/sub1/`), 

You can also run using `td_submission/sub1/app.py`, if not using Docker.

The `Fairy-Stockfish/` directory is forked from <https://github.com/fairy-stockfish/Fairy-Stockfish>.
