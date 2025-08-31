import flet as ft
import random
from collections import Counter
from parts.appbar import Appbar
from datetime import datetime
from parts.db import add,procura,quantidade,last_item
class Main_humor(ft.View):
    def __init__(self,route:str,page):
        super().__init__()
        self.route = route
        self.page = page
        self.appbar = Appbar(title='Humorado',page=page)
        self.scroll = ft.ScrollMode.AUTO
# input card drugs
        self.nic = ft.Checkbox(label="Nicotina", value=False,col={'xs':4})
        self.weed = ft.Checkbox(label="Maconha", value=False,col={'xs':4})
        self.alc = ft.Checkbox(label="Alcool", value=False,col={'xs':4})
        self.outer = ft.TextField(visible=False,col={'xs':6})
        self.drug = ft.Card(visible=False,col={'xs':7},content=ft.ResponsiveRow(
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
            columns=12,
            controls=[
                self.nic,
                self.weed,
                self.alc,
                ft.ResponsiveRow(alignment=ft.MainAxisAlignment.START,controls=[
                    ft.Checkbox(label="Outro", value=False,on_change=self.outra_drug,col={'xs':5}),
                    self.outer,
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                    ft.TextButton(text='Salvar',on_click=self.aditivos),ft.TextButton(text='Cancelar',on_click=self.hide_card)
                    ])
            ]#
        ))
# inputs gerais
        self.rd_dia = ft.RadioGroup(content=ft.Row(controls=[
            ft.Radio(label='Ruim',value="ruim"),
            ft.Radio(label='Normal',value="normal"),
            ft.Radio(label='Otimo',value="otimo"),
        ]))
        self.comen = ft.TextField(label='Comentario sobre o dia',multiline=True,min_lines=1,col={'xs':4})
        self.exe = ft.Switch(label="Foi feito exercicio fisico",value=False)
        self.soc = ft.Switch(label="Saiu de casa hoje?",value=False)
        self.adit = ft.Switch(label='Houve aditivos?',on_change=self.show_card,value=False)
        self.grat = ft.TextField(label='Coisas a ser grato no dia de hoje',multiline=True,min_lines=1,col={'xs':7})
        self.sono = ft.TextField(label='Quantas horas de sono?',col={'xs':5})
        self.dia = ft.TextField(label='Data',on_change=self.ver_data,max_length=10)
# banner preview
        self.con_banner = ft.ResponsiveRow(columns=12,controls=[
            ft.Text('Preview')
        ])
        self.banner = ft.Banner(
            open=False,
            content=self.con_banner,
            actions=[
                ft.TextButton('Salvar',on_click=self.adicionar),
                ft.TextButton('Limpar',on_click=self.adicionar,data=1),
                ft.TextButton('Cancelar',on_click=self.hide_card,data=0)
            ]
        )
        fit=ft.ImageFit.CONTAIN
        self.linh1 = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=20,
            run_spacing=20,
            #tight=True,
            controls=[
                ft.TextButton(tooltip='Feliz',data='feliz',on_click=self.set_humor,content=ft.Image(src="images/happy.png",width=60,fit=fit)),
                ft.TextButton(tooltip='Triste',data='triste',on_click=self.set_humor,content=ft.Image(src="images/sad.png",width=60,fit=fit)),
                ft.TextButton(tooltip='Irritado',data='irritado',on_click=self.set_humor,content=ft.Image(src="images/angry.png",width=60,fit=fit)),
                ft.TextButton(tooltip='Ansioso',data='ansioso',on_click=self.set_humor,content=ft.Image(src="images/anxious.png",width=60,fit=fit)),
            ]
        )
        #feliz,triste,irritado,ansioso,orgulhoso,empolgado,frustrado,entediado
        self.linh2 = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=10,
            run_spacing=20,
            #tight=True,
            controls=[
                ft.TextButton(tooltip='Orgulhoso',data='orgulhoso',on_click=self.set_humor,content=ft.Image(src="images/proud.png",width=60,fit=fit)),
                ft.TextButton(tooltip='Empolgado',data='empolgado',on_click=self.set_humor,content=ft.Image(src="images/excited.png",width=60,fit=fit)),
                ft.TextButton(tooltip='Frustrado',data='frustrado',on_click=self.set_humor,content=ft.Image(src="images/frustrated.png",width=60,fit=fit)),
                ft.TextButton(tooltip='Entediado',data='entediado',on_click=self.set_humor,content=ft.Image(src="images/bored.png",width=60,fit=fit))
            ]
        )
