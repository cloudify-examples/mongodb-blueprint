#! /bin/bash -e

SCRIPT_MODE=${install_mode}
TEMP_DIR='/tmp'
INSTANCE_ID=$(ctx instance id)
MONGO_VERSION=${mongo_version}
MONGO_TARBALL_NAME=mongodb_${MONGO_VERSION}.tgz
MONGO_ROOT_PATH=${TEMP_DIR}/$(ctx execution-id)/mongodb
MONGO_DATA_PATH=${MONGO_ROOT_PATH}/${INSTANCE_ID}/data
MONGO_BINARIES_PATH=${MONGO_ROOT_PATH}/mongodb-binaries

function install() {
    ctx logger info "starting MongoDB installation"

    cd ${TEMP_DIR}
    mkdir -p ${MONGO_ROOT_PATH}
    if [ ! -f ${MONGO_TARBALL_NAME} ]; then
        wget -O ${MONGO_TARBALL_NAME} http://downloads.mongodb.org/linux/mongodb-linux-x86_64-${MONGO_VERSION}.tgz
    fi
    if [ ! -d ${MONGO_BINARIES_PATH} ]; then
        mkdir -p ${MONGO_BINARIES_PATH}
        MONGO_APP_NAME=$(tar -tf "${MONGO_TARBALL_NAME}" | grep -o '^[^/]\+' | sort -u)
        tar -xzvf ${MONGO_TARBALL_NAME} -C ${MONGO_BINARIES_PATH}
        mv ${MONGO_BINARIES_PATH}/${MONGO_APP_NAME}/* ${MONGO_BINARIES_PATH}
        ctx logger info "MongoDB binary directory: ${MONGO_BINARIES_PATH}"
    fi

    ctx logger info "Creating MongoDB data directory in ${MONGO_DATA_PATH}"
    mkdir -p ${MONGO_DATA_PATH}

    ctx logger info "Installing pymongo"
    pip install pymongo
    ctx logger info "Installed pymongo"

    # these runtime properties are used by the start-mongo script.
    ctx instance runtime-properties mongo_root_path ${MONGO_ROOT_PATH}
    ctx instance runtime-properties mongo_binaries_path ${MONGO_BINARIES_PATH}
    ctx instance runtime-properties mongo_data_path ${MONGO_DATA_PATH}

    ctx logger info "Successfully installed MongoDB"
}

function uninstall() {
    ctx logger info "starting MongoDB uninstallation"
    rm -rf ${MONGO_ROOT_PATH}
    ctx logger info "Successfully uninstalled MongoDB"

    ctx logger info "Uninstalling pymongo"
    pip uninstall -y pymongo
    ctx logger info "Uninstalled pymongo"
}

if [ ${SCRIPT_MODE} == "true" ]; then
    install
else
    uninstall
fi
