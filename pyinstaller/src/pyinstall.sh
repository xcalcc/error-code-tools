#!/bin/bash

	DIR=$(pwd)
	XCAL_DIR=$(dirname $(dirname ${DIR}))
	yesNo="1"

# --------------------------------------------------------------------- #

gen_errCode() {
	read -p "Do you want Generate ErrorCode tools Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
	  	command cp ${XCAL_DIR}/errorCode/errorCode.py errorCode.py
	  	command cp ${XCAL_DIR}/errorCode/initAction.py initAction.py
	  	command cp ${XCAL_DIR}/errorCode/ui.py ui.py
		command cp ${XCAL_DIR}/errorCode/login.py login.py
		echo "......Generate ErrorCode tools Package File(Linux)......"
		command pyinstaller -F login.py --hidden-import=psutil  --hidden-import=cffi
		command  sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
		echo "......Generate buildTask Package File(Windows)......"
		command  sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
		echo "......Delete ErrorCode tools Spec File......"
		rm ui.spec
		rm ui.py
		rm errorCode.py
		rm initAction.py
		echo "......Generate ErrorCode tools Package Finished......"
	fi
}


prepare_folder() {
	cp -R "${XCAL_DIR}"/common ${DIR}

}



install() {
	echo "dir : " ${DIR}
	echo "dir : " ${XCAL_DIR}

	prepare_folder
	gen_errCode
}


install
