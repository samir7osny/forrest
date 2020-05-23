/*
 * MICRO-CONTROLLER_LAYER.h
 *
 *  Created on: Mar 15, 2020
 *      Author: Omar Touny
 */

#ifndef MICRO_CONTROLLER_LAYER_H_
#define MICRO_CONTROLLER_LAYER_H_
//#include <stdint.h>

extern void CLCK_INIT(void);
extern void CLOCK_TEST();
extern void SysTick_Init(void);
extern void SysTick_Wait(uint32_t delay);

extern void DELAY(uint32_t _dalay);

extern void ADC_INIT();

extern void GPIO_INIT();

extern void UART_INIT();
extern void UART_CONFIG();

#endif /* MICRO_CONTROLLER_LAYER_H_ */
