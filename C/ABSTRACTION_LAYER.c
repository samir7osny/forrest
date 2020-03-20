/*
 * ABSTRACTION_LAYER.c
 *
 *  Created on: Mar 15, 2020
 *      Author: Omar Touny
 */

//#include "ABSTRACTION_LAYER.h"
#include <stdint.h>
#include <stdlib.h>
#include"tm4c123gh6pm.h"
#include "MICRO-CONTROLLER_LAYER.h"
void INIT(void){
    //extern CLOCK_TEST();
    GPIO_INIT();
    UART_INIT();
    UART_CONFIG();
    SysTick_Init();
    //extern CLCK_INIT();
    //extern ADC_INIT();
}

void delay_ms(uint32_t delay){
    uint32_t i;
    for(i=0; i<delay; i++){
        SysTick_Wait(1600000); //100ms
    }
}

char READ_CHAR_UART0(){
    char c;
    while ((UART0_FR_R & (1<<4)) !=0);
    c=UART0_DR_R;
    return c;
}
void SEND_CHAR_UART0(char c){
    while ((UART0_FR_R & (1<<5)) !=0);
    UART0_DR_R=c;
}
void SEND_DIGIT_UART0(uint8_t c){
    while ((UART0_FR_R & (1<<5)) !=0);
    UART0_DR_R=c+'0';
}
void SEND_STRING_UART0(char *string){
    while(*string){
        SEND_CHAR_UART0(*(string++));
    }
}
/*
void SEND_INT_UART0(int Num){
    int *num_Array=calloc(10,sizeof(int));
    int i=0;
    while(Num !=0){
        *(num_Array+i)=Num%10;
        //SEND_DIGIT_UART0(Num%10);
        Num=Num/10;
        i++;
    }
    i-=1;
    while(i>=0){
        SEND_DIGIT_UART0(*(num_Array+i));
        i--;
    }
    free(num_Array);
}
*/
void SEND_INT_UART0(int Num,int space){
    int num_Array[10];
    int i=0;
    while(Num !=0){
        *(num_Array+i)=Num%10;
        //SEND_DIGIT_UART0(Num%10);
        Num=Num/10;
        i++;
    }
    i-=1;
    while(i>=0){
        SEND_DIGIT_UART0(*(num_Array+i));
        i--;
    }
    if(space){
        SEND_STRING_UART0(" ");
    }
    else{
        SEND_STRING_UART0("\n\r");
    }
}
char READ_CHAR_UART1(){
    char c;
    while ((UART1_FR_R & (1<<4)) !=0);
    c=UART1_DR_R;
    return c;
}

void SEND_CHAR_UART1(char c){
    while ((UART1_FR_R & (1<<5)) !=0);
    UART1_DR_R=c;
}
void SEND_STRING_UART1(char *string){
    while(*string){
        SEND_CHAR_UART1(*(string++));
    }
}

uint32_t ADC_Value(){
    uint32_t ADCRESULT=0;
    ADCRESULT=ADC1_SSFIFO3_R;
    ADC1_ISC_R|=(1<<3);
    return ADCRESULT;
}
