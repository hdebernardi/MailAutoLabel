all :
	pip install -r requirements.txt --user

clean :
	rm -rf env
	pip uninstall -r requirements.txt --user
