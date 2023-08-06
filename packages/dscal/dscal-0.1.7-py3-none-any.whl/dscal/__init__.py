from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.style as st
import numexpr as ne
import numpy as np
import sympy as sym

class calculus:
    pi=np.pi
    e=np.e
    st.use('ggplot')
    def __init__(self,*expression:list):
        '''Tools for calculus of expressions
         and plotting them
                
        >>> import dscal
        >>> expr=dscal.calculus('sinx','x+5')
        >>> print(expr)
        ['sin(x)', '(x)+5']
        >>> expr1=dscal.calculus('sinx')
        >>> expr2=dscal.calculus('x+5')
        >>> expr3=expr1+expr2
        >>> print(expr3)
        ['sin(x)', '(x)+5']
        >>>
         '''
        self.x=sym.symbols('x')
        self.expressions_=expression
        self.expressions=[]
        for i in expression:
            self.expressions.append(calculus.adjust(i))

    def simplify(self):
        '''Returns arithematic simplified value.
        >>> import dscal
        >>> expr=dscal.calculus('29+6-sin(2)')
        >>> expr.simplify()
        '34.09070257317432'
        '''
        solved=[]
        for i in self.expressions:
            if 'x' not in i:
                solved.append(str(ne.evaluate(i)))
            else:
                solved.append('cannot evaluate expression with variable.')
        if len(solved)==1:
            return solved[0]
        else:
            return tuple(solved)

    def factorize(self):
        '''If factorizable ,returns factorized form of the expression 
        >>> import dscal
        >>> expr=dscal.calculus('x^3-1')
        >>> expr.factorize()
        '(x - 1)*(x^2 + x + 1)'
        >>> '''
        solved_fac=[]
        for i in self.expressions:
            try:
                if 'x' in i:
                    solved_fac.append(calculus.readjust(str(sym.factor(i,self.x))))
                else:
                    solved_fac.append(calculus.primefactor(i))
            except:
                solved_fac.append('Not factorisable')
        if len(solved_fac)==1:
            return solved_fac[0]
        else:
            return tuple(solved_fac)

    def integral(self,limit:list=[None,None]):
        '''Returns integration of the given expression(s).
        >>> import dscal
        >>> expr=dscal.calculus('logx')
        >>> expr.integral()
        'x*logx - x'
        >>> expr.integral([1,10])
        '-9 + 10*log(10)'
        >>> '''
        solved_int=[]
        for i in self.expressions:
            solved_int.append(calculus.readjust(str(sym.integrate(i,(self.x,limit[0],limit[1])))))
        if len(solved_int)==1:
            return solved_int[0]
        else:
            return tuple(solved_int)

    def derivative(self):
        '''Returns dervative of the given expression(s).
        >>> import dscal
        >>> expr=dscal.calculus('secx')
        >>> expr.derivative()
        'sinx/cosx^2'
        >>> '''
        solved_diff=[]
        for i in self.expressions:
            solved_diff.append(calculus.readjust(str(sym.diff(i,self.x))))
        if len(solved_diff)==1:
            return solved_diff[0]
        else:
            return tuple(solved_diff)

    def nature(self,interval:list=None):
        '''Returns nature of the function(expression) given.
        >>> import dscal
        >>> expr=dscal.calculus('x^2+sinx')
        >>> expr.nature()
        'the function is neither increasing nor decreasing.'
        >>> expr.nature([0,3])
        'the function is neither increasing nor decreasing.'
        >>> 
        >>> expr=dscal.calculus('sinx')
        >>> expr.nature()
        'the function is neither increasing nor decreasing.'
        >>> expr.nature([0,1])
        'increasing function'
        >>> '''
        solved_nat=[]
        if interval==None:
            for i in self.expressions:
                if sym.is_decreasing(i)==True:
                    solved_nat.append('decreasing function')
                elif sym.is_increasing(i)==True:
                    solved_nat.append('increasing function')
                else:
                    solved_nat.append('the function is neither increasing nor decreasing.')
        elif len(interval)==2:
            n_interval=sym.Interval(interval[0],interval[1])
            for i in self.expressions:
                if sym.is_decreasing(i,n_interval)==True:
                    solved_nat.append('decreasing function')
                elif sym.is_increasing(i,n_interval)==True:
                    solved_nat.append('increasing function')
                else:
                    solved_nat.append('the function is neither increasing nor decreasing.')
        if len(solved_nat)==1:
            return solved_nat[0]
        else:
            return tuple(solved_nat)

    @staticmethod
    def primefactor(num:int):
        '''Returns prime factorization of a number.              
        >>> import dscal
        >>> dscal.calculus.primefactor(124)
        >>> '2*31*2'
        '''
        a=int(num)
        s=''
        while a!=1:
            for i in range(2,a+1):
                if a%i==0:
                    for j in range(2,i):
                        if i%j==0:
                            break
                    else:
                        s+=f"{i}*"
                        a=a//i
        s=s[:-1]
        return s

    @staticmethod
    def adjust(string:str):
        '''Adjusts mathematical expressions to
        computer(python-based) form.
        >>> import dscal
        >>> dscal.calculus.adjust('sinx+x^3+secx')
        >>> 'sin(x)+(x)**3+1/cos(x)'
        '''
        string=string.lower()
        cd={'sin^-1':'arcsin','cos^-1':'arccos','tan^-1':'arctan','^':'**','cosec':'1/sin','sec':'1/cos','cot':'1/tan','e':f'{np.e}','pi':f'{np.pi}'}
        for i in cd:    
            if i in string:
                string=string.replace(i,cd[i])
        string2=string[0]
        for i in range(1,len(string)):
            if string[i]=='x' and string[i-1].isdigit():
                string2+='*x'
            else:
                string2+=string[i]
        string2=string2.replace('x','(x)')
        return string2

    def plot(self,limit:list=[-10,10]):
        '''Plot 2D graph for the expression(s).
        >>> expr=dscal.calculus('sinx')
        >>> expr.plot()
        >>> expr.plot([-3,10])
        >>> '''
        x=np.arange(limit[0],limit[1],0.01)
        plt.plot(x,x*0,label='x-axis')
        try:
            vals=[]
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                vals.append(max(list(y)))
                plt.plot(x,y,label=self.expressions_[i])
            y_vals=np.arange(-(max(vals)),max(vals),0.1)
            plt.plot(y_vals*0,y_vals,label='y-axis')
        except ValueError:
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                plt.plot(x,y,label=self.expressions_[i])
            y_vals=np.arange(-20,20,0.01)
            plt.plot(y_vals*0,y_vals,label='y-axis')    
        plt.legend()
        plt.show()
    
    def plot_3D(self,limit:list=[-10,10],surface_plot=0,colormap=plt.cm.jet):
        '''Plot 3D graph for the expression(s).
        >>> expr=dscal.calculus('sinx')
        >>> expr.plot_3D()
        >>> expr.plot_3D([-3,10])'''
        x=np.arange(limit[0],limit[1],0.01)
        if surface_plot==1:
            fig=plt.figure()
            a=fig.add_subplot(111,projection='3d')
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                a.plot_trisurf(x,y*y,y,cmap=colormap)
            plt.show()
        elif surface_plot==0:
            fig=plt.figure()
            a=fig.add_subplot(111,projection='3d')
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                plt.plot(x,y*y,y,label=f'{self.expressions[i]}')
            plt.show()

    @staticmethod    
    def readjust(string:str):
        '''Adjusts Mathematical expression
        to human-read form
        Equivalent to inverse of adjust().
        >>> import dscal
        >>> dscal.calculus.readjust('sin(x)+(x)**3+1/cos(x)')
        'sinx+x^3+secx'
        >>> '''
        d={'(x)':'x','*(x)':'x','arcsin': 'sin^-1', 'arccos': 'cos^-1', 'arctan': 'tan^-1', '**': '^', '1/sin': 'cosec', '1/cos': 'sec', '1/tan': 'cot', str(np.e): 'e', str(np.pi): 'pi'}
        for i in d:
            if i in string:
                string=string.replace(i,d[i])
        return string

    def __str__(self):
        '''Returns expressions of the instance print function is assigned to.'''
        return f"{self.expressions}"

    def __add__(self,*others):
        '''Adds calculus instances assigning to a new object.'''
        expressions_sum=self.expressions_
        for ex in others:
            expressions_sum+=ex.expressions_
        return calculus(*expressions_sum)

