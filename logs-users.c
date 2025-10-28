#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    FILE *arquivo = fopen("logins.csv", "w");
    if (!arquivo) {
        perror("Erro ao criar logins.csv");
        return 1;
    }

    const char *usuarios[20] = {
        "Allicia","Miguel","Maria Fernanda","Fernanda","Raissa","Gabrielle",
        "Henri","Joao","Laura","Marcos","Sofia","Ricardo","Bianca","Eduardo",
        "Larissa","Melissa","Julia","Roberta","Clara","Chaulim"
    };

    fprintf(arquivo, "Nome,IP,Data,Hora\n");

    srand((unsigned)(time(NULL) ^ (uintptr_t)&arquivo ^ (unsigned)clock()));

    time_t agora = time(NULL);
    time_t inicio = agora - (time_t)(30LL * 24LL * 60LL * 60LL);
    long long range = (long long)(agora - inicio); /* número de segundos no intervalo */

    if (range <= 0) {
        fprintf(stderr, "Intervalo inválido de datas.\n");
        fclose(arquivo);
        return 1;
    }

    for (int i = 0; i < 20; ++i) {
        long long a = ((long long)rand() & 0x7FFF);
        long long b = ((long long)rand() & 0x7FFF);
        long long c = ((long long)rand() & 0x7FFF);
        long long combined = (a << 30) ^ (b << 15) ^ c; 
        if (combined < 0) combined = -combined;
        long long offset = combined % (range + 1); 

        time_t t = inicio + (time_t)offset;
        struct tm tm_info = *localtime(&t);

        char data[16], hora[8];
        strftime(data, sizeof(data), "%d-%m-%Y", &tm_info);
        strftime(hora, sizeof(hora), "%H:%M", &tm_info);

        /* IP aleatório (privado) */
        int ip1 = 192, ip2 = 168, ip3 = rand() % 256, ip4 = 1 + rand() % 254;

        fprintf(arquivo, "%s,%d.%d.%d.%d,%s,%s\n",
                usuarios[i], ip1, ip2, ip3, ip4, data, hora);
    }

    fclose(arquivo);
    printf("Arquivo 'logins.csv' criado com sucesso com datas aleatórias nos últimos 30 dias.\n");
    return 0;
}