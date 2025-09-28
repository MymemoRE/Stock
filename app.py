import sqlite3
import datetime
import simplenote
from flask import Flask,render_template,request,g
from markdown import Markdown

app = Flask(__name__)


# dbを呼出してオブジェクトに格納するサブルーチン
# databaseをopenしてFlaskのglobal変数gに格納
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('stock.db')
    return g.db



# Top画面のレンダラー
@app.route('/')
def index():
    con = get_db()
    cur = con.execute("select *,rowid from trade order by date desc")
    data = cur.fetchall()
    cur = con.execute("select * from corp order by name asc")
    data_corp=cur.fetchall()
    cur = con.execute("select rowid from trade order by rowid desc limit 1")
    last_rowid = cur.fetchone()[0]

    con.close()
    return render_template('index.html', data = data,data_corp=data_corp,last_rowid=last_rowid)


# Top画面でformが実行された場合のレンダラー
@app.route('/result', methods=["POST"])
def result_post():
    name = request.form["name"]
    print(name)
    con = get_db()
    sql=name
    con.execute(sql)
    print(sql)
    con.commit()
# sql再読み込み
    cur = con.execute("select *,rowid from trade order by date desc")
    data = cur.fetchall()
    con.close()
    return render_template('index.html', data = data)
    


@app.route('/jp', methods=["GET","POST"])
def indexget():
    if(request.method=='POST'):
        name=request.form["name"]
        print(name)
        con=get_db()
        con.execute(name)
        con.commit()
    con = get_db()
# 一覧再読み込み
    cur = con.execute("select tradejp_1.date,corpjp.name_s,tradejp_1.term,tradejp_1.price,tradejp_1.cost,tradejp_1.rowid,tradejp_1.code from tradejp_1 inner join corpjp on tradejp_1.code=corpjp.id order by tradejp_1.date desc")
    data = cur.fetchall()
    cur=con.execute("select * from corpjp order by name asc")
    corp=cur.fetchall()
    con.close()
    return render_template('index_jp.html',data=data,corp=corp)


@app.route('/jp/result', methods=["POST"])
def jp_post():
    name = request.form["namejp"]
    print(name)
    con = get_db()
    sql=name
    con.execute(sql)
    print(sql)
    con.commit()
# sql再読み込み
    cur = con.execute("select *,rowid from tradejp")
    data = cur.fetchall()
    con.close()
    return render_template('index_jp.html', data = data)



@app.route('/corp/<string:cname>')
def corp(cname):
    div_sum=0
    buy_sum=0
    buysell_sum=0
    div_ratio=0
    con = get_db()
    cur = con.execute("select *,rowid from trade where name='"+cname+"' order by date desc")
    data = cur.fetchall()
    cur = con.execute("select rowid,* from corp where name='"+cname+"'")
    corp_data=cur.fetchall()
    cur = con.execute("select * from exdiv where corp='"+cname+"' order by exdiv desc")
    exdiv_data=cur.fetchall()
    print(corp_data[0][2])
    cur=con.execute("select sum(cost) from trade where name='"+cname+"' and trade='div'")
    div_sum=cur.fetchone()[0]
    if div_sum is None:
        div_sum=0;
    else:
        div_sum=round(div_sum,2)
        
    cur=con.execute("select sum(cost) from trade where name='"+cname+"' and trade='buy'")
    buy_sum=cur.fetchone()[0]
    if buy_sum is None:
        buy_sum=0
    else:
        buy_sum=buy_sum*(-1)
        buy_sum=round(buy_sum,2)
    cur=con.execute(f"select price from corp where name='{cname}'")
    last_price=cur.fetchone()[0]
    #売買収支
    cur=con.execute("select sum(cost) from trade where name='"+cname+"' and trade in ('buy','sell')")
    buysell_sum=cur.fetchall()[0][0]
    if buysell_sum is None:
        buysell_sum=0
    else:
        buysell_sum=round(buysell_sum,2)
    #
    cur=con.execute("select cost,num from trade where name='"+cname+"' and trade='div' order by date desc limit 1")
    tmp1=cur.fetchall()
    print(tmp1)
    if not tmp1:
        print("null")
    elif tmp1[0] is None:
        print("None")
    else:
        print("else")


        
    con.close()
    
    #保有株式数の計算
    stock=0
    for trade in data:
        if trade[2]=="buy":
            stock=stock+trade[8]
        elif trade[2]=="sell":
            stock=stock-trade[8]

    #配当性向の計算
    

    if not tmp1:
        div_ratio=0
    else:
        div_ratio=tmp1[0][0]/tmp1[0][1]/float(last_price)*100
        div_ratio=round(div_ratio,2)
        print(div_ratio,"%")
        print("test")
        
    

    return render_template('corp.html',cname=cname,data=data,corp_data=corp_data,exdiv_data=exdiv_data,stock=stock,div_sum=div_sum,buy_sum=buy_sum,last_price=last_price,buysell_sum=buysell_sum,div_ratio=div_ratio)





