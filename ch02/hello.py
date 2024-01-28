#!/usr/bin/python3

from bcc import BPF

program = r"""
int hello(void *ctx) {
  bpf_trace_printk("Hello World!");
  return 0;
}
"""

b = BPF(text=program)
# ユーザ空間の名前からカーネル内部の関数名を取得
syscall = b.get_syscall_fnname("execve")
# => b'__arm64_sys_execve'
print(syscall)
# execve()の実行のたびにeBPFプログラムを呼び出すよう登録
b.attach_kprobe(event=syscall, fn_name="hello")
# 専用領域に出力されたトレース結果（コンテキストを含む）を画面に出力し続ける
# 実際のbpf_trace_printk()の出力先は /sys/kernel/debug/tracing/trace_pipe 擬似ファイル
b.trace_print()
