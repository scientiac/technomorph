# Install pyserial with uv
uv add pyserial

# Bind
sudo rfcomm bind 0 44:1D:64:F7:CA:A2 1

# Unbind
sudo rfcomm release 0