@app.route('/div_ditale')
def div_ditale():
    con = get_db()
    cur = con.execute("select *,rowid from trade where trade='div' order by date desc")
    data = cur.fetchall()
    con = get_db()
    cur = con.execute("select * from exdiv")
    exdiv = cur.fetchall()
    con = get_db()
    cur = con.execute("select * from corp")
    corp = cur.fetchall()
    date_li=[]
    corp_li=[]
    corp_li2=[]#new
    exdiv_li2=[]#new
    date_li2=[]
    exdiv_index=[]
    dt=datetime.datetime.today()
    year1=str(dt.year)
    month1=str(dt.month)
    month=month1.zfill(2)
    div_unit=0
    div_cost=0
    cost_sum=0

    for tmp in corp: #loop for corpolation
        con = get_db()
        cur = con.execute("select *,rowid from trade where trade='div' and name='"+tmp[0]+"' order by date desc")
        data_li = cur.fetchall()
        #当該企業の配当レコードのみ抽出した行列
        
        con = get_db()
        cur = con.execute("select * from exdiv where corp='"+tmp[0]+"'")
        exdiv_li= cur.fetchall()
        #当該企業のexdivレコードのみ抽出
        #exdiv_index=[]
        data_index=[]
        div_cost="yet"
        for ii in exdiv_li:
            print(tmp[0])
            jj=ii[2]
            print(jj)
            #jjは配当支給日            
            #exdiv_index.append(jj[5:7]+jj[8:11])
            #配当日をリスト化し、exdiv_indexとする
            #corp_li2.append(tmp[0])
            #exdiv_li2.append(jj)
            #div_cost="yet"
            for kk in data_li:
                print(kk[1],kk[0])
                div_date=str(kk[0])
                div_year=div_date[:2]
                div_month=div_date[2:4]
                if div_year==year1[2:] and div_month==jj[5:7]:
                    print("match_month")
                    print(kk)
                    div_unit=kk[3]
                    print(div_unit)
                    div_cost=kk[5]
                    cost_sum=cost_sum+div_cost
                    print(div_cost)
                    print("break")
                    break
                else:
                    div_unit="non"
                    div_cost="yet"
            print("cost")
            print(div_cost)
            date_li2.append([jj[5:7]+"月"+jj[8:11],tmp[0],ii[1][2:],div_unit,div_cost])
#            if div_month in exdiv_index:
#                ll=exdiv_index.index(div_month)
#                kk=exdiv_li[ll]
#                date_li.append([div_month+"月"+div_date#[4:6]+"日",tmp[0],kk[1],ii[3],ii[5]])
#            else:
#                date_li.append([div_month+"月"+div_date#[4:6]+"日",tmp[0],"test",ii[3],ii[5]])
#        for ii in exdiv_index:
#            ll=exdiv_index.index(ii)
#            if ii not in data_index:
#                kk=exdiv_li[ll][2]
#                date_li.append([str(ii)+"月"+kk[8:10]+"日",tmp[0],exdiv_li[ll][1],"",""])
            
                        
    date_li2.sort()
    con.close()
    cost_sum=round(cost_sum,2)
    return render_template('div_ditale.html',exdiv=exdiv,exdiv_li2=exdiv_li2,corp_li2=corp_li2,exdiv_index=exdiv_index,date_li2=date_li2,cost_sum=cost_sum)


@app.route('/note_page')
def note_page():
    return render_template('note_page.html')

@app.route('/stock')
def stock():
    con = get_db()
    cur = con.execute("select * from corp")
    data = cur.fetchall()
    return render_template('stock.html',data=data)


@app.route('/test')
def test():
    sn=simplenote.Simplenote("yamyamyan8@hotmail.com","my88yam\
a")
    status=sn.get_note_list(data=False)
    simple=sn.get_note('22b7ec27-6491-4759-8129-a9bae3198a66')
    simple_con=simple[0]["content"]
    md=Markdown()
    simple_html=md.convert(simple_con)
    print(simple_html)
    return render_template('test.html',simple_html=simple_html)


@app.route('/sq_lite')
def sq_lite():
    return render_template('sqlite.html')

@app.route('/product')
def product():
    g.db = sqlite3.connect('product.db')
    con=g.db
    cur = con.execute("select code,code_name,growp_name,price from product where growp_name not like '%部品%' and not growp_name glob '*値引*' and not code glob '[0-9]*' and not price glob '0.00'  limit 500")
    data=cur.fetchall()
    return render_template('product.html',data=data)



if __name__ == '__main__':
    app.debug = True
    # app.run(host='localhost')
    app.run(host="0.0.0.0", port=5000)



