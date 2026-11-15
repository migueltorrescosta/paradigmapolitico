# paradigmapolitico

Running this locally

```bash
uv venv -p 3.12 && uv pip install -r requirements.txt
uv run streamlit run Home.py   # Run local streamlit app
uv run --with pytest pytest tests/   # Walk the quiz flows with AppTest
```
