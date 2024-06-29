.PHONY : run_server run_frontend

run_server:
	uvicorn src.server:app --reload
run_frontend:
	streamlit run src/frontend.py
