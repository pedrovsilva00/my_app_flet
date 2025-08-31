import sqlite3 


def add(name_table:str,colunas:tuple,valores:tuple):#

    try:
        conn=sqlite3.connect('database.db') 
        cur = conn.cursor()
        sql = f'''INSERT INTO {name_table} {colunas} VALUES {valores}'''
        cur.execute('PRAGMA journal_mode = OFF')
        conn.commit()
        cur.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print('Erro em adicionar: ',e)
def procura(name_table:str,all:bool,cres=True,pesquisa=(),coluna=''):
    try:
        conn=sqlite3.connect('database.db', check_same_thread=False) 
        cur = conn.cursor()
        if cres == True:
            if all == True:#procura('passbank',True)
                sql = f'''SELECT * FROM {name_table}'''
                cur.execute(sql)
                #resul = cur.fetchall()
                resul = cur.fetchall()       
            else:#procura(name_table = 'passbank',coluna = 'conta',pesquisa = ['continha'],all=False)
                sql = f'''SELECT * FROM {name_table} WHERE {coluna} LIKE '%{pesquisa}%' '''
                cur.execute(sql)
                resul = cur.fetchall()
                conn.close()
        else:
            if all == True:#procura('passbank',True)
                sql = f'''SELECT * FROM {name_table} ORDER BY ROWID DESC'''
                cur.execute(sql)
                #resul = cur.fetchall()
                resul = cur.fetchall()       
            else:#procura(name_table = 'passbank',coluna = 'conta',pesquisa = ['continha'],all=False)
                sql = f'''SELECT * FROM {name_table} WHERE {coluna} LIKE '%{pesquisa}%' ORDER BY ROWID DESC'''
                cur.execute(sql)
                resul = cur.fetchall()
                conn.close()

    except Exception as e:
        print('Erro em procurar: ',e)
    return resul
def procura_in(name_table:str,coluna:str,valores:tuple,cres=True):
    try:
        conn=sqlite3.connect('database.db', check_same_thread=False) 
        cur = conn.cursor()
        if cres == True:
            sql = f'''SELECT * FROM {name_table} WHERE {coluna} IN {valores}'''
            cur.execute(sql)
            resul = cur.fetchall()
            conn.close()
        else:
            sql = f'''SELECT * FROM {name_table} WHERE {coluna} IN {valores} ORDER BY ROWID DESC'''
            cur.execute(sql)
            resul = cur.fetchall()
            conn.close()
    except Exception as e:
        print('Erro em procurar: ',e)
    return resul

def quantidade(name_table:str,coluna:str):
    conn=sqlite3.connect('database.db', check_same_thread=False) #
    cur = conn.cursor()
    x =cur.execute(f'SELECT {coluna} FROM {name_table}')
    l = 0
    for linhas in x:
        l = l + 1
    quanta = l
    conn.close()
    return int(quanta)

def last_item(name_table:str):
    conn=sqlite3.connect('database.db', check_same_thread=False) #
    cur = conn.cursor()
    sql = f"SELECT * FROM {name_table} ORDER BY ROWID DESC LIMIT 1"
    cur.execute(sql)
    last = cur.fetchone()
    conn.close()
    return last
'''x = last_item('recipe')
print(x[0])'''
def atualiza(name_table:str,colunas:list,valores:list,q_colunas:int,colu_id:str,item): #mudei o item para aceitar qualquer tipo de variavel, v
    conn=sqlite3.connect('database.db', check_same_thread=False)                       #se der erro em outra parte do app voltar para str e fazer outra logica para mudar pelo id int
    cur = conn.cursor()
    try: 
        if q_colunas == 1: 
            sql = f'''UPDATE {name_table} SET {colunas[0]}=? WHERE {colu_id}=?'''
            cur.execute('PRAGMA journal_mode = OFF')
            conn.commit()
            cur.execute(sql,(valores[0],item))   
            conn.commit()  
            conn.close()  
        elif q_colunas == 2: #atualiza('finance',['status',"date"],[0,'05/12/1965'],2,'item','teste')
            sql = f'''UPDATE {name_table} SET {colunas[0]}=?,{colunas[1]}=? WHERE {colu_id}=?'''
            cur.execute('PRAGMA journal_mode = OFF')
            conn.commit()
            cur.execute(sql,(valores[0],valores[1],item))   
            conn.commit()  
            conn.close() 
        elif q_colunas == 3: 
            sql = f'''UPDATE {name_table} SET {colunas[0]}=?,{colunas[1]}=?,{colunas[2]}=? WHERE {colu_id}=?'''
            cur.execute('PRAGMA journal_mode = OFF')
            conn.commit()
            cur.execute(sql,(valores[0],valores[1],valores[2],item))   
            conn.commit()  
            conn.close() 
        elif q_colunas == 5:
            sql = f'''UPDATE {name_table} SET {colunas[0]}=?,{colunas[1]}=?,{colunas[2]}=?,{colunas[3]}=?,{colunas[4]}=? WHERE {colu_id}=?'''      
            cur.execute('PRAGMA journal_mode = OFF')
            conn.commit()
            cur.execute(sql,(valores[0],valores[1],valores[2],valores[3],valores[4],item))   
            conn.commit()  
            conn.close()
        elif q_colunas == 6:
            sql = f'''UPDATE {name_table} SET {colunas[0]}=?,{colunas[1]}=?,{colunas[2]}=?,{colunas[3]}=?,{colunas[4]}=?,{colunas[5]}=? WHERE {colu_id}=?'''      
            cur.execute('PRAGMA journal_mode = OFF')
            conn.commit()
            cur.execute(sql,(valores[0],valores[1],valores[2],valores[3],valores[4],valores[5],item))   
            conn.commit()  
            conn.close() 
        else: print('add quando houver outra tabela')
    except Exception as e:
        print('Erro em atualizar: ',e)

def excluir(name_table:str,coluna:str,valor:str): #excluir('passbank','grupo',['havainas'])
    try:
        conn=sqlite3.connect('database.db', check_same_thread=False) 
        cur = conn.cursor()
        sql = f'''DELETE FROM {name_table} WHERE {coluna}='{valor}' '''
        print(sql)
        cur.execute('PRAGMA journal_mode = OFF')
        conn.commit()
        cur.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print('Erro em excluir: ',e)

'''sear = ('drink') # Exemplo de como transformar o sesultado em lista novamente, feita no codigo da pagina
c = "categ"
resul = []
r = procura('recipe',False,sear,c)
for item in r:
    resul += item
print(len(resul))''' 