#variaveis diversas de controle
        self.h = ''
        self.subs = 'nenhum'
        self.tb = ft.DataTable(
            visible=False,
            columns=[
                ft.DataColumn(label=ft.Text(value='Data'),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text(value='Comentarios do dia')), #
                ft.DataColumn(ft.Text(value='Gratidão do dia'))
            ],
            rows=[]
        )
        self.hoje =datetime.now().strftime("%d/%m/%Y")
    def show_card(self,e):
        if self.adit.value == True:
            self.drug.visible = True
        else:
            self.drug.visible = False
        self.drug.update()
    def hide_card(self,e):
        if e.control.data == 0:
            self.page.close(self.banner)
        else:
            self.drug.visible = False
            self.adit.value = False
            
        self.page.update()
    def outra_drug(self,e):
        if e.control.value == True:
            self.outer.visible = True
            self.outer.update()
        else:
            self.outer.visible = False
            self.outer.update()
    def set_humor(self,e):
        if e.control.data:
            self.h = e.control.data
        else:
            self.h = 'não definido'
    def aditivos(self,e):
        self.subs = ''
        if self.adit.value == True:
            self.subs += '1='
            if self.nic.value == True:
                self.subs+='nicotina+'
            if self.weed.value == True:
                self.subs+='maconha+'
            if self.alc.value == True:
                self.subs+='alcool+'
            if self.outer.visible == True:
                self.subs += self.outer.value
            else:
                self.subs = self.subs[:-1]
    def adicionar(self,e):
        temp = []
        if self.rd_dia.value == None:
            estado = ft.Text(value=f'Estado do dia não defido',color='red')
        else: 
            estado = ft.Text(value=f'O dia de hoje foi {self.rd_dia.value}')
            temp.append(self.rd_dia.value)
        if self.exe.value == False:
            exe = 'Não'
        else: 
            exe = ''
        if self.soc.value == False:
            soc ='Não'
        else: soc = ''
        if self.grat.value == "":
            self.grat.error_text = 'Falta colocar'
            self.grat.update()
            grat = ft.Text(value=f'Não teve nada a ser grato hoje', color='red')
            
        else:
            self.grat.error_text = ''
            grat = ft.Text(value=f'As gratitudes de hoje {self.grat.value}')
            temp.append(self.grat.value)
        if self.sono.value == '':
            self.sono.error_text = 'Falta definir'
            self.sono.update()
            sono = ft.Text(value=f'Não definido',color='red')
        else:
            self.sono.error_text = ''
            sono = ft.Text(value=f'Quantidade de sono {self.sono.value}')
            temp.append(self.sono.value)
        if self.comen.value == '':
            comen = ''
        else: comen = f'-{self.comen.value}'
        if e.control.data == 0: #Preview
            self.con_banner.controls.clear()
            self.page.open(self.banner)
            self.con_banner.controls.append(
                ft.Column([
                    ft.Text(value=f'Humor do dia {self.h}'),
                    ft.Text(value=f'Comentario do dia: {comen}'),
                    estado,
                    ft.Text(value=f'{exe} Houve atividade fisica hoje'),
                    ft.Text(value=f'{soc} Houve interação social hoje'),
                    sono,
                    grat,
                    ft.Text(value=f'Substancias psicoativas {self.subs}'),
                    
                ])
            )
            self.con_banner.update()
            self.page.update()
        elif e.control.data == 1: #Limpar
            self.comen.value,self.grat.value,self.sono.value = '','',''
            self.exe.value,self.soc.value,self.adit.value= False,False,False 
            self.nic.value,self.weed.value,self.alc.value = False,False,False
            self.drug.visible = False
            self.rd_dia.value = None
            self.h = 'não definido'
            self.con_banner.controls.clear()
            self.page.close(self.banner)
            self.page.update()
        else:
            # ('13/01/2025', 'irritado', 'normal-nenhum', 8, True, False, 'nenhum', 'gratitudes')
            if temp:
                ir=(self.hoje,self.h,temp[0]+comen,int(temp[2]),self.exe.value,self.soc.value,self.subs,temp[1])
                c = ("date","humor","dia","sono","exer","soci","subs","grat")   
                add('humorado',c,ir)
            else: pass
           
    def diahumor(self,e):
        temp = []
        if e == 0:
            c = 0
            self.d = ['ruim','normal','otimo']
            for dia in self.d:
                x = procura('humorado',False,True,(dia),'dia')  
                c+=len(x)
                temp.append(len(x))    
        else:
            self.hum = ['feliz','triste','irritado','ansioso','orgulhoso','empolgado','frustrado','entediado']
            for humor in self.hum: 
                x = procura('humorado',False,True,(humor),'humor')     
                temp.append(len(x))  
        return temp
    def boleanos(self,c):
        temp = []
        if c == 0:
            s = procura('humorado',False,True,(1),'exer')
            temp.append(len(s))
            n = procura('humorado',False,True,(0),'exer')
            temp.append(len(n))
        elif c==1:
            s = procura('humorado',False,True,(1),'soci')
            temp.append(len(s))
            n = procura('humorado',False,True,(0),'soci')
            temp.append(len(n))
        else:
            s = procura('humorado',False,True,('='),'subs')
            temp.append(len(s))
            n = procura('humorado',False,True,('nenhum'),'subs')
            temp.append(len(n))
        return temp
    def maisinfo(self,e):
        n,w,a = 0,0,0
        ot = []
        x = procura('humorado',False,True,('1'),'subs')
        for linha in x:
            t =linha[6][2:]
            temp = t.split('+')
            for item in temp:
                if item == 'nicotina':
                    n +=1
                elif item == 'maconha':
                    w+=1
                elif item == 'alcool':
                    a +=1
                else: 
                    ot.append(item)
                    
        v =  [n,w,a,len(ot)]  
        cot = Counter(ot)  
        itens = list(cot.keys())
        quantidades = list(cot.values())
        self.con_banner.controls.clear()
        self.banner.actions.clear()
        self.banner.actions.append(
           ft.TextButton(icon='close',on_click=self.hide_card,data=0) 
        )
        self.page.open(self.banner)
        self.con_banner.controls.append(
            pizza({'xs':12,'md':6},'Quantidade de dias usando aditivos',v,['Tabaco','Weed','Alcool','Outros'])
        )
        self.con_banner.controls.append(
            pizza({'xs':12,'md':6},'Outras substancias usadas',itens,quantidades)
        )
        
        self.con_banner.update()
        self.page.update()

    def tb_cg(self,e):        
        x = procura('humorado',True,False)
        for item in x:
            t = item[2]
            temp = t.split('-')
            if len(temp) >1:
                com = temp[1]
            else: com = 'nenhum'
            self.tb.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(value=item[0],text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text(com)),
                    ft.DataCell(ft.Text(item[7])),
                ])
            )
        self.tb.visible = True
        self.tb.update()
    def show_graf(self,e):
        if e.control.data == 0:
            self.inputs.visible = True
            self.tab_graf.visible = False
            self.tb.visible = False
        else:
            self.inputs.visible = False
            self.tab_graf.visible = True
        self.page.update()

    def ver_data(self,e):
        if self.dia.value == '':
            self.dia.error_text = 'Falta data'
            self.dia.update()
        else:
            raw_text = self.dia.value
            formatted_text = ""
            for i in range(len(raw_text)):
                if i == 2 or i == 4:
                    formatted_text += "/"
                formatted_text += raw_text[i]
            if len(formatted_text) == 10:
                self.dia.value = formatted_text
                self.dia.update()
            else:pass 
    def saveday(self,e):
        if e.control.data == 0:
            self.hoje = self.dia.value
            self.page.close(self.banner)
            self.page.update()

        else:
            self.hoje = datetime.now().strftime("%d/%m/%Y")
            self.page.close(self.banner)
            self.page.update()
    def mudardia(self,e):
        if e.control.value == False:
            self.hoje = datetime.now().strftime("%d/%m/%Y")
        else:
            self.con_banner.controls.clear()
            
            self.con_banner.controls.append(
                self.dia
            )
            self.banner.actions.clear()
            self.banner.actions.append(
                ft.Row([
                    ft.TextButton('Salvar',on_click=self.saveday,data=0),
                    ft.TextButton('Cancelar',on_click=self.saveday,data=1)
                ])
            )
            self.page.open(self.banner)
            self.page.update()

    def build(self):
        self.sel_hum = ft.Column([self.linh1,self.linh2])
        pd = self.diahumor(0)
        ph = self.diahumor(1)
        pex = self.boleanos(c=0)
        psc = self.boleanos(c=1)
        pad = self.boleanos(c=2)
        infodrug = ft.Stack(col={'xs':4},controls=[
            barra({'xs':3},'Dias com aditivos',pad,['Com','Sem'],'Aditivos'),
            ft.IconButton(icon='add',on_click=self.maisinfo,top=10,right=80,tooltip='Mais Info')
        ])
        q = quantidade('humorado','sono')
        s=0
        x = procura('humorado',True)
        for linha in x:
            s += linha[3]
        media = s/q
        horas = int(media)  # Parte inteira (horas)
        minutos = round((media - horas) * 60)
        media_sono = f"{horas} horas e {minutos} minutos"
        l = last_item('humorado')

        self.infos = ft.Column(spacing=15,horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=True,col={'xs':4},controls=[
                        ft.Text('Informações',style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.Text(f'Media de sono: {media_sono}'),
                        ft.Text(f'Quantidade de registros: {q}'),
                        ft.Text(f'Ultimo registro: {l[0]}'),
                        ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                            ft.TextButton('Comentarios e Gratitudes',on_click=self.tb_cg),
                            ft.TextButton('Voltar',data=0,on_click=self.show_graf)
                        ])
        ])
        self.tab_graf = ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER,visible=False,columns=12,controls=[
                        pizza({'xs':3},'Classificação do dia',pd,self.d),
                        pizza({'xs':3},'Classificação por humor',ph,self.hum),
                        self.infos,
                        barra({'xs':3},'Dias de exercicio',pex,['Sim','Não'],'Exercicios fisicos'),
                        barra({'xs':3},'Dias de sociabilidade',psc,['Sim','Não'],'Sociabilidade'),
                        infodrug,
                        self.tb,
                    ])
        self.inputs = ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                columns=12,
                col={'xs':6,'md':5},
                controls=[
                    ft.Text(value=f'Qual seu mood do dia',text_align=ft.TextAlign.CENTER,style=ft.TextThemeStyle.HEADLINE_SMALL,col={'xs':8}),
                    ft.Checkbox(label='Mudar data',value=False,on_change=self.mudardia,col={'xs':4}),
                    self.sel_hum,
                    ft.Divider(color='purple'),
                    self.comen,
                    ft.Container(col={'xs':8},content=self.rd_dia),
                    ft.Divider(color=ft.colors.PURPLE_800),
                    ft.Text('Fatores externos'),
                    ft.Column(col={'xs':5},controls=[
                       self.exe,
                       self.soc, 
                       self.adit,
                    ]),
                    self.drug,
                    ft.Divider(color=ft.colors.PURPLE_800),
                    self.grat,
                    self.sono,
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                        ft.TextButton(text='SUBMIT',on_click=self.adicionar),
                        ft.TextButton(text='PREVIEW',on_click=self.adicionar,data=0),
                        ft.TextButton(text='Show Info',on_click=self.show_graf)
                    ]),
                    
                ]
            )
        return ft.ResponsiveRow(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=30,
            controls=[
                self.inputs,
                self.tab_graf
            ]
        )
    
