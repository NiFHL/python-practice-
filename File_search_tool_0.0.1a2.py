# -*- coding:utf-8 -*-

# File scanning tool

import os, pickle, tkinter, numpy, json
from tkinter import filedialog as tk_filedialog
from tkinter import messagebox as tk_messagebox

class Mains():
    def scan(self, path):
        self.return_value = {'files':[], 'dirs':[]}
        for self.root, self.dirs, self.files in os.walk(path):
            for self.name in self.files:
                self.return_value['files'].append(os.path.join(self.root, self.name))

            for self.name in self.dirs:
                self.return_value['dirs'].append(os.path.join(self.root, self.name))

        return self.return_value
    
    def judge(self, strs, accord):
        if accord == '*':
            return True

        if '*' not in accord and '?' not in accord:
            if strs == accord:
                return True
            else:
                return False

        elif '*' in accord and '?' not in accord:
            self.accord_list = []
            self.accord_find = []

            accord_temp = accord.split('*')
            for i in accord_temp:
                if i != '':
                    self.accord_list.append(i)

            for i in self.accord_list:
                if i in strs:
                    self.accord_find.append(strs.find(i))
                    strs = strs[strs.find(i)+len(i):]

                else:
                    return False

            for i in self.accord_find[1:]:
                if i == 0:
                    return False

            if accord[0] == '*' and self.accord_find[0] != 0:
                if accord[len(accord)-1] == '*' and len(strs) != 0:
                    return True

                elif accord[len(accord)-1] != '*' and len(strs) == 0:
                    return True

                else:
                    return False

            elif accord[0] != '*' and self.accord_find[0] == 0:
                if accord[len(accord)-1] == '*' and len(strs) != 0:
                    return True

                elif accord[len(accord)-1] != '*' and len(strs) == 0:
                    return True

                else:
                    return False

            else:
                return False

        else:
            return False

    def judges(self, strs, accords):
        self.list_accord = accords.split(';')
        self.stres       = strs.replace('/', '\\')
        self.list_strs   = self.stres.split('\\')
        self.result_out = False
        for self.accord in self.list_accord:
            if self.judge(self.list_strs[-1], self.accord):
                self.result_out = True

        return self.result_out



class Lists():
    def def_explorer(self):
        global output
        self.path = output[self.root_list.curselection()[0]].replace('/', '\\')
        os.system('explorer /select,'+self.path)

    def main(self):
        global output
        self.root = tkinter.Tk()

        self.root_sw = self.root.winfo_screenwidth()
        self.root_sh = self.root.winfo_screenheight()

        self.root.geometry('1280x720+'+str(int( (self.root_sw-1280)/2 ))+'+'+str(int( (self.root_sh-720-20)/2 )))
        self.root.title('筛选结果')

        self.root_Scrollbar_y = tkinter.Scrollbar(self.root)

        self.root_Scrollbar_x = tkinter.Scrollbar(self.root, orient='horizontal')


        self.root_list = tkinter.Listbox(self.root, height = 1, width = 10, xscrollcommand=self.root_Scrollbar_x.set, yscrollcommand=self.root_Scrollbar_y.set)
        for self.i in output:
            self.root_list.insert("end", self.i)

        self.root_Scrollbar_y.config(command=self.root_list.yview)
        self.root_Scrollbar_x.config(command=self.root_list.xview)

        self.root_button = tkinter.Button(self.root, text = '在文件资源管理器中显示', relief="groove", command=self.def_explorer)

        self.root_button.pack(side="bottom", fill='x')
        self.root_Scrollbar_y.pack(side="right", fill="y")
        self.root_list.pack(fill="both", expand="yes")
        self.root_Scrollbar_x.pack(side="top", fill='x')

        self.root.mainloop()



