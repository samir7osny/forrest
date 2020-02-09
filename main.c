#include <stdint.h>
#include"tm4c123gh6pm.h"

/**
 * main.c
 */
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
void SEND_STRING_UART0(char *string){
    while(*string){
        SEND_CHAR_UART0(*(string++));
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
    UART0_IBRD_R =104;
    UART1_IBRD_R =104;
    //3. Write the fractional portion of the BRD to the UARTFBRD register.
    UART0_FBRD_R =11;
    UART1_FBRD_R =11;
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
void UART0_TESTING(char c){
    SYSCTL_RCGCGPIO_R|= (1<<5);
    GPIO_PORTF_DIR_R|=(1<<1)|(1<<2)|(1<<3);
    GPIO_PORTF_DEN_R|= (1<<1)|(1<<2)|(1<<3);
    GPIO_PORTF_DATA_R&=~((1<<1)|(1<<2)|(1<<3));
    SEND_STRING_UART0("Enter, r, g , b : \n \r");
    c= READ_CHAR_UART0();
    SEND_CHAR_UART0(c);
    SEND_STRING_UART0("\n");

    switch(c){
          case 'r':
              GPIO_PORTF_DATA_R|=(1<<1);
              break;
          case 'g':
              GPIO_PORTF_DATA_R|=(1<<3);
              break;
          case 'b':
              GPIO_PORTF_DATA_R|=(1<<2);
              break;
          default:
              GPIO_PORTF_DATA_R&=~((1<<1)|(1<<2)|(1<<3));
              break;
          }
}
int main(void){
    char c;
    UART_INIT();
    UART_CONFIG();
    //SEND_STRING_UART1("2P900#8P1500T100\r\n");
    //SEND_STRING_UART1("#2P900T2000\r\n");
    c= READ_CHAR_UART1();
    SEND_CHAR_UART0(c);
    while(1){

        //SEND_STRING_UART1("#2P1500T1000");


    }

}
