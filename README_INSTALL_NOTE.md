# Installation Note

If you encounter bcrypt compatibility issues, install dependencies with:

```bash
pip install --upgrade 'bcrypt==4.0.1' 'passlib==1.7.4'
pip install -r requirements.txt
```

Or use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install 'bcrypt==4.0.1' 'passlib==1.7.4'
pip install -r requirements.txt
```
