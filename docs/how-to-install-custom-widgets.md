# How to Install Custom Widgets

### Downgrade/Upgrade Python
- `sudo apt update`
- `sudo apt install python3.9`
- `sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1`
- `sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2`
- `sudo update-alternatives --config python3`
- `cd /usr/local/python`
- `mkdir -p 3.9/bin`
- `ln -s /usr/bin/python3.9 python`
- `unlink current`
- `ln -s 3.9 current`


### Install PyQt Custom Widgets & Dependencies
- `sudo apt install libgl1-mesa-dev`
- `ldconfig -p | grep libGL.so`
- `libGL.so.1 (libc6,x86-64) => /usr/lib/x86_64-linux-gnu/libGL.so.1`
- `pip install QT-PyQt-PySide-Custom-Widgets`
- `pip install PySide6`


### Create the Custom Widgets Project
- `mkdir -p custom-widgets`
- `cd custom-widgets`
- `Custom_Widgets --create-project`
- Qt binding/API Name: (Default: PySide6) (Options: PySide6, PySide2, PyQt6, PyQt5)
- Icons Color: #d7d5dc
- QT Designer Icons Color: #d7d5dc
- App Background: #4e0d3a
- App Text Color: #d7d5dc
- App Accent Color: #720d5d
