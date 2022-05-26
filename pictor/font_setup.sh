# Sets up TeX typesetting engine for pyx module

mkdir ${HOME}/amsfonts
cd ${HOME}/amsfonts
wget http://www.ams.org/arc/tex/amsfonts.zip
unzip amsfonts.zip
ls -R > ls-R
echo "[filelocator]" > ${HOME}/.pyxrc
echo "methods = local internal ls-R" >> ${HOME}/.pyxrc
echo "ls-R = ${HOME}/amsfonts/ls-R" >> ${HOME}/.pyxrc
rm amsfonts.zip