# Özet 
Bu repository, Çok Disiplinli Tasarım Projesi'nin çözümünü içermektedir. Çok Disiplinli Tasarım Projesi'nde farklı mühendislik bölümlerinden bir araya gelen 7 kişilik gruplar bir robotik projesi üzerinde çalışır.   

# Problem 
Bu dönemin problemi, 2D Strip Packing problemidir. Kargo taşıyon kişiler, farklı boyuttaki kargoları, büyük bir kutunun içine (belli bir alana) minimum boşluk kalacak şekilde dizmek isterler, buradan yola çıkarak, bu problemin 2 Boyutlu versiyonunu çözmemiz istenmiştir.Büyük bir karenin içine küçük, farklı boyutta kareler/dikdörtgenler uygun şekilde yerleştirilmelidir. Son yerleştirmede oluşan boşluk minimum olmalıdır, yani optimum yerleştirme bulunmalıdır. Sonra bu optimum yerleştirmeyi bir robotik kol yardımıyla, A4 kağıdına yazdırmamız istenmiştir.   

# Çözüm 
Bu çözümde backtracking algoritması kullanılmıştır. Proje Python ile yazılmıştır. Tkinter kullanarak bir arayüz tasarlanmıştır. 
original klasöründeki dosyalar farklı boyutlarda 
Kullanıcı farklı boyutta karelerin bulunduğu dosyayı seçer. Program, bu dosyayı girdi olarak alır, bu kareler en büyük kareye yerleştirilir, sonucunda oluşan optimum durumu arayüzden görülmektedir. 
Ayrıca sonuçları robot kol makineye göndermek için GCODE dosyaları oluşturmaktadır.


[![Video](https://img.youtube.com/vi/YXW24vJ2_uY/0.jpg)](https://www.youtube.com/watch?v=YXW24vJ2_uY)
