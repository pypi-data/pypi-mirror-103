# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import argparse
from subprocess import Popen, PIPE

def insdat():
    # Input data, var, and pass for encrypting.
    
    from tkinter import Tk, Label, Entry, E, simpledialog

    root = Tk()
    root.withdraw()
    class MyDialog(simpledialog.Dialog):
    
        def body(self, master):
            self.title('Choose File')
            Label(master, text="Data: ").grid(row=0, column = 0, sticky = E)
            self.e1 = Entry(master, show = '-')
            self.e1.grid(row=0, column=1)
            Label(master, text="Var: ").grid(row=1, column = 0, sticky = E)
            self.e2 = Entry(master)
            self.e2.grid(row=1, column=1)
            Label(master, text="Pass: ").grid(row=2, column = 0, sticky = E)
            self.e3 = Entry(master, )
            self.e3.grid(row=2, column=1)            
            return self.e1
    
        def apply(self):
            if self.e1.get() and self.e2.get() and self.e3.get():
                self.result = (self.e1.get(), self.e2.get(), self.e3.get())
            else:
                self.result = None
                
    d = MyDialog(root)
    root.destroy()
    if d.result:
        return d.result

def pssd():
    
    from tkinter import Tk, Label, Entry, E, simpledialog

    root = Tk()
    root.withdraw()
    class MyDialog(simpledialog.Dialog):
    
        def body(self, master):
            self.title('Choose File')
            Label(master, text="Pass: ").grid(row=0, column = 0, sticky = E)
            self.e1 = Entry(master, show = '-')
            self.e1.grid(row=0, column=1)            
            return self.e1
    
        def apply(self):
            self.result = self.e1.get()
                
    d = MyDialog(root)
    root.destroy()
    if d.result:
        return d.result    
    
def cmsk(data: str, varn: str, base: str):
    # WARNING:
    # Do not set variable that already exist and important.
    
    try:
        lb = len(base)
        base = sum([ord(i) for i in base])
        base = base - lb if base > lb else base + lb
        nlt = ''.join([chr(ord(i) + base) for i in data]).encode('punycode')
    except Exception as e:
        raise e
    
    pnam = f'setx {varn} {nlt.decode()}'
    with Popen(pnam, stdout = PIPE, bufsize = 1, universal_newlines = True, text = True) as p:
        for line in p.stdout:
            print(line, end='')
    print(f'var: {varn}')
    del lb, base, nlt
    
def reading(data: str, base: str):
    # reading var that created
    
    lb = len(base)
    base = sum([ord(i) for i in base])
    base = base - lb if base > lb else base + lb        
    nlt = ''.join([chr(ord(i) - base) for i in data.encode().decode('punycode')])        
    print(nlt)
    del lb, base, nlt
        
def main():
    parser = argparse.ArgumentParser(prog = "CP", description = 'Create Password')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", 
                               action = 'store_true', 
                               help = 'Creating encrypted password file',
                              )
    group.add_argument("-r", "--read", 
                               nargs = 1,
                               type = str,
                               help = 'Read ecnrypted password',
                              )
    args = parser.parse_args()
    if args.create:
        a = insdat()
        if a:
            cmsk(a[0], a[1], a[2])
        else:
            print('Please fill all fields!')
    elif args.read:
        a = pssd()
        if a:
            reading(args.read[0], a)
        else:
            print('Please fill field!')

if __name__ == "__main__":
    main()