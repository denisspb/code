#include <iostream>
#include <stdlib.h>

std::string getHashFromUrl(std::string const& s)
{
    std::string::size_type pos = s.rfind('/');
    return (pos != std::string::npos) ? 
        s.substr(pos + 1, s.length() - (pos + 1)) :    
        "";    
}

std::string joinPath(const std::string& part1, const std::string& part2) {
    return (part1.empty() || part1.back() == '/') ? 
        part1 + part2 :
        part1 + "/" + part2;    
}

void tstsystem() {
    std::string cmd = "cp -r '/tmp/den src/' '/tmp/den dst'";
    auto s = system(cmd.c_str());

    if (s != 0) {
        std::cout << "ERROR:" << s << std::endl;    
    } else {
        std::cout << "SUCCESS" << std::endl;
    }
    
}

int main(int argc, char** argv) {
    tstsystem();
    return 0;

    std::cout << joinPath("sss/xxx/", "yyy") << std::endl;
    std::cout << joinPath("", "yyy") << std::endl;
    std::cout << joinPath("sss/xxx/", "") << std::endl;
    std::cout << joinPath("sss/xxx", "yyy") << std::endl;

    return 0;

    auto s = getHashFromUrl("http://config-manager-vip.dev.box.net:2663/e15980a52c0d6af29a80630f32fb97c56e2e58c0");
    if (s.empty()) {
        std::cout << "no hash" << std::endl;
    } else {
        std::cout << s << std::endl;
    }

    return 0;

    if (argc != 2) {
        std::cout << "must specify param" << std::endl;
        return -1;
    }

    FILE* f = fopen(argv[1], "r");

    if (f != NULL) {
        std::cout << "Hi! press any key" << std::endl;
        std::string line;
        std::getline(std::cin, line);

        char buffer[1024];
        if (fgets(buffer, sizeof(buffer), f) != NULL) {
            std::cout << buffer << std::endl;
        } else {
            std::cout << "Cannot read content" << std::endl;
        }

        fclose(f);
        
        return 0;
    } else {
        std::cout << "cannot open file " << argv[1] << std::endl;
        
        return -1;        
    }
}