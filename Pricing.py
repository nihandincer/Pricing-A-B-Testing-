
###########################
# Pricing
###########################

#Kütüphaneler import edildi.
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_=pd.read_csv("/Users/nHn/Desktop/pricing.csv", sep=";")
df=df_.copy()


#veri inceleme
df.head()
df.shape  # (3448,2)
df.columns  # 'category_id', 'price'


############################
# Descriptive Statistics
############################

#betimsel analiz sonucunda price değişkeninde %99 luk değer ile max değer arasında
#büyük fark olduğu gözlemlenmiştir. Outlier değer olabilir.
df.describe([0.01, 0.05, 0.50, 0.95, 0.99]).T


#eksik değer bulunmamıstır.
df.isnull().sum()

#Outlier değerler için alt ve üst limitler belirlendi.

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.05)
    quartile3 = dataframe[variable].quantile(0.95)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit



def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


replace_with_thresholds(df, "price")

df.shape


#kategoriler arasındaki fark
category=df["category_id"].value_counts()
category



df.groupby("category_id")["price"].agg(["mean","sum","std"])



############################
# AB Testing (Bağımsız İki Örneklem T Testi)
############################

############################
# 1. Varsayım Kontrolü
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

from scipy.stats import shapiro


for i in df["category_id"].unique():
    test_statistic, pvalue = shapiro(df.loc[df["category_id"] == i, "price"])
    if (pvalue < 0.05):
        print('Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue), "H0 red.")
    else:
        print('Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue), "H0 reddedilemez")


#p-value değeri 0.05 ten küçük olduğundan H0 red edilir.
#Normal dağılım varsayımı sağlanmamaktadır.
#Normallik sağlanmadığı için varyans homojenliğine bakılmamıştır.




############################
# NonParametrik Test
############################
# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)


from scipy import stats
import itertools
#Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)


N=[]
for i in itertools.combinations(df["category_id"].unique(),2):
    N.append(i)



A=[]
for i in N:
    test_statistic, pvalue = stats.stats.mannwhitneyu(df.loc[df["category_id"]==i[0], "price"],
                                                      df.loc[df["category_id"]==i[1], "price"])
    if(pvalue< 0.05):
        A.append((i[0],i[1], "H0 red"))
        print('\n',"({0} - {1}) -> ".format(i[0],i[1]),'Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue),"H0 red.")
    else:
        A.append((i[0],i[1], "H0 reddedilemez"))
        print('\n',"({0} - {1}) -> ".format(i[0],i[1]),'Test statistic = %.4f, p-Value = %.4f' % (test_statistic, pvalue),"H0 reddedilemez")

#bir dataframe tanımlayıp içine oluşturmuş olduğum ikili kombinasyonları ve bunların H0 hiptozlerini koydum.

df1=pd.DataFrame()
df1["cat1"]=[N[0] for N in A]
df1["cat2"]=[N[1] for N in A]
df1["H0"]=[N[2] for N in A]


#oluşturduğum df1 dataframe inden H0 ın reddedilemez olanlarını çağırdım.
#Çünkü bunlar arasında istatistiksel bir farklılık yoktur.
df1[df1["H0"] == "H0 reddedilemez"]

df.groupby("category_id").agg({"price":"mean"})


#burada H0 reddedilemez sonucu çıkan değişkenler var.
#bunların veri içerisinden price karşılıklarını alıp oradan dördünün ortalamasını bulacağım.
#bu benim item fiyatım.
signif_cat = [361254,874521,675201,201436]
sum = 0
for i in signif_cat:
    sum += df.loc[df["category_id"]== i,"price"].mean()
PRICE = sum/4

print("PRICE :{%.4f}"%PRICE)


# esnek fiyatlandırmaya gidilmiştir.
#bunun için H0 reddedilemez denen grubun price değişkenlerini çağırıp bunları bir listeye ekledim.
#guven aralıklarına baktım.
prices = []
for category in signif_cat:
    for i in df.loc[df["category_id"]== category,"price"]:
        prices.append(i)


print("Felexible Price Range: ", sms.DescrStatsW(prices).tconfint_mean())


#simülasyon için güven aralıklarını min,karar verilen değer,max olacak şekilde ayarlayıp simüle ettim.
#min
freq = len(df[df["price"]>=38.94778731600629])
income = freq * 38.94778731600629
print("Income: ", income)


# karar verilen değer
freq = len(df[df["price"]>=39.0579])
income = freq * 39.0579
print("Income: ", income)

# max
freq = len(df[df["price"]>=41.38332006743786])
income = freq * 41.38332006743786
print("Income: ",income)