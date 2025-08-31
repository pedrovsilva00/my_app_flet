import flet as ft  
from parts.appbar import Appbar
from parts.db import procura,add,atualiza,excluir
from datetime import datetime

class Main_financa(ft.View):
    def __init__(self,route:str,page):
        super().__init__()
        self.route = route
        self.page = page
        self.appbar = Appbar(title='Finanças',page=page)
        self.scroll = ft.ScrollMode.AUTO
    def build(self):
        return ft.ResponsiveRow(columns=12,controls=[
            ft.Column(col={'xs':12,'md':4},controls=[
                Finances('aaaa')
            ]),
            ft.Column(col={'xs':12,'md':8},controls=[
                wishlist('bbbbb')
            ]),
        ])
class Finances(ft.Container):
    def __init__(self,txt):
        super().__init__()  
        t =txt
        self.money = ft.TextField(label='Valor',prefix_text='R$',col={'xs':6,'md':4})
        self.categ = drop({'xs':6,'md':5},'Categoria',['Salario','Investimento','Alimentação','Transporte','Palas','Lazer','Educação','Casa','Roupa','Festas','Saúde',"Outros"])
        self.categ.on_change = self.outer    
        self.in_outro  = ft.TextField(label='Outros',col={'xs':12,'md':3},visible=False)
        self.dia = ft.TextField(label='Data',col={'xs':7,'md':8},visible=False,on_change=self.ver_data)
        self.input_finance = ft.Column(
            spacing=15,
            run_spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value='Perdas e Ganhos'),
                ft.Text(value='Balanço '),
                ft.ResponsiveRow(columns=12,controls=[
                    self.money,
                    self.categ,
                    self.in_outro,
                    ft.Checkbox(label='Mudar data',value=False,on_change=self.adicionar,col={'xs':5,'md':4},data=0),
                    self.dia
                ]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[
                    ft.TextButton(text='Historico'),
                    ft.TextButton(text='Adicionar',on_click=self.adicionar)
                ])
            ]
        )
        self.tb_finance = ft.DataTable(
            expand=True,
            columns=[
                ft.DataColumn(ft.Text(value='Ações'),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text(value='Data'),heading_row_alignment=ft.MainAxisAlignment.CENTER), #
                ft.DataColumn(ft.Text(value='Valor')), # 
                ft.DataColumn(ft.Text(value='Categoria')), # 
            ],
            rows=[]
        )
        self.pesq = ft.TextField(label='Pesquisa por data',on_change=self.ver_data,col={'xs':5})
        self.history = ft.ResponsiveRow(columns=12,controls=[
            ft.TextButton('Gastos',col={'xs':3},data=0,on_click=self.show_finance),
            ft.TextButton('Ganhos',col={'xs':3},data=1,on_click=self.show_finance),
            self.pesq,
            ft.IconButton(icon='search',col={'xs':1},icon_size=15),
            self.tb_finance
        ])
        self.hoje = ''
        self.content = ft.Column(spacing=15,run_spacing=15,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[
            self.input_finance,
            self.history
            ])
    def adicionar(self,e):
        ir = ()
        hoje = datetime.now().strftime("%d/%m/%Y")
        if e.control.data == 0:
            if e.control.value == False:
                self.dia.visible = False
                self.dia.update()
            else:
                self.dia.visible = True
                self.dia.update()
        else: 
            if self.dia.value == '':
                self.dia.error_text ='Faltando'
                self.dia.update()
            else:
                self.dia.error_text = ''
                hoje = self.dia.value
            if self.categ.value == '':
                self.categ.error_text = 'Definir categoria'
                self.categ.update()
            elif self.categ.value == 'Salario' or self.categ.value == 'Investimento':
                ir += (hoje,True,self.categ.value)
            elif self.categ.value == 'Outros':
                if self.in_outro.value == '':
                    self.in_outro.error_text = 'Falta definir'
                    self.in_outro.update()
                else: 
                    self.in_outro.error_text = ''
                    ir += (hoje,False,self.in_outro.value)
            else: ir += (hoje,False,self.categ.value)
            if self.money.value == '':
                self.money.error_text = 'Falta colocar o valor'
                self.money.update()
            else:
                self.money.error_text = ''
                ir +=(float(self.money.value),)
            if len(ir) == 4:
                c = ('data','tipo','categ','valor')
                add('finance',c,ir)
            else: pass
    def outer(self,e):
        if self.categ.value == 'Outros':
            self.in_outro.visible = True  
        else:
            self.in_outro.visible = False
        self.input_finance.update()
    def show_finance(self,e):
        if e.control.data == 0:
            self.tb_finance.rows.clear()
            x = procura('finance',False,False,(0),'tipo')
            print(x)
        else:# e.control.data == 1:
            self.tb_finance.rows.clear()
            x = procura('finance',False,False,(1),'tipo')
        if x:
            for item in x:
                if item[2] == 0:
                    m = '-'
                else: m= '+'
                self.tb_finance.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon='create',
                                        icon_color='blue',
                                        data=item,
                                        #on_click=self.show_input
                                    ),
                                    ft.IconButton(
                                        icon='delete',
                                        icon_color='red',
                                        data=item[0],
                                        on_click=self.del_finance
                                    ),
                                ])
                            ),
                            ft.DataCell(ft.Text(item[1])),
                            ft.DataCell(ft.Text(f'R${m}{item[4]}')),
                            ft.DataCell(ft.Text(item[3])),

                        ],
                    ),
                )
            else:pass
            self.tb_finance.update()
            self.history.update()
            self.content.update()
    def del_finance(self,e):
        myid = e.control.data
        excluir('finance','id',myid)
        print('excluido o id:',myid)
    def ver_data(self,e):
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

