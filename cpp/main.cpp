#include <iostream>

int main(int argc, char** argv) {
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