class pizza(ft.Container): #deixar mais bonito o nome ou criar legenda
    def __init__(self,col,title:str,vals:list,labels:list):
        super().__init__()
        self.col = col
        self.border = ft.border.all(1,'grey')
        self.border_radius = ft.border_radius.all(60)

        style = ft.TextStyle(size=14, color='white', weight=ft.FontWeight.BOLD)
        pie = ft.PieChart(
            expand=True,
            center_space_radius = 0,
            sections_space = 1,
            sections=[]
        )
        cores = ["red", "blue", "green", "cyan", "orange", "purple", "pink", "brown"]
        random.shuffle(cores)
        c = 0
        for item in vals:
            pie.sections.append(
                ft.PieChartSection(
                    item,
                    title = f'{labels[c]} {item}',
                    title_position=1,
                    color=cores[c],
                    radius=80,
                    title_style=style,
                    #border_side=normal_border,
           )
            )
            c +=1

        self.content = ft.Stack(controls=[
            ft.Text(value=title,style=ft.TextThemeStyle.TITLE_MEDIUM ,color='white',top=35,right=100),
            pie,
        ])
class barra(ft.Container):
    def __init__(self,col,title:str,vals:list,labels:list,nome:str):
        super().__init__()
        self.col = col
        self.border_radius = ft.border_radius.all(60)
        self.border = ft.border.all(2,'grey')
        self.margin = 10
        self.padding = 10
        cores = ["red", "blue", "green", "cyan", "orange", "purple", "pink", "yellow"]
        cor = random.sample(cores, 2)
        bar = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=vals[0],
                            width=40,
                            color=cor[0],
                            tooltip=labels[0],
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=vals[1],
                            width=40,
                            color=cor[1],
                            tooltip=labels[1],
                            border_radius=0,
                        ),
                    ],
                ),
            ],
            left_axis=ft.ChartAxis(labels_size=25, title=ft.Text(value=title), title_size=25),
            bottom_axis=ft.ChartAxis(
                labels=[
                ft.ChartAxisLabel(value=0,label=ft.Text(value=labels[0])),
                ft.ChartAxisLabel(value=1,label=ft.Text(value=labels[1]))
                ]
            )
        )
        random.shuffle(cores)
        self.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,tight=True,controls=[
            ft.Text(value=nome,style=ft.TextThemeStyle.TITLE_MEDIUM),
            bar
        ])

