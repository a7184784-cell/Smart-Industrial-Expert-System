import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
import os
warnings.filterwarnings('ignore')

class IndustrialExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🏭 Smart Industrial Expert System")
        self.root.geometry("1400x850")
        self.root.configure(bg='#1a1a2e')
        
        try:
            # الحصول على مسار مجلد ملف Python
            base_dir = os.path.dirname(os.path.abspath(__file__))

            # إنشاء المسار الكامل لملف CSV
            csv_path = os.path.join(base_dir, 'ai4i2020.csv')

            # قراءة البيانات
            self.df = pd.read_csv(csv_path)

        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                f"الملف ai4i2020.csv غير موجود!\n\n"
                f"تأكد أن الملف موجود بجانب ملف uo.py\n\n"
                f"المسار المتوقع:\n{csv_path}"
            )
            self.df = pd.DataFrame()
        

        
        self.knowledge_base = self.initialize_knowledge_base()
        self.rules = self.initialize_rules()

        # تصميم الواجهة
        self.setup_ui()
        
    def initialize_knowledge_base(self):
        """قاعدة المعرفة - تعريف المصطلحات والعلاقات"""
        return {
            'failure_types': {
                'TWF': 'Tool Wear Failure',
                'HDF': 'Heat Dissipation Failure', 
                'PWF': 'Power Failure',
                'OSF': 'Overstrain Failure',
                'RNF': 'Random Failure'
            },
            'severity_levels': {
                0: '✅ Normal',
                1: '⚠️ Warning',
                2: '🔶 High',
                3: '🔴 Critical'
            },
            'priority_levels': {
                0: '🟢 Low',
                1: '🟡 Medium',
                2: '🟠 High', 
                3: '🔴 Urgent'
            }
        }
    
    def initialize_rules(self):
        """قواعد النظام الخبير - IF-THEN قواعد"""
        rules = []
        
        # قاعدة 1: اكتشاف أعطال تبديد الحرارة
        rules.append({
            'id': 'R01',
            'condition': lambda row: (row['Process Temperature [K]'] - row['Air temperature [K]']) < 5 and row['Rotational speed [rpm]'] < 1500,
            'result': lambda row: {
                'fault': 'HDF',
                'severity': 3 if row.get('Process Temperature [K]', 0) > 320 else 2,
                'priority': 3 if row.get('Process Temperature [K]', 0) > 320 else 2,
                'action': 'Stop Machine + Inspect Cooling System' if row.get('Process Temperature [K]', 0) > 320 else 'Inspect Cooling System',
                'explanation': 'فرق الحرارة منخفض مع انخفاض سرعة الدوران، مما يشير إلى مشكلة في تبديد الحرارة'
            }
        })
        
        # قاعدة 2: اكتشاف أعطال تآكل الأداة
        rules.append({
            'id': 'R02',
            'condition': lambda row: row['Tool wear [min]'] > 200 and row['Torque [Nm]'] > 20,
            'result': lambda row: {
                'fault': 'TWF',
                'severity': 3 if row['Tool wear [min]'] > 250 else 2,
                'priority': 3 if row['Tool wear [min]'] > 250 else 2,
                'action': 'Replace Tool Immediately' if row['Tool wear [min]'] > 250 else 'Schedule Tool Replacement',
                'explanation': 'تآكل الأداة مرتفع مع عزم دوران مرتفع، مما يؤدي إلى فشل الأداة'
            }
        })
        
        # قاعدة 3: اكتشاف أعطال الطاقة
        rules.append({
            'id': 'R03',
            'condition': lambda row: row['Torque [Nm]'] < 5 and row['Rotational speed [rpm]'] < 2000,
            'result': lambda row: {
                'fault': 'PWF',
                'severity': 2,
                'priority': 2,
                'action': 'Check Power Supply',
                'explanation': 'انخفاض العزم والسرعة يشير إلى مشكلة في مصدر الطاقة'
            }
        })
        
        # قاعدة 4: اكتشاف أعطال الإجهاد الزائد
        rules.append({
            'id': 'R04',
            'condition': lambda row: row['Torque [Nm]'] > 35 and row['Tool wear [min]'] < 100,
            'result': lambda row: {
                'fault': 'OSF',
                'severity': 3 if row['Torque [Nm]'] > 40 else 2,
                'priority': 3 if row['Torque [Nm]'] > 40 else 2,
                'action': 'Reduce Load + Inspect Machine' if row['Torque [Nm]'] > 40 else 'Monitor Load',
                'explanation': 'عزم دوران مرتفع مع تآكل أداة منخفض يشير إلى إجهاد زائد على الآلة'
            }
        })
        
        # قاعدة 5: اكتشاف الأعطال العشوائية (معدلة)
        rules.append({
            'id': 'R05',
            'condition': lambda row: row.get('Random failure', 0) == 1,  # استخدام العمود الموجود
            'result': lambda row: {
                'fault': 'RNF',
                'severity': 1,
                'priority': 1,
                'action': 'Run Diagnostics',
                'explanation': 'كشف عطل عشوائي غير محدد، يوصى بإجراء فحص شامل'
            }
        })
        
        return rules
    
    def setup_ui(self):
        """تصميم الواجهة الرسومية"""
        # إطار رئيسي
        main_frame = Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
        
        # العنوان
        title_frame = Frame(main_frame, bg='#1a1a2e')
        title_frame.pack(fill=X, pady=(0, 20))
        
        title = Label(title_frame, text='🏭 Smart Industrial Expert System',
                     font=('Helvetica', 28, 'bold'), fg='#4fc3f7', bg='#1a1a2e')
        title.pack()
        
        subtitle = Label(title_frame, text='Fault Diagnosis • Risk Assessment • Maintenance Decision Support',
                        font=('Helvetica', 14), fg='#7f8c8d', bg='#1a1a2e')
        subtitle.pack()
        
        # إطار التحكم
        control_frame = Frame(main_frame, bg='#1a1a2e')
        control_frame.pack(fill=X, pady=10)
        
        # زر اختيار عينة عشوائية
        random_btn = Button(control_frame, text='🎲 Random Sample',
                           font=('Helvetica', 12, 'bold'), bg='#4fc3f7', fg='white',
                           command=self.analyze_random_sample, padx=20, pady=10,
                           relief=FLAT, cursor='hand2')
        random_btn.pack(side=LEFT, padx=5)
        
        # زر تحليل محدد
        self.id_entry = Entry(control_frame, font=('Helvetica', 12), width=10, bg='#2d2d44', fg='white')
        self.id_entry.pack(side=LEFT, padx=5)
        self.id_entry.insert(0, 'ID')
        
        analyze_btn = Button(control_frame, text='🔍 Analyze ID',
                            font=('Helvetica', 12, 'bold'), bg='#6c5ce7', fg='white',
                            command=self.analyze_by_id, padx=20, pady=10,
                            relief=FLAT, cursor='hand2')
        analyze_btn.pack(side=LEFT, padx=5)
        
        # زر عرض الإحصائيات
        stats_btn = Button(control_frame, text='📊 Statistics',
                          font=('Helvetica', 12, 'bold'), bg='#00b894', fg='white',
                          command=self.show_statistics, padx=20, pady=10,
                          relief=FLAT, cursor='hand2')
        stats_btn.pack(side=LEFT, padx=5)
        
        # ملء الفراغ
        Label(control_frame, bg='#1a1a2e').pack(side=RIGHT, expand=True)
        
        # إطار النتائج
        results_frame = Frame(main_frame, bg='#1a1a2e')
        results_frame.pack(fill=BOTH, expand=True)
        
        # إطار النتائج الرئيسي
        left_frame = Frame(results_frame, bg='#1a1a2e')
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # بطاقة النتائج
        self.result_card = Frame(left_frame, bg='#2d2d44', relief=RAISED, bd=2)
        self.result_card.pack(fill=BOTH, expand=True)
        
        # تنسيق النتائج
        self.result_text = scrolledtext.ScrolledText(self.result_card, font=('Consolas', 11),
                                                    bg='#1a1a2e', fg='#e0e0e0',
                                                    insertbackground='white',
                                                    height=20, wrap=WORD)
        self.result_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # إطار الرسم البياني
        right_frame = Frame(results_frame, bg='#1a1a2e')
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
        
        self.fig = Figure(figsize=(7, 5), facecolor='#1a1a2e', dpi=100)
        self.ax = self.fig.add_subplot(111, facecolor='#2d2d44')
        self.canvas = FigureCanvasTkAgg(self.fig, right_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # رسالة افتراضية
        self.result_text.insert(END, "👋 مرحباً بك في نظام الخبراء الذكي!\n\n")
        self.result_text.insert(END, "🔹 انقر على 'Random Sample' لتحليل عينة عشوائية\n")
        self.result_text.insert(END, "🔹 أدخل رقم ID وانقر 'Analyze ID' لتحليل آلة محددة\n")
        self.result_text.insert(END, "🔹 انقر 'Statistics' لعرض إحصائيات النظام\n\n")
        self.result_text.insert(END, "✅ النظام جاهز لتحليل البيانات...")
        self.result_text.config(state=DISABLED)
        
        # شريط الحالة
        self.status_bar = Label(main_frame, text='🟢 System Ready',
                               font=('Helvetica', 10), bg='#1a1a2e', fg='#27ae60',
                               anchor=W, padx=10)
        self.status_bar.pack(fill=X, pady=(10, 0))
    
    def analyze_machine(self, row_data, idx):
        """تحليل بيانات الآلة واستنتاج النتائج"""
        # تحويل البيانات إلى صيغة قابلة للاستخدام
        if isinstance(row_data, pd.DataFrame):
            row = row_data.iloc[0]
        else:
            row = pd.Series(row_data)
        
        # تطبيق القواعد
        detected_faults = []
        for rule in self.rules:
            try:
                if rule['condition'](row):
                    result = rule['result'](row).copy()
                    result['rule_id'] = rule['id']
                    detected_faults.append(result)
            except:
                continue
        
        # الحصول على معلومات الآلة
        machine_info = {
            'ID': idx,
            'Type': row.get('Type', 'N/A'),
            'Air Temp': f"{row.get('Air temperature [K]', 0):.1f} K",
            'Process Temp': f"{row.get('Process Temperature [K]', 0):.1f} K",
            'Speed': f"{row.get('Rotational speed [rpm]', 0):.0f} rpm",
            'Torque': f"{row.get('Torque [Nm]', 0):.1f} Nm",
            'Tool Wear': f"{row.get('Tool wear [min]', 0):.1f} min"
        }
        
        # بناء النتائج النهائية
        if detected_faults:
            # اختيار العطل الأكثر خطورة
            best_fault = max(detected_faults, key=lambda x: x['severity'])
            return {
                'status': '⚠️ Fault Detected',
                'fault_type': self.knowledge_base['failure_types'].get(best_fault['fault'], 'Unknown'),
                'severity': self.knowledge_base['severity_levels'].get(best_fault['severity'], 'Unknown'),
                'priority': self.knowledge_base['priority_levels'].get(best_fault['priority'], 'Unknown'),
                'action': best_fault['action'],
                'explanation': best_fault['explanation'],
                'rule_id': best_fault['rule_id'],
                'all_faults': len(detected_faults),
                'machine_info': machine_info
            }
        else:
            return {
                'status': '✅ Normal Operation',
                'fault_type': 'None',
                'severity': self.knowledge_base['severity_levels'][0],
                'priority': self.knowledge_base['priority_levels'][0],
                'action': 'Continue Normal Operation',
                'explanation': 'جميع المؤشرات ضمن الحدود الطبيعية',
                'rule_id': 'N/A',
                'all_faults': 0,
                'machine_info': machine_info
            }
    
    def display_results(self, results):
        """عرض النتائج في الواجهة"""
        self.result_text.config(state=NORMAL)
        self.result_text.delete(1.0, END)
        
        # عنوان النتائج
        self.result_text.insert(END, "═" * 50 + "\n", 'header')
        self.result_text.insert(END, "  🔍 نظام تشخيص الأعطال - نتائج التحليل\n", 'header')
        self.result_text.insert(END, "═" * 50 + "\n\n", 'header')
        
        # معلومات الآلة
        machine_info = results['machine_info']
        self.result_text.insert(END, "📋 معلومات الآلة\n", 'subheader')
        self.result_text.insert(END, "─" * 40 + "\n", 'header')
        for key, value in machine_info.items():
            self.result_text.insert(END, f"  {key}: {value}\n", 'info')
        self.result_text.insert(END, "\n")
        
        # حالة التشغيل
        self.result_text.insert(END, f"📊 الحالة: {results['status']}\n", 'status')
        
        # نوع العطل
        if results['fault_type'] != 'None':
            self.result_text.insert(END, f"⚠️  نوع العطل: {results['fault_type']}\n", 'fault')
        
        # درجة الخطورة
        self.result_text.insert(END, f"🔄 درجة الخطورة: {results['severity']}\n", 'severity')
        
        # الأولوية
        self.result_text.insert(END, f"⏰ الأولوية: {results['priority']}\n", 'priority')
        
        # الإجراء الموصى به
        self.result_text.insert(END, f"🔧 الإجراء: {results['action']}\n\n", 'action')
        
        # الشرح
        self.result_text.insert(END, "📝 الشرح\n", 'subheader')
        self.result_text.insert(END, "─" * 40 + "\n", 'header')
        self.result_text.insert(END, f"  {results['explanation']}\n", 'explanation')
        
        # قاعدة التشغيل
        if results['rule_id'] != 'N/A':
            self.result_text.insert(END, f"\n  🔗 تم تطبيق القاعدة: {results['rule_id']}\n", 'rule')
        
        # إحصاءات
        self.result_text.insert(END, f"\n  📌 عدد الأعطال المكتشفة: {results['all_faults']}\n", 'info')
        
        # تنسيق الألوان
        self.result_text.tag_configure('header', foreground='#4fc3f7', font=('Helvetica', 12, 'bold'))
        self.result_text.tag_configure('subheader', foreground='#f39c12', font=('Helvetica', 11, 'bold'))
        self.result_text.tag_configure('status', foreground='#ff6b6b' if 'Fault' in results['status'] else '#27ae60', font=('Helvetica', 12, 'bold'))
        self.result_text.tag_configure('fault', foreground='#ff6b6b', font=('Helvetica', 11, 'bold'))
        self.result_text.tag_configure('severity', foreground='#ff6b6b' if 'Critical' in results['severity'] else '#f39c12', font=('Helvetica', 11, 'bold'))
        self.result_text.tag_configure('priority', foreground='#ff6b6b' if 'Urgent' in results['priority'] else '#f39c12', font=('Helvetica', 11, 'bold'))
        self.result_text.tag_configure('action', foreground='#4fc3f7', font=('Helvetica', 11, 'bold'))
        self.result_text.tag_configure('explanation', foreground='#bdc3c7', font=('Helvetica', 10))
        self.result_text.tag_configure('rule', foreground='#f39c12', font=('Helvetica', 10, 'italic'))
        self.result_text.tag_configure('info', foreground='#bdc3c7')
        
        self.result_text.config(state=DISABLED)
        
        # تحديث الرسم البياني
        self.update_chart(results)
        
        # تحديث شريط الحالة
        self.status_bar.config(text=f"🟢 تحليل اكتمل - {results['status']} - {results['action']}")
    
    def update_chart(self, results):
        """تحديث الرسم البياني لعرض بيانات الآلة"""
        self.ax.clear()
        
        machine_info = results['machine_info']
        
        # استخراج القيم العددية
        try:
            temp_air = float(machine_info['Air Temp'].split()[0])
            temp_proc = float(machine_info['Process Temp'].split()[0])
            speed = float(machine_info['Speed'].split()[0])
            torque = float(machine_info['Torque'].split()[0])
            tool_wear = float(machine_info['Tool Wear'].split()[0])
        except:
            return
        
        # إنشاء الرسم البياني
        categories = ['Air Temp', 'Process Temp', 'Speed/100', 'Torque', 'Tool Wear']
        values = [temp_air, temp_proc, speed/100, torque, tool_wear]
        colors = ['#4fc3f7', '#ff6b6b', '#f39c12', '#00b894', '#6c5ce7']
        
        bars = self.ax.bar(categories, values, color=colors, alpha=0.7)
        self.ax.set_ylim(0, max(values) * 1.3)
        self.ax.set_facecolor('#2d2d44')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        
        # إضافة القيم على الأعمدة
        for bar, val in zip(bars, values):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=10)
        
        # إضافة حالة الآلة
        status_color = '#27ae60' if 'Normal' in results['status'] else '#ff6b6b'
        self.ax.text(0.5, 0.95, results['status'], transform=self.ax.transAxes,
                    ha='center', va='top', color=status_color, fontsize=14, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='#2d2d44', edgecolor=status_color, alpha=0.5))
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def analyze_random_sample(self):
        """تحليل عينة عشوائية من البيانات"""
        if self.df.empty:
            messagebox.showerror("Error", "لا توجد بيانات للتحليل!")
            return
            
        try:
            sample = self.df.sample(n=1)
            idx = sample.index[0]
            results = self.analyze_machine(sample, idx)
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", f"حدث خطأ أثناء التحليل: {str(e)}")
    
    def analyze_by_id(self):
        """تحليل آلة برقم ID محدد"""
        if self.df.empty:
            messagebox.showerror("Error", "لا توجد بيانات للتحليل!")
            return
            
        try:
            id_val = self.id_entry.get()
            if not id_val.isdigit():
                messagebox.showwarning("Warning", "الرجاء إدخال رقم ID صحيح")
                return
            
            idx = int(id_val)
            if idx not in self.df.index:
                messagebox.showwarning("Warning", f"لا يوجد آلة برقم ID {idx}")
                return
            
            results = self.analyze_machine(self.df.loc[idx], idx)
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", f"حدث خطأ أثناء التحليل: {str(e)}")
    
    def show_statistics(self):
        """عرض إحصائيات النظام"""
        if self.df.empty:
            messagebox.showerror("Error", "لا توجد بيانات لعرض الإحصائيات!")
            return
            
        try:
            # تحليل جميع البيانات
            results = []
            for idx, row in self.df.iterrows():
                result = self.analyze_machine(row, idx)
                results.append(result)
            
            # حساب الإحصائيات
            total = len(results)
            normal = sum(1 for r in results if 'Normal' in r['status'])
            faults = total - normal
            
            # إحصائيات الأعطال
            fault_types = {}
            for r in results:
                if r['fault_type'] != 'None':
                    fault_types[r['fault_type']] = fault_types.get(r['fault_type'], 0) + 1
            
            # عرض النتائج
            stats_window = Toplevel(self.root)
            stats_window.title("📊 إحصائيات النظام")
            stats_window.geometry("600x500")
            stats_window.configure(bg='#1a1a2e')
            
            stats_text = scrolledtext.ScrolledText(stats_window, font=('Consolas', 11),
                                                  bg='#2d2d44', fg='#e0e0e0',
                                                  insertbackground='white', wrap=WORD)
            stats_text.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            # كتابة الإحصائيات
            stats_text.insert(END, "═" * 40 + "\n", 'header')
            stats_text.insert(END, "  📊 إحصائيات النظام الخبير\n", 'header')
            stats_text.insert(END, "═" * 40 + "\n\n", 'header')
            
            stats_text.insert(END, f"📌 إجمالي الآلات: {total}\n", 'info')
            stats_text.insert(END, f"✅ الآلات السليمة: {normal}\n", 'good')
            stats_text.insert(END, f"⚠️ الآلات المعطلة: {faults}\n\n", 'bad')
            
            stats_text.insert(END, "📊 توزيع الأعطال\n", 'subheader')
            stats_text.insert(END, "─" * 30 + "\n", 'header')
            for fault_type, count in fault_types.items():
                percentage = (count / faults * 100) if faults > 0 else 0
                stats_text.insert(END, f"  {fault_type}: {count} ({percentage:.1f}%)\n", 'fault')
            
            stats_text.insert(END, f"\n📈 معدل الأعطال: {(faults/total*100):.2f}%\n", 'info')
            stats_text.insert(END, f"🔹 عدد القواعد: {len(self.rules)}\n", 'info')
            
            # تنسيق الألوان
            stats_text.tag_configure('header', foreground='#4fc3f7', font=('Helvetica', 14, 'bold'))
            stats_text.tag_configure('subheader', foreground='#f39c12', font=('Helvetica', 12, 'bold'))
            stats_text.tag_configure('info', foreground='#bdc3c7')
            stats_text.tag_configure('good', foreground='#27ae60', font=('Helvetica', 11, 'bold'))
            stats_text.tag_configure('bad', foreground='#ff6b6b', font=('Helvetica', 11, 'bold'))
            stats_text.tag_configure('fault', foreground='#f39c12')
            
            stats_text.config(state=DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"حدث خطأ أثناء عرض الإحصائيات: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = IndustrialExpertSystem(root)
    root.mainloop()