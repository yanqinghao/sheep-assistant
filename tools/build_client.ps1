python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
.venv\Scripts\python -m pip install python-suanpan-slim -i https://pypi.tuna.tsinghua.edu.cn/simple
.venv\Scripts\python -m pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
.venv\Scripts\python -m pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple

.venv\Scripts\pyinstaller --additional-hooks-dir tools/hooks --clean --noconfirm -D run.py -n sheep-assistant
