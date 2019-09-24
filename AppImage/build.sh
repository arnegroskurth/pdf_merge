#!/usr/bin/env bash

PYTHON_VERSION=3.7.4


set -e

THIS_DIR="$(dirname "$(readlink -e "$0")")"
ROOT_DIR="$(dirname "${THIS_DIR}")"
BUILD_DIR=${ROOT_DIR}/build
APP_DIR=${BUILD_DIR}/.AppDir
mkdir -p "${APP_DIR}"

# Download and build Python
cd "${BUILD_DIR}" || exit 1
if [ ! -f "Python-${PYTHON_VERSION}.tgz" ]; then
  wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
fi
tar -xzf Python-${PYTHON_VERSION}.tgz
cd Python-${PYTHON_VERSION} || exit 1
mkdir -p "${APP_DIR}"/usr
./configure --prefix="${APP_DIR}"/usr
make -j && make install

# Update pip
"${APP_DIR}"/usr/bin/pip3 install --upgrade pip

# Install dependencies
"${APP_DIR}"/usr/bin/pip3 install -r "${ROOT_DIR}"/requirements.txt

# see: https://stackoverflow.com/questions/45978113/pypdf2-write-doesnt-work-on-some-pdf-files-python-3-5-1
PDF_PY="${APP_DIR}/usr/lib/python3.7/site-packages/PyPDF2/pdf.py"
if grep -Fq "#if self.strict:" "${PDF_PY}" # idempotence
then
  cp "${PDF_PY}" "${PDF_PY}.bak"
  patch "${PDF_PY}" < "${THIS_DIR}/pdf.py.patch"
fi

# Get appimagetool
cd "${BUILD_DIR}" || exit 1
if [ ! -f "appimagetool" ]; then
  wget -O appimagetool https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
  chmod +x appimagetool
fi

# Build AppImage
cp "${ROOT_DIR}"/pdf_merge.py "${APP_DIR}"/
cp "${THIS_DIR}"/{AppRun,pdf_merge.desktop,pdf_merge.png} "${APP_DIR}"/
BUILD_ARTIFACT="${BUILD_DIR}"/pdf_merge.AppImage
ARCH=x86_64 "${BUILD_DIR}"/appimagetool -v "${APP_DIR}" "${BUILD_ARTIFACT}"

printf "\n\nResult: %s\n\nSuccess!\n" "${BUILD_ARTIFACT}"