class graph(calculus):
    def __init__(self,*expression:list):
        '''Access graphs for tkinter GUI applications directly , power of dscal.calculus'''
        super().__init__(*expression)
        
        
    def get_graph2D(self,master,limit=[-10,10]):    
        '''Get FigureCanvasTkAgg figure with 2D projection.'''
        self.figure2=plt.figure()
        x=np.arange(limit[0],limit[1],0.01)
        plt.plot(x,x*0,label='x-axis')
        try:
            vals=[]
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                vals.append(max(list(y)))
                plt.plot(x,y,label=self.expressions_[i])
            y_vals=np.arange(-(max(vals)),max(vals),0.01)
            plt.plot(y_vals*0,y_vals,label='y-axis')
        except ValueError:
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                plt.plot(x,y,label=self.expressions_[i])
            y_vals=np.arange(-20,20,0.01)
            plt.plot(y_vals*0,y_vals,label='y-axis')    
        plt.legend()
        return FigureCanvasTkAgg(self.figure2,master)


    def get_graph3D(self,master,limit=[-10,10],surface_plot=0,colormap=plt.cm.hsv):
        '''Get FigureCanvasTkAgg figure with 3D projection.'''
        x=np.arange(limit[0],limit[1],0.01)
        if surface_plot==1:
            self.figure3=plt.figure()
            a=self.figure3.add_subplot(111,projection='3d')
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                a.plot_trisurf(x,y*y,y,cmap=colormap)
            plt.show()
        elif surface_plot==0:
            self.figure3=plt.figure()
            a=self.figure3.add_subplot(111,projection='3d')
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                plt.plot(x,y*y,y,label=f'{self.expressions[i]}')
        return FigureCanvasTkAgg(self.figure3,master)

    def __add__(self, *others):
        '''Adds graph instances assigning to a new object.'''
        expressions_sum=self.expressions_
        for ex in others:
            expressions_sum+=ex.expressions_
        return graph(*expressions_sum)

    def __str__(self):
        return super().__str__()
    '''Example

        from dscal import graph
        from tkinter import *

        root=Tk()

        expr_graph=graph('sinx','cosx','x')

        expr_graph_canvas=expr_graph.get_graph2D(root)

        expr_graph_canvas.get_tk_widget().pack(side=LEFT,fill=BOTH,expand=True)

        expr_graph_canvas3D=expr_graph.get_graph3D(root)

        expr_graph_canvas3D.get_tk_widget().pack(side=LEFT,fill=BOTH,expand=True)

        root.mainloop() '''