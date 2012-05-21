//
//  main.c
//  HPBPwdBreaker
//
//  Created by pheehs on 12/05/11.
//  Copyright (c) 2012年 pheehs All rights reserved.
//

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

static char *keyString = "UMh]`ahyY`g`]_^Z``_]";
static char *indexbase = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
int baselen;

int checkpasswd(const char *keyin){
    unsigned int enqlen, passlen;
    int i, j, k;
    char *decrypted, *decryptedPassword, *decryptedPath, *targetUrl;
    int chr1, chr2;
    double nbase;
    int estart, eend;
    
    enqlen = strlen(keyString);
    if ((passlen = strlen(keyin)) <= 0) {
        printf("パスワードを入力してください\n");
        return 1;
    }
    decrypted = (char *)malloc(21);
    decryptedPassword = (char *)malloc(21);
    
    printf("keyin: '%s'\n", keyin);
    
    for (i=0, j=passlen-1, k=0; i < enqlen; i++, j--, k=0){
        if (j < 0)
            j = passlen - 1;
        
        //printf("strchr(indexbase, keyin[j](= %c) ) = %p\n", keyin[j], strchr(indexbase, keyin[j]));
        //printf("keyin = %p\n", indexbase);
        chr1 = strchr(indexbase, keyin[j]) - indexbase;
        chr2 = strchr(indexbase, keyString[i]) - indexbase;
        
        //printf("chr1: %d\n", chr1);
        //printf("chr2: %d\n", chr2);
        
        if (chr2 < (chr1 + j)) {
            nbase = (chr1 + j - chr2) / 0x5f; // 0x5f = 95 (= len(indexbase)) !!
            //printf("nbase = %f\n", nbase);
            //printf("ceil(nbase) = %f\n", ceil(nbase));
            k += (int)(0x5f * ceil(nbase));
        }
        k += chr2 - chr1 - j;
        
        //printf("decrypted = %hhd; c = %d; indexbase[k] = %c\n", *decrypted, i, indexbase[k]);
        //strcat(decrypted, (const char *)indexbase[k]);
        //memset(decrypted+i, (int)indexbase[k], 1);
        *(decrypted+i) = indexbase[k];
    }
    //memset(decrypted+i, (int)"\0", 1);
    *(decrypted+i) = '\0';
    
    eend = strlen(decrypted);  
    estart = eend - passlen;
    if (estart < 0)
        estart = eend + estart;
    
    //printf("decrypted: %s\n", decrypted);
    //printf("strncpy(decryptedPassword, decrypted[%d], %d);\n", estart, eend - estart);
    strncpy(decryptedPassword, decrypted+estart, (size_t)eend - estart);
    
    printf("decryptedPassword: %s\n", decryptedPassword);
    
    if (strcmp(keyin, decryptedPassword) == 0){
        decryptedPath = (char *)malloc( strlen(decrypted) - passlen );
        strncpy(decryptedPath, decrypted, strlen(decrypted) - passlen);
        printf("decryptedPath: %s\n", decryptedPath);
        
        passlen = strlen(decryptedPath);
        targetUrl = (char *)malloc(7);
        j = 0;
        for (i = 0; i < passlen; i++){
            chr1 = decryptedPath[i];
            if (chr1 == '%'){
                strncpy(targetUrl+j, decryptedPath+i, 6);
                i += 11;
                j += 6;
            }
            else {
                targetUrl[j] = chr1;
            }
        }
        printf("Success!!\n");
        printf("targetUrl: %s\n", targetUrl);
        if (targetUrl )
            free(targetUrl);
        free(decrypted);
        free(decryptedPassword);
        free(decryptedPath);
        
        return 0;
    } else {
        free(decrypted);
        free(decryptedPassword);
        printf("Failed!!\n");
        return 1;
    }
}

void keygen_next(const int p_min, const int p_max, char *prev){
    int i, prevlen, counter = 0;
    prevlen = strlen(prev);
    
    if (prevlen == 0) {
        counter = 0;//(int)pow((double)baselen, (double)p_min);
        prevlen = p_min;
    }else{
        for (i = 0; i < prevlen; i++){
            counter += ((int)pow((double)baselen, (double)(prevlen-i-1)) * (strchr(indexbase, prev[prevlen-i-1]) - indexbase));
            // prev をbaselen進法としてみて、10進法に直す
        }
        printf("counter(before-add1): %d\n", counter);
        counter += 1;
        printf("counter(after-add1): %d\n", counter);
        if (counter >= pow((double)baselen, (double)p_max)) {
            // 指定された範囲を超えたら
            memset(prev, 0, p_max+1);
            printf("over--------------!!\n");
            return;
        }
    }
    //printf("counter: %d\n", counter);
    for (i = 0; i < prevlen; i++){
        prev[prevlen-i-1] = indexbase[counter / (int)pow((double)baselen, (double)(prevlen-i-1))];
        counter %= (int)pow((double)baselen, (double)(prevlen-i-1));
        // 今度はbaselen進法にする
        //printf("counter: %d\n", counter);
    }
    return;
}

int main(int argc, char *argv[]){
    int p_min, p_max;
    char *passwd = NULL;
    baselen = strlen(indexbase);
    
    if (argc < 3){
        printf("Usage: %s <MIN> <MAX>\n", argv[0]);
        return 1;
    }
    p_min = atoi(argv[1]);
    p_max = atoi(argv[2]);
    if (p_min > p_max){
        printf("Error: <MIN> must not larger than <MAX>!\n");
        return 1;
    }
    
    passwd = (char *)malloc(p_max+1);
    memset(passwd, 0, p_max+1);
    
    keygen_next(p_min, p_max, passwd);
    while (strcmp(passwd, "") != 0) {
        printf("passwd@main: '%s'\n", passwd);
        if (checkpasswd(passwd) == 0){
            printf("One of the answer is '%s'", passwd);
        }
        
        keygen_next(p_min, p_max, passwd);
    }
    
    free(passwd);
    return 0;
}
