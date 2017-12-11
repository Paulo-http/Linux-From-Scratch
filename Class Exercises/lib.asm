;------------------------------------------------
;	int strlen(char *msg)
;	-determina numero de bytes da mensagem

strlen:
	push	ebx
	mov		ebx, eax

nextchar:
	cmp		byte [eax], 0
	jz		finished
	inc		eax
	jmp		nextchar

finished:
	sub		eax, ebx
	pop		ebx
	ret

;------------------------------------------------
;	void print(char *msg)
;	- imprime msg em stdout

print:
	push	edx
	push	ecx
	push	ebx
	push	eax
	call	strlen
	mov		edx, eax
	pop		eax
	mov		ecx, eax
	mov		ebx, 1
	mov		eax, 4
	int		80h
	pop		ebx
	pop		ecx
	pop		edx
	ret

;------------------------------------------------
;	void quit()
;	- sai do programa com codigo de erro 0

quit:
	mov		ebx, 0
	mov		eax, 1
	int 	80h
	ret	