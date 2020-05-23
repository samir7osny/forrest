/*
 * ABSTRACTION_LAYER.h
 *
 *  Created on: Mar 15, 2020
 *      Author: Omar Touny
 */

#ifndef ABSTRACTION_LAYER_H_
#define ABSTRACTION_LAYER_H_

//#include <stdint.h>
//#include"tm4c123gh6pm.h"
//#include"MICRO-CONTROLLER_LAYER.h"

extern void INIT(void);

extern char READ_CHAR_UART0();
extern void SEND_CHAR_UART0(char c);
extern void SEND_INT_UART0(int c,int space);
extern void SEND_STRING_UART0(char *string);
extern char READ_CHAR_UART1();
extern void SEND_CHAR_UART1(char c);
extern void SEND_STRING_UART1(char *string);

extern uint32_t ADC_Value();

extern void delay_ms(uint32_t delay);
#endif /* ABSTRACTION_LAYER_H_ */
