// C
#include <stdio.h>
#include <openssl/sha.h>

int main() {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, "hello world", 11);
    SHA256_Final(hash, &sha256);

    printf("SHA-256: ");
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
    return 0;
}
