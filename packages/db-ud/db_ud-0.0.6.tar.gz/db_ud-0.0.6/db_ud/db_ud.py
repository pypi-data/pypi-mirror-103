import pymysql
import pandas
import requests
import getpass
import sqlalchemy

def f_mysql(host,db,user,password,sql=None,table=None,port=3306,field='*',where=None):
    conn=pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    cur=conn.cursor()
    if sql:
        cur.execute(sql)
        df=pandas.DataFrame(list(cur))
    elif table:
        cur.execute(f'select {field} from {table} where {where}')
        df=pandas.DataFrame(list(cur))
        if field!='*':
            fields=[f.strip() for f in field.split(',')]
            df.columns=fields
    else:
        raise Exception('para: sql and table both None!')
    cur.close()
    conn.close()
    return df


def t_hive(df,table,host):
    target=f'C:/Users/{getpass.getuser()}/AppData/Local/Temp/{table}'
    df.to_csv(target,sep='`',index=False)
    requests.post(host,data={'sep':'`'}
        ,files={'file':(f'{table}'
                        ,open(target,'rb'))})


def t_mysql(df,table,host,db,user,password,port=3306,if_exists='replace',index=False,method='multi'):
    try:
        conn=sqlalchemy.create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
        df.to_sql(table,conn,if_exists=if_exists,index=index,method=method)
    except Exception as e: 
        raise e

# df = pandas.DataFrame({'id': [1, 2], 'value': [12.0, 13.55],'mark': ['a','测试']})
