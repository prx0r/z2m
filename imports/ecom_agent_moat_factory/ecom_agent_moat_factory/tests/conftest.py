import os, tempfile
os.environ["ADMIN_TOKEN"]="test-token"
os.environ["DATABASE_PATH"]=tempfile.mktemp(suffix=".db")
