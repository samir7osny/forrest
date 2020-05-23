/*
 * MICRO-CONTROLLER_LAYER.c
 *
 *  Created on: Mar 15, 2020
 *      Author: Omar Touny
 */
//#include "MICRO-CONTROLLER_LAYER.h"
#include <stdint.h>
#include"tm4c123gh6pm.h"

void CLCK_INIT(void){
    SYSCTL_RCC2_R |=(1<<31)|(1<<11);
    SYSCTL_RCC_R= 0x078E3AD1;
    //Choose Precision internal Oscillator
    SYSCTL_RCC2_R |=(1<<4) &~(1<<5) &~(1<<6);
    //Disable PLL
    SYSCTL_RCC2_R &=~(1<<13);
    //Setting the Divisor Value =4
    SYSCTL_RCC2_R &=~(1<<22) &~(1<<23) |(1<<24) &~(1<<25) &~(0xF<<26);
    SYSCTL_RCC2_R|=(1<<30);
    while((SYSCTL_RIS_R&0x00000040)==0){}
    SYSCTL_RCC2_R &=~(1<<11);
}
void CLOCK_TEST(){
    SYSCTL_RCC2_R |=0x80000000;
    SYSCTL_RCC2_R |=0x00000800;
    SYSCTL_RCC_R =(SYSCTL_RCC_R&~0x000007C0)+0x0000008;
    SYSCTL_RCC2_R &=~0x00000010;
    SYSCTL_RCC2_R &=~0x00002000;
    SYSCTL_RCC2_R |=0x40000000;
    SYSCTL_RCC2_R =(SYSCTL_RCC2_R&~0x1FC00000)+(4<<22);
    while((SYSCTL_RIS_R&0x00000040)==0){};
    SYSCTL_RCC2_R &=~0x00000800;
}
void SysTick_Init(void){
    NVIC_ST_CTRL_R |=(0<<0); // 1) disable SysTick during setup
    NVIC_ST_RELOAD_R = 0x00FFFFFF; // 2) maximum reload value
    NVIC_ST_CURRENT_R = 0; // 3) any write to current clears it
    NVIC_ST_CTRL_R |=(1<<0)|(0<<1)|(1<<2); // 4) enable SysTick with core clock
}
// The delay parameter is in units of the 80 MHz core clock. (12.5 ns)
void SysTick_Wait(uint32_t delay){
    NVIC_ST_RELOAD_R = delay-1; // number of counts to wait
    NVIC_ST_CURRENT_R = 0;
    while((NVIC_ST_CTRL_R&(1<<16))==0){ // wait for count flag
    }
}


void ADC_INIT(){

    SYSCTL_RCGCADC_R|= (1<<1);
    ADC1_ACTSS_R&=~(1<<3);
    ADC1_EMUX_R|=(1<<12)|(1<<13)|(1<<14)|(1<<15);
    ADC1_SSMUX3_R|=7;
    ADC1_SSCTL3_R|=(1<<1)|(1<<2);
    ADC1_ACTSS_R|=(1<<3);
    ADC1_ISC_R|(1<<3);
}
void GPIO_INIT(){
    //PD0 For The FSR Sensor
    SYSCTL_RCGCGPIO_R|= (1<<3);
    GPIO_PORTD_DIR_R&= ~(1<<1);
    GPIO_PORTD_AFSEL_R|= (1<<0);
    GPIO_PORTD_ADCCTL_R|= (1<<0);
    GPIO_PORTD_DEN_R&= ~(1<<0);
    GPIO_PORTD_AMSEL_R|= (1<<0);

    //PORTF For Testing
    SYSCTL_RCGCGPIO_R|= (1<<5);
    GPIO_PORTF_DIR_R|=(1<<1)|(1<<2)|(1<<3);
    GPIO_PORTF_DEN_R|= (1<<1)|(1<<2)|(1<<3);
    GPIO_PORTF_DATA_R&=~((1<<1)|(1<<2)|(1<<3));
    GPIO_PORTF_DATA_R&=~((1<<1)|(1<<2)|(1<<3));
    //TIMER Clock Initialization
}

