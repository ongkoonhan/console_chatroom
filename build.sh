SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mkdir -p $SCRIPT_DIR/build/gen   # for protobuf
cd $SCRIPT_DIR/build
cmake ..
make
cmake --install .