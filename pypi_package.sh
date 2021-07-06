# Delete unnecessary files
rm -rv dist
rm -rv rpi_gpio_devices.egg-info

python3 -m pip install --upgrade pip && # Install latest pip
python3 -m pip install --upgrade build && # Install latest package builder
python3 -m pip install --upgrade twine && # Install latest twine

python3 -m build && # Build project
python3 -m twine upload dist/* # Upload archives
