## Running the project locally
### Create and activate virtual environment
```
python -m venv venv
./venv/Scripts/activate
```

### Install pip requirements
Then install packages from requirements.txt:
```
pip install -r requirements.txt
```

### Run the project
```
python src/main.py
```

## Building From Source
### Nuitka
I've been building with MSVC, which can be installed through Visual Studio Installer. The --msvc switch can be removed if you want Nuitka to figure out which compiler to use.

standalone:
```
nuitka --msvc="14.3" --lto=no --standalone --disable-console --output-dir=dist/ --output-filename="custom_xp_curve" src/main.py && rm dist/main.dist/ucrtbase.dll && rm dist/main.dist/api-ms-*.dll
```

onefile:
```
nuitka --msvc="14.3" --lto=no --onefile --disable-console --output-dir=dist/ --output-filename="custom_xp_curve" src/main.py
```

## Installing a fresh venv
```
deactivate
rm -r venv
python -m venv venv
./venv/Scripts/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
