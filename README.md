Dockerfile is `td_submission/sub1/Dockerfile`.

`src/` is forked from <https://github.com/fairy-stockfish/Fairy-Stockfish>

The agent is in the file `sf_agent.py`. It depends on the `stockfish` binary, which may need to be built
(run `make clean && make -j build`, possibly with more options to specify architecture, etc.)
It's run using either `app.py` or `player1.py`, depending on whether you're looking at the 
docker version.

Since we have two copies of the code, we'd like for the contents of `td_submission/sub1/` to be our official submission.
