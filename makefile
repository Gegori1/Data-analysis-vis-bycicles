create_run:
	shinylive export myapp docs
	python3 -m http.server --directory docs --bind localhost 8008