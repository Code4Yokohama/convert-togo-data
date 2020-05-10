import pandas as pd
import datetime
import_csv = 'takeoutyokohama.csv'

# ngram
def ngram(w1, w2, n):
    w1_list =[]
    for i in range(len(w1)-(n-1)):
        w1_list.append(w1[i:i+n])

    w2_list =[]
    for i in range(len(w2)-(n-1)):
        w2_list.append(w2[i:i+n])

    total_check_count = 0
    equal_count = 0
    for wa in w1_list:
        total_check_count = total_check_count+1
        equal_flag = 0
        for wb in w2_list:
            if wa == wb:
                equal_flag = 1
        equal_count = equal_count+equal_flag

    return equal_count/total_check_count


# CSV読み込み
df = pd.read_csv(import_csv).fillna("")

# 必要な列だけ抜き出し
df_d = df[['タイムスタンプ', '02　新規登録ですか、修正依頼ですか', '03　店舗名（正式名称）＜公開＞', '04-1　店舗住所・区名＜公開＞', '04-2　店舗住所・区以降＜公開＞', '04-3　店舗住所・建物名称など＜公開＞', '06　最寄り駅＜公開＞']]

df_o = df_d[df_d['02　新規登録ですか、修正依頼ですか'] == '新規登録']
df_o = pd.concat([df_o['タイムスタンプ'], df_o['03　店舗名（正式名称）＜公開＞'].str.cat(df_o['04-1　店舗住所・区名＜公開＞']).str.cat(df_o['04-3　店舗住所・建物名称など＜公開＞']).str.cat(df_o['06　最寄り駅＜公開＞'])], axis=1)

df_m = df_d[df_d['02　新規登録ですか、修正依頼ですか'] == '修正依頼']
df_m = pd.concat([df_m['タイムスタンプ'], df_m['03　店舗名（正式名称）＜公開＞'].str.cat(df_m['04-1　店舗住所・区名＜公開＞']).str.cat(df_m['04-3　店舗住所・建物名称など＜公開＞']).str.cat(df_m['06　最寄り駅＜公開＞'])], axis=1)

# スコアの閾値
t = 0.7

# 修正依頼のレコードをループ
for index_m, row_m in df_m.iterrows():
    

    max_score = 0
    # オリジナルのレコードと総当たりで近似度を評価
    for index_o, row_o in df_o.iterrows():
        score = ngram(row_o['03　店舗名（正式名称）＜公開＞'].upper(), row_m['03　店舗名（正式名称）＜公開＞'].upper(), 2)
        if max_score < score:
            max_score = score
            
            # 閾値を超えていれば上書き
            if max_score >= t:
                df.iloc[index_o] = df.iloc[index_m]
                # 「修正依頼」で上書きされるので「修正済み」にしておく
                df.at[df.index[index_o], '02　新規登録ですか、修正依頼ですか'] = '修正済み'
                # 「修正依頼」が完了したところは「適用済み」にしておく
                df.at[df.index[index_m], '02　新規登録ですか、修正依頼ですか'] = '適用済み'

                # どこをどのように書き換えたかわかるようにしておく
                df.at[df.index[index_o], 'over_write_from'] = index_m
                df.at[df.index[index_m], 'over_write_to'] = index_o


# CSV書き出し

date = datetime.datetime.utcnow().date()

# 全レコード残して書き出し
df.to_csv(str(date) + '_record.csv')
# 新規登録＆修正適用済みレコードのみ残して書き出し
df[(df['02　新規登録ですか、修正依頼ですか'] == '新規登録') | (df['02　新規登録ですか、修正依頼ですか'] == '修正済み')].to_csv(str(date) + '_updated.csv')
# 処理できなかったレコードのみ書き出し
df[df['02　新規登録ですか、修正依頼ですか'] == '修正依頼'].to_csv(str(date) + '_unfinished.csv')