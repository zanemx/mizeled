deploy: client git-push push-to-server	

client:
	@cd ../client && npm run build 
	@rm -rf ./public/*
	@mv ../client/dist/* ./public

git-push:
	@git add . 
	@git commit -m "updating stack"
	@git push origin main

push-to-server:
	@./upload_ubuntu.sh





