#include <stdint.h>
#include"tm4c123gh6pm.h"
#include "MICRO-CONTROLLER_LAYER.h"
#include "ABSTRACTION_LAYER.h"

#define LHandPN 3
#define LHandZERO 1500
#define LElbowPIN 2
#define LElbowZERO 1500
#define LShoulderPIN 1
#define LShoulderZERO 1500

#define RHandPIN 30
#define RHandZERO 1500
#define RElbowPIN 31
#define RElbowZERO 1500
#define RShoulderPIN 32
#define RShoulderZERO 1500

#define LFootPIN 12
#define LFootZERO 1550
#define LAnklePIN 11
#define LAnkleZERO 1500
#define LKneePIN 10
#define LKneeZERO 1500
#define LLegPIN 9
#define LLegZERO 1550
#define LHipPIN 8
#define LHipZERO 1450

#define RFootPIN 21
#define RFootZERO 1500
#define RAnklePIN 22
#define RAnkleZERO 1400
#define RKneePIN 23
#define RKneeZERO 1600
#define RLegPIN 24
#define RLegZERO 1450
#define RHipPIN 25
#define RHipZERO 1500

#define HeadPIN 17
#define HeadZERO 1500

/**
 * main.c
 */

void main(void){
    INIT();
    //If \n add \r
    //DELAY(2000);
    //SEND_INT_UART0(10);
    SEND_INT_UART0(100,1);
    delay_ms(100);
    SEND_STRING_UART0("Test\n\r");
    int i=100;
    while(1){
        //SEND_STRING_UART0("Test\n\r");
        delay_ms(i);
        i+=i;
    }

}
