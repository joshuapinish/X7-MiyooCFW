.PHONY: all configure build test clean
BUILD_DIR ?= build
RAM_MIB ?= 32
all: test
configure:
	cmake -S . -B $(BUILD_DIR) -DX7_RAM_MIB=$(RAM_MIB) -DX7_BUILD_TESTS=ON
build: configure
	cmake --build $(BUILD_DIR) --parallel
test: build
	ctest --test-dir $(BUILD_DIR) --output-on-failure
clean:
	rm -rf $(BUILD_DIR)
