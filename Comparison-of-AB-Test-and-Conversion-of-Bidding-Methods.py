import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
###########################################
#Görev 1:  Veriyi Hazırlama ve Analiz Etme
###########################################
# Adım 1

df_control = pd.read_excel("datasets/ab_testing.xlsx",sheet_name="Control Group")
df_test = pd.read_excel("datasets/ab_testing.xlsx",sheet_name="Test Group")

# Adım 2
df_control.head()
df_test.head()
df_control.describe().T
df_test.describe().T
df_control.shape
df_test.shape

# Adım 3

df = pd.concat([df_control, df_test], ignore_index=True)

##########################################
#Görev 2:  A/B Testinin Hipotezinin Tanımlanması
###########################################

# Adım 1

# H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
# H1 : M1!= M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)

# Adım 2

df_control["Purchase"].mean()
df_test["Purchase"].mean()
# Her iki test grubunun kazanç ortalamalarına bakıldığında test grubunun daha yüksek ortalamalara sahip
# olduğu görülmektedir.

##########################################
# Görev 3:  Hipotez Testinin Gerçekleştirilmesi
##########################################

# Adım 1

# Varsayım kontrolü

#   -Normallik Varsayımı
#   -Varyans Homojenliği


# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.

test_stat, pvalue = shapiro(df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p-value = 0.5891 H0 Reddedilemez

test_stat, pvalue = shapiro(df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p-value = 0.1541 H0 Reddedilemez

#Varyans Homojenliği :
#H0: Varyanslar homojendir.
#H1: Varyanslar homojen Değildir.

test_stat, pvalue = levene(df_control["Purchase"], df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p-value = 0.1083

# Adım 2


test_stat, pvalue = ttest_ind(df_control["Purchase"], df_test["Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p-value = 0.3493

# Adım 3

# Testler sonucunda p-value değerleri 0.05'ten büyük çıkmıştır. Bu sebepten H0 reddedilemez.
# Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.

##########################################
# Görev 4:  Sonuçların Analizi
##########################################

# Adım 1

# Normallik varsayımı için shapiro, varyans homojenliği varsayımı için levene testleri kullanılmıştır.
# Normal dağılım varsayımı ve varyans homojenliği varsayımlarının p-value değerleri 0.05'ten büyük
# çıktığı için parametrik bir test olan T testi kullanılmıştır. Bu testler sonucunda normal dağılım varsayımının
# sağlandığı ve varyansların homojen dağıldığı gözlemlenmiştir.

# Adım 2

# Veriye ilk olarak bakıldığında Average Bidding ve Maximum Bidding arasında bir miktar farklı
# satın alma ortalamaları görülmüştür. Fakat bilimsel testler yapıldıktan sonra bu farkın şans eseri
# oluştuğu ve bu iki teklif verme türü arasında anlamlı bir fark olmadığı görülmüştür.
# Bu iki teklif verme türü de hemen hemen aynı sonuçları verdiğinden dolayı maliyetlerine bakılıp
# daha az maliyetli olan tür seçilmelidir. Böylece maliyet şimdikine kıyasla yarıya inecek ve etki olarak
# bir farklılık olmayacaktır.



