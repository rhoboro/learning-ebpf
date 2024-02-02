https://www.oreilly.co.jp/books/9784814400560/

```bash
# using lima's default vm(qemu,ubuntu) on M2 MacBookAir
# https://github.com/lima-vm/lima
$ limactl start
# Enter vm's shell
$ lima
```

```bash
# install bcc
$ sudo apt-get install bpfcc-tools linux-headers-$(uname -r) linux-tools-common linux-tools-generic llvm
# move to a writable directory
$ cd /tmp
$ cat <<EOF > hello.py
#!/usr/bin/python3

from bcc import BPF

program = r"""
int hello(void *ctx) {
  bpf_trace_printk("Hello World!");
  return 0;
}
"""

b = BPF(text=program)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")

b.trace_print()
EOF

$ sudo python3 hello.py
b'           <...>-4126    [003] d..21  2226.121641: bpf_trace_printk: Hello World!'
b'            bash-4126    [003] d..21  2226.124909: bpf_trace_printk: Hello World!'
b'            bash-4127    [001] d..21  2226.125955: bpf_trace_printk: Hello World!'
b'           <...>-4128    [000] d..21  2226.126704: bpf_trace_printk: Hello World!'
b'           <...>-4129    [002] d..21  2226.127494: bpf_trace_printk: Hello World!'
b'           <...>-4132    [002] d..21  2226.134399: bpf_trace_printk: Hello World!'
b'        lesspipe-4133    [001] d..21  2226.134779: bpf_trace_printk: Hello World!'
b'           <...>-4135    [001] d..21  2226.135404: bpf_trace_printk: Hello World!'
b'           <...>-4136    [000] d..21  2226.136350: bpf_trace_printk: Hello World!'
```
