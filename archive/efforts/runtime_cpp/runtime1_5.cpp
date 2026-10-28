// runtime1_5: the five console tools in one binary. Windows and Linux.
// g++ -std=c++17 -O2 -o runtime1_5 runtime1_5.cpp walk.cpp player.cpp paint.cpp graphics.cpp driver.cpp standin.cpp script.cpp openscript.cpp handler.cpp path.cpp session.cpp
// runtime1_5 path lesson.json
// runtime1_5 player lesson.json out.html
// runtime1_5 paint lesson.tbk P400 out.svg
// runtime1_5 standin lesson.tbk P400
// runtime1_5 script lesson.tbk lesson.json P400

#include <iostream>
#include <string>

int cmd_path(int argc, char** argv);
int cmd_player(int argc, char** argv);
int cmd_paint(int argc, char** argv);
int cmd_standin(int argc, char** argv);
int cmd_script(int argc, char** argv);

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "runtime1_5 <path|player|paint|standin|script> ...\n"
                  << "  path    <lesson.json> [record-dir]\n"
                  << "  player  <lesson.json> <out.html>\n"
                  << "  paint   <lesson.tbk> <page> [out.svg]\n"
                  << "  standin <lesson.tbk> <page> [record-dir]\n"
                  << "  script  <lesson.tbk> <lesson.json> <page>\n";
        return 2;
    }
    std::string cmd = argv[1];
    int n = argc - 1;
    char** rest = argv + 1;
    rest[0] = argv[0];
    if (cmd == "path") return cmd_path(n, rest);
    if (cmd == "player") return cmd_player(n, rest);
    if (cmd == "paint") return cmd_paint(n, rest);
    if (cmd == "standin") return cmd_standin(n, rest);
    if (cmd == "script") return cmd_script(n, rest);
    std::cerr << "unknown command " << cmd << "\n";
    return 2;
}
