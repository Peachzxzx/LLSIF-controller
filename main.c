/*
 *  LLSIF Arcade Controller
 *  Copyright (C) 2020  Peerawich Pruthametvisut
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <avr/io.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include <avr/pgmspace.h>   /* required by usbdrv.h */

#include "usbdrv.h"

/*  Button formation diagram
 *    
 *    A               I   |
 *      B           H     |
 *        C       G       | Right
 *          D   F         |
 *            E           |
 */

// Python is slower than AVR operation
#define SWITCH_PRESSED_A() ((PINB & (1<<PB0))==0)
#define SWITCH_PRESSED_B() ((PINB & (1<<PB1))==0)
#define SWITCH_PRESSED_C() ((PINB & (1<<PB2))==0)
#define SWITCH_PRESSED_D() ((PINB & (1<<PB3))==0)
#define SWITCH_PRESSED_E() ((PINB & (1<<PB4))==0)
#define SWITCH_PRESSED_F() ((PINC & (1<<PC0))==0)
#define SWITCH_PRESSED_G() ((PINC & (1<<PC1))==0)
#define SWITCH_PRESSED_H() ((PINC & (1<<PC2))==0)
#define SWITCH_PRESSED_I() ((PINC & (1<<PC3))==0)
//

#define RQ_GET_SWITCH      10

void init_peri()
{
	DDRB = 0x1F;
	DDRC = 0x0F;

	PORTB = 0x1F;
	PORTC = 0x0F;
}

/* ------------------------------------------------------------------------- */
/* ----------------------------- USB interface ----------------------------- */
/* ------------------------------------------------------------------------- */
usbMsgLen_t usbFunctionSetup(uint8_t data[8])
{
	usbRequest_t *rq = (void *)data;

	/* declared as static so they stay valid when usbFunctionSetup returns */
	static uint8_t buttonsState[9];
	static uint8_t state = 0;
	static uint8_t switch_state;

	switch (rq->bRequest)
	{
	case RQ_SWITCH_MODE:
		state = ~state;
			PORTD ^= 0b1000;
		usbMsgPtr = (uint8_t*) &state;
		return 1;
		break;
	case RQ_GET_SWITCH_A:
		switch_state = SWITCH_PRESSED_A();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_B:
		switch_state = SWITCH_PRESSED_B();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_C:
		switch_state = SWITCH_PRESSED_C();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_E:
		switch_state = SWITCH_PRESSED_E();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_F:
		switch_state = SWITCH_PRESSED_F();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_G:
		switch_state = SWITCH_PRESSED_G();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_H:
		switch_state = SWITCH_PRESSED_H();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH_I:
		switch_state = SWITCH_PRESSED_I();
		usbMsgPtr = (uint8_t*) &switch_state;
		return 1;
		break;
	case RQ_GET_SWITCH:
		buttonsState[0] = SWITCH_PRESSED_A();
		buttonsState[1] = SWITCH_PRESSED_B();
		buttonsState[2] = SWITCH_PRESSED_C();
		buttonsState[3] = SWITCH_PRESSED_D();
		buttonsState[4] = SWITCH_PRESSED_E();
		buttonsState[5] = SWITCH_PRESSED_F();
		buttonsState[6] = SWITCH_PRESSED_G();
		buttonsState[7] = SWITCH_PRESSED_H();
		buttonsState[8] = SWITCH_PRESSED_I();
		buttonsState[9] = 1;
		switch_state = 9;
		while (switch_state--)
		{
		  	if (buttonsState[switch_state])
		  	{
				buttonsState[9] = 0;
				break;
		  	}
		}
		usbMsgPtr = buttonsState;
		return 10;
		break;
	}

	/* default for not implemented requests: return no data back to host */
	return 0;
}

/* ------------------------------------------------------------------------- */
int main(void)
{
	init_peri();

	usbInit();

	/* enforce re-enumeration, do this while interrupts are disabled! */
	usbDeviceDisconnect();
	_delay_ms(300);
	usbDeviceConnect();

	/* enable global interrupts */
	sei();

	/* main event loop */
	for(;;)
	{
		usbPoll();
	}

	return 0;
}

/* ------------------------------------------------------------------------- */
