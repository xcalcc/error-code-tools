#!/bin/bash

	DIR=$(pwd)
	XCAL_DIR=$(dirname $(dirname ${DIR}))
	
# --------------------------------------------------------------------- #
gen_setup() {
	read -p "Do you want Generate Setup Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
		echo "......Generate Agent-Setup Package File(Linux)......"
		command pyinstaller -F XcalAgentSetup.py --hidden-import=psutil
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
		echo "......Generate Agent-Setup Package File(Windows)......"
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows 
		echo "......Delete Agent-Setup Spec File......"
		rm XcalAgentSetup.spec
		echo "......Generate Agent-Setup Package Finished......"
	fi
}

gen_start() {
	read -p "Do you want Generate Start Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
		echo "......Generate Agent-Start Package File(Linux)......"
		command pyinstaller -F XcalAgentStart.py --hidden-import=psutil  --hidden-import=cffi
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
		echo "......Generate Agent-Start Package File(Windows)......"
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows 
		echo "......Delete Agent-Start Spec File......"
		rm XcalAgentStart.spec
		echo "......Generate Agent-Start Package Finished......"	
	fi
}

gen_xcalbuild_linux() {
	read -p "Do you want Generate Xcalbuild Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
		command cp ${XCAL_DIR}/xcalbuild/linux/xcalbuild.py xcalbuild.py
		echo "......Generate Xcalbuild Package File(Linux)......"	
		command pyinstaller -F xcalbuild.py --hidden-import=psutil  --hidden-import=cffi		
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
		echo "......Delete Xcalbuild Spec File......"
		rm xcalbuild.spec
		rm xcalbuild.py
		echo "......Generate Xcalbuild Package Finished......\n"	
	fi
}

gen_xcalbuild_windows() {
	read -p "Do you want Generate Xcalbuild Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
		command cp ${XCAL_DIR}/xcalbuild/win/xcalbuild.py xcalbuild.py
		echo "......Generate Xcalbuild Package File(Linux)......"	
		command pyinstaller -F xcalbuild.py --hidden-import=psutil  --hidden-import=cffi		
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
		echo "......Delete Xcalbuild Spec File......"
		rm xcalbuild.spec
		rm xcalbuild.py
		echo "......Generate Xcalbuild Package Finished......\n"	
	fi
}

gen_xcal_agent() {
	read -p "Do you want Generate Xcal_agent Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
		command cp ${XCAL_DIR}/tools/xcal-agent.py xcal-agent.py
		echo "......Generate Xcal_agent Package File(Linux)......"	
		command pyinstaller -F xcal-agent.py --hidden-import=psutil  --hidden-import=cffi		
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
		echo "......Generate Xcal_agent Package File(Windows)......"
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows 
		echo "......Delete Xcal_agent Spec File......"
		rm xcal-agent.spec
		rm xcal-agent.py
		echo "......Generate Xcal_agent Package Finished......\n"	
	fi
}

gen_xcal_scanner() {
	read -p "Do you want Generate Xcal_scanner Package? [0- No/ 1- Yes]:" yesNo
	if [ "${yesNo}" = "1" ]; then
		command cp ${XCAL_DIR}/tools/xcal-scanner.py xcal-scanner.py
		echo "......Generate Xcal_scanner Package File(Linux)......"	
		command pyinstaller -F xcal-scanner.py --hidden-import=psutil  --hidden-import=cffi		
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
		echo "......Generate Xcal_scanner Package File(Windows)......"
		command sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows 
		echo "......Delete Xcal_scanner Spec File......"
		rm xcal-scanner.spec
		rm xcal-scanner.py
		echo "......Generate Xcal_scanner Package Finished......\n"	
	fi
}

prepare_folder() {
	cp "${XCAL_DIR}"/XcalAgentSetup.py ${DIR}/XcalAgentSetup.py
	cp "${XCAL_DIR}"/XcalAgentStart.py ${DIR}/XcalAgentStart.py
	cp -R "${XCAL_DIR}"/tools ${DIR}
	cp -R "${XCAL_DIR}"/xcalbuild ${DIR}
	cp -R "${XCAL_DIR}"/agent/components ${DIR}
	cp -R "${XCAL_DIR}"/agent/util ${DIR}
	cp -R "${XCAL_DIR}"/agent/common ${DIR}
	cp -R "${XCAL_DIR}"/agent/fastagent.py ${DIR}/fastagent.py
	cp -R "${XCAL_DIR}"/agent/XcalGlobals.py ${DIR}/XcalGlobals.py
}
			
copy_package(){

	cp ${DIR}/dist/linux/XcalAgentSetup "${XCAL_DIR}"
	cp ${DIR}/dist/linux/XcalAgentStart "${XCAL_DIR}"
	cp ${DIR}/dist/windows/XcalAgentSetup.exe "${XCAL_DIR}"
	cp ${DIR}/dist/windows/XcalAgentStart.exe "${XCAL_DIR}"
	cp ${DIR}/dist/linux/xcal-agent "${XCAL_DIR}"/tools
	cp ${DIR}/dist/linux/xcal-scanner "${XCAL_DIR}"/tools
	cp ${DIR}/dist/windows/xcal-agent.exe "${XCAL_DIR}"/tools
	cp ${DIR}/dist/windows/xcal-scanner.exe "${XCAL_DIR}"/tools
	#cp ${DIR}/dist/linux/xcalbuild "${XCAL_DIR}"/xcalbuild/linux
	#cp ${DIR}/dist/windows/xcalbuild.exe "${XCAL_DIR}"/xcalbuild/win
}

delete_folder(){
	rm -R ${DIR}/common
	rm -R ${DIR}/components
	rm -R ${DIR}/tools
	rm -R ${DIR}/util
	#rm -R ${DIR}/xcalbuild
	rm ${DIR}/fastagent.py
	rm ${DIR}/XcalAgentSetup.py
	rm ${DIR}/XcalAgentStart.py
	rm ${DIR}/XcalGlobals.py
	rm -R ${DIR}/build
	rm -R ${DIR}/dist
	sudo rm -R ${DIR}/__pycache__

}


install() {
	prepare_folder
	gen_setup
	gen_start
	gen_xcalbuild_linux
	gen_xcalbuild_windows
	gen_xcal_agent
	gen_xcal_scanner
	copy_package
	delete_folder
}


install





