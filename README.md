# AMP Tool 

**1. Tiện ích:**

- **_AMP Tool_** sẽ có chức năng chính là `lọc toàn bộ thông tin cần thiết` để việc recon với anh em pentest trở nên dễ dàng hơn bao giờ hết
- Ngoài ra tool vẫn đang được phát triển thêm các tính năng về `Scan Vuln tự động` với đầu ra được lấy từ quá trình `Recon tự động`

**2. Giao diện:**

- Giao diện thân thiện, chạy trong terminal với kernel là Linux
- Dưới đây là hình ảnh demo của tool
![image](https://user-images.githubusercontent.com/61643034/212592445-1a13068f-357f-4b9b-9755-261adead0fb2.png)


**3. Hướng dẫn sử dụng**

- Đầu tiên, bạn cần sử dụng lệnh 
```bash
  cd $HOME; git clone https://github.com/w4rf0t/AMP-Tools ; cd AMP-Tools ; chmod +x AutoRecon/install.sh; ./AutoRecon/install.sh
  ``` 
để cài các **_requirements_** cần thiết cho chương trình
- Sau đấy để tools chạy 1 cách mượt mà nhất, bạn cần sửa file `config.json` của knockpy.
- Nếu bạn cài bằng pip thì file này ở trong /dist_packages/knockpy `"strftime":""` (trường này để format output của chương trình)
