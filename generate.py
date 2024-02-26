import random
import string


def make_key(gen: random.Random):
  len = int(2**(gen.randrange(2, 7) + gen.random()))
  return ''.join(
    gen.choice(string.ascii_letters)
    for _ in range(len)
  )

def make_map(n: int):
  gen = random.Random(0)
  out = {}
  for _ in range(n):
    key = make_key(gen)
    val = gen.randrange(0, 2**64)
    out[key] = val
  return out

def write_unordered_map(data, path):
  with open(path, 'w') as fh:
    print("#include <unordered_map>", file=fh)
    print("#include <absl/container/flat_hash_map.h>", file=fh)
    print("#include <utility>", file=fh)
    print("#include <stdint.h>", file=fh)
    print(file=fh)
    print("using namespace std;", file=fh)
    print("template <typename K, typename V>", file=fh)
    print("#ifdef USE_ABSL_MAP", file=fh)
    print("using map_type = absl::flat_hash_map<K, V>;", file=fh)
    print("#else", file=fh)
    print("using map_type = std::unordered_map<K, V>;", file=fh)
    print("#endif", file=fh)
    print(file=fh)

    # print("extern unordered_map<const char*, uint64_t> the_map;", file=fh)
    print("map_type<const char*, uint64_t> the_map = {", file=fh)
    for key, v in data.items():
      print(f"  make_pair(\"{key}\", {v}ul),", file=fh)
    print("};", file=fh)
    print(file=fh)

    print("""\
uint64_t do_it() {
    uint64_t s = 0;
    for (auto it = the_map.begin(); it != the_map.end(); ++it) {
     s+= it->second;
    }
    return s;
}
    """, file=fh)
  pass

def main():
  data = make_map(3_000)

  write_unordered_map(data, "unordered_map.cc")
  pass

if __name__ == '__main__':
  main()
