#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>
#include <fcntl.h>
#include <semaphore.h>
#define HOST getenv("ADMIN_SERVER_HOSTNAME")
#define PORT atoi(getenv("ADMIN_SERVER_PORT"))
#define FIFO_PATH getenv("FIFO_PATH")
#define NUM_WORKERS 4
sem_t* fifoSemaphore;
sem_t* workersSemaphore;

int error(const char* msg) {
    perror(msg);
    sem_close(fifoSemaphore);
    sem_unlink("/run");
    sem_close(workersSemaphore);
    sem_unlink("/workers");
    kill(0, SIGTERM);
    return 1;
}

void triggerWorker(int signal_number) {
    if (signal_number == SIGUSR1) {
        char* msg = "Signal received.\n";
        write(1, msg, strlen(msg));
        if (sem_post(workersSemaphore) < 0)
            error("Failed to increase semaphore");
    }
}

void sendmessage(char* host, int port, char* message) {
    struct sockaddr_in serv_addr;
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    sockfd < 0 && error("ERROR opening socket");
    struct hostent* server = gethostbyname(host);
    bzero((char*)&serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char*)server->h_addr,
        (char*)&serv_addr.sin_addr.s_addr,
        server->h_length);
    serv_addr.sin_port = htons(port);
    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR connecting");
    int n = write(sockfd, message, strlen(message));
    if (n < 0)
        error("ERROR writing to socket");
    close(sockfd);
}

int main(int argc, char* argv[]) {
    setbuf(stdout, NULL);
    int fifofd = open(FIFO_PATH, O_RDONLY | O_NONBLOCK);
    if (fifofd < 0) {
        printf("Failed to open %s\n", FIFO_PATH);
        perror(NULL);
        return EXIT_FAILURE;
    }
    if ((fifoSemaphore = sem_open("/fifo", O_CREAT, 0644, 1)) == SEM_FAILED) {
        printf("Failed to open fifo semaphore\n");
        perror(NULL);
        return EXIT_FAILURE;
    }
    if ((workersSemaphore = sem_open("/workers", O_CREAT, 0644, 0)) == SEM_FAILED) {
        printf("Failed to create workers seamphore\n");
        perror(NULL);
        return EXIT_FAILURE;
    }

    int isDaemon = 1;
    int isWorker = 0;
    for (int i = 0; i < NUM_WORKERS; i++) {
        int result = fork();
        if (result < 0) {
            error("Failed to create worker");
        }
        else if (result == 0) {
            isDaemon = 0;
            isWorker = 1;
            break;
        }
    }

    if (isDaemon) {
        signal(SIGUSR1, triggerWorker);
        close(fifofd);
        while (1) {
            pause();
        }
    }
    else if (isWorker) {
        FILE* fifofp = fdopen(fifofd, "r");
        while (1) {
            sem_wait(workersSemaphore);
            sem_wait(fifoSemaphore);
            char url[512];
            fgets(url, 512, fifofp);
            sem_post(fifoSemaphore);
            sendmessage(HOST, PORT, url);
        }
    }
    else {
        error("Fork error");
    }

    return EXIT_SUCCESS;
}
