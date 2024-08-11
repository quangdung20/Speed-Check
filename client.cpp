// #include <iostream>
// #include <cstring>
// #include <unistd.h>
// #include <arpa/inet.h>
// #include <sys/types.h>
// #include <sys/socket.h>
// #include <chrono>
// #include <thread>
// #include <cstdlib> // For rand() and srand()
// #include <ctime>   // For time()

// using namespace std;

// const char *SERVER_IP = "127.0.0.1";
// const int SERVER_PORT = 6543;

// int main()
// {
//     // Initialize random seed
//     srand(static_cast<unsigned>(time(0)));

//     // Create socket
//     int sock = socket(AF_INET, SOCK_STREAM, 0);
//     if (sock < 0)
//     {
//         cerr << "Socket creation failed\n";
//         return 1;
//     }

//     // Set up server address
//     sockaddr_in server_addr;
//     server_addr.sin_family = AF_INET;
//     server_addr.sin_port = htons(SERVER_PORT);
//     inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

//     // Connect to server
//     if (connect(sock, (sockaddr *)&server_addr, sizeof(server_addr)) < 0)
//     {
//         cerr << "Connect failed\n";
//         close(sock);
//         return 1;
//     }

//     cout << "Connected to server\n";

//     while (true)
//     {
//         // Generate four random values
//         int left_value1 = rand() % 3 + 1;  // Random value between 1 and 10
//         int right_value1 = rand() % 3 + 1; // Random value between 1 and 10
//         int left_value2 = rand() % 3 + 1;  // Random value between 1 and 10
//         int right_value2 = rand() % 3 + 1; // Random value between 1 and 10

//         // Format the data to send
//         char buffer[256];
//         snprintf(buffer, sizeof(buffer), "L%d,R%d,L%d,R%d\n", left_value1, right_value1, left_value2, right_value2);

//         // Send data to server
//         if (send(sock, buffer, strlen(buffer), 0) < 0)
//         {
//             cerr << "Send failed\n";
//             break;
//         }

//         cout << "Sent: " << buffer << endl;

//         // Wait for 2 seconds before sending next data
//         this_thread::sleep_for(chrono::milliseconds(500));
//     }

//     close(sock);
//     return 0;
// }

#include <cpr/cpr.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <random>
#include <ctime>

std::string current_time()
{
    auto now = std::chrono::system_clock::now();
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);
    char buf[80];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now_time));
    return std::string(buf);
}

double random_value(double min, double max)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(min, max);
    return dis(gen);
}

int main()
{
    std::string url = "http://127.0.0.1:8050/data";

    while (true)
    {
        std::string currentTime = current_time();
        double left1 = random_value(0, 10);
        double left2 = random_value(0, 10);
        double right1 = random_value(0, 10);
        double right2 = random_value(0, 10);

        cpr::Response r = cpr::Post(cpr::Url{url},
                                    cpr::Body{"{\"time\":\"" + currentTime +
                                              "\",\"left1\":" + std::to_string(left1) +
                                              ",\"left2\":" + std::to_string(left2) +
                                              ",\"right1\":" + std::to_string(right1) +
                                              ",\"right2\":" + std::to_string(right2) + "}"},
                                    cpr::Header{{"Content-Type", "application/json"}});

        std::cout << "Sent data: {\"time\":\"" << currentTime
                  << "\", \"left1\":" << left1
                  << ", \"left2\":" << left2
                  << ", \"right1\":" << right1
                  << ", \"right2\":" << right2 << "}, Response: " << r.status_code << std::endl;

        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
