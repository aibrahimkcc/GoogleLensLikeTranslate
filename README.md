# GoogleLensLikeTranslate

## Requirements
  [CUDA GPU](https://developer.nvidia.com/cuda-gpus),
  Pytorch,
  FFMPEG,
  Numpy,
  Opencv,
  GoogleTranslateApi


## Nasıl Çalışır
FFMPEG ile video istenilen resimlere dönüştürülür
```
 ffmpeg -hwaccel cuda -i video1.mp4 -vf "fps=24" frames/output_%05d.png
```
deneme.py çalıştırılır.

FFMPEG ile resimler videoya geri dönüştürülür.
```
ffmpeg -framerate 24 -i editedframes/editedoutput_%05d.png -s 1920x1080 -c:v h264_nvenc -preset medium -b:v 10M -pix_fmt yuv420p output.mp4
```

## Geliştirilecekler
- cv2.putText() Türkçe karakter desteklemediği için Türkçeye yapılan çevirilerde harf hataları oluşuyor. Pillow kullanılabilir ama o da işlemi yavaşlatıyor.
- Googleapi tek seferde  128 segment kabul ettiği için çeviri metinlerini tek bir arrayle apiye gönderme error veriyor. Bu nedenle tek tek gönderiyoruz ama tek tek gönderme işlemi yavaşlatıyor.
- Bu haliyle (24 frame) resimde bir yapılan çeviri 24fps  5dklık video için 12dk sürüyor.
- Fonksiyon olarak düzenleme gerekiyor :)

## Örnek Video text translate

![input](./example/input.gif)

![output](./example/output.gif)