// The delay parameter is in units of the 80 MHz core clock. (12.5 ns)
void DELAY(uint32_t _dalay){
    _dalay*=1000000;
    SYSCTL_RCGCTIMER_R|=0x01;
    TIMER0_CTL_R&=~(0x00000001);
    TIMER0_CFG_R=0x00000000;
    TIMER0_TAMR_R=0x00000001;
    //WTIMER0_TAMR_R|=(1<<0);

    TIMER0_TAILR_R= _dalay-1;
    TIMER0_ICR_R =0x00000001;
    TIMER0_CTL_R|=0x00000001;
    while(TIMER0_RIS_R&(1<<0)==0){
    }
    WTIMER0_ICR_R|=(1<<0);
    WTIMER0_CTL_R&=~(1<<1);
    //SYSCTL_RCGCWTIMER_R&=~(1<<0);
}


void UART_INIT(){

    //Enable the UART module using the RCGCUART register
    SYSCTL_RCGCUART_R|= (1<<0)|(1<<1);
    //Enable the clock to the appropriate GPIO module via the RCGCGPIO register
    SYSCTL_RCGCGPIO_R|= (1<<0)|(1<<1);
    //Set the GPIO AFSEL bits for the appropriate pins
    GPIO_PORTB_AFSEL_R|= (1<<1)|(1<<0);
    GPIO_PORTA_AFSEL_R|= (1<<1)|(1<<0);
    //SYSCTL_RCGCGPIO_R= (1<<1) | (1<<0);

    //Configure the PMCn fields in the GPIOPCTL register to assign the UART signals to the appropriate pins
    GPIO_PORTA_PCTL_R|= (1<<0)|(1<<4);
    GPIO_PORTA_DEN_R|= (1<<0)|(1<<1);
    GPIO_PORTB_PCTL_R|= (1<<0)|(1<<4);
    GPIO_PORTB_DEN_R|= (1<<0)|(1<<1);
}

void UART_CONFIG(){
    //BRD=16000000/(16*9600)=104.16666666666666667;
    //UARTFBRD[DIVFRAC] = integer(0.166667 * 64 + 0.5) = 11
    //Disable the UART by clearing the UARTEN bit in the UARTCTL register
    UART0_CTL_R &= ~(1<<0);
    UART1_CTL_R &= ~(1<<0);
    //2. Write the integer portion of the BRD to the UARTIBRD register.
    //UART0_IBRD_R =104;
    //UART1_IBRD_R =104;
    UART0_IBRD_R =8;
    UART1_IBRD_R =8;
    //3. Write the fractional portion of the BRD to the UARTFBRD register.
    //UART0_FBRD_R =11;
    //UART1_FBRD_R =11;
    UART0_FBRD_R =44;
    UART1_FBRD_R =44;
    //4. Write the desired serial parameters to the UARTLCRH register (in this case, a value of 0x0000.0060).
    UART0_LCRH_R |=(1<<5)|(1<<6); //8- data bits , no parity, 1 stop bit
    UART1_LCRH_R |=(1<<5)|(1<<6);
    //UART0_LCRH_R =(0x3<<5);

    //5. Configure the UART clock source by writing to the UARTCC register.
    UART0_CC_R=0x0;
    UART1_CC_R=0x0;
    //6. Optionally, configure the MicroDMA channel (see “Micro Direct Memory Access (MicroDMA)” on page 585) and enable the DMA option(s) in the UARTDMACTL register.
    //7. Enable the UART by setting the UARTEN bit in the UARTCTL register.
    UART0_CTL_R |= (1<<0)|(1<<8)|(1<<9);
    UART1_CTL_R |= (1<<0)|(1<<8)|(1<<9);

}
