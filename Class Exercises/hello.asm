%include	'lib.asm'

SECTION .data
msg1	db		'Informe seu nome:', 0x00
msg2	db		'Oi, ', 0x00

SECTION .bss
sinput:		resb	255

SECTION	.text
global	_start

_start:
	
	mov		eax, msg1
	call	print

	mov		edx, 255
	mov		ecx, sinput
	mov		ebx, 0
	mov		eax, 3
	int		80h

	mov		eax, msg2
	call	print

	mov		eax, sinput
	call	print

	call	quit