class wishlist(ft.Container):
    def __init__(self,txt): 
        super().__init__()
        t = txt
        self.padding = 15
        self.item = ft.TextField(label='Item',col={'xs':4,'md':5})
        self.valor = ft.TextField(label='Valor',prefix_text='R$',col={'xs':4,'md':4})
        self.date = ft.TextField(label='Data para aquisição',col={'xs':4,'md':3},on_change=self.ver_data,max_length=10,tooltip='Only Numbers')
        self.desc = ft.TextField(label='Descrição',multiline=True,min_lines=1,col={'xs':8,'md':9})
        self.prior = drop({'xs':4,'md':3},'Prioridade',['Alta','Media','Baixa'])
        self.input = ft.Container(
            visible=False,
            padding=15,
            content=ft.Column(
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.ResponsiveRow(columns=12,controls=[
                        ft.Text('WishList'),
                        self.item,
                        self.valor,
                        self.date,
                        self.desc,
                        self.prior,
                        ft.Row(col={'xs':12},alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                            ft.TextButton(text='Salvar',on_click=self.pre_add),
                            ft.TextButton(text='Cancelar',on_click=self.hide_input,data=0)# data = 0
                        ])
                    ])
                ])
        )
        self.botoes = ft.ResponsiveRow(alignment=ft.MainAxisAlignment.SPACE_AROUND,expand=True,columns=12,controls=[
            ft.TextButton(text='Todos',col={'md':3},on_click=self.wishlist),
            ft.TextButton(col={'md':3},data=1,on_click=self.wishlist,content=ft.Row(tight=True,controls=[ #data = 1
                ft.Text('Prioridade'),
                ft.Icon(name=ft.icons.EXPAND_LESS)
            ])),
            ft.TextButton(text='Ja Adquiridos',on_click=self.wishlist,data=0,col={'md':3}), #data = 0
            ft.IconButton(col={'md':3},icon=ft.icons.ADD_SHARP,on_click=self.show_input,data=0) #data = 0
        ])
        self.tb = ft.DataTable(
            expand=True,
            columns=[
                ft.DataColumn(ft.Text(value='Ações'),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text(value='Item')), #
                ft.DataColumn(ft.Text(value='Valor')), # 
                ft.DataColumn(ft.Text(value='Prioridade')), # 
                ft.DataColumn(ft.Text(value='Status'),heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text(value='Data'),heading_row_alignment=ft.MainAxisAlignment.CENTER), #
            ],
            rows=[]
        )
        # input edit
        self.rank_edit = drop({'xs':4,'md':3},'Prioridade',['Alta','Media','Baixa'])
        self.edit_nome = ft.TextField(label='Nome do item',col={'md':3})
        self.edit_valor = ft.TextField(label='Valor',prefix_text='R$ ',col={'xs':4,'md':3})
        self.edit_data = ft.TextField(label='Data',col={'xs':4,'md':3},read_only=True)
        self.edit_desc = ft.TextField(label='Descrição',col={'xs':8,'md':9})
        self.edit_status = ft.Checkbox(label='Ja adquirido?',col={'xs':4,'md':3})
        self.edit = ft.Container(
            visible=False,
            padding=15,
            content=ft.ResponsiveRow(columns=12,alignment=ft.MainAxisAlignment.CENTER,controls=[
                self.edit_nome,
                self.edit_valor,
                self.edit_data,
                self.rank_edit,
                self.edit_desc,
                self.edit_status,
                ft.Row(col={'xs':12},alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                    ft.TextButton(text='Atualizar',on_click=self.mudar),
                    ft.TextButton('Excluir',on_click=self.tirar),
                    ft.TextButton('Cancelar',on_click=self.hide_input)
                ])
            ])
        )
        self.content = ft.Column(spacing=15,run_spacing=15,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[
            self.input,
            self.edit,
            self.botoes,
            self.tb
        ])

    def pre_add(self,e):
        wl = ()
        if self.item.value == '':
            self.item.error_text = 'Falta o nome do item'
            self.item.update()
        else: 
            self.item.error_text = ''
            wl += (self.item.value,)
        if self.valor.value == '':
            self.valor.error_text = 'Falta o valor aproximado'
            self.valor.update()
        else: 
            self.valor.error_text = ''
            temp = int(self.valor.value)
            wl += (temp,)
        if self.desc.value == '':
            self.desc.error_text = 'Falta breve descrição do item'
            self.desc.update()
        else: 
            self.desc.error_text = ''
            wl += (self.desc.value,0)
        if self.prior.value == '':
            self.prior.error_text = 'Falta definir'
            self.prior.update()
        else:
            self.prior.error_text = ''
            wl += (self.prior.value,)
        if self.date.value == '':
            self.date.error_text = 'Falta'
            self.date.update()
        else:
            self.date.error_text = ''
            wl +=(self.date.value,)
        if wl:
            print(wl)
            add('wishlist',('item','valor','descricao','status','rank','date'),wl)
        else: pass
    def wishlist(self,e):
        if e.control.data == 0:
           #ja adquiridos
            self.tb.rows.clear()
            x = procura('wishlist',False,True,(1),'status')
        elif e.control.data == 1:
            #prioritarios
            self.tb.rows.clear()
            x = procura('wishlist',False,True,('Alta'),'rank')
        else:
             #todos
            self.tb.rows.clear()
            x = procura('wishlist',True)
        if x:    
            for item in x:
                if item[3] == 0:
                    icone = ft.Icons.CHECK_BOX_OUTLINE_BLANK
                    cor = 'grey'
                    status = 'Não Comprado'
                elif item[3] == 1: 
                    icone = ft.Icons.CHECK_BOX_SHARP
                    cor = 'purple'
                    status = 'Adquirido'
                else:pass
                self.tb.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon='create',
                                        icon_color='blue',
                                        data=item,
                                        on_click=self.show_input
                                    ),
                                    ft.IconButton(
                                        icon=icone,
                                        icon_color=cor,
                                        data=item[0],
                                        on_click=self.check
                                    ),
                                ])
                            ),
                            ft.DataCell(ft.Text(item[0])),
                            ft.DataCell(ft.Text(f'R$ {item[1]}')),
                            ft.DataCell(ft.Text(item[4])),
                            ft.DataCell(ft.Text(status)),
                            ft.DataCell(ft.Text(item[5])),
                            #ft.DataCell(ft.Text(item[4])),
                        ],
                    ),
                )
        else:pass
        self.tb.update()
    def check(self,e):
        temp = e.control.data
        hoje = datetime.now().strftime("%d/%m/%Y")
        atualiza('wishlist',['status','date'],[1,str(hoje)],2,'item',str(temp))
    def ver_data(self,e):
        if e.control.data == 0:
            raw_text = self.dia.value
        else:
            raw_text = self.date.value
        formatted_text = ""
        for i in range(len(raw_text)):
            if i == 2 or i == 4:
                formatted_text += "/"
            formatted_text += raw_text[i]
        if len(formatted_text) == 10:
            self.date.value = formatted_text
            self.dia.value = formatted_text
            self.dia.update()
            self.date.update()
        else:pass
    def show_input(self,e): #show input e edit  ('teste', 100.0, 'descrisol', 1, 'Alta', '02/01/2025')
        if e.control.data == 0:
            self.input.visible = True
        else:
            self.edit.visible = True
            temp = e.control.data
            self.edit_nome.value=temp[0]
            self.edit_valor.value=temp[1]
            self.edit_data.value=temp[5]
            self.rank_edit.value = temp[4]
            self.edit_desc.value = temp[2]
            if temp[3] == 0: s = False 
            else: s = True
            self.edit_status.value = s
        self.page.update()
    def hide_input(self,e):
        if e.control.data == 0:
            self.input.visible = False
        else: 
            self.edit.visible = False
        self.page.update()
    def mudar(self,e):
        colunas = ['item','valor','descricao','status','rank',"date"]
        if self.edit_status.value == True: s = 1
        else: s=0
        valores = [self.edit_nome.value,float(self.edit_valor.value),self.edit_desc.value,s,self.rank_edit.value,self.edit_data.value]
        atualiza('wishlist',colunas,valores,6,'date',self.edit_data.value)
        self.wishlist
    def tirar(self,e):
        excluir('wishlist','date',self.edit_data.value)

class drop(ft.Dropdown):
    def __init__(self,col,label,vars): 
        super().__init__()
        self.label = label,
        self.col= col #{'xs':4,'md':3}
        self.value = ''
        self.options=[]
        for item in vars:
            self.options.append(
                ft.dropdown.Option(item)
            )
