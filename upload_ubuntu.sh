echo "update nginx ubuntu fastapi server"
ssh -i ~/.ssh/aws-ubuntu-24.pem ubuntu@3.89.88.232 -t 'source ~/.zshrc; cd apis/mizeled; git pull origin main; exit;'
echo "finished updating server"