class Roots():
    # 创建主窗口框架
    def main(self):
        self.root = tkinter.Tk()

        self.root_sw = self.root.winfo_screenwidth()
        self.root_sh = self.root.winfo_screenheight()

        self.root.geometry('500x300+'+str(int( (self.root_sw-500)/2 ))+'+'+str(int( (self.root_sh-300-20)/2 )))
        self.root.title('文件搜索工具 v0.0.1a2')
        self.root.resizable(width=False, height=False) # 禁止调整窗口大小

    def default(self):
        self.root_choice_file = tkinter.IntVar() # <变量>.set(<值>) 对其进行修改
        self.root_choice_dirs = tkinter.IntVar() # <变量>.get()     获取对应的值

        self.root_choice_file.set(1)

    def bin_error(self, mode=0):
        if mode == 1:
            tk_messagebox.showerror('[ERROR] 出错啦！', '程式出现了一点错误\n这也不能说是一个BUG 只是单纯的技术不到位\n快去把作者骂一顿')

        if mode == 2:
            tk_messagebox.showinfo('[INFO] 信息', '咱先扫出点数据再导出好伐\n乖 听话')
        
        if mode == 3:
            tk_messagebox.showinfo('[INFO] 信息', '咱先扫出点数据再进行筛选好伐\n哪怕是导入的也行\n乖 听话')
        
        if mode == 4:
            tk_messagebox.showinfo('[INFO] 信息', '咱先把规则写好再进行筛选好伐\n乖 听话')
        
        if mode == 5:
            tk_messagebox.showinfo('[INFO] 信息', '文件和文件夹总得选一个吧\n乖 听话')
        
        if mode == 6:
            tk_messagebox.showinfo('[INFO] 信息', '未能找到任何符合规定的文件或文件夹\n请尝试更改筛选关键词或者...\n有没有可能这是个BUG...')

    def bin_started(self):
        global global_dict, output
        if len(global_dict['files']) == len(global_dict['dirs']) == 0:
            self.bin_error(3)
            return False
        
        if self.root_Entry_target.get() == '':
            self.bin_error(4)
            return False

        if self.root_choice_file.get() == self.root_choice_dirs.get() == 0:
            self.bin_error(5)
            return False

        output = []

        if self.root_choice_file.get():
            for self.strs in global_dict['files']:
                if Main.judges(self.strs, self.root_Entry_target.get()):
                    output.append(self.strs)

        if self.root_choice_dirs.get():
            for self.strs in global_dict['dirs']:
                if Main.judges(self.strs, self.root_Entry_target.get()):
                    output.append(self.strs)

        if len(output) == 0:
            self.bin_error(6)
            return False

        List.main()

    def bin_allpath(self):
        global global_dict
        for self.disk in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.path = self.disk+':\\'
            if os.path.isdir(self.path):
                self.temp_dict = Main.scan(self.path)
                global_dict['files'] += self.temp_dict['files']
                global_dict['dirs']  += self.temp_dict['dirs']
                self.root_Message_fileinfo['text'] = str(len(global_dict['files']))+'\n'+str(len(global_dict['dirs']))

    def bin_setpath(self):
        global global_dict
        self.path = tk_filedialog.askdirectory(title='选择扫描目录')
        if os.path.isdir(self.path):
            self.path.replace('/', '\\')
            if self.path[-1] != '\\':
                self.path = self.path + '\\'
            self.temp_dict = Main.scan(self.path)

            global_dict['files'] += self.temp_dict['files']
            global_dict['dirs']  += self.temp_dict['dirs']

            self.root_Message_fileinfo['text'] = str(len(global_dict['files']))+'\n'+str(len(global_dict['dirs']))
        
        elif self.path == '':
            pass

        else:
            self.bin_error(1)

    def bin_delpath(self):
        global global_dict
        del global_dict
        global_dict = {'files':[], 'dirs':[]}
        self.root_Message_fileinfo['text'] = str(len(global_dict['files']))+'\n'+str(len(global_dict['dirs']))

    def bin_dataint(self):
        #pass # 这个东西有点小问题
        global global_dict
        self.file_path = tk_filedialog.askopenfilename(title='选择一个FCT数据文件', filetypes=[('数据文件', '*.npy'), ('配置文件', '*.ini'), ('Json', '*.json'), ('All Files', '*')])

        if self.file_path != '':
            self.temp_dict = numpy.load(self.file_path, allow_pickle=True)

            global_dict['files'] += self.temp_dict.item().get('files')
            global_dict['dirs']  += self.temp_dict.item().get('dirs')

        self.root_Message_fileinfo['text'] = str(len(global_dict['files']))+'\n'+str(len(global_dict['dirs']))

    def bin_dataout(self):
        global global_dict
        if len(global_dict['files']) == len(global_dict['dirs']) == 0:
            self.bin_error(2)
            return False

        self.path = tk_filedialog.asksaveasfilename(title='导出扫描数据', filetype=[('数据文件', '*.npy')]) # , defaultextension='.fdict'

        if self.path != '':
            numpy.save(self.path, global_dict)

    def sbin(self):
        self.root_Label_status = tkinter.Label(self.root, text='状态：空闲', justify='left', bg='#cccccc', anchor='w')
        self.root_Label_remind = tkinter.Label(self.root, text='在下面键入筛选关键词 支持通配符"*" 使用";"分割 空格也会当成字符串处理')

        self.root_Message_helptext = tkinter.Message(self.root, anchor='w'     , justify='l', width=450, text='使用方式：扫描目标文件夹 -> 输入筛选关键词 -> 开始筛选  是不是特别简单\n在扫描过程中磁盘占用过高均属于正常现象\n你可以将扫描结果保存以便于下次直接导入')
        self.root_Message_fileinfo = tkinter.Message(self.root, anchor='e'     , justify='r', width=225, text='0\n0')
        self.root_Message_pathinfo = tkinter.Message(self.root, anchor='center', justify='l',            text='文件\n文件夹')

        self.root_Checkbutton_file = tkinter.Checkbutton(self.root, variable=self.root_choice_file, onvalue = 1, offvalue = 0)
        self.root_Checkbutton_dirs = tkinter.Checkbutton(self.root, variable=self.root_choice_dirs, onvalue = 1, offvalue = 0)

        self.root_Entry_target = tkinter.Entry(self.root)

        self.root_Button_started = tkinter.Button(self.root, relief='groove', command=self.bin_started ,text='开始筛选', )
        self.root_Button_allpath = tkinter.Button(self.root, relief='groove', command=self.bin_allpath, text='扫描电脑上所有的盘符')
        self.root_Button_setpath = tkinter.Button(self.root, relief='groove', command=self.bin_setpath, text='扫描指定目录')
        self.root_Button_delpath = tkinter.Button(self.root, relief='groove', command=self.bin_delpath, text='清除已扫描的项目')
        self.root_Button_dataint = tkinter.Button(self.root, relief='groove', command=self.bin_dataint, text='导入扫描文件')
        self.root_Button_dataout = tkinter.Button(self.root, relief='groove', command=self.bin_dataout, text='导出扫描文件')


        self.root_Label_status.pack(side="bottom", fill='x')

        self.root_Message_helptext.place(x=25 , rely=0   , width=450, y=5)
        self.root_Message_fileinfo.place(x=25 , rely=0.35, width=225)
        self.root_Message_pathinfo.place(x=250, rely=0.35)

        self.root_Checkbutton_file.place(x=300, rely=0.35)
        self.root_Checkbutton_dirs.place(x=300, rely=0.40, y=2)

        self.root_Button_allpath.place(x=25 , rely=0.25, width=150)
        self.root_Button_setpath.place(x=175, rely=0.25, width=150)
        self.root_Button_delpath.place(x=325, rely=0.25, width=150)
        self.root_Button_dataint.place(x=25 , rely=0.5 , width=225)
        self.root_Button_dataout.place(x=250, rely=0.5 , width=225)
        self.root_Button_started.place(x=25 , rely=0.8 , width=450)

        self.root_Label_remind.place(x=25, rely=0.6, width=450)
        self.root_Entry_target.place(x=25, rely=0.7, width=450)

    def dev(self):
        pass

    def __init__(self):
        self.main()
        self.default()
        self.sbin()
        self.root.mainloop()



global_dict = {'files':[], 'dirs':[]}

List = Lists()
Main = Mains()
Root = Roots()
