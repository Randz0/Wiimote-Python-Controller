Some important details to include

Button Codes:
	* The DLL I compiled returns codes which are supposed to be enums in C which get casted to chars.
	* I've taken the liberty to simply document what these seemingly random #'s mean so here you go:

	* Event ID's (event.type)
		* 0 --> No event ocurred on wiimote
		* 1 --> Button Pressed Event ocurred on wiimtoe
		* 2 --> Button Released Event ocurred on wiimote

	* Butt ID's
		* 0 --> 1 button on wiimote
		* 1 --> 2 button on wiimote
		* 2 --> b back button on wiimote
		* 6 --> D-Pad left on wiimote

	* As a final note you can also find these in the source code for the C code if you want more details