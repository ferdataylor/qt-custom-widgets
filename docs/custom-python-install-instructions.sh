Step 1: Create the Python 3.9 directory structure

sudo mkdir -p /usr/local/python/3.9.18




Step 2: Download and compile Python 3.9

# Move to a temporary directory
cd /tmp

# Download Python 3.9.18 (latest 3.9 version)
wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz
tar -xzf Python-3.9.18.tgz
cd Python-3.9.18

# Install build dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# Configure Python to install to /usr/local/python/3.9.18
./configure --prefix=/usr/local/python/3.9.18 --enable-optimizations --with-ensurepip=install

# Compile (this will take several minutes)
make -j$(nproc)

# Install
sudo make install




Step 3: Update the current symlink to point to Python 3.9

# Remove the existing current symlink/directory
sudo rm -rf /usr/local/python/current

# Create new symlink pointing to Python 3.9
sudo ln -sf /usr/local/python/3.9.18 /usr/local/python/current




Step 4: Update /usr/bin links

# Create/update symlinks in /usr/bin
sudo ln -sf /usr/local/python/current/bin/python3.9 /usr/bin/python3.9
sudo ln -sf /usr/local/python/current/bin/python3.9 /usr/bin/python3
sudo ln -sf /usr/local/python/current/bin/python3.9 /usr/bin/python

# Update pip links
sudo ln -sf /usr/local/python/current/bin/pip3.9 /usr/bin/pip3.9
sudo ln -sf /usr/local/python/current/bin/pip3.9 /usr/bin/pip3
sudo ln -sf /usr/local/python/current/bin/pip3.9 /usr/bin/pip