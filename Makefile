CXXFLAGS=-std=c++17 -I/opt/homebrew/include/

unordered_map.cc: generate.py
	python generate.py

timeit_stl: unordered_map.cc
	time $(CXX) $(CXXFLAGS) -o unordered_map_stl.o -c unordered_map.cc

timeit_absl: unordered_map.cc
	time $(CXX) -DUSE_ABSL_MAP $(CXXFLAGS) -o unordered_map_absl.o -c unordered_map.cc
