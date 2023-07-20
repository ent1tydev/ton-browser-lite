#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void flushHistory() {
    FILE *historyFile = fopen("history.txt", "w");
    if (historyFile != NULL) {
        fclose(historyFile);
        printf("history.txt has been flushed.\n");
    } else {
        printf("Error: Unable to create history.txt\n");
    }
}

void stopProxy() {
    system("taskkill /im rldp-http-proxy.exe /f");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <stop|flush>\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "stop") == 0) {
        stopProxy();
    } else if (strcmp(argv[1], "flush") == 0) {
        flushHistory();
    } else {
        printf("Unknown argument: %s\n", argv[1]);
        return 1;
    }

    return 0;
}
